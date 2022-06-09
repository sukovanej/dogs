from dogs.core.function import apply, curry, pipe


def test_curry():
    @curry
    def add(a, b):
        return a + b

    assert pipe(1, add(1)) == 2

    @curry
    def another(a, b, c):
        return a + b + c

    assert pipe(another, apply(1), apply(2), apply(3)) == 6

    @curry
    def and_another(a, b, c, d):
        return a + b + c + d

    assert pipe(and_another, apply(1), apply(2), apply(3), apply(4)) == 10
