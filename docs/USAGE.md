# Pinepy Documentation

This doc is intentionally practical: concepts, API behavior, and examples.

## Table of contents
- Overview
- Data model
- Series behavior
- NA handling
- Indicator details
- Array helpers
- Input stubs
- API reference
- Testing and validation

## Overview
`pinepy` is a compatibility-first subset of Pine Script v5 focused on
indicator and series computations using pandas and numpy.

Core design decisions:
- Use pandas Series for time-series values.
- Preserve Pine-like history access using `Series.__getitem__` and `series.ref`.
- Prefer explicit functions to emulate Pine namespaces.
- Keep behavior deterministic and vectorized when possible.

## Data model
`pinepy` expects one of:
- `pandas.Series`
- `numpy.ndarray`
- Python `list`
- `pinepy.Series`

If you pass scalars, they are broadcast to match the length of a `like`
Series when the function accepts it.

## Series behavior
Pine allows `close[1]` to reference prior bars. In `pinepy`:

```python
from pinepy import Series
close = Series(df["close"])
prev = close[1]
```

Alternatively:

```python
from pinepy import series
prev = series.ref(df["close"], 1)
```

Internally, history references are implemented using `pandas.Series.shift`.

## NA handling
Pine uses `na` as a missing value. In `pinepy`:
- `pinepy.math.na` is `numpy.nan`.
- `pinepy.math.isna(x)` checks for missing values.
- `pinepy.math.nz(x, replacement)` replaces missing values.

## Indicator details
All TA functions are built on pandas rolling/ewm operations. Core notes:
- `sma`: rolling mean with `min_periods=length`.
- `ema`: exponential moving average, `adjust=False`, `min_periods=length`.
- `rma`: Pine's RMA using `alpha = 1/length`, `adjust=False`.
- `wma`: weighted moving average with weights 1..length.
- `vwma`: volume-weighted moving average via rolling sums.
- `atr`: RMA of true range.
- `rsi`: RMA of gains/losses with standard 100 - 100/(1+RS).

## Array helpers
`pinepy.array.Array` is a simple mutable container with Pine-like methods.
It is not a pandas/numpy object; it is a Python list wrapper.

## Input stubs
All `input.*` functions return the default value. This matches Pine's
behavior where defaults apply unless overridden in UI.

## API Reference
### `pinepy.series`
- `Series(data, index=None, name=None)`
- `ref(source, length=1)`
- `nz(source, replacement=0)`

### `pinepy.math`
- `na`
- `isna(source)`
- `nz(source, replacement=0)`
- `abs(source)`
- `sqrt(source)`
- `pow(source, power)`
- `max(source, other)`
- `min(source, other)`
- `avg(a, b)`
- `ceil(source)`
- `floor(source)`
- `round_(source, precision=0)`

### `pinepy.ta`
- `sma(source, length)`
- `ema(source, length)`
- `rma(source, length)`
- `wma(source, length)`
- `vwma(source, volume, length)`
- `stdev(source, length)`
- `variance(source, length)`
- `highest(source, length)`
- `lowest(source, length)`
- `highestbars(source, length)`
- `lowestbars(source, length)`
- `change(source, length=1)`
- `roc(source, length=1)`
- `sum(source, length)`
- `cum(source)`
- `cross(source, other)`
- `crossover(source, other)`
- `crossunder(source, other)`
- `barssince(condition)`
- `barslast(condition)`
- `valuewhen(condition, source, occurrence=0)`
- `true_range(high, low, close)`
- `atr(high, low, close, length)`
- `rsi(source, length)`
- `hl2(high, low)`
- `hlc3(high, low, close)`
- `ohlc4(open_, high, low, close)`

### `pinepy.array`
- `Array(data=None)`
- `new_float(size=0, initial_value=0.0)`
- `new_int(size=0, initial_value=0)`
- `new_bool(size=0, initial_value=False)`
- `new_string(size=0, initial_value="")`

### `pinepy.input`
- `int(defval, ...)`
- `float(defval, ...)`
- `bool(defval, ...)`
- `string(defval, ...)`
- `source(defval, ...)`

## Testing and validation
A good first check is comparing with TradingView output on a small dataset:
- Export OHLCV data.
- Compute the indicator in `pinepy`.
- Compare to TradingView values visually or by numeric diff.
