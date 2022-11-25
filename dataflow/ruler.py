from typing import Callable
from dataflow.expresser import Expression
from util.processor import Process


class Ruler:
    def __init__(self, master: str, name: str, settings: dict):
        self._master_: str = master.strip()
        self._name_: str = name.strip()
        self._type_: str = settings.pop("type", "expr")
        self._rule_value_: Callable

        value = settings.pop("value", "")
        env = settings.pop("env", {})
        if self._type_ == "expr":
            self._rule_value_ = Expression(value)
        elif self._type_ == "proc":
            self._rule_value_ = Process(value, env)
        elif self._type_ == "lambda":
            self._rule_value_ = Process(f"return {value.replace('$[name]', self._master_)}", env)
        else:
            raise ValueError(f"Unrecognized rule type: {self._type_}")

    def __call__(self, *args, **kwargs):
        return bool(self._rule_value_(*args, **kwargs))

    def __str__(self):
        return f"Rule({self._name_}) from Master({self._master_})"



