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

def r_precision(res,rel):
	i = 0
	rel_ret = 0
	for doc1 in res:
		if i == len(rel):
			break 
		for doc0 in rel:
			if doc0 in doc1:
				rel_ret +=1
		i+=1
	if len(rel) == 0:
		return 0.0
	return rel_ret/len(rel)

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
	if docs_found == 0:
		return 0.0
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

parser = argparse.ArgumentParser('gmetrics')
parser.add_argument('-g','--gpath',help='Path to galago binary',required=False,default='')
parser.add_argument('-x','--idxpath',help='Path to galago index',required=False,default='index/')
parser.add_argument('-i','--inpath',help='Path to input',required=True)
parser.add_argument('-q','--qpath',help='Path to query xml file',required=False,default='cacm.query.xml')
# parser.add_argument('--query',help='Query id to extract relevance about',required=True)
parser.add_argument('-r','--rpath',help='Path to the .rel relevance file of galago',required=False,default='cacm.rel')
args = parser.parse_args();
g_bin = args.gpath + 'galago'
index_path = args.idxpath
input_path = args.inpath
query_path = args.qpath
# query_idx = args.query
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
avg_prec = []
prec = {}
recall = {}
for i in relevant_docs_per_query.keys():
	avg_prec.append(average_precision(ranking_per_query[i],relevant_docs_per_query[i]))
	recall[i],prec[i] = recall_precision(ranking_per_query[i],relevant_docs_per_query[i])
	# print "Query "+str(i)+": Average Precision --> "+str(average_precision(ranking_per_query[i],relevant_docs_per_query[i]))

print "Mean Average Precision"
print sum(avg_prec)/len(avg_prec)
int_graph = {}
points = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
for i in ranking_per_query.keys():
	int_graph[i] = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
	for j in range(0,10):
		point = points[j]
		for x in range(1,len(recall[i])):
			if recall[i][x-1]<point and recall[i][x]>point:
				int_graph[i][j] = prec[i][x]

average_int_graph = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
with open('cacm_graph','w+') as fp:
	for j in range(0,9):
		for i in ranking_per_query.keys():
			average_int_graph[j] += int_graph[i][j]
		average_int_graph[j] = average_int_graph[j]/len(ranking_per_query.keys())
		fp.write(str(((j+1)*0.1))+" "+str(average_int_graph[j])+"\n")

avg_ndcg5 = 0.0
avg_ndcg10 = 0.0
avg_prec10 = 0.0
avg_rprec = 0.0
for i in relevant_docs_per_query.keys():
	avg_ndcg5+= ndcg(top_ten_per_query[i],relevant_docs_per_query[i],5)
	avg_ndcg10+= ndcg(top_ten_per_query[i],relevant_docs_per_query[i],10)
	avg_prec10+=precision(top_ten_per_query[i],relevant_docs_per_query[i])
	avg_rprec +=r_precision(ranking_per_query[i],relevant_docs_per_query[i])
avg_ndcg5 = avg_ndcg5/ len(relevant_docs_per_query.keys())
avg_ndcg10 = avg_ndcg10/ len(relevant_docs_per_query.keys())
avg_prec10 = avg_prec10/len(relevant_docs_per_query.keys())
avg_rprec = avg_rprec/len(relevant_docs_per_query.keys())
print "Average NDCG@5"
print avg_ndcg5
print "Average NDCG@10"
print avg_ndcg10
print "Precision@10"
print avg_prec10
print "Average R-Precision"
print avg_rprec