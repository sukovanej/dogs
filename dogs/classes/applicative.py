from typing import TypeVar

from .apply import Apply
from .pointed import Pointed

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class Applicative(Apply[F], Pointed[F]):
    ...
