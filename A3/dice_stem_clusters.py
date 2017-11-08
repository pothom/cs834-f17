import os
# import os.path
import csv
from bs4 import BeautifulSoup
import nltk
import argparse
import krovetzstemmer

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

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
		if count == 1000:
			continue;
		stem = krovetz.stem(word)
		if stem not in stem_words:
			stem_words[stem] = []
		stem_words[stem].append(word)
		count+=1

coef_thres = 0.001
before_dice = []
after_dice = {}
for stem in sorted(stem_words):
	bigrams = nltk.bigrams(stem_words[stem])
	for a,b in bigrams:
		f_a = index[a]
		len_f_a = len(f_a)
		f_b = index[b]
		len_f_b = len(f_b)
		f_ab = set(index[a]) & set (index[b])
		len_f_ab = len(f_ab)
		before_dice.append((stem,a,b))
		coef = float(2*len_f_ab)/(len_f_a+len_f_b)
		if coef > coef_thres:
			if stem not in after_dice:
				after_dice[stem] = set()
			after_dice[stem].add(a)
			after_dice[stem].add(b)


for stem in after_dice:
	print stem +": {", 
	for word in after_dice[stem]:
		print word,
	print "}"
