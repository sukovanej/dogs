from collections.abc import Awaitable
from typing import TypeVar

from dogs.core.classes.applicative import Applicative
from dogs.core.classes.apply import Apply
from dogs.core.classes.apply import ap as _ap
from dogs.core.classes.chain import Chain
from dogs.core.classes.functor import Functor
from dogs.core.classes.functor import map as _map
from dogs.core.classes.monad import Monad
from dogs.core.classes.pointed import Pointed
from dogs.core.classes.pointed import of as _of
from dogs.core.function import Fn, Lazy

A = TypeVar("A")
B = TypeVar("B")

# model

Task = Lazy[Awaitable[A]]

# helper interop functions


async def _async_of(a: A) -> A:
    return a


async def _async_map(f: Fn[A, B], a: Awaitable[A]) -> B:
    return f(await a)


async def _async_ap(f: Awaitable[Fn[A, B]], fa: Awaitable[A]) -> B:
    return (await f)(await fa)


async def _async_chain(f: Fn[A, Awaitable[B]], fa: Awaitable[A]) -> B:
    return await f(await fa)


# Instances


class _PointedInstance(Pointed):
    def of(self, a: A) -> Task[A]:
        return lambda: _async_of(a)


class _FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: Task[A]) -> Task[B]:
        return lambda: _async_map(f, fa())


class _ApplyInstance(Apply, _FunctorInstance):
    def ap(self, f: Task[Fn[A, B]], fa: Task[A]) -> Task[B]:
        return lambda: _async_ap(f(), fa())


class _ApplicativeInstance(Applicative, _ApplyInstance, _PointedInstance):
    pass


class _ChainInstance(Chain, _ApplyInstance):
    def chain(self, f: Fn[A, Task[B]], fa: Task[A]) -> Task[B]:
        return lambda: _async_chain(lambda a: f(a)(), fa())


class _MonadInstance(Monad, _ApplicativeInstance, _ChainInstance):
    pass


pointed = _PointedInstance()
functor = _FunctorInstance()
apply = _ApplyInstance()
applicative = _ApplicativeInstance()
chain = _ChainInstance()
monad = _MonadInstance()

of = _of(pointed)
map = _map(functor)
ap = _ap(apply)
