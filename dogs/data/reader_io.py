from typing import TypeVar

from dogs.data import io as IO
from dogs.data import reader as R
from dogs.function import Fn, constant, curry, pipe

A = TypeVar("A")
B = TypeVar("B")
D = TypeVar("D")


ReaderIO = R.Reader[D, IO.IO[A]]

# Instances


def of(a: A) -> ReaderIO[None, A]:
    """Pointed"""
    return R.of(IO.of(a))


@curry
def fmap(f: Fn[A, B], fa: ReaderIO[D, A]) -> ReaderIO[D, B]:
    """Functor"""
    return R.fmap(IO.fmap(f))(fa)


@curry
def ap(f: ReaderIO[D, Fn[A, B]], fa: ReaderIO[D, A]) -> ReaderIO[D, B]:
    """Apply"""
    return lambda r: pipe(fa(r), IO.ap(f(r)))  # type: ignore


@curry
def chain(f: Fn[A, ReaderIO[D, B]], fa: ReaderIO[D, A]) -> ReaderIO[D, B]:
    """Chain"""
    return lambda r: pipe(fa(r), IO.chain(lambda a: f(a)(r)))  # type: ignore


@curry
def from_io(fa: IO.IO[A]) -> ReaderIO[None, A]:
    """FromIO"""
    return constant(fa)


@curry
def chain_io(f: Fn[A, IO.IO[B]], fa: ReaderIO[D, A]) -> ReaderIO[D, B]:
    """Chain IO effect in the Task monad."""
    return lambda r: IO.chain(f)(fa(r))


# Constructors


def ask() -> ReaderIO[D, D]:
    """Create reader with the dependency in the value."""
    return lambda r: IO.of(r)
