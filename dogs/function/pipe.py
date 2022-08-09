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
def pipe(init: A, /) -> A:
    ...


@overload
def pipe(init: A, f: Fn[A, B], /) -> B:
    ...


@overload
def pipe(init: A, f: Fn[A, B], g: Fn[B, C], /) -> C:
    ...


@overload
def pipe(init: A, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], /) -> D:
    ...


@overload
def pipe(init: A, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], /) -> E:
    ...


@overload
def pipe(
    init: A, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], j: Fn[E, F], /
) -> F:
    ...


@overload
def pipe(
    init: A,
    f: Fn[A, B],
    g: Fn[B, C],
    h: Fn[C, D],
    i: Fn[D, E],
    j: Fn[E, F],
    k: Fn[F, G],
    /,
) -> G:
    ...


@overload
def pipe(
    init: A,
    f: Fn[A, B],
    g: Fn[B, C],
    h: Fn[C, D],
    i: Fn[D, E],
    j: Fn[E, F],
    k: Fn[F, G],
    l: Fn[G, H],
    /,
) -> H:
    ...


def pipe(init: Any, *fns: Any) -> Any:
    """Transform value `init` using provided function one by one."""
    if len(fns) == 0:
        return init
    return pipe(fns[0](init), *fns[1:])
