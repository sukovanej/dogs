from typing import Any, TypeVar
from collections.abc import Coroutine
from dogs.function import Fn, Lazy, curry

A = TypeVar("A")
B = TypeVar("B")

# model

Task = Lazy[Coroutine[None, None, A]]

# Pointed


def of(a: A) -> Task[A]:
    return lambda: a
