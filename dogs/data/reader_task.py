from typing import TypeVar

from dogs.function import Fn, curry, pipe
from dogs.data import task as T
from dogs.data import reader as R
from dogs.data import io as IO

A = TypeVar("A")
B = TypeVar("B")
D = TypeVar("D")


ReaderTask = R.Reader[D, T.Task[A]]

# Instances


def of(a: A) -> ReaderTask[None, A]:
    """Pointed"""
    return R.of(T.of(a))


@curry
def fmap(f: Fn[A, B], fa: ReaderTask[D, A]) -> ReaderTask[D, B]:
    """Functor"""
    return pipe(fa, R.fmap(T.fmap(f)))


@curry
def ap(f: ReaderTask[D, Fn[A, B]], fa: ReaderTask[D, A]) -> ReaderTask[D, B]:
    """Apply"""
    return lambda r: pipe(fa(r), T.ap(f(r)))


@curry
def chain(f: Fn[A, ReaderTask[D, B]], fa: ReaderTask[D, A]) -> ReaderTask[D, B]:
    """Chain"""
    return lambda r: pipe(fa(r), T.chain(lambda a: f(a)(r)))


@curry
def from_io(fa: IO.IO[A]) -> ReaderTask[None, A]:
    """FromIO"""
    return lambda _: T.from_io(fa)


@curry
def chain_io(f: Fn[A, IO.IO[B]], fa: ReaderTask[D, A]) -> ReaderTask[D, B]:
    """Chain IO effect in the Task monad."""
    return lambda r: T.chain_io(f)(fa(r))


# Constructors


def ask() -> ReaderTask[D, D]:
    """Create reader with the dependency in the value."""
    return lambda r: T.of(r)
