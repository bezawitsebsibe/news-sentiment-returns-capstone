import pandas as pd

def clean_news_data(news_df: pd.DataFrame) -> pd.DataFrame:
    """Remove rows with missing dates and standardize date format."""
    news_df = news_df.dropna(subset=['date'])
    # Ensure datetime is timezone-aware UTC
    if news_df['date'].dt.tz is None:
        news_df['date'] = news_df['date'].dt.tz_localize('UTC')
    return news_df

def align_news_to_stock(news_df: pd.DataFrame, stock_df: pd.DataFrame, stock_symbol: str) -> pd.DataFrame:
    """Keep only news that matches trading dates of a given stock."""
    trading_dates = stock_df.index.tz_localize('UTC', ambiguous='infer') if stock_df.index.tz is None else stock_df.index
    aligned_news = news_df[news_df['date'].dt.normalize().isin(trading_dates.normalize()) & (news_df['stock'] == stock_symbol)]
    return aligned_news

def save_processed_data(df: pd.DataFrame, filepath: str):
    """Save cleaned/processed data to CSV."""
    df.to_csv(filepath, index=False)
    print(f"Saved processed data to {filepath}")