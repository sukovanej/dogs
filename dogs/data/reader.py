from typing import Any, TypeVar

from dogs.function import Fn, curry

A = TypeVar("A")
B = TypeVar("B")
R = TypeVar("R")

# Model

Reader = Fn[R, A]

# Constructors


def ask() -> Reader[R, R]:
    return lambda r: r


# Pointed


def of(a: A) -> Reader[Any, A]:
    return lambda _: a


# Functor


@curry
def map(f: Fn[A, B], fa: Reader[R, A]) -> Reader[R, B]:
    return lambda r: f(fa(r))


# Apply


@curry
def ap(f: Reader[R, Fn[A, B]], fa: Reader[R, A]) -> Reader[R, B]:
    return lambda r: f(r)(fa(r))


# Chain


def chain(f: Fn[A, Reader[B]], fa: Reader[R, A]) -> Reader[R, B]:
    return lambda r: f(fa(r))(r)
