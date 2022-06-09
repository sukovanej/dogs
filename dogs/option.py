from abc import ABC, abstractmethod
from typing import Optional, TypeGuard, TypeVar, Generic

from .function import Fn, curry

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model

class Option(Generic[T], ABC):
    @abstractmethod
    def get_value(self) -> Optional[T]:
        ...

class Some(Option[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def get_value(self) -> T:
        return self._value

class Nothing(Option[T]):
    def get_value(self) -> None:
        return None

# Constructors

def some(a: A) -> Option[A]:
    return Some(a)

none = Nothing()

# Destructors

def is_some(fa: Option[A]) -> TypeGuard[Some[A]]:
    return fa.get_value() is not None

def is_none(fa: Option[A]) -> TypeGuard[Nothing[A]]:
    return fa.get_value() is None

# Pointed

def of(a: T) -> Option[T]:
    return Some(a)


# Functor

@curry
def map(f: Fn[A, B], fa: Option[A]) -> Option[B]:
    if is_some(fa):
        return some(f(fa._value))
    return none


# Apply

@curry
def ap(f: Option[Fn[A, B]], fa: Option[A]) -> Option[B]:
    if is_some(f) and is_some(fa):
        return Some((f.get_value())(fa.get_value()))
    return none

# Chain

@curry
def chain(f: Fn[A, Option[B]], fa: Option[A]) -> Option[B]:
    if is_some(fa):
        return f(fa.get_value())
    return none
