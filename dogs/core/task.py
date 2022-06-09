from typing import TypeVar
from collections.abc import Coroutine
from dogs.core.function import Lazy

A = TypeVar("A")
B = TypeVar("B")

# model

Task = Lazy[Coroutine[None, None, A]]

# Pointed


def of(a: A) -> Task[A]:
    return lambda: a
