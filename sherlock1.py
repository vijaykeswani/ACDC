import MySQLdb
with open(".variables") as f:
        content=f.readlines()
password=content[0][:-1]
tags=[]
wordtags={}
bigrams={}
unigrams={}
viterbi_list={}
root="treebank/raw/wsj_"
number="0004"
base_prob=1000000000000000000000

def dbconnect():
	global tags, wordtags,bigrams,unigrams
	db = MySQLdb.connect("localhost","root",password,"ACDC" )
	cursor = db.cursor()
	sql="select tag from tag_count"
	cursor.execute(sql)
	results = cursor.fetchall()
	for value in results:
	                        tags.append(value[0])
	sql="select * from wordtag_estimate"
	cursor.execute(sql)
	results = cursor.fetchall()
	for value in results:
	                        temp=value[0]+"~"+value[1]
	                        wordtags[temp]=value[2]
	sql="select * from bigram_estimate"
	cursor.execute(sql)
	results = cursor.fetchall()
	for value in results:
	                        temp=value[0]+"~"+value[1]
	                        bigrams[temp]=value[2]
	sql="select * from unigram_estimate"
	cursor.execute(sql)
	results = cursor.fetchall()
	for value in results:
	                        temp=value[0]
	                        unigrams[temp]=value[1]

def max2(a,b):
	if(a>b): return a
	return b

def isnumber(string):
	try:
		float(string)
		return 1
	except ValueError:
		return 0

def append_to_words(word):
				global words
 
                                if(len(word)>1 and (word[-1]=='\n' or word[-1]=='.' or word[-1]==',' or word[-1]==';' or word[-1]=="%")):
					append_to_words(word[:-1])
					append_to_words(word[-1])

                                elif(len(word)>0):
					if(word[0]=="$"):
						words.append("$")
						if(len(word)>1): append_to_words(word[1:])
					else:	words.append(word)


def bigram_prob(bia):
	if bia in bigrams.keys():	return bigrams[bia]
	return 0

def unigram_prob(unigram):
	if unigram in unigrams.keys():	return unigrams[unigram]
	return 0

def wordtag_prob_if_present(word_tag):
	if word_tag in wordtags.keys():
		return wordtags[word_tag]

def wordtag_prob(word,tag):

		e=0

                word_tag=word+"~"+tag
		e=max2(e,wordtag_prob_if_present(word_tag))

                word_tag=word+"."+"~"+tag
		e=max2(e,wordtag_prob_if_present(word_tag))

		if(len(word)>1):
			if(word[-1]=="'" or word[-1]=='"'):
				word_tag=word[:-1]+"~"+tag
				e=max2(e,wordtag_prob_if_present(word_tag))
			if(word[0]=='"'):
				word_tag=word[1:]+"~"+tag
				e=max2(e,wordtag_prob_if_present(word_tag))

		if(len(word)>2):
			if(word[-2]=="'"):
                        	word_tag=word[:-2]+"~"+tag
				e=max2(e,wordtag_prob_if_present(word_tag))
		return e


def init_viterbi():
	for i in range(0,len(words)):
		for tag in tags:
			key=str(i)+tag
			viterbi_list[key]=-1
		viterbi_list[str(i)+'.']=-1


def viterbi(n,tag):
	global vbilist
	if n==-1: return base_prob
	
	viterbi_list_key=str(n)+tag
	if (viterbi_list[viterbi_list_key]!=-1):
		return viterbi_list[viterbi_list_key]

	mymax=0.0
	

	for tag_iterator in tags:
		recursion_parameter=viterbi(n-1,tag_iterator)

		q1=bigram_prob(tag_iterator+"~"+tag)
		q2=unigram_prob(tag)
		tuned_prob=(0.5*q1)+(0.5*q2)
		if(tag=="CD"):
			if(isnumber(words[n])): tuned_prob=1

		emission_parameter=wordtag_prob(words[n],tag)

		mymax=max2(mymax,recursion_parameter * tuned_prob * emission_parameter)

	viterbi_list[viterbi_list_key]=mymax
	return mymax


dbconnect()

filename=root+number;
with open(filename) as f:
	content=f.readlines()
words=[]
counter=0
for lines in content:
	
	if(lines!='\n' and lines!=".START \n"):
		counter+=1
		line=lines[:-1]
		for word1 in line.split('/'):
			for word in word1.split(' '):
				append_to_words(word)

		init_viterbi()
		res=viterbi(len(words)-1,".")

		if(res>0): print str(counter).ljust(5)+"\tdone! \t["+str(res)+"]"
		else: print "[ERROR] "+line
		#raw_input()
		del words[:]
