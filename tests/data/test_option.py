from dogs.data import option as O
from dogs.function import pipe


def add_1(a: int) -> int:
    return a + 1


def test_option():
    result = pipe(O.some(1), O.map(add_1), O.chain(lambda x: O.some(x + 2)))

    assert O.StandardEq.equals(result, O.some(4))
