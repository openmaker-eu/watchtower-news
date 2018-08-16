from mongoengine import connect

__author__ = 'Enis Simsar'

from time import sleep
from decouple import config

from listen_module.twitter_stream_thread import StreamCreator
from models.Topic import Topic
from models.Tweet import Tweet
from bson.objectid import ObjectId


class TwitterListen:
    def __init__(self):
        self.topic_dic = {}
        self.thread = None

    def setup(self, topic_list):
        if len(topic_list) != 0:
            for topic in topic_list:
                if str(topic['id']) not in self.topic_dic:
                    self.topic_dic[str(topic['id'])] = topic
            self.thread = StreamCreator(self.topic_dic)
            self.thread.start()

    def restart(self, topic_list):
        self.topic_dic = {}
        if self.thread is not None:
            self.kill()
        if len(topic_list) != 0:
            for topic in topic_list:
                if str(topic['id']) not in self.topic_dic:
                    self.topic_dic[str(topic['id'])] = topic
            self.thread = StreamCreator(self.topic_dic)
            self.thread.start()

    def kill(self):
        self.thread.terminate()
        del self.thread
        self.thread = None


def get_last_sequence_id():
    last_tweet = Tweet.objects.order_by('-_id').first()
    return last_tweet.id if last_tweet is not None else ObjectId()


def main():
    connect(
        config('MONGODB_DB'),
        username=config('MONGODB_USER'),
        password=config('MONGODB_PASSWORD'),
        host=config('MONGODB_HOST'),
        port=config('MONGODB_PORT', cast=int),
        authentication_source='admin',
        connect=False
    )

    running_topic_list = [topic.to_dict() for topic in Topic.objects.filter(is_active=True)]
    twitter_module = TwitterListen()
    twitter_module.setup(running_topic_list)

    last_sequence_id = get_last_sequence_id()

    count = 0
    while True:
        print("Loop is continuing. count = {0}".format(count))
        count += 1
        sleep(300)
        new_running_topic_list = [topic.to_dict() for topic in Topic.objects.filter(is_active=True)]

        current_keywords = [i['keywords'] for i in running_topic_list]
        current_languages = [i['languages'] for i in running_topic_list]

        new_keywords = [i['keywords'] for i in new_running_topic_list]
        new_languages = [i['languages'] for i in new_running_topic_list]

        if current_keywords != new_keywords or current_languages != new_languages:
            running_topic_list = new_running_topic_list
            print("Restarting Twitter Module!")
            twitter_module.restart(new_running_topic_list)

        if count % 6 == 0:
            new_last_sequence_id = get_last_sequence_id()
            print("last_id = {0}, new_last_id = {1}".format(last_sequence_id, new_last_sequence_id))
            if last_sequence_id == new_last_sequence_id:
                running_topic_list = new_running_topic_list
                print("Unexpectedly Stopped Module, Restarting...")
                twitter_module.restart(new_running_topic_list)
            last_sequence_id = get_last_sequence_id()


if __name__ == "__main__":
    main()
