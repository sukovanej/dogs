from typing import Any, TypeVar, overload

from .types import Fn

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")


@overload
def flow(f: Fn[A, B], /) -> Fn[A, B]:
    ...


@overload
def flow(f: Fn[A, B], g: Fn[B, C], /) -> Fn[A, C]:
    ...


@overload
def flow(f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], /) -> Fn[A, D]:
    ...


@overload
def flow(f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], /) -> Fn[A, E]:
    ...


@overload
def flow(
    f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], j: Fn[E, F], /
) -> Fn[A, F]:
    ...


@overload
def flow(
    f: Fn[A, B],
    g: Fn[B, C],
    h: Fn[C, D],
    i: Fn[D, E],
    j: Fn[E, F],
    k: Fn[F, G],
    /,
) -> Fn[A, G]:
    ...


@overload
def flow(
    f: Fn[A, B],
    g: Fn[B, C],
    h: Fn[C, D],
    i: Fn[D, E],
    j: Fn[E, F],
    k: Fn[F, G],
    l: Fn[G, H],
    /,
) -> Fn[A, H]:
    ...


def flow(*fns: Any) -> Any:
    """Transform value `init` using provided function one by one."""
    if len(fns) == 1:
        return lambda a: fns[0](a)
    return lambda a: flow(*fns[1:])(fns[0](a))
