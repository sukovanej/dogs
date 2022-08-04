from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from dogs.function import Fn2, curry

A = TypeVar("A")


class Eq(ABC, Generic[A]):
    """Class defining how to compare objects of type A."""

    @abstractmethod
    def equals(self, left: A, right: A) -> bool:
        """Checker whether left === right under Eq[A]."""


@curry
def equals(eq: Eq[A], a: A, b: A) -> bool:
    """Checker whether left === right under Eq[A]."""
    return eq.equals(a, b)


class _EqFromFn(Eq[A]):
    def __init__(self, fn: Fn2[A, A, bool]) -> None:
        self._fn = fn

    def equals(self, left: A, right: A) -> bool:
        return self._fn(left, right)


def from_equals(f: Fn2[A, A, bool]) -> Eq[A]:
    """Construct Eq[A] from a function A -> A -> bool."""
    return _EqFromFn(f)


standard_eq: Eq[Any] = from_equals(lambda a, b: a == b)

# eq for builtin types

intEq: Eq[int] = standard_eq
strEq: Eq[str] = standard_eq
