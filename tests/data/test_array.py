from dogs.data import array as A
from dogs.function import Fn
from dogs.function.pipe_operator import end_pipe, start_pipe

add_1: Fn[int, int] = lambda x: x + 1
multiply_by: Fn[int, Fn[int, int]] = lambda y: lambda x: x * y


def test_replicate() -> None:
    result = start_pipe(1) | A.replicate(3) | end_pipe
    assert result == [1, 1, 1]


def test_map() -> None:
    result = start_pipe([1, 1]) | A.fmap(add_1) | end_pipe
    assert result == [2, 2]


def test_replicate_map() -> None:
    result = start_pipe(1) | A.replicate(3) | A.fmap(add_1) | end_pipe
    assert result == [2, 2, 2]


def test_long_example() -> None:
    result = (
        start_pipe(1)
        | A.replicate(3)
        | A.fmap(add_1)
        | A.replicate(2)
        | A.flatten
        | A.fmap(multiply_by(2))
        | end_pipe
    )
    assert result == [4, 4, 4, 4, 4, 4]
