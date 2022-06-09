from abc import abstractmethod
from typing import TypeVar

from dogs.function import Fn, curry
from dogs.hkt import Kind

from .functor import Functor

F = TypeVar("F")
A = TypeVar("A", covariant=True)
B = TypeVar("B", covariant=True)


class Apply(Functor[F]):
    @abstractmethod
    def ap(self, f: Kind[F, Fn[A, B]], fa: Kind[F, A]) -> Kind[F, B]:
        ...


@curry
def ap(F: Apply[F], f: Kind[F, Fn[A, B]], fa: Kind[F, A]) -> Kind[F, B]:
    return F.ap(f, fa)
