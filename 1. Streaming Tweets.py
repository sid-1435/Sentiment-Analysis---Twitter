import string
import nltk
import pandas as pd
import GetOldTweets3 as got
from datetime import date

#text = open('read.txt', encoding='utf-8').read()
#lower_text = text.lower()
#cleaned_text = lower_text.translate(str.maketrans('','', string.punctuation))

class TweetStreamer():
    
    """
    Functionality for fetching the tweets based on keywords or username
    """
    
    start_date = str(date(date.today().year, 1, 1))
    end_date = str(date.today())
    
    def get_tweets_by_keywords(self, hash_tag_list, count=50, start_date=start_date, end_date=end_date):
        
        for hash_tag in hash_tag_list:
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hash_tag)\
                                                   .setSince(start_date)\
                                                   .setUntil(end_date)\
                                                   .setMaxTweets(count)\
                                                   .setEmoji("unicode")
        
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
            df['id'] = np.array([tweet.id for tweet in tweets])
            df['len'] = np.array([len(tweet.text) for tweet in tweets])
            df['date'] = np.array([tweet.date for tweet in tweets])
            df['username'] = np.array([tweet.username for tweet in tweets])
            df['likes'] = np.array([tweet.favorites for tweet in tweets])
            df['retweets'] = np.array([tweet.retweets for tweet in tweets])
            return df
    
    
    def get_tweets_by_user(self, username, count=50, start_date=start_date, end_date=end_date):
        
        for hash_tag in hash_tag_list:
            tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                                   .setSince(start_date)\
                                                   .setUntil(end_date)\
                                                   .setMaxTweets(count)\
                                                   .setEmoji("unicode")
        
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
            df['id'] = np.array([tweet.id for tweet in tweets])
            df['len'] = np.array([len(tweet.text) for tweet in tweets])
            df['date'] = np.array([tweet.date for tweet in tweets])
            df['username'] = np.array([tweet.username for tweet in tweets])
            df['likes'] = np.array([tweet.favorites for tweet in tweets])
            df['retweets'] = np.array([tweet.retweets for tweet in tweets])
            return df


hash_tag_list = ['trump']
tweet_streamer  =TweetStreamer()
text = tweet_streamer.get_tweets_by_keywords(hash_tag_list, count=200)
text.to_csv('tweets.csv')

    