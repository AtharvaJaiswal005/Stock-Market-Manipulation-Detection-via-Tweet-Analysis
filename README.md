# Stock Market Manipulation Detection via Tweet Analysis

This project focuses on detecting potential stock market manipulation by analyzing tweets related to major companies. The aim is to identify signs of insider trading and the spread of false information intended to influence stock prices.

## Project Overview

We have collected a dataset of tweets mentioning companies listed in the **Nifty 50**, the top 50 companies on the National Stock Exchange of India. By examining this data, we intend to uncover patterns that might indicate manipulative practices affecting stock market behavior.

## Data Collection

### Tweet Data

We monitored all Nifty 50 companies and collected tweets from **January 1, 2023, to December 31, 2023**. Using the **twikit** library, we scraped 10 tweets per day for each company, totaling approximately 500 tweets per day.

The data collection process involved constructing specific search queries for each company to retrieve relevant tweets. The **twikit** library enabled efficient scraping while handling potential limitations. The collected tweets for each company were saved as individual CSV files in the `collected_tweets/` folder. These individual CSV files were then merged and saved in the `data/raw/split_data/` folder for easy access and analysis.

### Stock Market Data

We utilized the `yfinance` library to download historical stock prices for the same Nifty 50 companies, matching the date range of the tweet data for accurate comparison. The stock price data is saved as `historical_prices.csv` in the repository.

## Repository Structure

The repository is organized as follows:

```
Stock-Market-Manipulation-Detection/
├── data/
│   ├── collection/
│   │   ├── stock_market_collections_src/
│   │   │   ├── 0_stock_data_collector.ipynb
│   │   │   └── historical_prices.csv
│   │   └── tweets_collections_src/
│   │       ├── 0_stock_tweet_collector.ipynb
│   │       ├── scraper.py
│   │       ├── collected_tweets/
│   │       │   ├── ADANIENT.csv
│   │       │   ├── ADANIGREEN.csv
│   │       │   ├── ADANIPORTS.csv
│   │       │   ├── APOLLOHOSP.csv
│   │       │   ├── ASIANPAINT.csv
│   │       │   ├── AXISBANK.csv
│   │       │   ├── BAJAJ-AUTO.csv
│   │       │   ├── BAJAJFINSV.csv
│   │       │   ├── BAJFINANCE.csv
│   │       │   ├── ...
│   │       │   └── WIPRO.csv
│   │       ├── other files and folders (cookies, logs, etc.)
│   ├── raw/
│   │   └── split_data/
│   │       ├── ADANIENT.csv
│   │       ├── ADANIGREEN.csv
│   │       ├── ADANIPORTS.csv
│   │       ├── APOLLOHOSP.csv
│   │       ├── ASIANPAINT.csv
│   │       ├── AXISBANK.csv
│   │       ├── BAJAJ-AUTO.csv
│   │       ├── BAJAJFINSV.csv
│   │       ├── BAJFINANCE.csv
│   │       ├── ...
│   │       └── WIPRO.csv
├── README.md
```

- **data/**: Contains datasets and data collection scripts.
  - **collection/**: Contains the data collection code and raw collected data.
    - **stock_market_collections_src/**: Folder containing the stock market data collection notebook.
      - `0_stock_data_collector.ipynb`: Jupyter notebook that uses `yfinance` to download stock prices.
      - `historical_prices.csv`: Collected historical stock prices.
    - **tweets_collections_src/**: Folder containing the tweet collection code and data.
      - `0_stock_tweet_collector.ipynb`: Jupyter notebook that uses `twikit` to scrape tweets.
      - `scraper.py`: Script used for scraping tweets.
      - `collected_tweets/`: Folder containing individual CSV files for each company's tweets.
        - `ADANIENT.csv`, `ADANIGREEN.csv`, `ADANIPORTS.csv`, ..., `WIPRO.csv`: Collected tweets for each company.
      - Other files and folders: Cookie files, logs, and temporary files.
  - **raw/**: Contains processed data ready for analysis.
    - **split_data/**: Merged and cleaned CSV files for each company.
      - `ADANIENT.csv`, `ADANIGREEN.csv`, `ADANIPORTS.csv`, ..., `WIPRO.csv`: Merged and processed tweets for each company.

## Data Collection Process

### Tweets Collection

- **Notebook**: `data/collection/tweets_collections_src/0_stock_tweet_collector.ipynb`
- **Process**:
  - Constructed specific search queries for each Nifty 50 company.
  - Used the **twikit** library to scrape tweets.
  - Collected 10 tweets per day per company, from January 1, 2023, to December 31, 2023.
  - Saved individual CSV files for each company in `collected_tweets/`.
  - Merged these individual CSV files and saved the consolidated data in `data/raw/split_data/`.

### Stock Market Data Collection

- **Notebook**: `data/collection/stock_market_collections_src/0_stock_data_collector.ipynb`
- **Process**:
  - Used the `yfinance` library to download historical stock prices for the Nifty 50 companies.
  - Collected data matching the date range of the tweets.
  - Saved the historical prices in `historical_prices.csv`.

## Notes

- The CSV files in `collected_tweets/` are the raw tweet data for each company.
- These individual CSV files are merged and saved in the `data/raw/split_data/` folder for further analysis.
- Additional files like cookies, logs, and temporary files are present in the `tweets_collections_src/` folder, used during the scraping process.

## Contact

For questions or suggestions, please reach out to:

- **Atharva Jaiswal**
- **Email**: atharvajaiswal005@gmail.com
- **LinkedIn**: [Atharva Jaiswal](https://www.linkedin.com/in/atharva-jaiswal/)
