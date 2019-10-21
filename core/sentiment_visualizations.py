import json
import matplotlib.pyplot as plt
import pandas as pd
from configuration.config import root

SENTIMENT_PATH = root / 'data' / 'sentiment_avg_daily.json'
BITCOIN_PRICE_PATH = root / 'data' / 'bitcoin_price.json'


def read_json(json_path):
    with open(json_path, 'r') as outfile:
        json_content = json.load(outfile)
    return json_content


def create_df(json_text, index_column):
    df = pd.DataFrame(json_text)
    df[index_column] = pd.to_datetime(df[index_column], format='%Y-%m-%d %H:%M:%S')
    df = df.set_index(index_column)
    df.index = df.index.strftime('%Y-%m-%d')
    df = df.sort_index()
    return df


def get_lineplot(df, column_name, title, ylabel, xlabel):
    df[column_name].plot(linewidth=0.5)
    plt.title(title, fontsize=14)
    plt.ylabel(ylabel, fontsize=10)
    plt.xlabel(xlabel, fontsize=10)


def get_scatterplot(x, y, title, ylabel, xlabel):
    plt.scatter(x, y)
    plt.title(title, fontsize=14)
    plt.ylabel(ylabel, fontsize=10)
    plt.xlabel(xlabel, fontsize=10)
    plt.show()


if __name__ == '__main__':

    tweets_daily_sentiment = read_json(SENTIMENT_PATH)
    tweets_df = create_df(tweets_daily_sentiment, 'tweet_date')

    plt.subplot(211)
    get_lineplot(tweets_df, 'avg', 'Denní sentiment tweetů', 'sentiment', 'datum')

    bitcoin_price_json = read_json(BITCOIN_PRICE_PATH)
    bitcoin_price = {'date': list(bitcoin_price_json.keys()), 'bitcoin_price': list(bitcoin_price_json.values())}
    bitcoin_price_df = create_df(bitcoin_price, 'date')

    plt.subplot(212)
    get_lineplot(bitcoin_price_df, 'bitcoin_price', 'Vývoj ceny Bitcoinu', 'cena', 'datum')

    plt.tight_layout()
    plt.show()

    merged_dfs = pd.merge(tweets_df, bitcoin_price_df, left_index=True, right_index=True)

    get_scatterplot(merged_dfs['avg'], merged_dfs['bitcoin_price'], 'Correlation between BTC price and sentiment', 'BTC price', 'sentiment')

