import pandas as pd

def compute_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily log returns for stock dataframe.
    
    Args:
        df: DataFrame with 'Close' price column
    
    Returns:
        DataFrame with 'log_return' column
    """
    df = df.copy()
    df['log_return'] = (df['Close'] / df['Close'].shift(1)).apply(lambda x: pd.np.log(x) if x > 0 else 0)
    return df
