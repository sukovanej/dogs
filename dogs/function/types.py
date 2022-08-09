from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")

Lazy = Callable[[], A]
Fn = Callable[[A], B]
Fn2 = Callable[[A, B], C]
Fn3 = Callable[[A, B, C], D]
Fn4 = Callable[[A, B, C, D], E]
