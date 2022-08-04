from typing import Generic, TypeVar

from dogs.hkt.kind import Kind1

A = TypeVar("A")
M = TypeVar("M")


class TaskT(Generic[M, A]):
    def run(self) -> Kind1[M, A]:
        raise NotImplemented
