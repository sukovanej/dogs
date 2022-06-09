from collections.abc import Awaitable
from typing import TypeVar

from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.from_io import FromIO, from_io as _from_io
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.monad_io import MonadIO
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.data import io
from dogs.function import Fn, Lazy

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


class _FromIOInstance(FromIO):
    def from_io(self, fa: io.IO[A]) -> Task[A]:
        return lambda: _async_of(fa())


class _MonadIOInstance(MonadIO, _FromIOInstance, _MonadInstance):
    pass


Pointed = _PointedInstance()
Functor = _FunctorInstance()
Apply = _ApplyInstance()
Applicative = _ApplicativeInstance()
Chain = _ChainInstance()
Monad = _MonadInstance()
FromIO = _FromIOInstance()
MonadIO = _MonadIOInstance()


of = _of(Pointed)
map = _map(Functor)
ap = _ap(Apply)
from_io = _from_io(FromIO)
