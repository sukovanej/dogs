from dogs.data import either as E
from dogs.function import pipe


def test_either():
    result = pipe(E.of(69), E.fmap(lambda a: a + 1), E.chain(lambda a: E.of(a + 1)))

    assert E.StandardEq.equals(result, E.of(71))
