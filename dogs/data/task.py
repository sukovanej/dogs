from collections.abc import Awaitable
from typing import TypeVar

from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.from_io import FromIO
from dogs.classes.from_io import from_io as _from_io
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.monad_io import MonadIO
from dogs.classes.monad_io import chain_io as _chain_io
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


class PointedInstance(Pointed):
    def of(self, a: A) -> Task[A]:
        return lambda: _async_of(a)


class FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: Task[A]) -> Task[B]:
        return lambda: _async_map(f, fa())


class ApplyInstance(Apply, FunctorInstance):
    def ap(self, f: Task[Fn[A, B]], fa: Task[A]) -> Task[B]:
        return lambda: _async_ap(f(), fa())


class ApplicativeInstance(Applicative, ApplyInstance, PointedInstance):
    pass


class ChainInstance(Chain, ApplyInstance):
    def chain(self, f: Fn[A, Task[B]], fa: Task[A]) -> Task[B]:
        return lambda: _async_chain(lambda a: f(a)(), fa())


class MonadInstance(Monad, ApplicativeInstance, ChainInstance):
    pass


class FromIOInstance(FromIO):
    def from_io(self, fa: io.IO[A]) -> Task[A]:
        return lambda: _async_of(fa())


class MonadIOInstance(MonadIO, FromIOInstance, MonadInstance):
    pass


pointed_instance = PointedInstance()
functor_instance = FunctorInstance()
apply_instance = ApplyInstance()
applicative_instance = ApplicativeInstance()
chain_instance = ChainInstance()
monad_instance = MonadInstance()
from_io_instance = FromIOInstance()
monad_io_instance = MonadIOInstance()


of = _of(pointed_instance)
map = _map(functor_instance)
ap = _ap(apply_instance)
from_io = _from_io(from_io_instance)
chain = _chain(chain_instance)
chain_io = _chain_io(monad_io_instance)

# Unsafe


async def unsafe_run_task(fa: Task[A]) -> A:
    return await fa()
