import subprocess
import argparse
import os
from math import log
def precision(res,rel):
	i = 0
	for doc0 in rel:
		for doc1 in res:
			if doc0 in doc1:
				i +=1
	return float(i)/len(res)

def average_precision(res,rel):
	docs_found = 0
	docs_avg = 0.0
	doc_idx = 0
	for doc1 in res:
		doc_idx +=1
		for doc0 in rel:
			if doc0 in doc1:
				docs_found+=1
				docs_avg += float(docs_found)/doc_idx
	return docs_avg/docs_found

def ndcg(res,rel,p):
	idcg = 1.0
	dcg = 0.0
	for i in range(2,p+1):
		idcg += 1/log(i,2)
	for doc0 in rel:
		if res[0] in doc0:
			dcg = 1.0
	doc_idx =1
	for doc1 in res[1:]:
		doc_idx +=1
		for doc0 in rel:
			if doc0 in doc1:
				dcg += 1/log(doc_idx,2)
	return dcg/idcg
def reciprocal(res,rel):
	doc_idx = 0
	for doc1 in res:
		doc_idx +=1
		for doc0 in rel:
			if doc0 in doc1:
				return float(1)/doc_idx

parser = argparse.ArgumentParser('gmetrics')
parser.add_argument('-g','--gpath',help='Path to galago binary',required=False,default='')
parser.add_argument('-x','--idxpath',help='Path to galago index',required=False,default='index/')
parser.add_argument('-i','--inpath',help='Path to input',required=True)
parser.add_argument('-q','--qpath',help='Path to query xml file',required=False,default='cacm.query.xml')
parser.add_argument('--query',help='Query id to extract relevance about',required=True)
parser.add_argument('-r','--rpath',help='Path to the .rel relevance file of galago',required=False,default='cacm.rel')
args = parser.parse_args();
g_bin = args.gpath + 'galago'
index_path = args.idxpath
input_path = args.inpath
query_path = args.qpath
query_idx = args.query
rel_path = args.rpath

if not os.path.exists(index_path):
	p = subprocess.Popen(g_bin+" build --indexPath "+index_path +" --inputPath "+input_path , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p.wait()

if not os.path.exists(query_path):
	print "Query file not found!"
	exit()

p = subprocess.Popen(g_bin+" batch-search --index="+index_path+" "+query_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
ranking =  p.communicate()[0]
ranking_per_query = {}
top_ten_per_query = {}
lines = []
lines = ranking.split('\n')
for line in lines:
	if line == '':
		continue 
	qid ,q ,file ,seq ,rank ,g = line.split(" ")
	if int(qid) not in ranking_per_query:
		ranking_per_query[int(qid)]=[]
		top_ten_per_query[int(qid)]=[]
	ranking_per_query[int(qid)].append([file,rank])

for qid in ranking_per_query.keys(): 
	for i in range(0,10):
		top_ten_per_query[int(qid)].append(ranking_per_query[qid][i][0])

relevant_docs_per_query = {}
with open(rel_path,'r') as f:
	for line in f:
		qid ,q ,file,isrel = line.split(" ")
		# print qid,q,file,isrel
		if int(qid) not in relevant_docs_per_query :
			relevant_docs_per_query[int(qid)] = [] 
		if int(isrel) == 1:
			relevant_docs_per_query[int(qid)].append(file)

print "Top ten documents from results:"
for doc in top_ten_per_query[int(query_idx)]:
	print doc[doc.rfind(input_path):].replace(input_path,""),
print
print "Relevant documents:"
for doc in relevant_docs_per_query[int(query_idx)]:
	print doc,
print
print "Precision@10:"
print precision(top_ten_per_query[int(query_idx)][:10],relevant_docs_per_query[int(query_idx)])
print "Average Precision:"
print average_precision(top_ten_per_query[int(query_idx)],relevant_docs_per_query[int(query_idx)])
print "NDCG@5"
print ndcg(top_ten_per_query[int(query_idx)],relevant_docs_per_query[int(query_idx)],5)
print "NDCG@10"
print ndcg(top_ten_per_query[int(query_idx)],relevant_docs_per_query[int(query_idx)],10)
print "Reciprocal"
print reciprocal(top_ten_per_query[int(query_idx)],relevant_docs_per_query[int(query_idx)])
