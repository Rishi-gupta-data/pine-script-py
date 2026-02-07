import numpy as np
import pandas as pd
from .series import Series, to_series, _return_type

na = np.nan


def isna(source):
    s = to_series(source)
    result = s.isna()
    return _return_type(result, source)


def nz(source, replacement=0):
    s = to_series(source)
    result = s.fillna(replacement)
    return _return_type(result, source)


def abs(source):
    s = to_series(source)
    result = s.abs()
    return _return_type(result, source)


def sqrt(source):
    s = to_series(source)
    result = np.sqrt(s)
    return _return_type(pd.Series(result, index=s.index), source)


def pow(source, power):
    s = to_series(source)
    p = to_series(power, like=s)
    result = s ** p
    return _return_type(result, source, power)


def max(source, other):
    a = to_series(source)
    b = to_series(other, like=a)
    result = np.maximum(a, b)
    return _return_type(pd.Series(result, index=a.index), source, other)


def min(source, other):
    a = to_series(source)
    b = to_series(other, like=a)
    result = np.minimum(a, b)
    return _return_type(pd.Series(result, index=a.index), source, other)


def avg(a, b):
    s1 = to_series(a)
    s2 = to_series(b, like=s1)
    result = (s1 + s2) / 2.0
    return _return_type(result, a, b)


def ceil(source):
    s = to_series(source)
    result = np.ceil(s)
    return _return_type(pd.Series(result, index=s.index), source)


def floor(source):
    s = to_series(source)
    result = np.floor(s)
    return _return_type(pd.Series(result, index=s.index), source)


def round_(source, precision=0):
    s = to_series(source)
    result = s.round(precision)
    return _return_type(result, source)
