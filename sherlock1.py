import MySQLdb
with open(".variables") as f:
        content=f.readlines()
password=content[0][:-1]
tag=[]
wordtag={}
bigram={}
unigram={}
vbilist={}
root="treebank/raw/wsj_"
number="0002"


def viterbi(words,n,u):

	vbilistkey=str(n)+u
	if (vbilist[vbilistkey]!=-1):
		return vbilist[vbilistkey]

	if n==0:
		vbilist[vbilistkey]=1000000000000000000000000000000
		return 100000000000000000000000000000
	mymax=0.0
	j=0
	for j in range(0,len(tag)):
		w=tag[j]
		temp=viterbi(words,n-1,w)
		temp1=w+"~"+u
	#	print temp1
		if temp1 in bigram.keys():
			q1=bigram[temp1]
		else:
			q1=0
	#	print u
		if u in unigram.keys():
			q2=unigram[u]
		else:
			q2=0
		q=(0.5*q1)+(0.5*q2)
	#	print q
		temp2=words[n]+"~"+u
#		print temp2
		if temp2 in wordtag.keys():
			e=wordtag[temp2]
		else:	
			e=0
	#	print e
		if(mymax<(temp*q*e)):
			mymax=temp*q*e
	#if max!=0.0:
#		print n,mymax
	vbilist[vbilistkey]=mymax
	if(mymax>0): print words[n],u
	return mymax



filename=root+number;
with open(filename) as f:
	content=f.readlines()
words=[]
words2=[]
for line in content:
	for b in line.split(' '):
     		for word in b.split('\n'):
             		words.append(word)
			if (len(word)>1 and (word[len(word)-1]=='\n' or word[len(word)-1]=='.' or word[len(word)-1]==',' or word[len(word)-1]==';')):
        		        words2.append(word[:-1])
                		words2.append(word[len(word)-1])
		        elif len(word)>0:
	        	        words2.append(word)


#print words
#for word in words1:
	#	print word[len(word)-1]
#	if len(word)>1:
#		if (word[len(word)-1]=='.' or word[len(word)-1]==',' or word[len(word)-1]==';') :
#			words2.append(word[:-1])
#			j=j+1
#			char=word[len(word)-1]
			#print words[j], char
#			words2.append(char)
#			j=j+1
#		else:
#			words2.append(word)
	#if word=="\n":
	#	del words[j]
#			j=j+1
#	else:
#		words.append(word)
#		j=j+1
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
#	print temp
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

print tag
for i in range(0,len(words2)):
        for j in range(0,len(tag)):
                key=str(i)+tag[j]
                vbilist[key]=-1
	vbilist[str(i)+'.']=-1

mymax=0
n=len(words2)
#print words2
#for u in tag:
res=viterbi(words2,n-1,".")
#if max<res:
#	max=res
print res
	
