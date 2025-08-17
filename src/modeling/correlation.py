from __future__ import annotations
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def daily_returns(prices: pd.DataFrame, price_col: str = "Close") -> pd.DataFrame:
    out = prices.copy()
    out["return"] = out[price_col].pct_change()
    return out

def merge_sentiment_returns(daily_sent: pd.DataFrame, returns: pd.DataFrame) -> pd.DataFrame:
    a = returns.copy()
    a["date"] = pd.to_datetime(a["date"]).dt.date
    b = daily_sent.copy()
    b["date"] = pd.to_datetime(b["date"]).dt.date
    return pd.merge(a, b, on="date", how="left")

def compute_correlations(df: pd.DataFrame, lags=(0, 1, 2, 3)) -> pd.DataFrame:
    rows = []
    for lag in lags:
        temp = df.copy()
        temp["lagged_sent"] = temp["daily_sentiment"].shift(lag)
        mask = temp[["return", "lagged_sent"]].dropna()
        if len(mask) > 3:
            r, p = pearsonr(mask["return"], mask["lagged_sent"])
        else:
            r, p = np.nan, np.nan
        rows.append({"lag": lag, "pearson_r": r, "p_value": p, "n": len(mask)})
    return pd.DataFrame(rows)
