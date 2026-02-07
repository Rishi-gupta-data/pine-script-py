import numpy as np
import pandas as pd
from .series import Series, to_series, _return_type


def sma(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).mean()
    return _return_type(result, source)


def ema(source, length):
    s = to_series(source)
    result = s.ewm(span=length, adjust=False, min_periods=length).mean()
    return _return_type(result, source)


def rma(source, length):
    s = to_series(source)
    alpha = 1.0 / float(length)
    result = s.ewm(alpha=alpha, adjust=False, min_periods=length).mean()
    return _return_type(result, source)


def wma(source, length):
    s = to_series(source)
    weights = np.arange(1, length + 1, dtype=float)
    denom = weights.sum()

    def _calc(x):
        return np.dot(x, weights) / denom

    result = s.rolling(length, min_periods=length).apply(_calc, raw=True)
    return _return_type(result, source)


def vwma(source, volume, length):
    s = to_series(source)
    v = to_series(volume, like=s)
    num = (s * v).rolling(length, min_periods=length).sum()
    den = v.rolling(length, min_periods=length).sum()
    result = num / den
    return _return_type(result, source, volume)


def stdev(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).std(ddof=0)
    return _return_type(result, source)


def variance(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).var(ddof=0)
    return _return_type(result, source)


def highest(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).max()
    return _return_type(result, source)


def lowest(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).min()
    return _return_type(result, source)


def highestbars(source, length):
    s = to_series(source)

    def _calc(x):
        idx = int(np.argmax(x))
        return len(x) - 1 - idx

    result = s.rolling(length, min_periods=length).apply(_calc, raw=True)
    return _return_type(result, source)


def lowestbars(source, length):
    s = to_series(source)

    def _calc(x):
        idx = int(np.argmin(x))
        return len(x) - 1 - idx

    result = s.rolling(length, min_periods=length).apply(_calc, raw=True)
    return _return_type(result, source)


def change(source, length=1):
    s = to_series(source)
    result = s.diff(length)
    return _return_type(result, source)


def roc(source, length=1):
    s = to_series(source)
    prev = s.shift(length)
    result = 100.0 * (s - prev) / prev
    return _return_type(result, source)


def sum(source, length):
    s = to_series(source)
    result = s.rolling(length, min_periods=length).sum()
    return _return_type(result, source)


def cum(source):
    s = to_series(source)
    result = s.cumsum()
    return _return_type(result, source)


def crossover(source, other):
    a = to_series(source)
    b = to_series(other, like=a)
    result = (a > b) & (a.shift(1) <= b.shift(1))
    return _return_type(result, source, other)


def crossunder(source, other):
    a = to_series(source)
    b = to_series(other, like=a)
    result = (a < b) & (a.shift(1) >= b.shift(1))
    return _return_type(result, source, other)


def cross(source, other):
    a = to_series(source)
    b = to_series(other, like=a)
    result = ((a > b) & (a.shift(1) <= b.shift(1))) | ((a < b) & (a.shift(1) >= b.shift(1)))
    return _return_type(result, source, other)


def barssince(condition):
    c = to_series(condition).astype(bool)
    out = pd.Series(index=c.index, dtype=float)
    last = np.nan
    for i, val in enumerate(c.values):
        if val:
            last = 0
        else:
            last = last + 1 if not np.isnan(last) else np.nan
        out.iloc[i] = last
    return _return_type(out, condition)


def barslast(condition):
    return barssince(condition)


def valuewhen(condition, source, occurrence=0):
    c = to_series(condition).astype(bool)
    s = to_series(source, like=c)
    out = pd.Series(index=c.index, dtype=float)
    hits = []
    for i, val in enumerate(c.values):
        if val:
            hits.append(s.iloc[i])
        if len(hits) > occurrence:
            out.iloc[i] = hits[-1 - occurrence]
        else:
            out.iloc[i] = np.nan
    return _return_type(out, condition, source)


def true_range(high, low, close):
    h = to_series(high)
    l = to_series(low, like=h)
    c = to_series(close, like=h)
    prev_close = c.shift(1)
    ranges = pd.concat(
        [
            h - l,
            (h - prev_close).abs(),
            (l - prev_close).abs(),
        ],
        axis=1,
    )
    result = ranges.max(axis=1)
    return _return_type(result, high, low, close)


def atr(high, low, close, length):
    tr = true_range(high, low, close)
    tr_s = to_series(tr)
    result = rma(tr_s, length)
    return _return_type(result, high, low, close)


def rsi(source, length):
    s = to_series(source)
    delta = s.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = rma(gain, length)
    avg_loss = rma(loss, length)
    avg_gain = to_series(avg_gain)
    avg_loss = to_series(avg_loss)
    rs = avg_gain / avg_loss
    result = 100.0 - (100.0 / (1.0 + rs))
    return _return_type(result, source)


def hl2(high, low):
    h = to_series(high)
    l = to_series(low, like=h)
    result = (h + l) / 2.0
    return _return_type(result, high, low)


def hlc3(high, low, close):
    h = to_series(high)
    l = to_series(low, like=h)
    c = to_series(close, like=h)
    result = (h + l + c) / 3.0
    return _return_type(result, high, low, close)


def ohlc4(open_, high, low, close):
    o = to_series(open_)
    h = to_series(high, like=o)
    l = to_series(low, like=o)
    c = to_series(close, like=o)
    result = (o + h + l + c) / 4.0
    return _return_type(result, open_, high, low, close)
