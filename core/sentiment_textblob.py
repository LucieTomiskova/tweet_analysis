import csv
import re
import json
import glob
import argparse
from statistics import mean

from textblob import TextBlob

from configuration.config import data_dir


tweets_folder = glob.glob(data_dir + '/*.csv')


def write_into_json(file_name):
    with open(file_name, 'w') as outfile:
        json.dump(all_days_sentiment, outfile)


def create_corpus(csv_path):
    """
    Function reads the csv file with all the fetched tweets and returns
    list of dictionaries. Each dictionary contains tweets_date and topis of the tweet.
    :param csv_path: columns: date, tweet text
    :return: corpus
    """

    corpus = []
    with open(csv_path, 'r', encoding='utf-8') as c:
        read_line = csv.reader(c, delimiter=',', quotechar="\"")
        for row in read_line:
            corpus.append({"tweet_date": row[0], "topic": row[1][2:-1]})

    return corpus


def _data_preprocessing(tweet_text):
    tweet = tweet_text.lower()
    tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    tweet = re.sub(r'\\x(([a-zA-Z]|\d){2})', '', tweet)
    tweet = tweet.replace('\\n', ' ')
    hashtags = re.findall(r'#([^\s]+)', tweet)

    return tweet, hashtags


def get_avg_value(values_list):
    avg = mean(values_list)
    return avg


def get_sentiment(tweets_corpus):

    sentiment_val = []
    for tweet in tweets_corpus:
        tweet_processed, hashtags = _data_preprocessing(tweet['topic'])
        tweet['topic'] = tweet_processed
        tweet['hashtags'] = hashtags
        wiki = TextBlob(tweet['topic'])
        tweet['sentiment'] = wiki.sentiment.polarity
        sentiment_val.append(tweet['sentiment'])
        tweet['subjectivity'] = wiki.sentiment.subjectivity

    avg = mean(sentiment_val)
    avg_med_dict = {
        'tweet_date': tweets_corpus[0]['tweet_date'],
        'avg': avg,
    }
    # write_into_json(tweets_corpus)
    return avg_med_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Get tweet sentiments.")
    parser.add_argument("output_filename", help="JSON file name")
    args = parser.parse_args()

    all_days_sentiment = []
    for daily_tweet in list(tweets_folder):
        corpus = create_corpus(daily_tweet)
        avg_sent_dict = get_sentiment(corpus)
        all_days_sentiment.append(avg_sent_dict)

    write_into_json(args.output_filename)
