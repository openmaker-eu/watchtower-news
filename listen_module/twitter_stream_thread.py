from mongoengine import signals

__author__ = 'Enis Simsar'

import json
import re
import threading
from datetime import datetime

from decouple import config
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from models.Tweet import Tweet
from models.Topic import Topic


def get_info(topic_dic):
    keywords = []
    topics = []
    lang = []
    for key in topic_dic:
        topic = topic_dic[key]
        topics = topics + [topic['id']]
        keywords = keywords + topic['keywords']
        lang = lang + topic['languages']
    lang = list(set(lang))
    lang = [str(l) for l in lang]
    keywords = list(set(keywords))
    keywords = [str(keyword) for keyword in keywords]
    result = {
        'topics': sorted(topics),
        'keywords': keywords,
        'lang': lang
    }
    return result


def create_tweet(topic_id, tweet):
    topic = Topic.objects.get(id=topic_id)

    tweet_obj = Tweet()
    tweet_obj.topic_id = topic.id
    tweet_obj.published_at = datetime.fromtimestamp(int(tweet['timestamp_ms']) / 1e3)
    tweet_obj.entry = tweet

    tweet_obj.save()

    topic.last_tweet_at = datetime.now
    topic.save()


def separates_tweet(topic_dic, tweet):
    for key in topic_dic:
        topic = topic_dic[key]
        if tweet['lang'] in topic['languages']:
            for keyword in topic['keywords']:
                keyword = re.compile(keyword.replace(" ", "(.?)"), re.IGNORECASE)
                if 'extended_tweet' in tweet and 'full_text' in tweet['extended_tweet']:
                    if re.search(keyword, str(tweet['extended_tweet']['full_text'])):
                        create_tweet(key, tweet)
                        break
                else:
                    if re.search(keyword, str(tweet['text'])):
                        create_tweet(key, tweet)
                        break


# Accessing Twitter API
consumer_key = config("TWITTER_CONSUMER_KEY")  # API key
consumer_secret = config("TWITTER_CONSUMER_SECRET")  # API secret
access_token = config("TWITTER_ACCESS_TOKEN")
access_secret = config("TWITTER_ACCESS_SECRET")


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, topic_dic):
        self.topic_dic = topic_dic
        self.terminate = False
        self.connection = True
        super(StdOutListener, self).__init__()

    def on_data(self, data):
        if not self.terminate:
            tweet = json.loads(data)
            separates_tweet(self.topic_dic, tweet)
            return True
        else:
            return False

    def on_disconnect(self, notice):
        self.connection = False
        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            return False

    def stop(self):
        self.terminate = True

    def on_timeout(self):
        return True  # To continue listening


class StreamCreator():
    def __init__(self, topic_dic):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        self.l = StdOutListener(topic_dic)

        signals.post_save.connect(Tweet.post_save, sender=Tweet)

        self.info = get_info(topic_dic=topic_dic)
        self.keywords = self.info['keywords']
        self.lang = self.info['lang']
        self.topics = self.info['topics']
        print(self.topics)
        print(self.keywords)
        print(self.lang)
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_secret)
        self.stream = Stream(self.auth, self.l)
        self.t = threading.Thread(target=self.stream.filter,
                                  kwargs={'track': self.keywords, 'languages': self.lang, 'stall_warnings': True})

    def start(self):
        self.t.deamon = True
        self.t.start()

    def terminate(self):
        self.l.running = False
        self.l.stop()
        self.l.terminate = True
