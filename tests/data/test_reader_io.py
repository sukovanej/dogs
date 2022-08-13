from typing import TypedDict

from dogs import RIO, IO, apply
from dogs.function.pipe_operator import start_empty_pipe, end_pipe


class Dependencies(TypedDict):
    getter: int


dependencies: Dependencies = {"getter": 1}

def add_1(i: int) -> int:
    return i + 1


def test_reader():
    program = (
        start_empty_pipe
        | RIO.ask()
        | RIO.fmap(lambda deps: deps["getter"])
        | RIO.fmap(add_1)
        | RIO.chain(lambda i: RIO.of(i + 1))
        | apply(dependencies)
        | end_pipe
    )

    result = IO.unsafe_run_io(program)

    assert result == 3
