from abc import ABC, abstractmethod
from typing import Any, Generic, TypeGuard, TypeVar, cast

from dogs.classes import eq
from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.chain import chain_first as _chain_first
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.data import option
from dogs.function import Fn, Lazy, curry
from dogs.hkt.kind import Kind2

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")
E = TypeVar("E")

# Model


class Either(Generic[E, A], ABC):
    @abstractmethod
    def get_value(self) -> E | A:
        ...

    @abstractmethod
    def is_left(self) -> bool:
        ...

class Right(Either[E, A]):
    def __init__(self, value: A) -> None:
        self._value = value

    def get_value(self) -> A:
        return self._value

    def is_left(self) -> bool:
        return False


class Left(Either[E, A]):
    def __init__(self, value: E) -> None:
        self._value = value

    def get_value(self) -> E:
        return self._value

    def is_left(self) -> bool:
        return True

EitherKind = TypeVar("EitherKind", bound=Either)


# Constructors


def left(e: E) -> Kind2[Either, E, Any]:
    return cast(Kind2[Either, E, Any], Left(e))


def right(a: A) -> Kind2[Either, Any, A]:
    return cast(Kind2[Either, E, Any], Right(a))


# Destructors


def is_left(fa: Either[E, A]) -> TypeGuard[Kind2[Left, E, A]]:
    return fa.is_left()


def is_right(fa: Either[E, A]) -> TypeGuard[Kind2[Right, E, A]]:
    return not fa.is_left()


# Instances


class _PointedInstance(Pointed):
    def of(self, a: A) -> Kind2[EitherKind, Any, A]:
        return right(a)


class _FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: Kind2[EitherKind, E, A]) -> Kind2[EitherKind, E, B]:
        if is_right(fa):
            return right(f(fa.get_value()))
        return cast(Either[E, B], fa)


class _ApplyInstance(Apply, _FunctorInstance):
    def ap(self, f: Either[E, Fn[A, B]], fa: Either[E, A]) -> Either[E, B]:
        if is_right(f) and is_right(fa):
            return Right(f.get_value()(fa.get_value()))
        return cast(Either[E, B], fa)


class _ApplicativeInstance(Applicative, _ApplyInstance, _PointedInstance):
    pass


class _ChainInstance(Chain, _ApplyInstance):
    def chain(self, f: Fn[A, Either[E, B]], fa: Either[E, A]) -> Either[E, B]:
        if is_right(fa):
            return f(fa.get_value())
        return cast(Either[E, B], fa)


class _MonadInstance(Monad, _ChainInstance, _ApplicativeInstance):
    pass


pointed_instance = _PointedInstance()
functor_instance = _FunctorInstance()
apply_instance = _ApplyInstance()
applicative_instance = _ApplicativeInstance()
chain_instance = _ChainInstance()
monad_instance = _MonadInstance()

of = _of(pointed_instance)
map = _map(functor_instance)
ap = _ap(apply_instance)
chain = _chain(chain_instance)
chain_first = _chain_first(chain_instance)


# Combinators


@curry
def from_option(on_empty: Lazy[E], fa: option.Option[A]) -> Either[E, A]:
    if option.is_some(fa):
        return right(fa.get_value())
    return left(on_empty())


def _equals(a: Either[A, B], b: Either[A, B]) -> bool:
    both_same_value = is_right(a) and is_right(b) and a.get_value() == b.get_value()
    both_same_err = is_left(a) and is_left(b) and a.get_value() == b.get_value()
    return both_same_err or both_same_value


StandardEq = eq.from_equals(_equals)
