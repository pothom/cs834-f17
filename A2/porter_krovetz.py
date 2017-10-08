import io
import sys
import os
from bs4 import BeautifulSoup
import nltk
from nltk.stem import *
import krovetzstemmer

tokenizer = nltk.RegexpTokenizer(r'\w+')
porterizer = PorterStemmer()
krovetzizer = krovetzstemmer.Stemmer()

print('~~~~~~~~~~~~~~~~~~~~~~~Starting~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
if len(sys.argv)< 6:
	print('Please provide 5 files to process')
	print('porter_krovetz <file1> <file2> <file3> <file4> <file5>')
	exit()

files = []
for arg in sys.argv[1:]:
	files.append(arg)

porter_stems = []
krovetz_stems = []
header = ('No','File','Porter stems #','Krovetz stems #')
results = []
i=0
print header
for file in files:
	i+=1
	with open(file) as curr_file:
		# print file
		soup = BeautifulSoup(curr_file.read(),'html.parser')
		tokens=  tokenizer.tokenize(soup.get_text())
		porter = []

		f = open(os.path.split(file)[1],'w')
		p = open(os.path.split(file)[1]+'.porter','w')
		k = open(os.path.split(file)[1]+'.krovetz','w')
		words = 0;
		for token in tokens:
			if(token.isalnum()):
				words+=1
				f.write(token.lower().encode('utf-8')+' ')
				porter_stems.append(porterizer.stem(token))
				krovetz_stems.append(krovetzizer.stem(token))
				p.write(porterizer.stem(token).encode('utf-8')+' ')
				k.write(krovetzizer.stem(token).encode('utf-8')+' ')
				if(words%15 == 0):
					f.write('\n')
					p.write('\n')
					k.write('\n')
	results.append((i,os.path.split(file)[1],len(set(porter_stems)),len(set(krovetz_stems))))
	
	print results[i-1]
