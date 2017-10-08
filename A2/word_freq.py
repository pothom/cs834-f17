import os
import csv
from bs4 import BeautifulSoup
import nltk

# Set the path to search for html files
root_dir = 'en'

# Set the tokenizer exrpresion
tokenizer = nltk.RegexpTokenizer(r'\w+')

# Find all files we need to parse
html_files = []
for root,dirs,files in os.walk(root_dir):
	for file in files:
		if file.endswith('.html'):
			html_files.append(os.path.join(root, file))



# Get the tokens for all files
tokens_found = {}
num_words = 0
tokens_in_bigrams = {}
for file in html_files:
	with open(file) as curr_file:
		print file
		soup = BeautifulSoup(curr_file.read(),'html.parser')
		tokens=  tokenizer.tokenize(soup.get_text())
		for token in tokens:
			token = token.encode('utf-8')
			if token not in tokens_found:
				tokens_found[token] = 0
			tokens_found[token] +=1
			num_words +=1
		# Get the bigrams from the tokens
		for token in nltk.bigrams(tokens):
			token = (token[0].encode('utf-8'),token[1].encode('utf-8'))
			if token not in tokens_in_bigrams:
				tokens_in_bigrams[token] = 0
			tokens_in_bigrams[token] += 1

# Write token resutls to a file
f = open('results.csv','w+')
writer = csv.writer(f)
writer.writerow(('Rank','Frequency','Word','Probability','c'))
rank=0
for w in sorted(tokens_found,key=tokens_found.get,reverse=True):
	rank+=1
	writer.writerow( (rank ,tokens_found[w] ,w ,float(tokens_found[w])/num_words ,(float(tokens_found[w])/num_words)*rank ))

f.close()


# Write bigram resutls to a file
f = open('results_bigrams.csv','w+')
writer = csv.writer(f)
writer.writerow(('Rank','Frequency','Word','Probability','c'))
rank=0
for w in sorted(tokens_in_bigrams,key=tokens_in_bigrams.get,reverse=True):
	rank+=1
	writer.writerow( (rank,tokens_in_bigrams[w],w,float(tokens_in_bigrams[w])/num_words,(float(tokens_in_bigrams[w])/num_words)*rank ))

f.close()