from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Generic, Optional, TypeGuard, TypeVar

from dogs.core.classes import eq
from dogs.core.classes.applicative import Applicative
from dogs.core.classes.apply import Apply
from dogs.core.classes.apply import ap as _ap
from dogs.core.classes.chain import Chain
from dogs.core.classes.chain import chain as _chain
from dogs.core.classes.functor import Functor
from dogs.core.classes.functor import map as _map
from dogs.core.classes.monad import Monad
from dogs.core.classes.pointed import Pointed
from dogs.core.classes.pointed import of as _of
from dogs.core.function import Fn
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

F = TypeVar("F")


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


pointed = _PointedInstance()
functor = _FunctorInstance()
apply = _ApplyInstance()
applicative = _ApplicativeInstance()
chain = _ChainInstance()
monad = _MonadInstance()

of = _of(pointed)
map = _map(functor)
ap = _ap(apply)
chain = _chain(chain)


def create_eq(E: eq.Eq[A]) -> eq.Eq[Option[A]]:
    return eq.from_equals(partial(_equals, E))


def _equals(E: eq.Eq[A], a: Option[A], b: Option[A]) -> bool:
    return is_some(a) and is_some(b) and E.equals(a.get_value(), b.get_value())


standard_eq = create_eq(eq.standard_eq)
