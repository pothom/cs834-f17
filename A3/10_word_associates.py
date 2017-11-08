import os
import csv
from bs4 import BeautifulSoup
import nltk
import argparse
import krovetzstemmer
import math

chosen_words = [ "instrument" ,"university", "book", "America", "fish", "dinosaur", "car" ,"food" ,"hit" ,"soccer"]

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def sortByValue(tup):
	return tup[1]

def insertAssociate(a,b,metric,coef):
	if a not in associates[metric]:
		associates[metric][a] = []
	associates[metric][a].append([b,coef])

def printIndex(index):
	for stem in chosen_words:
		print stem +": {",
		if( stem in index): 
			for word in index[stem]:
				print word,
			print "}"
		else:
			print "}"

def dice(a,b):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	coef = float(len_f_ab)/(len_f_a+len_f_b)
	insertAssociate(a,b,'dice',coef)
	
def mim(a,b):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	coef = float(len_f_ab)/(len_f_a*len_f_b)
	insertAssociate(a,b,'mim',coef)

def emim(a,b,N):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	if len_f_ab == 0:
		coef = 0.0
		insertAssociate(a,b,'emim',coef)
		return
	coef = len_f_ab*math.log(N*(float(len_f_ab)/(len_f_a*len_f_b)))
	insertAssociate(a,b,'emim',coef)

def chi_sqr(a,b,N):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	coef = len_f_ab-1/float(N)*len_f_a*len_f_b
	coef = coef*coef/(len_f_a*len_f_b)
	insertAssociate(a,b,'chi',coef)

tokenizer = nltk.RegexpTokenizer(r'\w+')

parser = argparse.ArgumentParser('invindex')
group = parser.add_mutually_exclusive_group(required= True)
group.add_argument('-l','--list', nargs='+', help='List of documents to parese', required=False)
group.add_argument('-p','--path', help='Path to directory to parse all of its files', required=False)
args = parser.parse_args();

html_files = []
if(args.path):
	root_dir = args.path
	for root,dirs,files in os.walk(root_dir):
		for file in files:
			if file.endswith('.html'):
				html_files.append(os.path.join(root, file))
else:
	html_files = [x for x in args.list if x.endswith('.html')]
	
inv_index = {}

if not os.path.exists("./inv_file.csv"):

	for file in html_files:
		print 'Indexing file: '+file
		with open(file) as f:
			soup = BeautifulSoup(f.read(),'html.parser')
			tokens=  tokenizer.tokenize(soup.get_text())
			for token in tokens:
				token = token.encode("utf-8")
				if token not in inv_index:
					inv_index[token] = set()
				inv_index[token].add(os.path.split(file)[1])

	outfile = open("inv_file.csv","w")
	for token in sorted(inv_index.iterkeys()):
		if  hasNumbers(token) or token.isupper():
			continue;
		outfile.write(token+",")
		i=0
		outfile.write('"')
		for file in inv_index[token]:
			i+=1
			outfile.write(file)
			if(i != len(inv_index[token])):
				outfile.write(",")
		outfile.write('"\n')

krovetz = krovetzstemmer.Stemmer()

stem_words = {}
index = {}
count = 0;
with open('inv_file.csv') as csvfile:
	for c in csvfile:
		word,files = c.split(",",1)
		files = files.replace("\"","")
		files = files.strip()
		index[word] = files.split(",")

words = index.keys()

associates = {}
associates['dice'] 	= {}
associates['mim'] 	= {}
associates['emim']	= {}
associates['chi']	= {}


for choice in chosen_words:
	for word in words:
		if word != choice:
			dice(choice,word)
			mim(choice,word)
			emim(choice,word,len(html_files))
			chi_sqr(choice,word,len(html_files))

per_word_associates = {}
out = open("associates","w")
for choice in chosen_words:
	per_word_associates[choice] = {}
	per_word_associates[choice]['dice'] = []
	per_word_associates[choice]['mim']  = []
	per_word_associates[choice]['emim'] = []
	per_word_associates[choice]['chi']  = []
	per_word_associates[choice]['dice'] = sorted(associates['dice'][choice],key=sortByValue,reverse=True)[:10] 
	per_word_associates[choice]['mim'] = sorted(associates['mim'][choice],key=sortByValue,reverse=True)[:10]
	per_word_associates[choice]['emim'] = sorted(associates['emim'][choice],key=sortByValue,reverse=True)[:10]
	per_word_associates[choice]['chi'] = sorted(associates['chi'][choice],key=sortByValue,reverse=True)[:10]
	out.write(choice+"\n")
	out.write("Dice,MIM,EMIM,Chi\n")
	for i in range(0,10): 
		out.write(per_word_associates[choice]['dice'][i][0]+","+per_word_associates[choice]['mim'][i][0]+","+per_word_associates[choice]['emim'][i][0]+","+per_word_associates[choice]['chi'][i][0]+"\n")