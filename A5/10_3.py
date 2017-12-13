def converged(I,R):
	threshold = 0.01
	for p in I:
		if I[p]-R[p]>threshold or I[p]-R[p]<-threshold :
			return False
	return True


def PageRank(G):
	l = 0.12
	nodes_size = len(G.get_nodes())
	I = {}
	R = {}
	for p in G.get_nodes():
		I[p] = float(1)/nodes_size
		R[p] = 0
	iters = 0
	while(1):
		iters +=1
		for r in R:
			R[r] = l/nodes_size
		for p in sorted(G.get_nodes()):
			Q = G.get_adj_nodes(p)
			if len(Q)>0:
				for q in Q:
					R[q] = R[q] + (1-l)*float(I[p])/len(Q)
			else :
				for q in G.get_nodes():
					R[q] = R[q] + (1-l)*float(I[p])/nodes_size
		
		if(converged(I,R)):
			break
		for p in R:
			I[p]=R[p]
		with open('PR_graph_iter_'+str(iters)+'.dot','w') as f:
			f.write("digraph g {\n")
			f.write("graph [nodesep=1];\n")
			for v in R:
				f.write(v+" [xlabel=\"("+str.format('{:.2f}',R[v])+")\"]\n")
			f.write(str(g))
			f.write("}\n")

	with open('PR_graph_iter_'+str(iters)+'.dot','w') as f:
			f.write("digraph g {\n")
			f.write("graph [nodesep=1];\n")
			for v in R:
				f.write(v+" [xlabel=\"("+str.format('{:.2f}',R[v])+")\"]\n")
			f.write(str(g))
			f.write("}\n")
	print str(iters)
	return R

def HITS(G,K):
	A = []
	H = []
	A.append(dict())
	H.append(dict())
	for p in G.get_nodes():
		A[0][p] = 1
		H[0][p] = 1
	for i in range(1,K+1):
		A.append(dict())
		H.append(dict())
		for p in G.get_nodes():
			A[i][p] = 0
			H[i][p] = 0
		Z_A = 0
		Z_H = 0
		for p in G.get_nodes():
			for q in G.get_nodes():
				if G.edge_exists(p,q):
					H[i][p]+= A[i-1][q]
					Z_H = Z_H + A[i-1][q]
				if G.edge_exists(q,p):
					A[i][p] += H[i-1][q]
					Z_A = Z_A + H[i-1][q]
		for p in G.get_nodes():
			A[i][p] = float(A[i][p])/Z_A
			H[i][p] = float(H[i][p])/Z_H
	return A[K],H[K]

class node:

	def __init__(self,name):
		self.adjacent_nodes = []
		self.name = name

	def add_adj_node(self,n):
		if n not in self.adjacent_nodes and n != self:
			self.adjacent_nodes.append(n)

	def __str__(self):
		return self.name

	def get_adj_nodes(self):
		return self.adjacent_nodes

	def is_connected(self,n):
		if n in self.adjacent_nodes:
			return True
		else:
			return False

	def __eq__(self,other):
		if isinstance(other,node):
			return self.name == other.name
		return False

	def __ne__(self,other):
		if isinstance(other,node):
			return self.name != other.name
		return True

class Graph:

	def __init__(self):
		self.g_nodes = {}

	def add_node(self,n):
		if str(n) not in self.g_nodes:
			self.g_nodes[str(n)] = n

	def get_nodes(self):
		return self.g_nodes

	def get_adj_nodes(self,n):
		adj = self.g_nodes[n].get_adj_nodes()
		names = []
		for a in adj:
			names.append(str(a))
		return names

	def add_edge(self,v1,v2):
		if v1 not in self.g_nodes or v2 not in self.g_nodes:
			return 
		self.g_nodes[v1].add_adj_node(self.g_nodes[v2])

	def edge_exists(self,v1,v2):
		if self.g_nodes[v1].is_connected(self.g_nodes[v2]):
			return True
		else:
			return False

	def __str__(self):
		graph_str =""
		for n in sorted(self.g_nodes):
			for adj in self.g_nodes[n].get_adj_nodes():
				graph_str += n +"-> "+str(adj)+";\n"
			if len(self.g_nodes[n].get_adj_nodes()) ==0:
				graph_str += n +";\n"

		return graph_str

g = Graph()
g.add_node(node('a'))
g.add_node(node('b'))
g.add_node(node('c'))
g.add_node(node('d'))
g.add_node(node('e'))
g.add_node(node('f'))
g.add_node(node('g'))
g.add_edge('a','b')
g.add_edge('c','a')
g.add_edge('c','b')
g.add_edge('c','d')
g.add_edge('e','d')
g.add_edge('f','d')

with open('initial_graph.dot','w') as f:
	f.write("digraph g {\n")
	f.write("graph [nodesep=1];\n")
	f.write(str(g))
	f.write("}\n")


for k in range(1,6):
	A,H = HITS(g,k)
	with open('HITS_graph_iter_'+str(k)+'.dot','w') as f:
		f.write("digraph g {\n")
		f.write("graph [nodesep=1];\n")

		for v in A:
			f.write(v+" [xlabel=\"("+str.format('{:.2f}',A[v])+","+str.format('{:.2f}',H[v])+")\"]\n")
		f.write(str(g))
		f.write("}\n")

PageRank(g)



