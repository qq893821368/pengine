from typing import List
from typing import Union
from typing import Iterable


def eval_boolean_postfix(postfix: Iterable[Union[bool, str]]) -> bool:
    stack: List[bool] = []

    for e in postfix:
        if type(e) is bool:
            stack.append(e)
        else:
            a, b = stack.pop(), stack.pop()
            if e == "|":
                stack.append(a or b)
            elif e == "&":
                stack.append(a and b)
            else:
                raise ValueError("Invalid operator: %s" % e)

    return stack[-1]
