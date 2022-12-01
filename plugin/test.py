import math


def network():
    def sigmoid(x):
        return 1 / (1 + math.e ** -x)

    return {
        "sigmoid": sigmoid
    }


class Net:
    pass


PI = math.pi


def export():
    return {
        "network": network,
        "Net": Net,
        "PI": PI
    }
