import random as ra
import networkx as nx

#def randomwalk(G):

G=nx.DiGraph()

nodes=[]

for i in range(1,101):
	nodes.append(i)

for i in range (1,2476):
	G.add_edge(ra.choice(nodes),ra.choice(nodes))

count={}
for item in nodes:
	count[item]=0

rnode=ra.choice(nodes)

for i in range(0,100000):
	nebor=[]
	nebor=list(G.neighbors(rnode))
	count[rnode]=count[rnode]+1
	if( len(nebor) == 0): #sink node 
		break;
	else:
		rnode=ra.choice(nebor)

s = {(k,count[k]) for k in sorted (count,key=count.get,reverse=True)   }
