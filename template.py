# -*- coding: latin-1 -*-
# Author: axel.tidemann@gmail.com
from collections import namedtuple
import random

from cc_pattern import noc
from hashtags import popular_hashtags

Topic = namedtuple('Topic', ['hashtag', 'who', 'what', 'where'])

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

def first_template(topic, me, other):
    return "{}: {} {} What do you think, {} (@convo_bot_2)?'".format(me.Character, topic.hashtag, creative_tweet(topic, me, 1), other.Character)

def second_template(topic, me, other):
    return '{}: {} (@convo_bot_1) {} {}'.format(me.Character, other.Character, topic.hashtag, creative_tweet(topic, me, -1))

def creative_tweet(topic, person, sentiment):
    if sentiment < 0:
        return "I know I am {}, but this is really boring. I prefer {}.".format(random.choice(person.Negative_Talking_Points), random.choice(person.Typical_Activity))
    else:
        return "I will jump in my {} and give everyone who doesn't think this is very important a round with my {}!".format(
            random.choice(person.Vehicle_of_Choice), random.choice(person.Weapon_of_Choice))

if __name__ == '__main__':
    hashes = popular_hashtags()
    hashtag = random.choice(hashes[random.choice(hashes.keys())])
    KB = KnowledgeBase()
    topic = Topic(hashtag, None, None, None)
    first = KB.random
    second = KB.random
    print first_template(topic, first, second)
    print
    print second_template(topic, second, first)

