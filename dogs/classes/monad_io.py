from typing import TypeVar

from dogs.data.io_model import IO
from dogs.function import Fn, curry, pipe
from dogs.hkt.kind import Kind1

from .from_io import FromIO
from .monad import Monad

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


class MonadIO(FromIO[F], Monad[F]):
    ...


@curry
def chain_io(M: MonadIO[F], f: Fn[A, IO[B]], fa: Kind1[F, A]) -> Kind1[F, B]:
    return M.chain(lambda a: pipe(a, f, M.from_io), fa)
