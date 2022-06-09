from typing import TypeVar

from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.chain import chain_first as _chain_first
from dogs.classes.from_io import FromIO
from dogs.classes.from_io import from_io as _from_io
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.monad_io import MonadIO
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.function import Fn

from .io_model import IO

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Instances


class _PointedInstance(Pointed):
    def of(self, a: T) -> IO[T]:
        return lambda: a


class _FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: IO[A]) -> IO[B]:
        return lambda: f(unsafe_run_io(fa))


class _ApplyInstance(Apply, _FunctorInstance):
    def ap(self, f: IO[Fn[A, B]], fa: IO[A]) -> IO[B]:
        return lambda: unsafe_run_io(f)(unsafe_run_io(fa))


class _ApplicativeInstance(Applicative, _ApplyInstance, _PointedInstance):
    pass


class _ChainInstance(Chain, _ApplyInstance):
    def chain(self, f: Fn[A, IO[B]], fa: IO[A]) -> IO[B]:
        return lambda: unsafe_run_io(f(fa()))


class _MonadInstance(Monad, _ApplicativeInstance, _ChainInstance):
    pass


class _FromIOInstance(FromIO):
    def from_io(self, fa: IO[A]) -> IO[A]:
        return fa


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
chain = _chain(Chain)
chain_first = _chain_first(Monad)

# Unsafe


def unsafe_run_io(fa: IO[A]) -> A:
    return fa()
