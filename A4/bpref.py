import subprocess
import argparse
import os
from math import log
def recall_precision(res,rel):
	recall = []
	precision = []
	rel_ret = 0.0
	i = 0
	for doc1 in res:
		i +=1
		for doc0 in rel:
			if doc0 in doc1:
				rel_ret +=1
		if len(rel) ==0:
			recall.append(0.0)
			precision.append(0.0)
		else:
			recall.append(rel_ret/len(rel))
			precision.append(rel_ret/i)
	points = i-2
	while points>=0:
		if precision[points+1]>precision[points]:
			precision[points] = precision[points+1]
		points-=1
	return recall,precision

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

def precision(res,rel):
	i = 0
	for doc0 in rel:
		for doc1 in res:
			if doc0 in doc1:
				i +=1
	return float(i)/len(res)

def bpref1(res,rel):
	result = 0.0
	found = False
	R = len(rel)
	R_non_relevant = []
	i = 0
	for doc1 in res:
		found = False
		for doc0 in rel:
			if doc0 in doc1:
				found = True
		if not found:
			i+=1
		if i> R:
			break
		R_non_relevant.append(doc1)
	# print len(R_non_relevant)
	for doc0 in rel:
		i =0
		Ndr = R
		# print "AGAIn"
		for doc1 in R_non_relevant:
			if doc0 in doc1:
				Ndr = i
			i +=1
		result += (1.0-float(Ndr)/R)
	return 1.00/R*result

def bpref2(res,rel):
	result = 0.0
	found = False
	R = len(rel)
	R_non_relevant = []
	i = 0
	for doc1 in res:
		found = False
		for doc0 in rel:
			if doc0 in doc1:
				found = True
		if not found:
			i+=1
		if i> R:
			break
		R_non_relevant.append(doc1)
	# print len(R_non_relevant)
	p = 0.0
	q = 0.0
	for doc0 in rel:
		i =0
		found = False
		# print "AGAIn"
		for doc1 in R_non_relevant:
			if doc0 in doc1:
				found = True
				q += i
				p += R-i
			i+=1
		if not found:
			q+=R

	return float(p)/(p+q)


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
query_idx = int(args.query)
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
lines = []
lines = ranking.split('\n')
top_ten_per_query = {}

for line in lines:
	if line == '':
		continue 
	qid ,q ,file ,seq ,rank ,g = line.split(" ")
	if int(qid) not in ranking_per_query:
		ranking_per_query[int(qid)]=[]
		top_ten_per_query[int(qid)]=[]
	ranking_per_query[int(qid)].append(file)
for qid in ranking_per_query.keys(): 
	for i in range(0,10):
		top_ten_per_query[int(qid)].append(ranking_per_query[qid][i])
relevant_docs_per_query = {}
for i in range(1,63):
	relevant_docs_per_query[i]=[]
with open(rel_path,'r') as f:
	for line in f:
		qid ,q ,file,isrel = line.split(" ")
		# print qid,q,file,isrel
		if int(qid) not in relevant_docs_per_query :
			relevant_docs_per_query[int(qid)] = [] 
		if int(isrel) == 1:
			relevant_docs_per_query[int(qid)].append(file)

bp1=bpref1(ranking_per_query[query_idx],relevant_docs_per_query[query_idx])
bp2=bpref2(ranking_per_query[query_idx],relevant_docs_per_query[query_idx])
print "BPREF1"
print bp1
print "BPREF2"
print bp2
