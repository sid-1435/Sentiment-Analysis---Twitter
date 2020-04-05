import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import GetOldTweets3 as got
from datetime import date
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import matplotlib.pyplot as plt

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
            df['permalink '] = np.array([tweet.retweets for tweet in tweets])
            
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


class TweetAnalyser():
    
    
    
    def clean_tweet(self, tweet):
        cleaned_tweet = tweet.translate(str.maketrans('', '', string.punctuation))
        return cleaned_tweet
    
    def analyze(self, tweet):
        
        vader = SentimentIntensityAnalyzer()
        score = vader.polarity_scores(tweet)['compound']
                
        if score>=0.05:
            return 'positive'
        elif score<=-0.05:
            return 'negative'
        else:
            return 'neutral'
        
    def lang_detect(self, tweet):
        blob = TextBlob(tweet)
        return blob.detect_language()
    
    def plot_sentiment(self, tweets_sent):
        
        positive_sent = 0
        negative_sent = 0
        neutral_sent = 0
        
        for sentiment in tweets_sent:
            if(sentiment=='positive'):
                positive_sent += 1
            elif(sentiment=='negative'):
                negative_sent += 1
            else:
                neutral_sent += 1
                
        labels = ['Positive: '+str(positive_sent/len(tweets_sent)*100)+'%', 'Negative: '+str(negative_sent/len(tweets_sent)*100)+'%', 'Neutral: '+str(neutral_sent/len(tweets_sent)*100)+'%']
        sizes = [positive_sent, negative_sent, neutral_sent]
        colors = ['lightgreen', 'lightsalmon', 'gold']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting:')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        


hash_tag_list = ['ronaldo']
tweet_streamer  =TweetStreamer()
tweets_df = tweet_streamer.get_tweets_by_keywords(hash_tag_list, count=20)
tweetanalyzer = TweetAnalyser()
tweets_df['Sentiment'] = ([tweetanalyzer.analyze(text) for text in tweets_df['Tweets']])
tweetanalyzer.plot_sentiment(tweets_df['Sentiment'])
tweets_df.to_csv('tweets.csv')


    