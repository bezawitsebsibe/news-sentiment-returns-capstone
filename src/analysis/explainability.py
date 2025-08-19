import shap
import pandas as pd
from sklearn.linear_model import LinearRegression

def explain_sentiment_model(news_df: pd.DataFrame, stock_df: pd.DataFrame, sentiment_col="vader_compound", return_col="log_return"):
    """
    Fit a simple linear model: sentiment -> stock returns and explain using SHAP
    """
    merged = pd.merge_asof(
        news_df.sort_values('date'), 
        stock_df.sort_index().reset_index().rename(columns={'date':'date'}),
        on='date', direction='backward'
    ).dropna(subset=[sentiment_col, return_col])
    
    X = merged[[sentiment_col]]
    y = merged[return_col]
    
    model = LinearRegression()
    model.fit(X, y)
    
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)
    
    return model, shap_values, merged
