import abc


def align_equation(left, right) -> tuple:
    if not hasattr(left, "__iter__"):
        if hasattr(right, "__iter__"):
            try:
                if type(right) is str:
                    return left, type(left)(right)
                else:
                    return left, right[0]
            except ValueError or IndexError:
                return left, None
        else:
            return left, right
    else:
        if type(left) is str:
            return left, str(right)
        if not hasattr(right, "__iter__"):
            return left, tuple(right for _ in range(len(left)))
        else:
            return left, right


class Matcher(abc.ABC, metaclass=abc.ABCMeta):
    _opname_: str = "Matcher"

    def __str__(self):
        return self._opname_

    @staticmethod
    def compare(left, right) -> bool:
        raise NotImplementedError("Can not call an abstract matcher.")


class Equals(Matcher):
    _opname_: str = "Equals"

    @staticmethod
    def compare(left, right) -> bool:
        left, right = align_equation(left, right)
        if not hasattr(left, "__iter__"):
            return left == right
        else:
            if not len(left) == len(right):
                return False
            return False not in (x == y for x, y in zip(left, right))


class NEquals(Matcher):
    _opname_: str = "NotEquals"

    @staticmethod
    def compare(left, right) -> bool:
        return not Equals.compare(left, right)


class GreaterThan(Matcher):
    _opname_: str = "GreaterThan"

    @staticmethod
    def compare(left, right) -> bool:
        left, right = align_equation(left, right)
        if right is None:
            return False
        if not hasattr(left, "__iter__"):
            return left > right
        else:
            if not len(left) == len(right):
                return False
            return False not in (x > y for x, y in zip(left, right))


class GreaterEquals(Matcher):
    _opname_: str = "GreaterThanOrEqualsTo"

    @staticmethod
    def compare(left, right) -> bool:
        left, right = align_equation(left, right)
        if right is None:
            return False
        if not hasattr(left, "__iter__"):
            return left >= right
        else:
            if not len(left) == len(right):
                return False
            return False not in (x >= y for x, y in zip(left, right))


class LessThan(Matcher):
    _opname_: str = "LessThan"

    @staticmethod
    def compare(left, right) -> bool:
        left, right = align_equation(left, right)
        if right is None:
            return False
        if not hasattr(left, "__iter__"):
            return left < right
        else:
            if not len(left) == len(right):
                return False
            return False not in (x < y for x, y in zip(left, right))


class LessEquals(Matcher):
    _opname_: str = "LessThanOrEqualsTo"

    @staticmethod
    def compare(left, right) -> bool:
        left, right = align_equation(left, right)
        if right is None:
            return False
        if not hasattr(left, "__iter__"):
            return left <= right
        else:
            if not len(left) == len(right):
                return False
            return False not in (x <= y for x, y in zip(left, right))


class Between(Matcher):
    _opname_: str = "Between"

    @staticmethod
    def _get_limits_(right):
        min_val, max_val = None, None
        if type(right) is str:
            return min_val, max_val
        elif type(right) is dict:
            min_val, max_val = right.get("min"), right.get("max")
        elif hasattr(right, "__iter__") and len(right) > 1:
            min_val, max_val = right[0], right[-1]
        else:
            pass
        return (min(min_val, max_val), max(min_val, max_val)) if None not in (min_val, max_val) else (min_val, max_val)

    @staticmethod
    def compare(left, right) -> bool:
        min_val, max_val = Between._get_limits_(right)
        if min_val is None or max_val is None:
            return False
        elif hasattr(left, "__iter__"):
            if False in (min_val < e < max_val for e in left):
                return False
            else:
                return True
        else:
            return min_val < left < max_val


class NotBetween(Between):
    _opname_: str = "NotBetween"

    @staticmethod
    def compare(left, right) -> bool:
        return not Between.compare(left, right)


class In(Between):
    _opname_: str = "In"

    @staticmethod
    def compare(left, right) -> bool:
        min_val, max_val = In._get_limits_(right)
        if min_val is None or max_val is None:
            return False
        elif hasattr(left, "__iter__"):
            if False in (min_val <= e <= max_val for e in left):
                return False
            else:
                return True
        else:
            return min_val <= left <= max_val


class NotIn(In):
    _opname_: str = "NotIn"

    @staticmethod
    def compare(left, right) -> bool:
        return not In.compare(left, right)


class StartsWith(Matcher):
    _opname_: str = "StartsWith"

    @staticmethod
    def compare(left, right) -> bool:
        if not hasattr(left, "__iter__"):
            return False
        if not hasattr(right, "__iter__"):
            right = (right, )
        if len(left) < len(right):
            return False
        else:
            head_n = left[:len(right)]
            return False not in (x == y for x, y in zip(head_n, right))


class EndsWith(Matcher):
    _opname_: str = "EndsWith"

    @staticmethod
    def compare(left, right) -> bool:
        if not hasattr(left, "__iter__"):
            return False
        if not hasattr(right, "__iter__"):
            right = (right, )
        if len(left) < len(right):
            return False
        else:
            tail_n = left[-len(right):]
            return False not in (x == y for x, y in zip(tail_n, right))


# todo more matchers


def create_matcher(op: str) -> Matcher:
    op = op.lower()
    if op in ("=", "==", "eq", "equals"):
        return Equals()
    elif op in ("!=", "<>", "neq", "nequals", "notequals"):
        return NEquals()
    elif op in (">", "gt", "greaterthan"):
        return GreaterThan()
    elif op in (">=", "ge", "gte", "greatereq", "greaterequals", "greaterthanorequalsto"):
        return GreaterEquals()
    elif op in ("<", "lt", "lessthan"):
        return LessThan()
    elif op in ("<=", "le", "lte", "lesseq", "lessequals", "lessthanorequalsto"):
        return LessEquals()
    elif op in ("betw", "between",):
        return Between()
    elif op in ("in",):
        return In()
    elif op in ("nbetw", "nbetween", "notbetween"):
        return NotBetween()
    elif op in ("nin", "notin"):
        return NotIn()
    elif op in ("start", "begin", "startswith"):
        return StartsWith()
    elif op in ("end", "ending", "finish", "endsof", "endswith"):
        return EndsWith()


