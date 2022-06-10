from typing import TypedDict

from dogs.data import io as IO
from dogs.data import reader as R
from dogs.function import Fn, apply, pipe


class Dependencies(TypedDict):
    getter: IO.IO[int]


dependencies: Dependencies = {"getter": IO.of(1)}


def test_reader():
    result = pipe(
        R.ask(),
        R.map(lambda deps: deps["getter"]),
        R.map(IO.map(lambda i: i + 1)),
        apply(dependencies),
        IO.unsafe_run_io,
    )

    assert result == 2
