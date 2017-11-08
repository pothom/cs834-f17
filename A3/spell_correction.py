import re
import sys
from collections import Counter

text = open('big.txt').read()
words = re.findall(r'\w+',text.lower())
word_freq = Counter(words)
num_words =0

if len(sys.argv) !=2:
	print 'Please input word to correct'
	exit()

input_word = sys.argv[1].lower() 


for counter in word_freq.values():
	num_words += counter

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def propability(word):
	return float(word_freq[word])/num_words


correct_words = set()

for x in edits1(input_word) or edits2(input_word):
	if x in word_freq:
		correct_words.add(x)

max_ = 0
corrected_word = input_word
for p in correct_words:
	if word_freq[p]>max_:
		max_ = word_freq[p]
		corrected_word = p
print corrected_word