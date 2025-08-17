import sys
import os

# Add the project root directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import modules
from data.data_preparation import load_news_data, load_stock_data, explore_news_data, explore_stock_data
from data.cleaning import clean_news_data, align_news_to_stock, save_processed_data

def main():
    print("Current working directory:", os.getcwd())
    
    news_file = "C:\\Users\\Win 10 Pro\\Documents\\10 Academy\\week-1\\news-sentiment-returns-capstone\\data\\raw\\raw_analyst_ratings.csv"
    stock_folder = "C:\\Users\\Win 10 Pro\\Documents\\10 Academy\\week-1\\news-sentiment-returns-capstone\\data\\raw\\yfinance_data"
    processed_folder = "C:\\Users\\Win 10 Pro\\Documents\\10 Academy\\week-1\\news-sentiment-returns-capstone\\data\\processed"

    # Load data
    news_df = load_news_data(news_file)
    stocks = load_stock_data(stock_folder)

    # Step 1: Explore raw data
    explore_news_data(news_df)
    explore_stock_data(stocks)

    # Step 2: Clean news data
    news_df = clean_news_data(news_df)

    # Step 2: Align news to stock trading dates and save processed datasets
    for symbol, stock_df in stocks.items():
        aligned_news = align_news_to_stock(news_df, stock_df, symbol)
        save_processed_data(aligned_news, os.path.join(processed_folder, f"{symbol}_news.csv"))

if __name__ == "__main__":
    main()
