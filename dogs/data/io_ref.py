from typing import Generic, TypeVar

from dogs.data import io
from dogs.data.unit import Unit, unit
from dogs.function import Fn, curry

A = TypeVar("A")

# Model


class IORef(Generic[A]):
    """Data structure representing mutable reference."""

    def __init__(self, value: A) -> None:
        self._value = value

    def get_value(self) -> A:
        """Get value under the reference"""
        return self._value

    def modify(self, value: A) -> Unit:
        """Modify value under the reference"""
        self._value = value
        return unit

    def __repr__(self):
        return f"[IORef] {self._value}"


# Constructor


def new_io_ref(a: A) -> io.IO[IORef[A]]:
    """Instantiate IORef with a value A."""
    return io.of(IORef(a))


# Utils


def read(ref: IORef[A]) -> io.IO[A]:
    """Read the value within the IO."""
    return lambda: ref.get_value()


@curry
def write(a: A, ref: IORef[A]) -> io.IO[Unit]:
    """Write the value within the IO."""
    return lambda: ref.modify(a)


@curry
def modify(f: Fn[A, A], ref: IORef[A]) -> io.IO[Unit]:
    """Modify the value within the IO."""
    return lambda: ref.modify(f(ref.get_value()))
