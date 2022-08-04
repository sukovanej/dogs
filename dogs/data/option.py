from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Generic, Optional, TypeGuard, TypeVar, cast

from dogs.classes import eq
from dogs.function import Fn, curry

A = TypeVar("A")
AC = TypeVar("AC", covariant=True)
B = TypeVar("B", covariant=True)

# Model


class Option(ABC, Generic[A]):
    @abstractmethod
    def get_value(self) -> Optional[A]:
        ...


class Some(Generic[A], Option[A]):
    def __init__(self, value: A) -> None:
        self._value = value

    def get_value(self) -> A:
        return self._value


class Nothing(Generic[A], Option[A]):
    def get_value(self) -> None:
        return None


# Constructors


def some(a: A) -> Option[A]:
    return Some(a)


def none() -> Nothing[Any]:
    return Nothing()


# Destructors


def is_some(fa: Option[A]) -> TypeGuard[Some[A]]:
    return fa.get_value() is not None


def is_none(fa: Option[A]) -> TypeGuard[Nothing[A]]:
    return fa.get_value() is None


# Instances


def of(a: A) -> Option[A]:
    return Some(a)


@curry
def map(f: Fn[AC, B], fa: Option[AC]) -> Option[B]:
    fa = cast(Option[AC], fa)

    if is_some(fa):
        return some(f(fa._value))
    return none()


@curry
def ap(f: Option[Fn[A, B]], fa: Option[A]) -> Option[B]:
    fa = cast(Option[A], fa)
    f = cast(Option[Fn[A, B]], f)

    if is_some(f) and is_some(fa):
        return Some((f.get_value())(fa.get_value()))
    return none()


@curry
def chain(f: Fn[A, Option[B]], fa: Option[A]) -> Option[B]:
    fa = cast(Option[A], fa)
    f = cast(Fn[A, Option[B]], f)

    if is_some(fa):
        return f(fa.get_value())
    return none()


def create_eq(E: eq.Eq[A]) -> eq.Eq[Option[A]]:
    return eq.from_equals(partial(_equals, E))


def _equals(E: eq.Eq[A], a: Option[A], b: Option[A]) -> bool:
    both_none = is_none(a) and is_none(b)
    both_same = is_some(a) and is_some(b) and E.equals(a.get_value(), b.get_value())
    return both_none or both_same


StandardEq = create_eq(eq.standard_eq)
