import pyparsing
from typing import List
from typing import Tuple


class ParsingPattern:
    NUMS = pyparsing.nums
    ALPHAS = pyparsing.alphas
    ALPHANUMS = pyparsing.alphanums
    LEFT_BRACKET = pyparsing.Literal("(")
    RIGHT_BRACKET = pyparsing.Literal(")")
    COMMA = pyparsing.Literal(",")
    VARIABLE = pyparsing.Word("$", ALPHAS + ALPHANUMS + "_")
    FUNCTION_HEAD = pyparsing.Word(ALPHAS, ALPHAS + ALPHANUMS + "_")
    NUMBER = pyparsing.Word(NUMS, "." + NUMS).set_parse_action(
        pyparsing.tokenMap(lambda x: int(x) if x.count(".") == 0 else float(x))
    )


def parse_rule_expr(func_expr: str) -> dict:
    lparen = ParsingPattern.LEFT_BRACKET.suppress()
    rparen = ParsingPattern.RIGHT_BRACKET.suppress()

    expression = pyparsing.Forward()
    func = ParsingPattern.FUNCTION_HEAD.setResultsName("function")
    arg = pyparsing.Group(expression) | func | ParsingPattern.VARIABLE | ParsingPattern.NUMBER
    args = arg + pyparsing.ZeroOrMore(ParsingPattern.COMMA.suppress() + arg)

    func_body = pyparsing.Group(lparen + pyparsing.Optional(args) + rparen)
    expression << func + func_body.setResultsName("args")

    return expression.parseString(func_expr).as_dict()


def infix2postfix(content: str) -> Tuple[str, ...]:
    not_number = {
        "(": 0,
        ")": 9,
        "&": 2,
        "|": 1,
    }
    content = content.replace(" ", "")
    opt_stack: List[str] = []
    r: List[str] = []

    i = 0
    while i < len(content):
        char = content[i]
        if char in not_number:
            if char == "(":
                opt_stack.append(char)
            elif char == ")":
                top = opt_stack.pop()
                while top != "(":
                    r.append(top)
                    top = opt_stack.pop()
            else:
                while len(opt_stack) > 0 and not_number[opt_stack[-1]] >= not_number[char]:
                    r.append(opt_stack.pop())
                opt_stack.append(char)
            i += 1
        else:
            var = []
            while char not in not_number:
                var.append(char)
                i += 1
                if i >= len(content):
                    break
                char = content[i]
            var = "".join(var)
            r.append(var)

    return *r, *opt_stack
