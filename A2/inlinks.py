import os
import csv
import operator
from bs4 import BeautifulSoup
import nltk

root_dir = 'en'

# Set the tokenizer exrpresion
tokenizer = nltk.RegexpTokenizer(r'\w+')

# Find all files we need to parse
html_files = []
for root,dirs,files in os.walk(root_dir):
	for file in files:
		if file.endswith('.html'):
			html_files.append(os.path.join(root, file))
file_str = []
for file in html_files:
	file_str.append( str(file))
inlinks = {}
anchor_texts = {}

for file in html_files:
	print file
	soup = BeautifulSoup(open(file),'html.parser')
	links = soup.find_all('a')
	for link in links:
		new_link = link.get('href')
		if not new_link:
			continue
		if new_link.startswith('http'):
			continue
		new_link = new_link.replace('../','')
		new_link = new_link.encode('utf-8')
		new_link = 'en/'+new_link
		if new_link in file_str and file !=new_link:
			if new_link not in inlinks:
				inlinks[new_link] = 0
				anchor_texts[new_link] = set()
			inlinks[new_link] += 1
			anchor_texts[new_link].add(link.text)
i=0
f = open("Inlinks_count","w")
writer = csv.writer(f)
writer.writerow(('No','Document','Inlinks #','Anchor texts'))
for k,v in sorted(inlinks.items(), key=operator.itemgetter(1),reverse=True):
	i+=1
	print i,str(v), k,
	anchors = ''
	for it in anchor_texts[k]:
		anchors+=it+','
	writer.writerow((i,str(v), k,anchors))
	if(i==10):
		break;
f.close()