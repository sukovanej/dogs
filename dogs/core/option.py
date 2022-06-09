from abc import ABC, abstractmethod
from typing import Any, Optional, TypeGuard, TypeVar, Generic

from dogs.core.classes.apply import Apply, ap as _ap
from dogs.core.classes.chain import Chain, chain as _chain
from dogs.core.classes.functor import Functor, map as _map
from dogs.core.classes.pointed import Pointed, of as _of
from dogs.hkt.kind import Kind

from .function import Fn, curry

T = TypeVar("T")
A = TypeVar("A")
B = TypeVar("B")

# Model

class Option(Generic[T], ABC, Kind[Any, T]):
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

# Instances

F = TypeVar("F")

class _FunctorInstance(Functor[Option]):
    def map(self, f: Fn[A, B], fa: Option[A]) -> Option[B]:
        if is_some(fa):
            return some(f(fa._value))
        return none

class _ApplyInstance(Apply[Option], _FunctorInstance):
    @curry
    def ap(self, f: Option[Fn[A, B]], fa: Option[A]) -> Option[B]:
        if is_some(f) and is_some(fa):
            return Some((f.get_value())(fa.get_value()))
        return none

class _PointedInstance(Pointed[Option]):
    def of(self, a: T) -> Option[T]:
        return Some(a)


class _ChainInstance(Chain[Option], _ApplyInstance):
    def chain(self, f: Fn[A, Option[B]], fa: Option[A]) -> Option[B]:
        if is_some(fa):
            return f(fa.get_value())
        return none


functor = _FunctorInstance()
apply = _ApplyInstance()
pointed = _PointedInstance()
chain = _ChainInstance()

map = _map(functor)
ap = _ap(apply)
of = _of(pointed)
chain = _chain(chain)
