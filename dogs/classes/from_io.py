from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dogs.data.io_model import IO
from dogs.function import curry
from dogs.hkt.kind import Kind

F = TypeVar("F", covariant=True)
A = TypeVar("A", covariant=True)


class FromIO(Generic[F], ABC):
    @abstractmethod
    def from_io(self, fa: IO[A]) -> Kind[F, A]:
        ...


@curry
def from_io(F: FromIO[F], fa: IO[A]) -> Kind[F, A]:
    return F.from_io(fa)
