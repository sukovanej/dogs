from typing import Any, Generic, TypeVar

F = TypeVar("F")
A = TypeVar("A")
E = TypeVar("E")
R = TypeVar("R")

# No idea now how to do this properly now


class Kind(Generic[F, A, E, R]):
    pass


Kind1 = Kind[F, A, Any, Any]
Kind2 = Kind[F, A, E, Any]
Kind3 = Kind[F, A, E, R]
