import functools
import re
import time
from typing import List


class TimeQuantum:
    quantum_pattern: str = "^(([0-1][0-9])|(2[0-3])):[0-5][0-9]$"

    def __init__(self, start: str, end: str):
        self._start_: str = "-00:00"
        self._end_: str = "-00:00"
        start = start.strip()
        end = end.strip()
        if re.match(TimeQuantum.quantum_pattern, start) is not None:
            self._start_ = start
        if re.match(TimeQuantum.quantum_pattern, end) is not None:
            self._end_ = end

    def __str__(self):
        return "-".join((self._start_, self._end_))

    def __repr__(self):
        return self.__str__()

    def __contains__(self, item: str):
        if self._start_.startswith("-"):
            if self._end_.startswith("-"):
                return False
            else:
                return item <= self._end_
        else:
            if self._end_.startswith("-"):
                return self._start_ <= item
            else:
                return self._start_ <= item <= self._end_


class Silenter:
    def __init__(self, data: List[str]):
        self._data_: List[TimeQuantum] = [TimeQuantum(*tq.split("-")) for tq in data]

    def __str__(self):
        return str([str(tq) for tq in self._data_])

    def __repr__(self):
        return f"{time.strftime('%H:%M')}{' not' if self.is_silent() else ''} in {self.__str__()}"

    def __call__(self, *args, **kwargs):
        return self.is_silent()

    def is_silent(self) -> bool:
        now: str = time.strftime("%H:%M")
        r: List[bool] = [(now in tq) for tq in self._data_]
        return functools.reduce(lambda x, y: x or y, r)
