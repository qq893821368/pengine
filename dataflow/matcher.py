import abc


class Matcher(abc.ABC, metaclass=abc.ABCMeta):
    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def compare(left, right) -> bool:
        raise NotImplementedError("Can not call an abstract matcher.")


class Equals(Matcher):
    @staticmethod
    def compare(left, right) -> bool:
        if not hasattr(left, "__iter__"):
            if not hasattr(right, "__iter__"):
                return left == right
            else:
                return left == right[0] if len(right) > 0 else False
        else:
            if not hasattr(right, "__iter__"):
                right = tuple(right for _ in range(len(left)))
            if not len(left) == len(right):
                return False
            else:
                return False not in (x == y for x, y in zip(left, right))


class NEquals(Matcher):
    @staticmethod
    def compare(left, right) -> bool:
        return not Equals.compare(left, right)


# todo more matchers


def create_matcher(op: str) -> Matcher:
    op = op.lower()
    if op in ("=", "==", "eq", "equals"):
        return Equals()
