from __future__ import annotations

from functools import reduce
from typing import Any, Generic, TypeGuard, TypeVar, cast, overload

from dogs.function import Fn

A = TypeVar("A")
B = TypeVar("B")


class _EndPipe:
    pass


end_pipe = _EndPipe()


class Pipeable(Generic[A]):
    def __init__(self, a: A) -> None:
        self._a = a
        self._fns: list[Fn[Any, Any]] = []

    def __with_new_fn(self, fn: Fn[A, B]) -> Pipeable[B]:
        new_pipeable = Pipeable(self._a)
        new_pipeable._fns = self._fns
        new_pipeable._fns.append(fn)
        return cast(Pipeable[B], new_pipeable)

    @staticmethod
    def __is_end_pipe(symbol: Any) -> TypeGuard[_EndPipe]:
        return isinstance(symbol, _EndPipe)

    @overload
    def __or__(self, fn: Fn[A, B]) -> Pipeable[B]:
        ...

    @overload
    def __or__(self, fn: _EndPipe) -> A:
        ...

    def __or__(self, fn: Fn[A, B] | _EndPipe) -> Pipeable[B] | A:
        if self.__is_end_pipe(fn):
            return self.eval()

        return self.__with_new_fn(cast(Fn[A, B], fn))

    def eval(self) -> A:
        return reduce(lambda acc, fn: fn(acc), self._fns, self._a)


def start_pipe(a: A) -> Pipeable[A]:
    return Pipeable(a)
