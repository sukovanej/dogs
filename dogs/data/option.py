from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Generic, Optional, TypeGuard, TypeVar

from dogs.classes import eq
from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.function import Fn
from dogs.hkt.kind import Kind

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model


class Option(Generic[T], ABC, Kind[Any, T]):
    @abstractmethod
    def get_value(self) -> Optional[T]:
        ...


class Some(Option[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def get_value(self) -> T:
        return self._value


class Nothing(Option[T]):
    def get_value(self) -> None:
        return None


# Constructors


def some(a: A) -> Option[A]:
    return Some(a)


def none() -> Nothing[T]:
    return Nothing()


# Destructors


def is_some(fa: Option[A]) -> TypeGuard[Some[A]]:
    return fa.get_value() is not None


def is_none(fa: Option[A]) -> TypeGuard[Nothing[A]]:
    return fa.get_value() is None


# Instances


class _PointedInstance(Pointed):
    def of(self, a: T) -> Option[T]:
        return Some(a)


class _FunctorInstance(Functor):
    def map(self, f: Fn[A, B], fa: Option[A]) -> Option[B]:
        if is_some(fa):
            return some(f(fa._value))
        return none()


class _ApplyInstance(Apply, _FunctorInstance):
    def ap(self, f: Option[Fn[A, B]], fa: Option[A]) -> Option[B]:
        if is_some(f) and is_some(fa):
            return Some((f.get_value())(fa.get_value()))
        return none()


class _ApplicativeInstance(Applicative, _ApplyInstance, _PointedInstance):
    pass


class _ChainInstance(Chain, _ApplyInstance):
    def chain(self, f: Fn[A, Option[B]], fa: Option[A]) -> Option[B]:
        if is_some(fa):
            return f(fa.get_value())
        return none()


class _MonadInstance(Monad, _ChainInstance, _ApplicativeInstance):
    pass


Pointed = _PointedInstance()
Functor = _FunctorInstance()
Apply = _ApplyInstance()
Applicative = _ApplicativeInstance()
Chain = _ChainInstance()
Monad = _MonadInstance()

of = _of(Pointed)
map = _map(Functor)
ap = _ap(Apply)
chain = _chain(Chain)


def create_eq(E: eq.Eq[A]) -> eq.Eq[Option[A]]:
    return eq.from_equals(partial(_equals, E))


def _equals(E: eq.Eq[A], a: Option[A], b: Option[A]) -> bool:
    return is_some(a) and is_some(b) and E.equals(a.get_value(), b.get_value())


StandardEq = create_eq(eq.standard_eq)
