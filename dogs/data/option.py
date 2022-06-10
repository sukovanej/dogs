from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Optional, TypeGuard, TypeVar, cast

from dogs.classes import eq
from dogs.classes.applicative import Applicative
from dogs.classes.apply import Apply
from dogs.classes.apply import ap as _ap
from dogs.classes.chain import Chain
from dogs.classes.chain import chain as _chain
from dogs.classes.functor import Functor
from dogs.classes.functor import map as _map
from dogs.classes.monad import Monad
from dogs.classes.pointed import Pointed
from dogs.classes.pointed import of as _of
from dogs.function import Fn
from dogs.hkt.kind import Kind1

A = TypeVar("A")
AC = TypeVar("AC", covariant=True)
B = TypeVar("B", covariant=True)

# Model


class Option(ABC, Kind1["Option", A]):
    @abstractmethod
    def get_value(self) -> Optional[A]:
        ...


OptionKind = Kind1[Option, A]


class Some(Option[A]):
    def __init__(self, value: A) -> None:
        self._value = value

    def get_value(self) -> A:
        return self._value


class Nothing(Option[A]):
    def get_value(self) -> None:
        return None


# Constructors


def some(a: A) -> Option[A]:
    return Some(a)


def none() -> Nothing[Any]:
    return Nothing()


# Destructors


def is_some(fa: Option[A]) -> TypeGuard[Some[A]]:
    return fa.get_value() is not None


def is_none(fa: Option[A]) -> TypeGuard[Nothing[A]]:
    return fa.get_value() is None


# Instances


class PointedInstance(Pointed[Option]):
    def of(self, a: A) -> OptionKind[A]:
        return Some(a)


class FunctorInstance(Functor[Option]):
    def map(self, f: Fn[AC, B], fa: OptionKind[AC]) -> Option[B]:
        fa = cast(Option[AC], fa)

        if is_some(fa):
            return some(f(fa._value))
        return none()


class ApplyInstance(Apply[Option], FunctorInstance):
    def ap(self, f: OptionKind[Fn[A, B]], fa: OptionKind[A]) -> OptionKind[B]:
        fa = cast(Option[A], fa)
        f = cast(Option[Fn[A, B]], f)

        if is_some(f) and is_some(fa):
            return Some((f.get_value())(fa.get_value()))
        return none()


class ApplicativeInstance(Applicative, ApplyInstance, PointedInstance):
    pass


class ChainInstance(Chain[Option], ApplyInstance):
    def chain(self, f: Fn[A, OptionKind[B]], fa: OptionKind[A]) -> OptionKind[B]:
        fa = cast(Option[A], fa)
        f = cast(Fn[A, Option[B]], f)

        if is_some(fa):
            return f(fa.get_value())
        return none()


class MonadInstance(Monad, ChainInstance, ApplicativeInstance):
    pass


pointed_instance = PointedInstance()
functor_instance = FunctorInstance()
apply_instance = ApplyInstance()
applicative_instance = ApplicativeInstance()
chain_instance = ChainInstance()
monad_instance = MonadInstance()

of = _of(pointed_instance)
map = _map(functor_instance)
ap = _ap(apply_instance)
chain = _chain(chain_instance)


def create_eq(E: eq.Eq[A]) -> eq.Eq[Option[A]]:
    return eq.from_equals(partial(_equals, E))


def _equals(E: eq.Eq[A], a: Option[A], b: Option[A]) -> bool:
    both_none = is_none(a) and is_none(b)
    both_same = is_some(a) and is_some(b) and E.equals(a.get_value(), b.get_value())
    return both_none or both_same


StandardEq = create_eq(eq.standard_eq)
