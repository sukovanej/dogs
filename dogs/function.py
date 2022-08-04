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
    """Convert a function of arbitrary number of argument into a curried function."""
    return CurriedFunction.from_fn(f)


class CurriedFunction:
    """Wraps a function a provides curried __call__ protocol."""

    def __init__(self, fn, remaining_arguments, args):
        self._fn = fn
        self._remaining_arguments = remaining_arguments
        self._args = args

    @classmethod
    def from_fn(cls, fn):
        """Create CurriedFunction from an arbitrary function."""

        remaining_arguments = len(signature(fn).parameters)
        return cls(fn, remaining_arguments, [])

    def _partialy_apply(self, arg):
        return CurriedFunction(
            self._fn, self._remaining_arguments - 1, self._args + [arg]
        )

    def __call__(self, arg):
        if self._remaining_arguments == 1:
            return self._fn(*(self._args + [arg]))
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


def pipe(init: Any, *fns: Any) -> Any:  # type: ignore
    """Transform value `init` using provided function one by one."""
    if len(fns) == 0:
        return init
    return pipe(fns[0](init), *fns[1:])


def apply(a: A) -> Fn[Fn[A, B], B]:
    """Created a function that accepts a function and returns a result of applying the
    function with the argument A.
    """

    def wrap(f: Fn[A, B]) -> B:
        return f(a)

    return wrap


def apply2(a: A, b: B) -> Fn[Fn[A, Fn[B, C]], C]:
    """Created a function that accepts a function and returns a result of applying the
    function with the argument A and B.
    """

    def wrap(f: Fn[A, Fn[B, C]]) -> C:
        return f(a)(b)

    return wrap


@curry
def tap(f: Fn[A, Any], a: A) -> A:
    """Unsafe version of chain_first.

    Don't use in the production code!
    """
    f(a)
    return a
