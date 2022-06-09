from abc import abstractmethod
from typing import Generic, TypeVar

from dogs.function import curry
from dogs.hkt import Kind

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Pointed(Generic[F]):
    @abstractmethod
    def of(self, a: A) -> Kind[F, A]:
        ...


@curry
def of(F: Pointed[F], a: A) -> Kind[F, A]:
    return F.of(a)
