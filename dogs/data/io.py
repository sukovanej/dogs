from typing import TypeVar

from dogs.function import Fn, Lazy, curry

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model

IO = Lazy[A]

# Instances


def of(a: A) -> IO[A]:
    """Pointed"""
    return lambda: a


@curry
def fmap(f: Fn[A, B], fa: IO[A]) -> IO[B]:
    """Functor"""
    return lambda: f(unsafe_run_io(fa))


@curry
def ap(f: IO[Fn[A, B]], fa: IO[A]) -> IO[B]:
    """Apply"""
    return lambda: unsafe_run_io(f)(unsafe_run_io(fa))


@curry
def chain(f: Fn[A, IO[B]], fa: IO[A]) -> IO[B]:
    """Chain"""
    return lambda: unsafe_run_io(f(fa()))


@curry
def chain_first(f: Fn[A, IO[B]], fa: IO[A]) -> IO[A]:
    """Chain"""

    def unsafe_run() -> A:
        first_result = unsafe_run_io(fa)
        unsafe_run_io(f(first_result))
        return first_result

    return unsafe_run


def from_io(fa: IO[A]) -> IO[A]:
    """FromIO"""
    return fa


# Unsafe


def unsafe_run_io(fa: IO[A]) -> A:
    """Run the IO."""
    return fa()
