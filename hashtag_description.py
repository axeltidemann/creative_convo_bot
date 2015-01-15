#entertainment(0), tech(1), politics(2)

from pattern.web import URL, plaintext, DOM
from pattern.en import parse, parsetree, Chunk
from pattern.search import search

import re

def get_ht_description(htag):
	WEBSITE = 'https://www.hashtags.org/analytics/'
	search = WEBSITE + htag
	src = URL(search).download(cached=True, unicode=True)
	dom = DOM(src)	
	for tagdef in dom("div#definition"):
		sentence = tagdef.content
		rest = sentence.split('.', 1)[0]
		return rest



def get_obj(sentence):
	print sentence
	sentence = sentence.lower()
	s = parsetree(sentence, relations=True, lemmata=True)
	
	#pattern2	"referring to..."
	for m in search("refer|referring to {NP}", s):
		print "pattern 2:"
		for nogo in ('things'):
			if nogo in m.group(1):
				break	
		return m.group(1).string	
		
	#pattern3	"sentence without verb, pure description"
	for m in search("{NP} that|which|who is", s):
		print "pattern 3:"
		for nogo in ('term', 'word', 'tag', 'hashtag'):
			if nogo in m.group(1):
				break	
		return m.group(1).string	
	
	#pattern1	"... is a ..."
	for m in search("be {NP}", s):
		print "pattern 1:"
		for nogo in ('thing', 'things'):
			if nogo in m.group(1):
				break	
		return m.group(1).string
		
	#pattern4	just the first noun that he encounters
	for m in search("{NP}", s):
		print "pattern 4:"
		return m.group(1).string	
	
	print "pattern 0"
	return None
		
def ht_to_descriptor(ht):
	print '#'+ht
	sentence = get_ht_description(ht)
	if sentence:
		return get_obj(sentence)
	return None		
		
for ht in ('dwts', 'globalwarming', 'photography', 'socialgood', 'cause', 'volunteer', 'drought'):
	print
	print ht_to_descriptor(ht)
	
	
	
	
