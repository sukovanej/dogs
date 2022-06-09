from typing import TypeVar

from .applicative import Applicative
from .chain import Chain



F = TypeVar("F")


class Monad(Applicative[F], Chain[F]):
    ...
