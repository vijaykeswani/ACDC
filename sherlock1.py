import MySQLdb
with open(".variables") as f:
        content=f.readlines()
password=content[0][:-1]
tag=[]
wordtag={}
bigram={}
unigram={}
def viterbi(words,n,u):
	if n==0:
		print "*"
		return 1
	max=0.0
	j=0
	for j in range(0,2):
		w=tag[j]
		temp=viterbi(words,n-1,w)
		#print temp
		temp1=w+"~"+u
		print temp1
		if temp1 in bigram:
			q1=bigram[temp1]
		else:
			q1=0
		print u
		if u in unigram:
			q2=unigram[u]
		else:
			q2=0
		q=0.5*q1+0.5*q2
		temp2=words[n]+"~"+u
		print temp2
		if temp2 in wordtag:
			e=wordtag[temp2]
		else:	
			e=0
		if(max<(temp*q*e)):
			max=temp*q*e
	#if max!=0.0:
	#	print max
	return max


with open("treebank/raw/wsj_0001") as f:
	content=f.readlines()
words=[]
for line in content:
	for b in line.split(' '):
     		for d in b.split('\n'):
             		words.append(d)
j=0
words1=[]
for word in words:
	if len(word)>0 and word[len(word)-1]=='\n':
		words1.append(word[:-1])
	else:
		words1.append(word)
	j=j+1		
j=0
words2=[]
for word in words1:
	#	print word[len(word)-1]
	if len(word)>1:
		if (word[len(word)-1]=='.' or word[len(word)-1]==',' or word[len(word)-1]==';') :
			words2.append(word[:-1])
			j=j+1
			char=word[len(word)-1]
			#print words[j], char
			words2.append(char)
			j=j+1
		else:
			words2.append(word)
	#if word=="\n":
	#	del words[j]
			j=j+1
	else:
		words.append(word)
		j=j+1
#for word in words2:
#	print word
db = MySQLdb.connect("localhost","root",password,"ACDC" )
cursor = db.cursor()
sql="select tag from tag_count"
cursor.execute(sql)
results = cursor.fetchall()
for value in results:
	tag.append(value[0])
sql="select * from wordtag_estimate"
cursor.execute(sql)
results = cursor.fetchall()
for value in results:
	temp=value[0]+"~"+value[1]
	wordtag[temp]=value[2]	
sql="select * from bigram_estimate"
cursor.execute(sql)
results = cursor.fetchall()
for value in results:
        temp=value[0]+"~"+value[1]
        bigram[temp]=value[2]
sql="select * from unigram_estimate"
cursor.execute(sql)
results = cursor.fetchall()
for value in results:
        temp=value[0]
        unigram[temp]=value[1]
'''
for value in tag:
	print value
for key, value in wordtag.iteritems():
	print key,value
for key, value in bigram.iteritems():
        print key,value
for key, value in unigram.iteritems():
        print key,value
'''
max=0
n=len(words2)
print n
#for u in tag:
res=viterbi(words2,n-1,".")
print res
#if max<res:
#	max=res
#print max
	
