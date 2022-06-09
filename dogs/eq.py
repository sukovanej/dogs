from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from dogs.function import curry

A = TypeVar("A")


class Eq(ABC, Generic[A]):
    @abstractmethod
    def equals(self, left: A, right: A) -> bool:
        ...

@curry
def equals(eq: Eq[A], a: A, b: A) -> bool:
    return eq.equals(a, b)
