import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

def add_sentiment(df: pd.DataFrame, text_col: str = "content") -> pd.DataFrame:
    """
    Add VADER and TextBlob sentiment scores to a dataframe with news content.
    
    Args:
        df: DataFrame with a column containing text
        text_col: Name of the column with news text
    
    Returns:
        DataFrame with new columns: 'vader_compound', 'textblob_polarity', 'textblob_subjectivity'
    """
    vader = SentimentIntensityAnalyzer()
    
    # VADER sentiment
    df['vader_compound'] = df[text_col].apply(lambda x: vader.polarity_scores(str(x))['compound'])
    
    # TextBlob sentiment
    df['textblob_polarity'] = df[text_col].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df['textblob_subjectivity'] = df[text_col].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)
    
    return df
