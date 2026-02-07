# pinepy

A Pine Script-like helper library for Python using only pandas and numpy.

## Goals
- Provide Pine-style series operations and indicator math in Python.
- Stay lightweight: no dependencies beyond pandas and numpy.
- Keep behavior close to Pine where it matters for calculations.

## Non-goals (for now)
- Chart rendering and UI (plotting is not implemented).
- Strategy execution engine (orders, fills, slippage).
- Real-time brokerage integration.

## Status
This is a compatibility-focused subset of Pine Script v5. It prioritizes
indicator calculations and series behaviors. Plotting, strategy orders,
alerts, and UI inputs are stubs.

## Install (editable, local dev)
```
pip install -e .
```

## Install (build + install)
```
pip install .
```

## Quick usage
```python
import pandas as pd
import pinepy as pine

# Example OHLCV DataFrame
# df = pd.read_csv(...)
close = df["close"]
volume = df["volume"]

ema_20 = pine.ta.ema(close, 20)
rsi_14 = pine.ta.rsi(close, 14)

# Pine-like history reference
ema_20_prev = pine.series.ref(ema_20, 1)
```

## Concepts
### Series and history referencing
Pine uses time-series values that can be indexed like `close[1]` to access
previous bars. In `pinepy`, you can do this via:

```python
from pinepy import Series
from pinepy import series as s

close = Series(df["close"])
prev_close = close[1]         # shift by 1
prev_close_alt = s.ref(close, 1)
```

### NA behavior
- `pinepy.math.na` is `numpy.nan`.
- `pinepy.math.nz(x, replacement)` replaces NA values.

### Input stubs
Pine `input.*` functions are UI-driven. In `pinepy`, they are simple stubs
that return the default value you provide.

## API Overview
### `pinepy.series`
- `Series`: wrapper class with Pine-like history indexing.
- `ref(source, length=1)`: shift series by `length`.
- `nz(source, replacement=0)`: replace NA values.

### `pinepy.math`
- `na`: NA constant (`numpy.nan`).
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
Core indicators and helpers:
- Moving averages: `sma`, `ema`, `rma`, `wma`, `vwma`
- Volatility: `stdev`, `variance`, `atr`, `true_range`
- Extremes: `highest`, `lowest`, `highestbars`, `lowestbars`
- Momentum: `rsi`, `roc`, `change`
- Aggregation: `sum`, `cum`
- Price composites: `hl2`, `hlc3`, `ohlc4`
- Crosses: `cross`, `crossover`, `crossunder`
- Signal helpers: `barssince` / `barslast`, `valuewhen`

### `pinepy.array`
- `Array` with `get`, `set`, `push`, `pop`, `size`, `clear`
- `new_float`, `new_int`, `new_bool`, `new_string`

### `pinepy.input`
- `int`, `float`, `bool`, `string`, `source` (all return defaults)

## Examples
### RSI + EMA signal
```python
import pinepy as pine

close = df["close"]

ema_fast = pine.ta.ema(close, 12)
ema_slow = pine.ta.ema(close, 26)

long_signal = pine.ta.crossover(ema_fast, ema_slow)
short_signal = pine.ta.crossunder(ema_fast, ema_slow)
```

### ATR-based stop
```python
import pinepy as pine

high = df["high"]
low = df["low"]
close = df["close"]

atr_14 = pine.ta.atr(high, low, close, 14)
stop = close - 3 * atr_14
```

### Value when
```python
import pinepy as pine

cond = df["close"] > df["open"]
value = pine.ta.valuewhen(cond, df["close"], 0)
```

## Compatibility notes
- Outputs are pandas Series unless you pass `pinepy.Series`, in which case
  outputs are wrapped as `pinepy.Series`.
- NA behavior follows pandas/numpy unless noted.
- `input.*` functions are stubs.

## Roadmap
Planned additions (incrementally, per request):
- Expand `ta` to cover the full Pine v5 indicator set.
- More Pine math functions and vectorized helpers.
- Session/time helpers.
- Plot/strategy stubs for API compatibility.

## Contributing
If you want a specific Pine function, open an issue or request it directly.
