from abc import abstractmethod
from typing import Any, TypeVar

from dogs.function import Fn, curry
from dogs.hkt.kind import Kind1

from .apply import Apply

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Chain(Apply[F]):
    @abstractmethod
    def chain(self, f: Fn[A, Kind1[F, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
        ...


@curry
def chain(F: Chain[F], f: Fn[A, Kind1[F, B]], fa: Kind1[F, A]) -> Kind1[F, B]:
    return F.chain(f, fa)


@curry
def chain_first(F: Chain[F], f: Fn[A, Kind1[F, Any]], fa: Kind1[F, A]) -> Kind1[F, A]:
    return F.chain(lambda i: F.map((lambda _: i), f(i)), fa)
