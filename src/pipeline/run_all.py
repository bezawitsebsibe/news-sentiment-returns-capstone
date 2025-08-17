from __future__ import annotations
import pandas as pd
import typer
from src.utils.logging_utils import get_logger
from src.data.loaders import load_demo_news, load_demo_prices
from src.features.sentiment import score_headlines_vader, aggregate_daily_sentiment
from src.features.technical import add_basic_indicators
from src.modeling.correlation import daily_returns, merge_sentiment_returns, compute_correlations

app = typer.Typer(add_completion=False)
log = get_logger()

@app.command()
def demo():
    log.info("Loading synthetic demo data...\n")
    news = load_demo_news(90)
    prices = load_demo_prices(90)

    log.info("Scoring sentiment...\n")
    news_scored = score_headlines_vader(news)
    daily_sent = aggregate_daily_sentiment(news_scored)

    log.info("Building features...\n")
    prices_feat = add_basic_indicators(prices)

    log.info("Computing returns & correlations...\n")
    rets = daily_returns(prices_feat)
    merged = merge_sentiment_returns(daily_sent, rets)
    cors = compute_correlations(merged)

    print("\n=== Correlations (daily returns vs. sentiment, with lags) ===")
    print(cors.to_string(index=False))

    out_path = "artifacts/demo_correlations.csv"
    import os
    os.makedirs("artifacts", exist_ok=True)
    cors.to_csv(out_path, index=False)
    print(f"\nSaved: {out_path}")

if __name__ == "__main__":
    app()
