from dogs.core import option
from dogs.core.function import pipe

def add_1(a: int) -> int:
    return a + 1

def test_map():
    pipe(
        option.some(1), 
        option.map(add_1)
    )
