import pandas as pd
import pandas_ta as ta

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add common technical indicators (SMA, RSI, MACD) to stock dataframe.
    
    Args:
        df: stock DataFrame with 'Close' column
    
    Returns:
        DataFrame with new indicator columns
    """
    df = df.copy()
    
    # Simple Moving Average (SMA)
    df['SMA_10'] = ta.sma(df['Close'], length=10)
    df['SMA_50'] = ta.sma(df['Close'], length=50)
    
    # Relative Strength Index (RSI)
    df['RSI_14'] = ta.rsi(df['Close'], length=14)
    
    # MACD
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    
    return df
