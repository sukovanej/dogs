from .data import io as IO
from .data import reader as R
from .data import reader_task as RT
from .data import task as T
from .function import Fn, apply, curry, pipe

__all__ = ["R", "T", "RT", "IO", "pipe", "Fn", "curry", "apply"]
