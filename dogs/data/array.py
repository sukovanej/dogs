from typing import TypeVar

from dogs.function import Fn
from dogs.function.function import curry

# combinators

A = TypeVar("A")
B = TypeVar("B")


@curry
def take(n: int, xs: list[A]) -> list[A]:
    return xs[:n]


@curry
def replicate(n: int, x: A) -> list[A]:
    return [x] * n


def flatten(xs: list[list[A]]) -> list[A]:
    return [k for i in xs for k in i]


@curry
def fmap(fn: Fn[A, B], xs: list[A]) -> list[B]:
    return [fn(i) for i in xs]


@curry
def filter(pred: Fn[A, bool], xs: list[A]) -> list[A]:
    return [i for i in xs if pred(i)]
