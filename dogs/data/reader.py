from typing import Any, TypeVar

from dogs.function import Fn, constant, curry, identity

A = TypeVar("A")
B = TypeVar("B")
R = TypeVar("R")

# Model

Reader = Fn[R, A]

# Instances


def of(a: A) -> Reader[Any, A]:
    """Pointed"""
    return constant(a)


@curry
def fmap(f: Fn[A, B], fa: Reader[R, A]) -> Reader[R, B]:
    """Functor"""
    return lambda r: f(fa(r))


@curry
def ap(f: Reader[R, Fn[A, B]], fa: Reader[R, A]) -> Reader[R, B]:
    """Apply"""
    return lambda r: f(r)(fa(r))


@curry
def chain(f: Fn[A, Reader[R, B]], fa: Reader[R, A]) -> Reader[R, B]:
    """Chain"""
    return lambda r: f(fa(r))(r)


# Constructors


def ask() -> Reader[R, R]:
    """Create reader with the dependency in the value."""
    return identity
