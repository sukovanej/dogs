from typing import Any, TypeVar

from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.chain import chain_first as _chain_first
from dogs.classes.from_io import from_io as _from_io
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.function import Fn

A = TypeVar("A")
B = TypeVar("B")
R = TypeVar("R")

# Model

Reader = Fn[R, A]

# Instances


class PointedInstance(Pointed):
    def of(self, a: A) -> Reader[Any, A]:
        return lambda _: a


class FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: Reader[R, A]) -> Reader[R, B]:
        return lambda r: f(fa(r))


class ApplyInstance(Apply, FunctorInstance):
    def ap(self, f: Reader[R, Fn[A, B]], fa: Reader[R, A]) -> Reader[R, B]:
        return lambda r: f(r)(fa(r))


class ApplicativeInstance(Applicative, ApplyInstance, PointedInstance):
    pass


class ChainInstance(Chain, ApplyInstance):
    def chain(self, f: Fn[A, Reader[R, B]], fa: Reader[R, A]) -> Reader[R, B]:
        return lambda r: f(fa(r))(r)


class MonadInstance(Monad, ApplicativeInstance, ChainInstance):
    pass


pointed_instance = PointedInstance()
functor_instance = FunctorInstance()
apply_instance = ApplyInstance()
applicative_instance = ApplicativeInstance()
chain_instance = ChainInstance()
monad_instance = MonadInstance()

of = _of(pointed_instance)
map = _map(functor_instance)
ap = _ap(apply_instance)
chain = _chain(chain_instance)
chain_first = _chain_first(chain_instance)


# Constructors


def ask() -> Reader[R, R]:
    return lambda r: r
