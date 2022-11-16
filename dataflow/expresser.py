import pandas
from typing import Callable
from util import mapper


class LeftExpression:
    def __init__(self, lexpr: dict):
        self._func_: Callable
        self._args_: list = []

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

    def map(self, data: pandas.DataFrame):
        # recursively call self._func_(*self._args_)
        # if a str that startswith $ in self._args_, transfers it to data[arg]
        args = self._args_.copy()
        for i in range(len(args)):
            if type(args[i]) is str and args[i].startswith("$"):
                args[i] = data[args[i]]
            elif isinstance(args[i], LeftExpression):
                args[i] = args[i].map(data)
        return self._func_(*args)
        # todo test with real data
        pass
