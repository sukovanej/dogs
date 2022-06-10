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


class PointedInstance(Pointed):
    def of(self, a: T) -> IO[T]:
        return lambda: a


class FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: IO[A]) -> IO[B]:
        return lambda: f(unsafe_run_io(fa))


class ApplyInstance(Apply, FunctorInstance):
    def ap(self, f: IO[Fn[A, B]], fa: IO[A]) -> IO[B]:
        return lambda: unsafe_run_io(f)(unsafe_run_io(fa))


class ApplicativeInstance(Applicative, ApplyInstance, PointedInstance):
    pass


class ChainInstance(Chain, ApplyInstance):
    def chain(self, f: Fn[A, IO[B]], fa: IO[A]) -> IO[B]:
        return lambda: unsafe_run_io(f(fa()))


class MonadInstance(Monad, ApplicativeInstance, ChainInstance):
    pass


class FromIOInstance(FromIO):
    def from_io(self, fa: IO[A]) -> IO[A]:
        return fa


class MonadIOInstance(MonadIO, FromIOInstance, MonadInstance):
    pass


pointed_instance = PointedInstance()
functor_instance = FunctorInstance()
apply_instance = ApplyInstance()
applicative_instance = ApplicativeInstance()
chain_instance = ChainInstance()
monad_instance = MonadInstance()
fromIO_instance = FromIOInstance()
monadIO_instance = MonadIOInstance()


of = _of(pointed_instance)
map = _map(functor_instance)
ap = _ap(apply_instance)
from_io = _from_io(fromIO_instance)
chain = _chain(chain_instance)
chain_first = _chain_first(chain_instance)

# Unsafe


def unsafe_run_io(fa: IO[A]) -> A:
    return fa()
