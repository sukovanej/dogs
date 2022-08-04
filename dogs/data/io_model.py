from typing import TypeVar

from dogs.function import Lazy

A = TypeVar("A")

# Model

IO = Lazy[A]
