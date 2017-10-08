import os
import csv
from bs4 import BeautifulSoup
import nltk
import argparse

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


for file in html_files:
	with open(file) as f:
		soup = BeautifulSoup(f.read(),'html.parser')
		tokens=  tokenizer.tokenize(soup.get_text())
		for token in tokens:
			token = token.encode("utf-8")
			if token not in inv_index:
				inv_index[token] = set()
			inv_index[token].add(os.path.split(file)[1])
	# break;

outfile = open("inv_file.csv","w")
for token in inv_index:
	outfile.write(token+",")
	i=0
	outfile.write('"')
	for file in inv_index[token]:
		i+=1
		outfile.write(file)
		if(i != len(inv_index[token])):
			outfile.write(",")
	outfile.write('"\n')
