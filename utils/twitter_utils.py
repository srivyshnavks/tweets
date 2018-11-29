from textblob import TextBlob
import re
import tweepy
import pandas as pd
import numpy as np
import os
from collections import Counter
import operator

consumer_key = 'GAecT7Wcv8dcW5H1OyZIVezdg'
consumer_secret = '4Aj3UBnC6MP06436VzENCRxOwcgUI039mVNa8asFSdMbmKoNb1'

access_token = '1863663470-FOAdGRxjqvCati5JML1u5bXNsZUimmn2KqyMHJt'
access_token_secret = 'lleZdlK6eCLAmHVRuJTDmCSlO0G5TNLfaWSu5hnuvXYdR'

# API's setup:
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Return API with authentication:
api = tweepy.API(auth)


def get_tweets(searchquery):
    tweets = api.search(q=searchquery, count=100, lang='en', result_type='mixed')
    print("Number of tweets extracted: {}\n".format(len(tweets)))

    for tweet in tweets:
        tweet.text = re.sub(r'@\S+|https?://\S+', '', tweet.text)

    return tweets


def create_dataframe(tweets, input_text):
    # Creating pandas dataframe:
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

    # Adding relevant data:
    data['len'] = np.array([len(tweet.text) for tweet in tweets])
    # data['ID'] = np.array([tweet.id for tweet in tweets])
    data['Date'] = np.array([tweet.created_at for tweet in tweets])
    data['Source'] = np.array([tweet.source for tweet in tweets])
    data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
    data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])
    data['Sentiment'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])
    pd.set_option('display.max_colwidth', -1)
    #print(data)

    sa = list(data.Sentiment)
    sa.sort()
    sa = Counter(sa)
    sent = [i for i in sa.values()]

    source = list(data.Source)
    source.sort()
    users = Counter(source)
    
    users = sorted(users.items(), key=operator.itemgetter(1), reverse = True)
    
    # Save the csv file
    csv_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv_files')
    data.to_csv(os.path.join(csv_file_path, input_text + '_twitter-data.csv'), sep=',', encoding='utf-8')

    return data, sent, users


'''def create_list_pie(tweets):
    # Creating pandas dataframe:
    data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

    data['Sentiment'] = np.array([analize_sentiment(tweet) for tweet in data['Tweets']])
    # pd.set_option('display.max_colwidth', -1)
    sa = list(data.Sentiment)
    sa = Counter(sa)
    sent = [i for i in sa.values()]

    return sent
'''

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    # return analysis.sentiment.polarity

    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1


if __name__ == '__main__':
    input_text = 'global warming'
    input_query = input_text + '-filter:retweets'
    tweets = get_tweets(input_query)
    create_dataframe(tweets, input_text)
