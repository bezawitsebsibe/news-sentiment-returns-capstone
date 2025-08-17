from __future__ import annotations
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()

def score_headlines_vader(df: pd.DataFrame, text_col: str = "headline") -> pd.DataFrame:
    scores = df[text_col].apply(lambda t: _analyzer.polarity_scores(str(t))["compound"])
    out = df.copy()
    out["sentiment"] = scores
    return out

def aggregate_daily_sentiment(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
    tmp = df.copy()
    tmp[date_col] = pd.to_datetime(tmp[date_col]).dt.date
    daily = tmp.groupby(date_col, as_index=False)["sentiment"].mean().rename(columns={"sentiment":"daily_sentiment"})
    return daily
