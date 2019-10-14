import re
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from utils.training_dataset_builder import build_training_dataset



class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

    def processTweets(self, list_of_tweets):
        processedTweets = []
        for tweet in list_of_tweets:
            processedTweets.append(self._processTweet(tweet["topic"]))
        return processedTweets

    def _processTweet(self, tweet):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet) # remove URLs
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)
        words_list = [word.strip().encode('ascii', 'ignore').decode('ascii') for word in tweet if word not in self._stopwords]
        # words_list[0] = words_list[0].replace("b'", '')
        return words_list


if __name__ == '__main__':

    test_data, training_data = build_training_dataset('../data/2019-04-06.csv')
    clean_tweets = PreProcessTweets()
    print(clean_tweets.processTweets(training_data))
    print(clean_tweets.processTweets(test_data))