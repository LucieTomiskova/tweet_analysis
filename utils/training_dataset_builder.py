import csv
import random


def build_training_dataset(csv_path):

    corpus = []

    with open(csv_path, 'r', encoding='utf-8') as c:
        read_line = csv.reader(c, delimiter=',', quotechar="\"")
        for row in read_line:
            corpus.append({"tweet_date": row[0], "topic": row[1]})

    training_dataset = []
    test_dataset = []

    for i in range(0, int(len(corpus)*0.8)):
        random_tweet = random.choice(corpus)
        random_tweet["topic"] = random_tweet["topic"][2:-1]
        training_dataset.append(random_tweet)

    for tweet in corpus:
        if tweet not in training_dataset:
            tweet["topic"] = tweet["topic"][2:-1]
            test_dataset.append(tweet)
        continue

    return test_dataset, training_dataset


def write_into_csv(path, tweets_training_list):
    with open(path, 'w', encoding='utf-8') as csvfile:
        write_line = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in tweets_training_list:

            try:
                write_line.writerow([tweet["tweet_date"], tweet["topic"].strip()])
            except Exception as e:
                print(e)


if __name__ == '__main__':
    test_data, train_data = build_training_dataset('../data/2019-04-06.csv')
    write_into_csv('../data/training_data/training_dataset.csv', train_data)
    write_into_csv('../data/test_data/testing_dataset.csv', test_data)