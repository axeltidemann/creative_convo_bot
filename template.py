# -*- coding: latin-1 -*-
# Author: axel.tidemann@gmail.com
from collections import namedtuple
import random

import numpy as np

from cc_pattern import noc

Topic = namedtuple('Topic', ['hashtag', 'who', 'what', 'where'])
TweetSkeleton = namedtuple('TweetSkeleton', ['topic', 'person', 'creative_tweet'])

class KnowledgeBase:
    def __init__(self):
        self.KB = noc.parse("Veale's The NOC List.xlsx")
    
    def _to_person(self, D):
        for key in D.keys():
            D[key.replace(' ', '_')] = D.pop(key)
        
        return namedtuple('Person', D.keys())(**D)

    def traits(self, name):
        for row in self.KB:
            if row['Character'] == name:
                return self._to_person(row)

    @property
    def random(self):
        return self._to_person(random.choice(self.KB))

def template(tweet_skeleton):
    return '{}: {} {}'.format(tweet_skeleton.person.Character, tweet_skeleton.topic.hashtag, tweet_skeleton.creative_tweet)

def create_tweet(topic, person, sentiment):
    if sentiment < 0:
        tweet = "This is really boring, I prefer {}.".format(random.choice(person.Typical_Activity))
    else:
        tweet = "I will jump in my {} and give everyone who doesn't think this is very important a round with my {}!".format(
            random.choice(person.Vehicle_of_Choice), random.choice(person.Weapon_of_Choice))

    return TweetSkeleton(topic, person, tweet)

if __name__ == '__main__':
    KB = KnowledgeBase()
    topic = Topic('#goldenglobe', None, None, None)
    print template(create_tweet(topic, KB.random, np.random.randint(-1,1)))

