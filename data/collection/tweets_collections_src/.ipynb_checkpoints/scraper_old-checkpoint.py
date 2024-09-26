import csv
import os
import time
import logging
from datetime import datetime, timedelta
from random import randint, uniform
from tqdm import tqdm
from twikit import Client, TooManyRequests

# Configuration
MINIMUM_TWEETS = 10
DELAY_BETWEEN_REQUESTS = (5, 15)  # Delay between requests in seconds (randomized)
MAX_CONSECUTIVE_ERRORS = 5  # Max consecutive errors before stopping the script
ERROR_WAIT_TIME = 60 * 15  # Wait time of 15 minutes after too many errors
cookies_files = ['cookies.json', 'cookies2.json', 'cookies3.json', 'cookies4.json']
current_cookie_index = 0
consecutive_errors = 0  # Track consecutive errors

# Initialize the total_tweets_collected variable
total_tweets_collected = 0  # Track total tweets collected globally

# Initialize Twitter client
client = Client()

# Setup logging
logging.basicConfig(filename='tweet_collection.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def switch_cookies():
    """Switches between cookies."""
    global current_cookie_index
    current_cookie_index = (current_cookie_index + 1) % len(cookies_files)
    client.load_cookies(cookies_files[current_cookie_index])
    logging.info(f'Switched to {cookies_files[current_cookie_index]}.')

def get_tweets(query, tweets=None):
    global consecutive_errors
    try:
        if tweets is None:
            logging.info(f'Getting tweets for query: {query}...')
            tweets = client.search_tweet(query, product='Top')
        else:
            wait_time = randint(5, 10)
            logging.info(f'Getting next tweets after {wait_time} seconds...')
            time.sleep(wait_time)
            tweets = tweets.next()

        # Reset error counter on success
        consecutive_errors = 0
        return tweets

    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        current_time = datetime.now()
        wait_time = (rate_limit_reset - current_time).total_seconds()

        logging.warning(f'Rate limit reached. Switching cookies.')
        switch_cookies()
        consecutive_errors += 1

        # Stop script if too many errors
        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
            logging.error(f'Max consecutive errors reached. Stopping the script to avoid ban.')
            raise SystemExit("Stopping script to avoid getting banned.")

        # Retry with new cookies
        try:
            tweets = get_tweets(query, tweets)
            logging.info('Successfully resumed after switching cookies.')
        except TooManyRequests:
            logging.warning(f'Rate limit still in place even after switching cookies.')
            if wait_time > 0:
                logging.warning(f'Waiting until {rate_limit_reset}')
                delay_for_minutes(15)  # Wait for 15 minutes
            else:
                logging.warning(f'Rate limit reset time is in the past. Waiting for 15 minutes as a precaution.')
                delay_for_minutes(15)
            consecutive_errors += 1
        return None
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        if '403' in str(e):
            logging.error('403 Forbidden error. Check your cookies and API permissions.')
            switch_cookies()
        consecutive_errors += 1

        # Stop the script after max consecutive errors
        if consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
            logging.error(f'Max consecutive errors reached. Stopping the script to avoid ban.')
            raise SystemExit("Stopping script to avoid getting banned.")
        return None

def construct_query(query_base, date):
    """Construct the query for the given date range."""
    next_day = date + timedelta(days=1)
    query = (f'({query_base}) lang:en until:{next_day.strftime("%Y-%m-%d")} '
             f'since:{date.strftime("%Y-%m-%d")}')
    return query

def delay_for_minutes(minutes=5):
    """Delays for the specified number of minutes, showing progress with tqdm."""
    wait_time = minutes * 60  # Convert minutes to seconds
    with tqdm(total=wait_time, desc=f'Waiting for {minutes} minutes', unit='s', leave=True) as rate_pbar:
        for _ in range(wait_time):
            time.sleep(1)
            rate_pbar.update(1)

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

def collect_tweets_for_day(query_base, date, csv_file):
    """Collect tweets for a specific day and save to a CSV file."""
    global total_tweets_collected  # Declare the variable as global so it can be updated
    query = construct_query(query_base, date)
    tweet_count = 0
    tweets = None
    daily_tweet_data = []

    # Initialize daily_stats list
    daily_stats = []  # Initialize the list here

    # Check if the CSV file exists
    file_exists = os.path.isfile(csv_file)

    # Also check if the file exists but is empty (i.e., no data or headers written yet)
    file_is_empty = os.path.getsize(csv_file) == 0 if file_exists else True

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = get_tweets(query, tweets)
        except TooManyRequests:
            continue

        if not tweets:
            logging.info(f'No more tweets found for {date.strftime("%Y-%m-%d")}')
            break

        for tweet in tweets:
            if tweet_count >= MINIMUM_TWEETS:
                break
            tweet_count += 1
            total_tweets_collected += 1  # Increment the total count when a tweet is collected
            daily_tweet_data.append([
                date.strftime('%Y-%m-%d'),
                tweet_count,
                tweet.user.name,
                tweet.text,
                tweet.created_at,
                tweet.retweet_count,
                tweet.favorite_count
            ])

        logging.info(f'Got {tweet_count} tweets for {date.strftime("%Y-%m-%d")}')
        daily_stats.append([date.strftime('%Y-%m-%d'), tweet_count])

        # Add random delay to simulate human-like behavior and avoid rate limits
        time.sleep(uniform(*DELAY_BETWEEN_REQUESTS))

    # Write daily tweet data to CSV after processing all tweets for the day
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header only if the file is empty or doesn't exist
        if file_is_empty:
            writer.writerow(['Date', 'Tweet Count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

        # Write the tweet data
        writer.writerows(daily_tweet_data)

    if tweet_count < MINIMUM_TWEETS:
        logging.warning(f'Collected {tweet_count} tweets for {date.strftime("%Y-%m-%d")}, which is less than the minimum of {MINIMUM_TWEETS}')
    
    logging.info(f'Done for {date.strftime("%Y-%m-%d")}')
