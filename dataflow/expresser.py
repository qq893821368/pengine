import ast
import pandas
import pyparsing
from typing import Any
from typing import Callable
from . import matcher
from util import mapper
from util import parser


class LeftExpression:
    """
    Not an actual left expression, but an expression in the form of `func1(args.., func2(args..., ...))`

    A LeftExpression obj initializes with a dict which parsed from `util.parser.parse_rule_lexpr` (str).
    """
    def __init__(self, lexpr: dict):
        self._func_: Callable
        self._fname_: str
        self._args_: list = []

        func: str = lexpr.get("function")
        if len(func) > 0:
            if func[0].isupper():
                self._func_ = mapper.__dict__[func]
            else:
                self._func_ = mapper.System[func]
            self._fname_ = func
        else:
            raise ValueError(f"存在无法解析的函数表达式，解析结果：{lexpr}")

        args = lexpr.get("args")
        for arg in args:
            if type(arg) is dict:
                self._args_.append(LeftExpression(arg))
            else:
                self._args_.append(arg)
    
    @property
    def function(self):
        return self._func_
    
    @property
    def function_name(self):
        return self._fname_
    
    @property
    def arguments(self):
        return self._args_.copy()
    
    def __str__(self):
        args = self.arguments
        for i in range(len(args)):
            if type(args[i]) is not str:
                args[i] = str(args[i])
        return self.function_name + "(" + ",".join(args) + ")"

    def map(self, data: pandas.DataFrame):
        """
        Recursively call self.function(*self.arguments) to map the original data into the result expressed by
        the obj self.

        If the string argument `arg` in the argument startswith $, convert it to data[arg].

        :param data: original data
        :return: mapped data
        """
        args = self.arguments
        for i in range(len(args)):
            if type(args[i]) is str and args[i].startswith("$"):
                args[i] = data[args[i][1:]]
            elif isinstance(args[i], LeftExpression):
                args[i] = args[i].map(data)
        return self.function(*args)


class Ruler:
    """
    A Ruler obj initializes with a raw rule expression string.

    Ruler obj will recognize expression automatically to parse it into a LeftExpression obj, an operator obj
    and a value, it checks whether the data matches the rule by calling the method `compare` of operator obj.
    """
    def __init__(self, expr: str):
        lexpr, op, rexpr = expr.split()[:3]
        try:
            lexpr = parser.parse_rule_lexpr(lexpr)
        except pyparsing.exceptions.ParseException:
            lexpr, rexpr = parser.parse_rule_lexpr(rexpr), lexpr
        self._lexpr_: LeftExpression = LeftExpression(lexpr)
        self._op_: matcher.Matcher = matcher.create_matcher(op)
        self._rexpr_: Any = ast.literal_eval(rexpr)

    @property
    def lexpr(self):
        return self._lexpr_

    @property
    def left_expression(self):
        return str(self._lexpr_)

    @property
    def val(self):
        return self._rexpr_

    @property
    def value(self):
        return str(self._rexpr_)
        
    @property
    def operator(self):
        return str(self._op_)

    @property
    def op(self):
        return self._op_

    def __str__(self):
        return " ".join((self.left_expression, self.operator, self.value))

    def match(self, data):
        return self.op.compare(self._lexpr_.map(data), self._rexpr_)


