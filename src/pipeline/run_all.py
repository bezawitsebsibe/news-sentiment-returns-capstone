import os
import pandas as pd
from src.data.data_preparation import load_news_data, load_stock_data, clean_news_data, align_news_to_stock, save_processed_data
from src.analysis.sentiment import add_sentiment
from src.analysis.technicals import add_technical_indicators, compute_returns
from src.analysis.explainability import explain_sentiment_model

def main():
    # --- Config ---
    news_file = "data/FNSPID_news.csv"
    symbols = ["AAPL", "TSLA"]
    start_date = "2021-01-01"
    end_date = "2021-12-31"
    processed_folder = "data/processed"
    os.makedirs(processed_folder, exist_ok=True)

    # --- Load & clean data ---
    print("Loading news data...")
    news_df = load_news_data(news_file)
    news_df = clean_news_data(news_df)

    print("Downloading stock data...")
    stocks = load_stock_data(symbols=symbols, start=start_date, end=end_date)

    # --- Process each stock ---
    for symbol in symbols:
        print(f"\nProcessing {symbol}...")
        stock_df = stocks[symbol]

        # Align news
        aligned_news = align_news_to_stock(news_df, stock_df, symbol)

        # Add sentiment
        aligned_news = add_sentiment(aligned_news)

        # Add technical indicators
        stock_df = add_technical_indicators(stock_df)

        # Compute returns
        stock_df = compute_returns(stock_df)

        # Save processed CSVs
        save_processed_data(aligned_news, os.path.join(processed_folder, f"{symbol}_aligned_news.csv"))
        save_processed_data(stock_df.reset_index(), os.path.join(processed_folder, f"{symbol}_stock.csv"))

        # Explainability (SHAP)
        model, shap_values, merged = explain_sentiment_model(aligned_news, stock_df)
        print(f"Explained sentiment impact on returns for {symbol}.")

    print("\nPipeline complete! Processed files saved in:", processed_folder)

if __name__ == "__main__":
    main()
