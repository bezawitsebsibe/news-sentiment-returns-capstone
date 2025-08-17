import argparse
import pandas as pd
import streamlit as st
from src.data.loaders import load_demo_news, load_demo_prices
from src.features.sentiment import score_headlines_vader, aggregate_daily_sentiment
from src.modeling.correlation import daily_returns, merge_sentiment_returns, compute_correlations
from src.features.technical import add_basic_indicators

parser = argparse.ArgumentParser()
parser.add_argument('--demo', action='store_true')
args, _ = parser.parse_known_args()

st.title("News Sentiment ↔ Stock Returns")
st.caption("Finance-ready demo focusing on reliability and transparency.")

if args.demo:
    news = load_demo_news(120)
    prices = load_demo_prices(120)
    st.success("Running in DEMO mode with synthetic data.")
else:
    st.warning("No data loader wired yet. Switch to --demo for a quick look.")

news_scored = score_headlines_vader(news)
daily_sent = aggregate_daily_sentiment(news_scored)
prices_feat = add_basic_indicators(prices)
rets = daily_returns(prices_feat)
merged = merge_sentiment_returns(daily_sent, rets)

st.subheader("Sample Data")
st.dataframe(news_scored.head())
st.dataframe(prices_feat.head())

st.subheader("Daily Sentiment vs Daily Returns")
df_plot = merged.dropna(subset=['daily_sentiment','return']).copy()
st.line_chart(df_plot.set_index(pd.to_datetime(df_plot['date']))[['daily_sentiment','return']])

st.subheader("Correlations (with lags)")
cors = compute_correlations(merged, lags=(0,1,2,3,5))
st.dataframe(cors)
