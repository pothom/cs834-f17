import os
import csv
from bs4 import BeautifulSoup
import nltk
import argparse


parser = argparse.ArgumentParser('vocgrowth')
parser.add_argument('--reverse','-r',help='Visit files in reverse order',default=False,type=bool)
args = parser.parse_args();
reverse = args.reverse
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

if reverse:
	html_files.reverse()
# Get the tokens for all files
tokens_found = []
voc_growth = []
i = 0;
for file in html_files:
	i+=1
	with open(file) as curr_file:
		print file
		soup = BeautifulSoup(curr_file.read(),'html.parser')
		tokens=  tokenizer.tokenize(soup.get_text())
		for token in tokens:
			token = token.encode('utf-8')
			tokens_found.append(token)
		voc_growth.append([i ,len(tokens_found),len(set(tokens_found))])

# Write token resutls to a file
if reverse:
	f = open('voc_growth_reverse.csv','w+')
else:
	f = open('voc_growth.csv','w+')
writer = csv.writer(f)
writer.writerow(('Files','Words','Vocabulary_size'))
for v in voc_growth:
	writer.writerow( (v[0],v[1],v[2]))

f.close()

