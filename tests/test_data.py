import os
import pandas as pd
import pytest
from src.data.data_preparation import load_news_data, load_stock_data
from src.data.cleaning import clean_news_data, align_news_to_stock

# ------------------ Fixtures ------------------

@pytest.fixture
def sample_news(tmp_path):
    file = tmp_path / "news.csv"
    df = pd.DataFrame({
        "date": ["2021-01-01", "2021-01-02"],  # lowercase
        "stock": ["AAPL", "TSLA"],
        "publisher": ["NYT", "Reuters"],
        "content": ["good news", "bad news"]
    })
    df.to_csv(file, index=False)
    return str(file)

@pytest.fixture
def sample_stock(tmp_path):
    file = tmp_path / "AAPL_data.csv"
    df = pd.DataFrame({
        "date": pd.date_range("2021-01-01", periods=2),  # lowercase
        "Close": [150, 152]
    })
    df.to_csv(file, index=False)
    return str(tmp_path)

# ------------------ Tests ------------------

def test_load_news_data(sample_news):
    df = load_news_data(sample_news)
    assert "date" in df.columns
    assert df["stock"].iloc[0] == "AAPL"

def test_load_stock_data(sample_stock):
    stocks = load_stock_data(sample_stock)
    assert "AAPL" in stocks
    assert "Close" in stocks["AAPL"].columns
    assert "date" in stocks["AAPL"].reset_index().columns  

def test_clean_news_data(sample_news):
    df = load_news_data(sample_news)
    cleaned = clean_news_data(df)
    assert cleaned["date"].dt.tz is not None  

def test_align_news_to_stock(sample_news, sample_stock):
    news_df = load_news_data(sample_news)
    stocks = load_stock_data(sample_stock)
    aligned = align_news_to_stock(news_df, stocks["AAPL"], "AAPL")
    assert all(aligned["stock"] == "AAPL")
    assert "date" in aligned.columns