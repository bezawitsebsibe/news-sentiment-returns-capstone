import pandas as pd
from src.modeling.correlation import daily_returns, merge_sentiment_returns, compute_correlations

def test_returns_and_merge_and_corr():
    prices = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=5, freq='D').date,
                           'Close':[100,101,99,100,102]})
    sent = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=5, freq='D').date,
                         'daily_sentiment':[0.1, -0.2, 0.0, 0.3, -0.1]})
    rets = daily_returns(prices)
    merged = merge_sentiment_returns(sent, rets)
    corr = compute_correlations(merged, lags=(0,1))
    assert {'lag','pearson_r','p_value','n'}.issubset(corr.columns)
    assert len(corr) == 2
