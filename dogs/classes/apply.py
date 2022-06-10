from abc import abstractmethod
from typing import TypeVar

from dogs.function import Fn, curry
from dogs.hkt.kind import Kind1

from .functor import Functor

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Apply(Functor[F]):
    @abstractmethod
    def ap(self, f: Kind1[F, Fn[A, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
        ...


@curry
def ap(F: Apply[F], f: Kind1[F, Fn[A, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
    return F.ap(f, fa)
