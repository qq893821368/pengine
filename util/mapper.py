import math

import pandas
from typing import Callable


# 1 to 1
Square: Callable = lambda x: math.pow(x, 2)
Pow: Callable = lambda x, n: math.pow(x, n)
Sqrt: Callable = math.sqrt
# n to 1
Min: Callable = pandas.DataFrame.min
Max: Callable = pandas.DataFrame.max
Sum: Callable = pandas.DataFrame.sum
Avg: Callable = pandas.DataFrame.mean
Count: Callable = pandas.DataFrame.count
Mean: Callable = pandas.DataFrame.mean
Mdev: Callable = lambda x: Sum(pandas.Series.map(x, lambda e: abs(e - Mean(x)))) / pandas.Series.count(x)
# n to m
Head: Callable = lambda n, x: pandas.DataFrame.head(x, n)
First: Callable = Head
Tail: Callable = lambda n, x: pandas.DataFrame.tail(x, n)
Last: Callable = Tail
Series: Callable = lambda n, x: tuple(pandas.DataFrame.rolling(x, n))[2:]
# n to n
Int: Callable = lambda x: pandas.Series.map(x, int)
Float: Callable = lambda x: pandas.Series.map(x, float)
Round: Callable = lambda x, n: pandas.Series.map(x, lambda e: round(e, n))
Number: Callable = lambda x: pandas.Series.map(x, lambda e: int(e) if str(e).count(".") == 0 else float(e))
Number2: Callable = lambda x: pandas.Series.map(x, lambda e: round(float(e), 2))
Number4: Callable = lambda x: pandas.Series.map(x, lambda e: round(float(e), 4))
String: Callable = lambda x: pandas.Series.map(x, str)
SquareAll: Callable = lambda x: pandas.Series.map(x, Square)
SqrtAll: Callable = lambda x: pandas.Series.map(x, Sqrt)
