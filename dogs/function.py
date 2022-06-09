from typing import Any, Callable, TypeVar, overload
from inspect import signature
from functools import partial

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")

Lazy = Callable[[], A]
Fn = Callable[[A], B]
Fn2 = Callable[[A, B], C]
Fn3 = Callable[[A, B, C], D]
Fn4 = Callable[[A, B, C, D], E]

# curry

@overload
def curry(f: Fn4[A, B, C, D, E]) -> Fn[A, Fn[B, Fn[C, Fn[D, E]]]]:
    ...

@overload
def curry(f: Fn3[A, B, C, D]) -> Fn[A, Fn[B, Fn[C, D]]]:
    ...

@overload
def curry(f: Fn2[A, B, C]) -> Fn[A, Fn[B, C]]:
    ...

@overload
def curry(f: Fn[A, B]) -> Fn[A, B]:
    ...

def curry(f: Any) -> Any:
    def wrapper(remaining_arguments: int, f, a):
        remaining_arguments = remaining_arguments - 1
        if remaining_arguments == 0:
            return f(a)
        return partial(wrapper, remaining_arguments - 1, partial(f, a))

    sig = signature(f)
    remaining_arguments = len(sig.parameters)

    return partial(wrapper, remaining_arguments)

# pipe

@overload
def pipe(init: A, /, f: Fn[A, B]) -> B:
    ...

@overload
def pipe(init: A, /, f: Fn[A, B], g: Fn[B, C]) -> C:
    ...

@overload
def pipe(init: A, /, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D]) -> D:
    ...

@overload
def pipe(init: A, /, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E]) -> E:
    ...

@overload
def pipe(init: A, /, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], j: Fn[E, F]) -> F:
    ...

def pipe(init: Any, /, *fns: Any) -> Any:
    if len(fns) == 0:
        return init
    return pipe(fns[0](init), *fns[1:])
