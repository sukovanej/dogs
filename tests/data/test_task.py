import asyncio

from dogs.data import io as IO
from dogs.data import task as T
from dogs.function import pipe


def test_task():
    my_effect = lambda a: T.of(a + 1)
    my_io_effect = lambda a: IO.of(a + 1)

    task = pipe(
        T.of(1),
        T.map(lambda a: a + 1),
        T.chain(my_effect),
        T.chain_io(my_io_effect),
    )

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(T.unsafe_run_task(task))

    assert result == 4
