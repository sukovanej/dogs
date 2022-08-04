from typing import TypeVar

from dogs.function import Fn, curry, Lazy

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model

IO = Lazy[A]

# Instances


def of(a: A) -> IO[A]:
    return lambda: a


@curry
def map(f: Fn[A, B], fa: IO[A]) -> IO[B]:
    return lambda: f(unsafe_run_io(fa))


@curry
def ap(f: IO[Fn[A, B]], fa: IO[A]) -> IO[B]:
    return lambda: unsafe_run_io(f)(unsafe_run_io(fa))


@curry
def chain(f: Fn[A, IO[B]], fa: IO[A]) -> IO[B]:
    return lambda: unsafe_run_io(f(fa()))


@curry
def chain_first(f: Fn[A, IO[B]], fa: IO[A]) -> IO[A]:
    def unsafe_run() -> A:
        first_result = unsafe_run_io(fa)
        unsafe_run_io(f(first_result))
        return first_result

    return unsafe_run


def from_io(fa: IO[A]) -> IO[A]:
    return fa


# Unsafe


def unsafe_run_io(fa: IO[A]) -> A:
    return fa()
