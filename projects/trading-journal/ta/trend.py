"""
Trend indicators: SMA, EMA, crossovers, ADX
"""

import pandas as pd
import numpy as np


def sma(series: pd.Series, window: int) -> pd.Series:
    """Simple Moving Average."""
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, window: int, adjust: bool = False) -> pd.Series:
    """Exponential Moving Average."""
    return series.ewm(span=window, adjust=adjust).mean()


def sma_crossover(
    fast_series: pd.Series,
    slow_series: pd.Series,
    fast_window: int,
    slow_window: int
) -> pd.Series:
    """
    Detect SMA crossovers.
    Returns: 1 for bullish crossover (fast crosses above slow),
             -1 for bearish crossover (fast crosses below slow),
             0 for no crossover.
    """
    fast_sma = sma(fast_series, fast_window)
    slow_sma = sma(slow_series, slow_window)

    crossover = pd.Series(0, index=fast_series.index)
    bullish = (fast_sma > slow_sma) & (fast_sma.shift(1) <= slow_sma.shift(1))
    bearish = (fast_sma < slow_sma) & (fast_sma.shift(1) >= slow_sma.shift(1))

    crossover[bullish] = 1
    crossover[bearish] = -1
    return crossover


def ema_crossover(
    fast_series: pd.Series,
    slow_series: pd.Series,
    fast_window: int,
    slow_window: int
) -> pd.Series:
    """
    Detect EMA crossovers.
    Returns: 1 for bullish crossover, -1 for bearish, 0 for none.
    """
    fast_ema = ema(fast_series, fast_window)
    slow_ema = ema(slow_series, slow_window)

    crossover = pd.Series(0, index=series.index)
    bullish = (fast_ema > slow_ema) & (fast_ema.shift(1) <= slow_ema.shift(1))
    bearish = (fast_ema < slow_ema) & (fast_ema.shift(1) >= slow_ema.shift(1))

    crossover[bullish] = 1
    crossover[bearish] = -1
    return crossover


def adx(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window: int = 14
) -> pd.Series:
    """
    Average Directional Index (ADX).
    Measures trend strength regardless of direction.
    """
    # True Range
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Directional Movement
    up_move = high - high.shift(1)
    down_move = low.shift(1) - low

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)

    plus_dm = pd.Series(plus_dm, index=high.index)
    minus_dm = pd.Series(minus_dm, index=high.index)

    # Smoothed TR and DM
    tr_smooth = tr.ewm(alpha=1/window, adjust=False).mean()
    plus_dm_smooth = plus_dm.ewm(alpha=1/window, adjust=False).mean()
    minus_dm_smooth = minus_dm.ewm(alpha=1/window, adjust=False).mean()

    # Directional Indicators
    plus_di = 100 * (plus_dm_smooth / tr_smooth)
    minus_di = 100 * (minus_dm_smooth / tr_smooth)

    # DX
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)

    # ADX
    adx_series = dx.ewm(alpha=1/window, adjust=False).mean()

    return adx_series