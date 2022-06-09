from typing import TypeVar

from .from_io import FromIO
from .monad import Monad

F = TypeVar("F")


class MonadIO(FromIO[F], Monad[F]):
    ...
