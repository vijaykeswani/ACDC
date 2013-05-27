#!/usr/bin/env python
#-*- coding: utf-8 -*-

from collections import defaultdict
from collections import Counter

word_tag = defaultdict(list)
word_count = {}
tag_count= {}
bigram_count = {}
with open("treebank/tagged/wsj_0001.pos") as f:
	content=f.readlines()
prev="*"
for line in content:
	words=line.split()
	for word in words:
		if "/" in word:
			combo=word.split("/")
			#if combo[0][0] in xrange(ord('a'), ord('z')+1):
			word_tag[combo[0]].append(combo[1])
			if word_count.has_key(combo[0]):
				word_count[combo[0]]+=1
			else:
				 word_count[combo[0]]=1
			#tag_count[combo[1]]+=1
                        if tag_count.has_key(combo[1]):
                                tag_count[combo[1]]+=1
                        else: 
                                tag_count[combo[1]]=1
			bigram=prev+"~"+combo[0]
			if bigram_count.has_key(bigram):
                                bigram_count[bigram]+=1
                        else:
                                bigram_count[bigram]=1	
			prev=combo[0]
print "\nword_tag...."
for key, values in word_tag.iteritems() :
	#print key, values
	c = Counter(values)
	print key, c.items()
print "\nword_count..."
for key, value in word_count.iteritems():
	print key, value
print "\ntag_count..."
for key, value in tag_count.iteritems():
	print key, value
print "\nbigram_count..."
for key, value in bigram_count.iteritems():
        pos=key.index('~')
	print key[:pos],key[pos+1:],value
 
