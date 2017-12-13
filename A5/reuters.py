from nltk.corpus import reuters
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

cachedStopWords = stopwords.words("english")

def tf_idf(docs):
    tfidf = TfidfVectorizer(tokenizer=tokenize,min_df=1, vocabulary=total_words,
                        use_idf=True, sublinear_tf=True, max_df=0.98,
                        norm='l2')
    return tfidf.fit(docs)

def feature_values(doc, representer):
    doc_representation = representer.transform([doc])
    features = representer.get_feature_names()
    return [(features[index], doc_representation[0, index])
                 for index in doc_representation.nonzero()[1]]

def tokenize(text):
    min_length = 3
    words = map(lambda word: word.lower(), word_tokenize(text));
    words = [word for word in words
                  if word not in cachedStopWords]
    tokens =(list(map(lambda token: PorterStemmer().stem(token),
                  words)));
    p = re.compile('[a-zA-Z]+');
    filtered_tokens =list(filter(lambda token:p.match(token) and len(token)>=min_length,
         tokens));
    return filtered_tokens

documentIDs= reuters.fileids()

print documentIDs[0]
word = 'Oil'
pos_list = []
neg_list = []
total_words = set()
for doc in documentIDs:
	words = reuters.words(doc)
	total_words = total_words.union(set(words))
	if word in words:
		pos_list.append(doc)
	else:
		neg_list.append(doc)
word_map = {}
idx = 1
for word in total_words:
	word_map[word] = idx
	idx +=1

# Write the positive train cases
features = []
for doc in pos_list[:100]:
	features.append(feature_values(reuters.raw(doc),tf_idf(reuters.words(doc))))

with open('train_data.dat','w+') as f:
	for feature in features:
		f.write("+1 ")
		idx_to_value = {}
		for term,value in feature:
			idx_to_value[word_map[term]] = value
		for idx in sorted(idx_to_value):
			f.write(str(idx)+":"+str(idx_to_value[idx])+" ")
		f.write('\n')

# Write the negative train cases
features  = []
for doc in neg_list[:100]:
	features.append(feature_values(reuters.raw(doc),tf_idf(reuters.words(doc))))

with open('train_data.dat','a') as f:
	for feature in features:
		f.write("-1 ")
		idx_to_value = {}
		for term,value in feature:
			idx_to_value[word_map[term]] = value
		for idx in sorted(idx_to_value):
			f.write(str(idx)+":"+str(idx_to_value[idx])+" ")
		f.write('\n')

# Write the positive test cases
features  = []
for doc in pos_list[101:116]:
	features.append(feature_values(reuters.raw(doc),tf_idf(reuters.words(doc))))

with open('test_data.dat','w+') as f:
	for feature in features:
		f.write("+1 ")
		idx_to_value = {}
		for term,value in feature:
			idx_to_value[word_map[term]] = value
		for idx in sorted(idx_to_value):
			f.write(str(idx)+":"+str(idx_to_value[idx])+" ")
		f.write('\n')

# Write the negative test cases
features  = []
for doc in neg_list[101:116]:
	features.append(feature_values(reuters.raw(doc),tf_idf(reuters.words(doc))))

with open('test_data.dat','a') as f:
	for feature in features:
		f.write("-1 ")
		idx_to_value = {}
		for term,value in feature:
			idx_to_value[word_map[term]] = value
		for idx in sorted(idx_to_value):
			f.write(str(idx)+":"+str(idx_to_value[idx])+" ")
		f.write('\n')
