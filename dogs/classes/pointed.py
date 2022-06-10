from abc import abstractmethod
from typing import Generic, TypeVar

from dogs.function import Fn, curry
from dogs.hkt.kind import Kind1

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Pointed(Generic[F]):
    @abstractmethod
    def of(self, a: A) -> Kind1[F, A]:
        ...


def of(F: Pointed[F]) -> Fn[A, Kind1[F, A]]:
    def f(a: A) -> Kind1[F, A]:
        return F.of(a)

    return f
