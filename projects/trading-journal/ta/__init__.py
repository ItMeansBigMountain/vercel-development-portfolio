"""
Technical Analysis Indicator Library

A deterministic, testable Python module for technical analysis indicators
using pandas and numpy.
"""

from ta.trend import (
    sma,
    ema,
    sma_crossover,
    ema_crossover,
    adx,
)
from ta.momentum import (
    rsi,
    macd,
    stochastic,
)
from ta.volatility import (
    bollinger_bands,
    atr,
    keltner_channels,
)
from ta.volume import (
    obv,
    vwap,
    mfi,
)
from ta.support_resistance import (
    pivot_points,
    fibonacci_retracements,
)

__all__ = [
    # Trend
    "sma",
    "ema",
    "sma_crossover",
    "ema_crossover",
    "adx",
    # Momentum
    "rsi",
    "macd",
    "stochastic",
    # Volatility
    "bollinger_bands",
    "atr",
    "keltner_channels",
    # Volume
    "obv",
    "vwap",
    "mfi",
    # Support/Resistance
    "pivot_points",
    "fibonacci_retracements",
]

__version__ = "1.0.0"