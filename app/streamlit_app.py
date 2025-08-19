import streamlit as st
import pandas as pd
import os
from src.data.data_preparation import load_news_data, load_stock_data, clean_news_data, align_news_to_stock
from src.analysis.sentiment import add_sentiment
from src.analysis.technicals import add_technical_indicators, compute_returns

st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

st.title("Stock Sentiment & Returns Dashboard")

# --- Sidebar for user input ---
symbols_input = st.text_input("Enter stock symbols (comma-separated):", "AAPL,TSLA")
start_date = st.date_input("Start date", pd.to_datetime("2021-01-01"))
end_date = st.date_input("End date", pd.to_datetime("2021-12-31"))

symbols = [s.strip().upper() for s in symbols_input.split(",")]

# --- Load and process data ---
news_file = "data/FNSPID_news.csv"
news_df = load_news_data(news_file)
news_df = clean_news_data(news_df)

data_processed = "data/processed"
os.makedirs(data_processed, exist_ok=True)

stocks = load_stock_data(symbols=symbols, start=start_date, end=end_date)

for symbol in symbols:
    stock_df = stocks[symbol]
    aligned_news = align_news_to_stock(news_df, stock_df, symbol)
    aligned_news = add_sentiment(aligned_news)
    stock_df = add_technical_indicators(stock_df)
    stock_df = compute_returns(stock_df)

    st.subheader(f"{symbol} Data Overview")
    st.write("Stock prices and indicators:")
    st.dataframe(stock_df.tail(10))

    st.write("Aligned news with sentiment:")
    st.dataframe(aligned_news.tail(10))

    # Optional: Download CSV
    csv_file = os.path.join(data_processed, f"{symbol}_aligned.csv")
    aligned_news.to_csv(csv_file, index=False)
    st.download_button(
        label=f"Download {symbol} news CSV",
        data=open(csv_file, "rb").read(),
        file_name=f"{symbol}_aligned.csv",
        mime="text/csv"
    )
