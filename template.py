# -*- coding: latin-1 -*-
# Author: axel.tidemann@gmail.com
from collections import namedtuple
import random

from cc_pattern import noc
from hashtags import popular_hashtags
from positive import positive, negative

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

def iam(person):
    return '#IAm{}'.format(person.Character.replace(' ',''))

def youare(person):
    return '#YouAre{}'.format(person.Character.replace(' ',''))

def first_template(topic, me, other): 
    location = 'bed' if len(me.Vehicle_of_Choice) == 1 else random.choice(me.Vehicle_of_Choice)
    return "{} In my {} realizing {} is {}. What's your opinion, @convo_bot_2? {}".format(iam(me), location, topic.hashtag, positive(topic.hashtag[1:]), youare(other))

def second_template(topic, me, other):
    return "@convo_bot_1 {} I know I am {}, but {} is {}. I prefer {}.".format(iam(me), random.choice(me.Negative_Talking_Points), topic.hashtag, negative(topic.hashtag[1:]), random.choice(me.Typical_Activity))
