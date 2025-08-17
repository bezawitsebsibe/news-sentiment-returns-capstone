import pandas as pd
from src.features.sentiment import score_headlines_vader, aggregate_daily_sentiment

def test_vader_scores_shape():
    df = pd.DataFrame({'headline':['good news','bad news']})
    out = score_headlines_vader(df)
    assert 'sentiment' in out.columns
    assert len(out) == 2

def test_aggregate_daily_sentiment():
    df = pd.DataFrame({'date':['2024-01-01','2024-01-01','2024-01-02'],
                       'headline':['a','b','c']})
    scored = score_headlines_vader(df)
    daily = aggregate_daily_sentiment(scored)
    assert set(daily.columns) == {'date','daily_sentiment'}
    assert len(daily) == 2
