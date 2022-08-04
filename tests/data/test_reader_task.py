import asyncio

from typing import TypedDict

from dogs import RT, apply, pipe, T


class Dependencies(TypedDict):
    getter: int


dependencies: Dependencies = {"getter": 1}


def test_reader():
    task = pipe(
        RT.ask(),
        RT.fmap(lambda deps: deps["getter"]),
        RT.fmap(lambda i: i + 1),
        RT.chain(lambda i: RT.of(i + 1)),
        apply(dependencies),
    )

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(T.unsafe_run_task(task))

    assert result == 3
