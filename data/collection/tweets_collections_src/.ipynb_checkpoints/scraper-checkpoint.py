import csv
import os
import time
import logging
from datetime import datetime, timedelta
from random import randint, uniform
from threading import Lock
from tqdm import tqdm
from twikit import Client, TooManyRequests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
MINIMUM_TWEETS = 10
DELAY_BETWEEN_REQUESTS = (2, 7)  # Delay between requests in seconds
MAX_CONSECUTIVE_ERRORS = 5       # Max consecutive errors before waiting
ERROR_WAIT_TIME = 60 * 15        # Wait time of 15 minutes after too many errors

# List of cookies files
cookies_files = [
    'cookies.json', 'cookies2.json', 'cookies3.json', 'cookies4.json',
    'cookies5.json', 'cookies6.json', 'cookies7.json', 'cookies8.json'
]

# Setup logging
logging.basicConfig(
    filename='tweet_collection.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Lock for file writing
file_write_lock = Lock()

def construct_query(query_base, date):
    """Construct the query for the given date range."""
    next_day = date + timedelta(days=1)
    query = (
        f'({query_base}) lang:en since:{date.strftime("%Y-%m-%d")} '
        f'until:{next_day.strftime("%Y-%m-%d")}'
    )
    return query

def get_last_collected_date(csv_file, start_date):
    """Reads the CSV file to find the last collected date."""
    if not os.path.exists(csv_file):
        return start_date
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) <= 1:
            return start_date
        last_date = rows[-1][0]
        return datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)

def get_tweets(client, query, tweets=None):
    """Fetch tweets using the provided client."""
    try:
        if tweets is None:
            logging.info(f'Getting tweets for query: {query}...')
            tweets = client.search_tweet(query, product='Top')
        else:
            wait_time = randint(*DELAY_BETWEEN_REQUESTS)
            logging.info(f'Waiting for {wait_time} seconds before getting next tweets...')
            time.sleep(wait_time)
            tweets = tweets.next()
        return tweets
    except TooManyRequests as e:
        logging.warning('Rate limit reached.')
        raise e
    except Exception as e:
        logging.error(f'An unexpected error occurred: {e}')
        raise e

def collect_tweets_for_day(query_base, date, csv_file, cookies_file):
    """Collect tweets for a specific day and save to a CSV file."""
    query = construct_query(query_base, date)
    tweet_count = 0
    tweets = None
    daily_tweet_data = []
    consecutive_errors = 0

    # Initialize the Twitter client
    client = Client()
    client.load_cookies(cookies_file)
    logging.info(f'Using cookies from {cookies_file}')

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = get_tweets(client, query, tweets)
            if not tweets:
                logging.info(f'No more tweets found for {date.strftime("%Y-%m-%d")}')
                break

            for tweet in tweets:
                if tweet_count >= MINIMUM_TWEETS:
                    break
                tweet_count += 1
                daily_tweet_data.append([
                    date.strftime('%Y-%m-%d'),
                    tweet_count,
                    tweet.user.name,
                    tweet.text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count
                ])
            logging.info(f'Collected {tweet_count} tweets for {date.strftime("%Y-%m-%d")}')
            consecutive_errors = 0  # Reset on successful fetch

            # Random delay to avoid rate limits
            time.sleep(uniform(*DELAY_BETWEEN_REQUESTS))

        except TooManyRequests:
            consecutive_errors += 1
            logging.warning(f'Too many requests. Consecutive errors: {consecutive_errors}')
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                logging.error(f'Max consecutive errors reached. Waiting for {ERROR_WAIT_TIME // 60} minutes.')
                time.sleep(ERROR_WAIT_TIME)
                consecutive_errors = 0
            else:
                time.sleep(ERROR_WAIT_TIME // MAX_CONSECUTIVE_ERRORS)
            continue
        except Exception as e:
            consecutive_errors += 1
            logging.error(f'Error fetching tweets: {e}')
            if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
                logging.error(f'Max consecutive errors reached. Waiting for {ERROR_WAIT_TIME // 60} minutes.')
                time.sleep(ERROR_WAIT_TIME)
                consecutive_errors = 0
            else:
                time.sleep(ERROR_WAIT_TIME // MAX_CONSECUTIVE_ERRORS)
            continue

    if daily_tweet_data:
        # Write data to CSV
        with file_write_lock:
            file_exists = os.path.isfile(csv_file)
            file_is_empty = os.path.getsize(csv_file) == 0 if file_exists else True

            with open(csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if file_is_empty:
                    writer.writerow(['Date', 'Tweet Count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])
                writer.writerows(daily_tweet_data)
        logging.info(f'Data written to {csv_file} for date {date.strftime("%Y-%m-%d")}')
    else:
        logging.info(f'No tweets collected for {date.strftime("%Y-%m-%d")}')

def scrape_tweets_parallel(query_base, start_date, end_date, csv_file):
    date_list = [
        start_date + timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    # Limit the number of workers to the number of cookies
    max_workers = min(len(cookies_files), 4)
    logging.info(f'Using {max_workers} worker threads.')

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, date in enumerate(date_list):
            cookies_file = cookies_files[i % len(cookies_files)]
            futures.append(
                executor.submit(
                    collect_tweets_for_day,
                    query_base,
                    date,
                    csv_file,
                    cookies_file
                )
            )

        for future in tqdm(
            as_completed(futures),
            total=len(futures),
            desc="Collecting Tweets"
        ):
            try:
                future.result()
            except Exception as e:
                logging.error(f'Error in thread: {e}')
