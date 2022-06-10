from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from dogs.function import Fn, curry
from dogs.hkt.kind import Kind1

F = TypeVar("F", covariant=True)
A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)


class Functor(Generic[F], ABC):
    @abstractmethod
    def map(self, f: Fn[A, B], fa: Kind1[F, A]) -> Kind1[F, B]:
        ...


@curry
def map(F: Functor[F], f: Fn[A, B], fa: Kind1[F, A]) -> Kind1[F, B]:
    return F.map(f, fa)
