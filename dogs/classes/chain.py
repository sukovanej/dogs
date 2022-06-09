from abc import abstractmethod
from typing import Any, TypeVar

from dogs.function import Fn, curry
from dogs.hkt import Kind

from .apply import Apply

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Chain(Apply[F]):
    @abstractmethod
    def chain(self, f: Fn[A, Kind[F, B]], fa: Kind[F, A]) -> Kind[F, B]:
        ...


@curry
def chain(F: Chain[F], f: Fn[A, Kind[F, B]], fa: Kind[F, A]) -> Kind[F, B]:
    return F.chain(f, fa)


@curry
def chain_first(F: Chain[F], f: Fn[A, Kind[F, Any]], fa: Kind[F, A]) -> Kind[F, A]:
    return F.chain(lambda i: F.map((lambda _: i), f(i)), fa)
