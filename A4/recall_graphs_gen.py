import subprocess
import argparse
import os
from math import log

def recall_precision(res,rel,fp,fp2):
	recall = []
	precision = []
	rel_ret = 0.0
	i = 0
	for doc1 in res:
		i +=1
		for doc0 in rel:
			if doc0 in doc1:
				rel_ret +=1
		recall.append(rel_ret/len(rel))
		precision.append(rel_ret/i)
		fp.write(str(rel_ret/len(rel))+" "+str(rel_ret/i)+"\n") 
	points = i-2
	while points>=0:
		if precision[points+1]>precision[points]:
			precision[points] = precision[points+1]
		points-=1
	
	for k in range(0,i):
		fp2.write(str(recall[k])+" "+str(precision[k])+"\n") 

	return rel_ret/len(rel)

parser = argparse.ArgumentParser('gmetrics')
parser.add_argument('-g','--gpath',help='Path to galago binary',required=False,default='')
parser.add_argument('-x','--idxpath',help='Path to galago index',required=False,default='index/')
parser.add_argument('-i','--inpath',help='Path to input',required=True)
parser.add_argument('-q','--qpath',help='Path to query xml file',required=False,default='cacm.query.xml')
parser.add_argument('--query1',help='1st Query id to graphs',required=True)
parser.add_argument('--query2',help='2nd Query id to graphs',required=True)
parser.add_argument('-r','--rpath',help='Path to the .rel relevance file of galago',required=False,default='cacm.rel')
args = parser.parse_args();
g_bin = args.gpath + 'galago'
index_path = args.idxpath
input_path = args.inpath
query_path = args.qpath
query1_idx = args.query1
query2_idx = args.query2
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
	ranking_per_query[int(qid)].append(file)
# print ranking_per_query.keys()
for qid in ranking_per_query.keys(): 
	for i in range(0,10):
		top_ten_per_query[int(qid)].append(ranking_per_query[int(qid)][i])

relevant_docs_per_query = {}
with open(rel_path,'r') as f:
	for line in f:
		qid ,q ,file,isrel = line.split(" ")
		# print qid,q,file,isrel
		if int(qid) not in relevant_docs_per_query :
			relevant_docs_per_query[int(qid)] = [] 
		if int(isrel) == 1:
			relevant_docs_per_query[int(qid)].append(file)

with open("graph1.txt",'w+') as fp:
	with open("int_graph1.txt",'w+') as fp2:
		recall_precision(ranking_per_query[int(query1_idx)],relevant_docs_per_query[int(query1_idx)],fp,fp2)
with open("graph2.txt",'w+') as fp:
	with open("int_graph2.txt",'w+') as fp2:
		recall_precision(ranking_per_query[int(query2_idx)],relevant_docs_per_query[int(query2_idx)],fp,fp2)

int1x =[]
int1y =[]
int2x =[]
int2y =[]
int1x_final = []
int1y_final = []
int2x_final = []
int2y_final = []

points = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
with open("int_graph1.txt",'r+') as fp2:
	for line in fp2:
		x,y = line.split(" ")
		int1x.append(float(x))
		int1y.append(float(y))

with open("int_graph2.txt",'r+') as fp2:
	for line in fp2:
		x,y = line.split(" ")
		int2x.append(float(x))
		int2y.append(float(y))


# print int1x
for point in points:
	for i in range(0,len(int1x)-1):
		if int1x[i]<point and int1x[i+1]>point:
			int1x_final.append(point)
			int1y_final.append(int1y[i])
		if int2x[i]<point and int2x[i+1]>point:
			int2x_final.append(point)
			int2y_final.append(int2y[i])

	if len(int1x_final)>len(int2x_final):
		for i in range(0,len(int1x_final)-len(int2x_final)):
			int2y_final.apend(0)
	else:
		for i in range(0,len(int2x_final)-len(int1x_final)):
			int1y_final.apend(0)
print "Interpolated values for standard recall values"
for i in range(0,len(int1x_final)):
	print int1x_final[i],int1y_final[i],int2y_final[i]

with open("avg_int_graph.txt",'w+') as fp2:
	fp2.write(str(0)+" "+str((int1y[0]+int2y[0])/2)+"\n") 
	
	for i in range(0,len(int1x_final)):
		fp2.write(str(int1x_final[i])+" "+str((int1y_final[i]+int2y_final[i])/2)+"\n") 