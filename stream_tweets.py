import json
import pymongo
import tweepy
 
consumer_key = 'icZAH9xFhcAWJcRXSopbbkH8i'
consumer_secret = 'DO2g9lndauAkdWlMsbTFmCq4eFXyAqkj5I9PAKgS4ay5HeyQLQ'
access_token = '538903756-6YwCQTMMMkmpMDQvikZm3S1lmQjjc8t5hJ9oJvTB'
access_secret = 'Zs3yXhhe89xNpvQA6o6HNaovyLWQInhULJxQsGJzdR0jJ'
 
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient().test

    def on_data(self, tweet):
        self.db.tweets.insert(json.loads(tweet))

    def on_error(self, status_code):
        return True # Don't kill the stream

    def on_timeout(self):
        return True # Don't kill the stream


sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['#USelections','#trump','#clinton'])
