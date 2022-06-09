from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dogs.data import io
from dogs.function import curry
from dogs.hkt.kind import Kind

F = TypeVar("F", covariant=True)
A = TypeVar("A", covariant=True)


class FromIO(Generic[F], ABC):
    @abstractmethod
    def from_io(self, fa: io.IO[A]) -> Kind[F, A]:
        ...


@curry
def from_io(F: FromIO[F], fa: io.IO[A]) -> Kind[F, A]:
    return F.from_io(fa)