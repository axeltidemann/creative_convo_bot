import random

from pattern.web import Twitter
from pattern.en import parsetree
from pattern.search import search
from pattern.en import sentiment

import re

def positive(hashtag):
    x = []
    twitter = Twitter()
    k = 0
    polarity = 0

    for i in range(1, 4):
        for tweet in twitter.search("\"%s is\"" % hashtag, start=i, count=100, cached=True):
            s = tweet.text
            s = s.lower()
            s = re.sub(r"http://.*?(\s|$)", "", s) # Remove URL's.
            s = parsetree(s, lemmata=True)

            for m in search(hashtag.lower() + " be {JJ}", s):
                x.append(m.group(1).string)

    adjective = None
    for word in x:
        s = sentiment(word)[0]
        if s > polarity:
            polarity = s
            adjective = word

    return adjective if adjective is not None else 'good'

def negative(hashtag):
    x = []
    twitter = Twitter()
    k = 0
    polarity = 0

    for i in range(1, 4):
        for tweet in twitter.search("\"%s is\"" % hashtag, start=i, count=100, cached=True):
            s = tweet.text
            s = s.lower()
            s = re.sub(r"http://.*?(\s|$)", "", s) # Remove URL's.
            s = parsetree(s, lemmata=True)

            for m in search(hashtag.lower() + " be {JJ}", s):
                x.append(m.group(1).string)

    adjective = None
    for word in x:
        s = sentiment(word)[0]
        if s < polarity:
            polarity = s
            adjective = word

    return adjective if adjective is not None else 'bad'
