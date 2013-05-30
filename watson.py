#!/usr/bin/env python
#-*- coding: utf-8 -*-
import MySQLdb
from collections import defaultdict
from collections import Counter
with open(".variables") as f:
        content=f.readlines()
password=content[0][:-1]
word_tag = defaultdict(list)
word_count = {}
tag_count= {}
bigram_count = {}
wordtag_estimate ={}
bigram_estimate ={}
unigram_estimate={}
for i in range(1,10):
	if(i<10):
		num="0"+str(i)
	else:
		num=str(i)
	print "treebank/tagged/wsj_00"+num+".pos"
	with open("treebank/tagged/wsj_00"+num+".pos") as f:
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
				bigram=prev+"~"+combo[1]
				if bigram_count.has_key(bigram):
                	                bigram_count[bigram]+=1
                	        else:
                	                bigram_count[bigram]=1	
				prev=combo[1]
	
val=["","",""]
db = MySQLdb.connect("localhost","root",password,"ACDC" )
cursor = db.cursor()
	
'''
#print "\nword_tag...."
for key, values in word_tag.iteritems() :
	#print key, values
	key=key.replace("'","");
	key=key.replace("\\","");
	c = Counter(values)
	for item1, item2 in c.iteritems():
		item1=item1.replace("'","")
		print item1,item2,key
		sql="INSERT INTO word_tag(word, tag, count) VALUES ('%s','%s', %d)" % (key,item1,item2)
        	cursor.execute(sql)
        	db.commit()
#print "\nword_count..."

for key, value in word_count.iteritems():
	print key, value
	key=key.replace("'","");
	key=key.replace("\\","");
	sql="INSERT INTO word_count(word, count) VALUES ('%s', %d)" % (key,value)
	cursor.execute(sql)
   	db.commit()
#print "\ntag_count..."
for key, value in tag_count.iteritems():
	print key, value
	key=key.replace("'","");
	key=key.replace("\\","");
	sql="INSERT INTO tag_count(tag, count) VALUES ('%s', %d)" % (key,value)
        cursor.execute(sql)
        db.commit()
#print "\nbigram_count..."
for key, value in bigram_count.iteritems():
        pos=key.index('~')
	key=key.replace("'","");
	key=key.replace("\\","");
	sql="INSERT INTO bigram_count(firstword,lastword, count) VALUES ('%s', '%s', %d)" % (key[:pos],key[pos+1:],value)
        cursor.execute(sql)
        db.commit()
	print key[:pos],key[pos+1:],value
 '''

for key, values in word_tag.iteritems() :
        c = Counter(values)
        for item1, item2 in c.iteritems():
                no_wordtag=float(item2)
                for key2, value2 in tag_count.iteritems():
                        if item1==key2 and value2!=0:
                                item2=no_wordtag/value2
                key1=key+"~"+item1
                wordtag_estimate[key1]=item2
for key, value in wordtag_estimate.iteritems() :
	pos=key.index('~')
	key=key.replace("'","");
        key=key.replace("\\","");
        print key,value
	sql="INSERT INTO wordtag_estimate(word,tag, count) VALUES ('%s', '%s', %f)" % (key[:pos],key[pos+1:],value)
        cursor.execute(sql)
        db.commit()
for key, value in bigram_count.iteritems():
        pos=key.index('~')
        print key[:pos],key[pos+1:],value
	c=float(value)
	for key1, value1 in tag_count.iteritems():
		if(key[pos+1:]==key1):
			value=c/value1
	bigram_estimate[key]=value
for key, value in bigram_estimate.iteritems() :
	pos=key.index('~')
        key=key.replace("'","");
        key=key.replace("\\","");
        print key,value
        sql="INSERT INTO bigram_estimate(firstword,lastword, count) VALUES ('%s', '%s', %f)" % (key[:pos],key[pos+1:],value)
        cursor.execute(sql)
        db.commit()	
total=0
for key, value in tag_count.iteritems():
	total=total+value
for key, value in tag_count.iteritems():
        c=float(value)
	value=c/total
	unigram_estimate[key]=value
for key, value in unigram_estimate.iteritems() :
        key=key.replace("'","");
        key=key.replace("\\","");
        print key,value
        sql="INSERT INTO unigram_estimate(word, count) VALUES ('%s', %f)" % (key,value)
        cursor.execute(sql)
        db.commit()
