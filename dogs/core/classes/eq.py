from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from dogs.core.function import Fn2

from dogs.core.function import curry

A = TypeVar("A")


class Eq(ABC, Generic[A]):
    @abstractmethod
    def equals(self, left: A, right: A) -> bool:
        ...


@curry
def equals(eq: Eq[A], a: A, b: A) -> bool:
    return eq.equals(a, b)


class _EqFromFn(Eq[A]):
    def __init__(self, fn: Fn2[A, A, bool]) -> None:
        self._fn = fn

    def equals(self, left: A, right: A) -> bool:
        return self._fn(left, right)


def from_equals(f: Fn2[A, A, bool]) -> Eq[A]:
    return _EqFromFn(f)


standard_eq = from_equals(lambda a, b: a == b)

# eq for builtin types

intEq: Eq[int] = standard_eq
strEq: Eq[str] = standard_eq
