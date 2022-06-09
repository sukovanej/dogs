from inspect import signature
from typing import Any, Callable, TypeVar, overload

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
    return CurriedFunction.from_fn(f)


class CurriedFunction:
    def __init__(self, fn, remaining_arguments, args):
        self._fn = fn
        self._remaining_arguments = remaining_arguments
        self._args = args
    
    @classmethod
    def from_fn(cls, fn):
        remaining_arguments = len(signature(fn).parameters)
        return cls(fn, remaining_arguments, [])

    def _partialy_apply(self, arg):
        return CurriedFunction(self._fn, self._remaining_arguments - 1, self._args + [arg])

    def __call__(self, arg):
        if self._remaining_arguments == 1:
            return self._fn(*(self._args + [arg]))
        else:
            return self._partialy_apply(arg)

    def __repr__(self):
        return f"[Curried function] {self._fn}"


# pipe


@overload
def pipe(init: A) -> A:
    ...


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
def pipe(
    init: A, /, f: Fn[A, B], g: Fn[B, C], h: Fn[C, D], i: Fn[D, E], j: Fn[E, F]
) -> F:
    ...


def pipe(init: Any, *fns: Any) -> Any:
    if len(fns) == 0:
        return init
    return pipe(fns[0](init), *fns[1:])


def apply(a: A) -> Fn[Fn[A, B], B]:
    def wrap(f: Fn[A, B]) -> B:
        return f(a)

    return wrap


def apply2(a: A, b: B) -> Fn[Fn[A, Fn[B, C]], C]:
    def wrap(f: Fn[A, Fn[B, C]]) -> C:
        return f(a)(b)

    return wrap

@curry
def tap(f: Fn[A, Any], a: A) -> A:
    f(a)
    return a
