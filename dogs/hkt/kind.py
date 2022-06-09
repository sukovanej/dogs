from typing import Generic, TypeVar

F = TypeVar("F")
A = TypeVar("A")

# No idea now how to do this properly now


class Kind(Generic[F, A]):
    pass
