from collections.abc import Awaitable
from typing import TypeVar

from dogs.data import io
from dogs.data.io import IO
from dogs.function import Fn, Lazy, curry

A = TypeVar("A")
B = TypeVar("B")

# model

Task = Lazy[Awaitable[A]]

# helper interop functions


async def _async_of(a: A) -> A:
    return a


async def _async_map(f: Fn[A, B], a: Awaitable[A]) -> B:
    return f(await a)


async def _async_ap(f: Awaitable[Fn[A, B]], fa: Awaitable[A]) -> B:
    return (await f)(await fa)


async def _async_chain(f: Fn[A, Awaitable[B]], fa: Awaitable[A]) -> B:
    return await f(await fa)


# Instances


def of(a: A) -> Task[A]:
    """Pointed"""
    return lambda: _async_of(a)


@curry
def fmap(f: Fn[A, B], fa: Task[A]) -> Task[B]:
    """Functor"""
    return lambda: _async_map(f, fa())


@curry
def ap(f: Task[Fn[A, B]], fa: Task[A]) -> Task[B]:
    """Apply"""
    return lambda: _async_ap(f(), fa())


@curry
def chain(f: Fn[A, Task[B]], fa: Task[A]) -> Task[B]:
    """Chain"""
    return lambda: _async_chain(lambda a: f(a)(), fa())


@curry
def from_io(fa: io.IO[A]) -> Task[A]:
    """FromIO"""
    return lambda: _async_of(fa())


@curry
def chain_io(f: Fn[A, IO[B]], fa: Task[A]) -> Task[B]:
    """Chain IO effect in the Task monad."""

    async def unsafe_run() -> B:
        a = await fa()
        return io.unsafe_run_io(f(a))

    return lambda: unsafe_run()


# Unsafe


async def unsafe_run_task(fa: Task[A]) -> A:
    """Run the task as a coroutine."""
    return await fa()
