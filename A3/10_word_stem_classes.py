import os
# import os.path
import csv
from bs4 import BeautifulSoup
import nltk
import argparse
import krovetzstemmer
import math
import random

chosen_words = [ "academician" ,"university", "mind", "synonym", "monitor", "owe", "top" ,"charge" ,"hit" ,"diverge"]
def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

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
	# before_dice.append((stem,a,b))
	coef = float(len_f_ab)/(len_f_a+len_f_b)
	if coef > coef_thres:
		return True
	return False

def mim(a,b):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	coef = float(len_f_ab)/(len_f_a*len_f_b)
	if coef > coef_thres:
		return True
	return False

def emim(a,b,N):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	if len_f_ab == 0:
		return False
	coef = len_f_ab*math.log(N*(float(len_f_ab)/(len_f_a*len_f_b)))
	if coef > coef_thres:
		return True
	return False

def chi_sqr(a,b,N):
	f_a = index[a]
	len_f_a = len(f_a)
	f_b = index[b]
	len_f_b = len(f_b)
	f_ab = set(index[a]) & set (index[b])
	len_f_ab = len(f_ab)
	coef = len_f_ab-1/float(N)*len_f_a*len_f_b
	coef = coef*coef/(len_f_a*len_f_b)
	if coef > coef_thres:
		return True
	return False	

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
		# if count == 1000:
			# continue;
		stem = krovetz.stem(word)
		if stem not in stem_words:
			stem_words[stem] = []
		stem_words[stem].append(word)
		# count+=1 
# print chosen_words
coef_thres = 0.01
dice_index = {}
mim_index = {}
emim_index = {}
chi_sqr_index = {}
for stem in sorted(stem_words):
	bigrams = nltk.bigrams(stem_words[stem])
	for a,b in bigrams:
		if dice(a,b):
			if stem not in dice_index:
				dice_index[stem] = set()
			dice_index[stem].add(a)
			dice_index[stem].add(b)
		if mim(a,b):
			if stem not in mim_index:
				mim_index[stem] = set()
			mim_index[stem].add(a)
			mim_index[stem].add(b)
		if emim(a,b,len(html_files)):
			if stem not in emim_index:
				emim_index[stem] = set()
			emim_index[stem].add(a)
			emim_index[stem].add(b)
		if  chi_sqr(a,b,len(html_files)):
			if stem not in chi_sqr_index:
				chi_sqr_index[stem] = set()
			chi_sqr_index[stem].add(a)
			chi_sqr_index[stem].add(b)
# print "N = ",len(html_files)
print "===================== Dice  ==============================="
printIndex(dice_index)
print "=====================  MIM  ==============================="
printIndex(mim_index)
print "===================== EMIM  ==============================="
printIndex(emim_index)
print "===================== CHI_SQR ==============================="
printIndex(chi_sqr_index)
