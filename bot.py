# -*- coding: latin-1 -*-
# Author: axel.tidemann@gmail.com
import random

from pattern.web import URL, Twitter

from hashtags import popular_hashtags
from mapping import mapping
from template import KnowledgeBase, first_template, second_template, Topic
from find_people import find_people

# abrahamlincoln292@gmail.com abeabeabe
# kardashiank170@gmail.com kim kim kim

def publish(auth_keys, tweet):
    url = URL("https://api.twitter.com/1.1/statuses/update.json", method="post", query={"status": tweet})

    twitter = Twitter(license=auth_keys)
    url = twitter._authenticate(url)

    try:
        url.open()
    except Exception as e:
        print e
        print e.src
        print e.src.read()
    

if __name__ == '__main__':
    genre, hashtag = mapping()
    first, second = find_people(genre)
    KB = KnowledgeBase()
    topic = Topic(hashtag, None, None, None)
    first_person = KB.traits(first)
    second_person = KB.traits(second)
    print first_template(topic, first_person, second_person)
    print
    print second_template(topic, second_person, first_person)

    # bot1_pattern = ('FHRtcITLNDk5HYtam6aIb230K',
    #                 '0z1aNYk4i8nc4KYyHNvmgkIoi3lkEfVAuRj8BgC9ynP6MAJW6o',
    #                 ('2978463185-sxEmSJblYUt9hD1lLzVtei4XnBN7btE1AlEYJ5P',
    #                  'fIE7sHt3VMLtptMEChJFCWFzY2zxqMv6qLDGdtPGyHf0a'))

    # tweet = "I'm alive!"
    # publish(bot1_pattern, tweet)

    # bot2_pattern = ('A77WTgalcwA8hfDhD6AqWOOaZ',
    #                 'C8nTcxf5SJHla2KVqwVTiiflpFyMmLpuEUES62ewp3EcsIErfq',
    #                 ('2978543729-GYVjPcoIMUbIqMK9tutLmIuX0gTDwRDHawpiAqc',
    #                  'STTt8CaqJ476FsgVPyit8iRHC5zvxaPXWRDUgPLevjrYS'))

    # tweet = "I'm alive!"
    # publish(bot2_pattern, tweet)
