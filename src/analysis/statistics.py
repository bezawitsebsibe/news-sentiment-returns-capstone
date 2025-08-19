import pandas as pd
from scipy.stats import pearsonr

def correlation_with_pvalues(news_df: pd.DataFrame, stock_df: pd.DataFrame, sentiment_col: str = "vader_compound", return_col: str = "log_return") -> pd.DataFrame:
    """
    Compute correlation between sentiment scores and stock returns.

    Args:
        news_df: DataFrame with aligned news and sentiment
        stock_df: DataFrame with stock returns
        sentiment_col: column in news_df with sentiment score
        return_col: column in stock_df with returns

    Returns:
        DataFrame with correlation coefficient and p-value
    """
    merged = pd.merge_asof(
        news_df.sort_values('date'), 
        stock_df.sort_index().reset_index().rename(columns={'date': 'date'}),
        on='date',
        direction='backward'
    )

    corr, pval = pearsonr(merged[sentiment_col], merged[return_col])
    result = pd.DataFrame({
        "sentiment_col": [sentiment_col],
        "return_col": [return_col],
        "correlation": [corr],
        "p_value": [pval]
    })
    return result


def rolling_correlation(news_df: pd.DataFrame, stock_df: pd.DataFrame, sentiment_col: str = "vader_compound", return_col: str = "log_return", window: int = 20) -> pd.DataFrame:
    """
    Compute rolling correlation between sentiment and stock returns.
    
    Args:
        window: rolling window size in days
    
    Returns:
        DataFrame with rolling correlation
    """
    merged = pd.merge_asof(
        news_df.sort_values('date'), 
        stock_df.sort_index().reset_index().rename(columns={'date': 'date'}),
        on='date',
        direction='backward'
    )
    
    merged.set_index('date', inplace=True)
    merged[f'rolling_corr_{window}'] = merged[sentiment_col].rolling(window).corr(merged[return_col])
    
    return merged[[sentiment_col, return_col, f'rolling_corr_{window}']].reset_index()
