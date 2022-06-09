from typing import Callable, TypeVar

from dogs.function import Fn, curry

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model

IO = Callable[[], T]

# Pointed


def of(a: T) -> IO[T]:
    return lambda: a


# Functor


@curry
def map(f: Fn[A, B], fa: IO[A]) -> IO[B]:
    return lambda: f(unsafe_run_io(fa))


# Apply


@curry
def ap(f: IO[Fn[A, B]], fa: IO[A]) -> IO[B]:
    return lambda: unsafe_run_io(f)(unsafe_run_io(fa))


# Chain


def chain(f: Fn[A, IO[B]], fa: IO[A]) -> IO[B]:
    return lambda: unsafe_run_io(f(fa()))


# Unsafe


def unsafe_run_io(fa: IO[A]) -> A:
    return fa()
