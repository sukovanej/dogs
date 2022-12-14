from abc import ABC, abstractmethod
from typing import Any, Generic, TypeGuard, TypeVar, cast

from dogs.classes import eq
from dogs.data import option
from dogs.function import Fn, Lazy, curry

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")
E = TypeVar("E")

# Model


class Either(Generic[E, A], ABC):
    """Data structure representing computation with possible error."""

    @abstractmethod
    def get_value(self) -> E | A:
        """Unwrap the Either to the error E or the value A."""

    @abstractmethod
    def is_left(self) -> bool:
        """Check whether the Either contains an error."""


class Right(Either[E, A]):
    """Data structure representing Either with a value."""

    def __init__(self, value: A) -> None:
        self._value = value

    def get_value(self) -> A:
        return self._value

    def is_left(self) -> bool:
        return False


class Left(Either[E, A]):
    """Data structure representing Either with an error."""

    def __init__(self, value: E) -> None:
        self._value = value

    def get_value(self) -> E:
        return self._value

    def is_left(self) -> bool:
        return True


# Constructors


def left(e: E) -> Left[E, Any]:
    """Create Either with error E."""
    return Left(e)


def right(a: A) -> Right[Any, A]:
    """Create Either with value A."""
    return Right(a)


# Destructors


def is_left(fa: Either[E, A]) -> TypeGuard[Left[E, A]]:
    """Check whether Either contains an error."""
    return fa.is_left()


def is_right(fa: Either[E, A]) -> TypeGuard[Right[E, A]]:
    """Check whether Either contains a value."""
    return not fa.is_left()


# Instances


def of(a: A) -> Either[Any, A]:
    """Pointed"""
    return right(a)


@curry
def fmap(f: Fn[A, B], fa: Either[E, A]) -> Either[E, B]:
    """Functor"""
    if is_right(fa):
        return right(f(fa.get_value()))
    return cast(Either[E, B], fa)


@curry
def ap(f: Either[E, Fn[A, B]], fa: Either[E, A]) -> Either[E, B]:
    """Apply"""
    if is_right(f) and is_right(fa):
        return Right(f.get_value()(fa.get_value()))
    return cast(Either[E, B], fa)


@curry
def chain(f: Fn[A, Either[E, B]], fa: Either[E, A]) -> Either[E, B]:
    """Chain"""
    if is_right(fa):
        return f(fa.get_value())
    return cast(Either[E, B], fa)


# Combinators


@curry
def from_option(on_empty: Lazy[E], fa: option.Option[A]) -> Either[E, A]:
    """Create Either from option by providing error E in case the option is None."""
    if option.is_some(fa):
        return right(fa.get_value())
    return left(on_empty())


def _equals(a: Either[A, B], b: Either[A, B]) -> bool:
    both_same_value = is_right(a) and is_right(b) and a.get_value() == b.get_value()
    both_same_err = is_left(a) and is_left(b) and a.get_value() == b.get_value()
    return both_same_err or both_same_value


StandardEq = eq.from_equals(_equals)
