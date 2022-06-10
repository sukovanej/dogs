from dogs.data import io, io_ref
from dogs.function import pipe


def test_io_ref():
    program = pipe(
        io_ref.new_io_ref(1), io.chain_first(io_ref.write(2)), io.chain(io_ref.read)
    )

    assert io.unsafe_run_io(program) == 2
