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
for i in range(1,99):
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
				bigram=prev+"~"+combo[0]
				if bigram_count.has_key(bigram):
                	                bigram_count[bigram]+=1
                	        else:
                	                bigram_count[bigram]=1	
				prev=combo[0]
	
val=["","",""]
db = MySQLdb.connect("localhost","root",password,"ACDC" )
cursor = db.cursor()
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
	sql="INSERT INTO word_count(word, count) VALUES ('''%s''', %d)" % (key,value)
	cursor.execute(sql)
   	db.commit()
#print "\ntag_count..."
for key, value in tag_count.iteritems():
	print key, value
	key=key.replace("'","");
	key=key.replace("\\","");
	sql="INSERT INTO tag_count(tag, count) VALUES ('''%s''', %d)" % (key,value)
        cursor.execute(sql)
        db.commit()
#print "\nbigram_count..."
for key, value in bigram_count.iteritems():
        pos=key.index('~')
	key=key.replace("'","");
	key=key.replace("\\","");
	sql="INSERT INTO bigram_count(firstword,lastword, count) VALUES ('''%s''', '''%s''', %d)" % (key[:pos],key[pos+1:],value)
        cursor.execute(sql)
        db.commit()
	print key[:pos],key[pos+1:],value
 
