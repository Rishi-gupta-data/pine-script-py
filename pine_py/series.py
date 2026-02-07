import numpy as np
import pandas as pd


def to_series(obj, like=None, index=None, name=None):
    if isinstance(obj, Series):
        s = obj.s
    elif isinstance(obj, pd.Series):
        s = obj
    elif isinstance(obj, np.ndarray):
        s = pd.Series(obj, index=index, name=name)
    elif isinstance(obj, list):
        s = pd.Series(obj, index=index, name=name)
    else:
        # Scalar or unknown: broadcast if possible
        if like is None:
            s = pd.Series([obj], index=index, name=name)
        else:
            s = pd.Series(np.full(len(like), obj), index=like.index, name=name)
    if name is not None:
        s = s.rename(name)
    return s


def _return_type(result, *inputs):
    if any(isinstance(x, Series) for x in inputs):
        return Series(result)
    return result


def ref(source, length=1):
    s = to_series(source)
    result = s.shift(length)
    return _return_type(result, source)


def nz(source, replacement=0):
    s = to_series(source)
    result = s.fillna(replacement)
    return _return_type(result, source)


class Series:
    def __init__(self, data, index=None, name=None):
        self.s = to_series(data, index=index, name=name)

    def __getitem__(self, key):
        if isinstance(key, int):
            return Series(self.s.shift(key))
        return self.s.__getitem__(key)

    def __getattr__(self, name):
        return getattr(self.s, name)

    def __array__(self, dtype=None):
        return np.asarray(self.s, dtype=dtype)

    @property
    def index(self):
        return self.s.index

    @property
    def name(self):
        return self.s.name

    def to_pandas(self):
        return self.s

    def shift(self, length=1):
        return Series(self.s.shift(length))

    def _binary_op(self, other, op):
        other_s = to_series(other, like=self.s)
        result = op(self.s, other_s)
        return Series(result)

    def _rbinary_op(self, other, op):
        other_s = to_series(other, like=self.s)
        result = op(other_s, self.s)
        return Series(result)

    def __add__(self, other):
        return self._binary_op(other, lambda a, b: a + b)

    def __radd__(self, other):
        return self._rbinary_op(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self._binary_op(other, lambda a, b: a - b)

    def __rsub__(self, other):
        return self._rbinary_op(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self._binary_op(other, lambda a, b: a * b)

    def __rmul__(self, other):
        return self._rbinary_op(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self._binary_op(other, lambda a, b: a / b)

    def __rtruediv__(self, other):
        return self._rbinary_op(other, lambda a, b: a / b)

    def __pow__(self, other):
        return self._binary_op(other, lambda a, b: a ** b)

    def __rpow__(self, other):
        return self._rbinary_op(other, lambda a, b: a ** b)

    def __neg__(self):
        return Series(-self.s)

    def __abs__(self):
        return Series(self.s.abs())

    def __repr__(self):
        return f"Series({repr(self.s)})"
