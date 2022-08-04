from typing import TypeVar

from dogs.function import Lazy
from dogs.hkt.kind import Kind1

A = TypeVar("A")

# Model

IOModel = Lazy[A]

IOKind = TypeVar("IOKind", bound=IOModel)

IO = Kind1[IOKind, A]
