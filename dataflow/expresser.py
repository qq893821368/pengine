import attr
from typing import Any
from typing import Callable
from util import mapper


class LeftExpression:
    def __init__(self, lexpr: dict):
        self._func_: Callable
        self._args_: list = []
        self._cures_: Any = None  # current result

        func: str = lexpr.get("function")
        if len(func) > 0:
            if func[0].isupper():
                self._func_ = mapper.__dict__[func]
            else:
                self._func_ = mapper.System[func]
        else:
            raise ValueError(f"存在无法解析的函数表达式，解析结果：{lexpr}")

        args = lexpr.get("args")
        for arg in args:
            if type(arg) is dict:
                self._args_.append(LeftExpression(arg))
            else:
                self._args_.append(arg)

    @property
    def current_result(self):
        return self.current_result

