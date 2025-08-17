from __future__ import annotations
import pandas as pd
import pandas_ta as ta

def add_basic_indicators(df: pd.DataFrame, close_col: str = "Close") -> pd.DataFrame:
    out = df.copy()
    out["rsi_14"] = ta.rsi(out[close_col], length=14)
    out["sma_20"] = ta.sma(out[close_col], length=20)
    out["sma_50"] = ta.sma(out[close_col], length=50)
    macd = ta.macd(out[close_col], fast=12, slow=26, signal=9)
    out = pd.concat([out, macd], axis=1)
    return out
