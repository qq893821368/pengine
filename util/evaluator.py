from typing import List
from typing import Tuple
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


def eval_boolean_sequential_postfix(seq_postfix) -> Tuple[bool]:
    stack: List[Tuple[bool]] = []

    for seq in seq_postfix:
        if type(seq[0]) is bool:
            stack.append(seq)
        else:
            a, b = stack.pop(), stack.pop()
            if seq == "|":
                stack.append(tuple(x or y for x, y in zip(a, b)))
            elif seq == "&":
                stack.append(tuple(x and y for x, y in zip(a, b)))
            else:
                raise ValueError("Invalid operator: %s" % seq)

    return stack[-1]
