from typing import TypeVar

from dogs.function import Lazy

T = TypeVar("T")

# Model

IO = Lazy[T]
