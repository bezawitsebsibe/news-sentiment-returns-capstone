import os
import sys
import pandas as pd
from src.data.data_preparation import load_news_data, load_stock_data, explore_news_data, explore_stock_data
from src.data.cleaning import clean_news_data, align_news_to_stock, save_processed_data

def main():
    # --- Paths ---
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_raw = os.path.join(project_root, "data", "raw")
    data_processed = os.path.join(project_root, "data", "processed")
    os.makedirs(data_processed, exist_ok=True)

    # FNSPID news CSV
    news_file = os.path.join(data_raw, "FNSPID_news.csv")

    # --- Load data ---
    print("Loading news data...")
    news_df = load_news_data(news_file)

    symbols = ["AAPL", "TSLA"]  # extend this list as needed
    print("Downloading stock data from yfinance...")
    stocks = load_stock_data(symbols=symbols, start="2021-01-01", end="2021-12-31")

    # --- Explore ---
    print("\nExploring news data:")
    explore_news_data(news_df)
    print("\nExploring stock data:")
    explore_stock_data(stocks)

    # --- Clean news ---
    print("\nCleaning news data...")
    news_df = clean_news_data(news_df)

    # --- Align news with stock data & save ---
    print("\nAligning news with stock trading dates and saving processed data...")
    for symbol, stock_df in stocks.items():
        aligned_news = align_news_to_stock(news_df, stock_df, symbol)
        output_file = os.path.join(data_processed, f"{symbol}_news.csv")
        save_processed_data(aligned_news, output_file)

    print("\nPipeline complete. Processed data saved in:", data_processed)
# src/run_pipeline.py
from src.analysis.sentiment import add_sentiment
from src.analysis.technicals import add_technical_indicators
from src.analysis.returns import compute_returns

# After aligning news to stock:
for symbol, stock_df in stocks.items():
    aligned_news = align_news_to_stock(news_df, stock_df, symbol)
    
    # --- Add sentiment ---
    aligned_news = add_sentiment(aligned_news)
    
    # --- Add technical indicators to stock data ---
    stock_df = add_technical_indicators(stock_df)
    
    # --- Compute returns ---
    stock_df = compute_returns(stock_df)
    
    # --- Save processed data ---
    save_processed_data(aligned_news, os.path.join(data_processed, f"{symbol}_news.csv"))
    save_processed_data(stock_df.reset_index(), os.path.join(data_processed, f"{symbol}_stock.csv"))

from src.analysis.statistics import correlation_with_pvalues, rolling_correlation

for symbol, stock_df in stocks.items():
    aligned_news = align_news_to_stock(news_df, stock_df, symbol)
    aligned_news = add_sentiment(aligned_news)
    stock_df = add_technical_indicators(stock_df)
    stock_df = compute_returns(stock_df)
    
    # --- Correlation and p-values ---
    corr_df = correlation_with_pvalues(aligned_news, stock_df)
    print(f"\nCorrelation between sentiment and returns for {symbol}:")
    print(corr_df)
    
    # --- Rolling correlation ---
    rolling_corr_df = rolling_correlation(aligned_news, stock_df, window=20)
    save_processed_data(rolling_corr_df, os.path.join(data_processed, f"{symbol}_rolling_corr.csv"))

if __name__ == "__main__":
    main()
