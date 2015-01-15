import random

from pattern.web import Twitter
from pattern.en import parsetree
from pattern.search import search
from pattern.en import sentiment

import re

who = "xfactor"

x = []

twitter = Twitter()

k = 0

polarity = 0
adjective = 'hello'

for i in range(1, 4):
    for tweet in twitter.search("\"%s is\"" % who, start=i, count=100, cached=True):
        
        s = tweet.text
        s = s.lower()
        s = re.sub(r"http://.*?(\s|$)", "", s) # Remove URL's.
        s = parsetree(s, lemmata=True)

        for m in search(who.lower() + " be {JJ}", s):
        	x.append(m.group(1).string)
        	

for word in x:
	s = sentiment(word)[0]
	if s > polarity:
		polarity = s
		adjective = word

print adjective

