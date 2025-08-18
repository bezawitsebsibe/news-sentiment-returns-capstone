import os
import pandas as pd

def load_news_data(news_file: str) -> pd.DataFrame:
    """Load and clean news dataset."""
    news_df = pd.read_csv(news_file)
    # Convert date to datetime without timezone first
    news_df['date'] = pd.to_datetime(news_df['date'], utc=False, errors='coerce')
    
    # Check if the date column is already timezone-aware
    if news_df['date'].dt.tz is None:
        # If not, localize to UTC
        news_df['date'] = news_df['date'].dt.tz_localize('UTC', ambiguous='infer')

    # Standardize stock symbols
    news_df['stock'] = news_df['stock'].str.upper()
    return news_df

def load_stock_data(stock_folder: str) -> dict:
    """Load historical stock data from CSV files in folder."""
    stocks = {}
    for file in os.listdir(stock_folder):
        if file.endswith(".csv"):
            symbol = file.split("_")[0]  # e.g., AAPL_historical_data.csv -> AAPL
            df = pd.read_csv(os.path.join(stock_folder, file))
            df['date'] = pd.to_datetime(df['date'])  # Ensure correct casing
            df.set_index('date', inplace=True)  # Use the correct column name
            stocks[symbol] = df
    return stocks

def explore_news_data(news_df: pd.DataFrame):
    """Print basic stats and information about news dataset."""
    print("News data shape:", news_df.shape)
    print("Columns:", news_df.columns.tolist())
    print(news_df.head())
    print(news_df.info())
    print("\nTop 10 publishers by article count:")
    print(news_df['publisher'].value_counts().head(10))

def explore_stock_data(stocks: dict):
    """Print basic info about each stock dataframe."""
    for symbol, df in stocks.items():
        print(f"{symbol}: {df.shape[0]} rows, columns: {df.columns.tolist()}")
        print(df.head(3))