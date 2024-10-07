# Stock Market Manipulation Detection via Tweet Analysis

This project focuses on detecting potential stock market manipulation by analyzing tweets related to major companies. The aim is to identify signs of insider trading and the spread of false information intended to influence stock prices.

## Project Overview

We have collected a dataset of tweets mentioning companies listed in the **Nifty 50**, the top 50 companies on the National Stock Exchange of India. By examining this data, we intend to uncover patterns that might indicate manipulative practices affecting stock market behavior.

## Data Collection

### Tweet Data

We monitored all Nifty 50 companies and collected tweets from **January 1, 2023, to December 31, 2023**. Using the **twikit** library, we scraped 10 tweets per day for each company, totaling approximately 500 tweets per day.

The data collection process involved constructing specific search queries for each company to retrieve relevant tweets. The **twikit** library enabled efficient scraping while handling potential limitations. The collected tweets for each company were saved as individual CSV files, later merged for easy access and analysis.

### Stock Market Data

We utilized the `yfinance` library to download historical stock prices for the same Nifty 50 companies, matching the date range of the tweet data for accurate comparison. The stock price data is saved in the `data` folder.

## Repository Structure

The repository is organized as follows:

```
Stock-Market-Manipulation-Detection/
│   .gitattributes
│   .gitignore
│   README.md
│   requirements.txt
│   setup.py
│
├───data/
│       balanced_data.csv
│       data.csv
│       historical_prices.csv
│       merged.csv
│       modified_data.csv
│       resampled_dataset.csv
│
└───src/
    │   data.csv
    │   EDA.ipynb
    │   EDA_Merged_Dataset_Analysis.ipynb
    │   historical_prices.csv
    │   lstm_autoencoder_model_tuned.h5
    │   merge_data_model_devlopment.ipynb
    │   stock_sentiment_analysis.ipynb
    │
    ├───data collection/
    │   └───tweet_collection/
    │           0_stock_tweet_collector.ipynb
    │           cookie_genrator.ipynb
    │           HINDUNILVR.ipynb
    │           Reliance_industry.ipynb
    │           tcs.ipynb
    │           Untitled.ipynb
    │
    └───nlp_tweets_processing/
        │   cleaned_data.csv
        │   tweet_preprocessing.ipynb
```

- **data/**: Contains cleaned and processed datasets used for analysis.
- **src/**: Contains Jupyter notebooks and scripts for data analysis, model development, and data preprocessing.
- **setup.py**: Script for setting up the environment, downloading required data, and installing dependencies.

## Data Collection Process

### Tweets Collection

- **Notebook**: `src/data collection/tweet_collection/0_stock_tweet_collector.ipynb`
- **Process**:
  - Constructed specific search queries for each Nifty 50 company.
  - Used the **twikit** library to scrape tweets.
  - Collected 10 tweets per day per company, from January 1, 2023, to December 31, 2023.
  - Saved individual CSV files for each company.
  - Merged these individual CSV files for further analysis.

### Stock Market Data Collection

- **Notebook**: `src/data collection/stock_market_collections_src/0_stock_data_collector.ipynb`
- **Process**:
  - Used the `yfinance` library to download historical stock prices for the Nifty 50 companies.
  - Collected data matching the date range of the tweets.
  - Saved the historical prices in `historical_prices.csv`.

## Data Access

The `data` folder containing the datasets is not directly stored in the repository due to size limitations. You can download the data using the provided `setup.py` script or directly from [this Google Drive link](https://drive.google.com/drive/folders/1VaRjz7jibiyqnhSESDJ_h1U33Vvhu_xh?usp=sharing).

To set up the data and dependencies, run:
```bash
python setup.py
```

This script will automatically download the necessary data and install all dependencies from `requirements.txt`.

## Contact

For questions or suggestions, please reach out to:

- **Atharva Jaiswal**
- **Email**: atharvapj5@gmail.com
- **LinkedIn**: [Atharva Jaiswal](https://www.linkedin.com/in/atharva-jaiswal/)
