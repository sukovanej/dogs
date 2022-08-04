from typing import TypedDict

from dogs.data import io as IO
from dogs.data import reader as R
from dogs.function import apply, pipe


class Dependencies(TypedDict):
    getter: IO.IO[int]


dependencies: Dependencies = {"getter": IO.of(1)}


def test_reader():
    result = pipe(
        R.ask(),
        R.fmap(lambda deps: deps["getter"]),
        R.fmap(IO.fmap(lambda i: i + 1)),
        apply(dependencies),
        IO.unsafe_run_io,
    )

    assert result == 2
