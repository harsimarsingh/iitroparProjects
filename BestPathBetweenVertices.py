'''
By - Harsimar Singh
Roll- 2018CSM1010
Editor - Sublime Text
Compiled and Run - Command Prompt (using python)

'''
import networkx as nx 
import matplotlib.pyplot as plt 	

#dfs function that will initialize a visited array for dfs
def dfs(G,s,d):
	visited=[]
	visited=[0 for i in range(1,20)]
	dfsutil(G,s,d,visited)

#original function that does all te fuctions
def dfsutil(G,s,d,visited):
	visited[s]=1
#print the source each time when a new source vertex is visited	
	print(s)
#if there is edge print the destination	and return 
	if(G.has_edge(s,d) ):
		print (d)
		return 
	else:
#sort the neighbours of the source according to edge weights which will ensure our greedy approach 
#since there can be loops of maximum edge weights, dfs will avoid looping and will choose the path greedily to the destination vertex		
		sortneighbor=sorted(G[s].items(), key=lambda edge: edge[1]['weight'],reverse=True)
		for items in sortneighbor:
			if visited[items[0]]==0 :
#running the dfs on all the neighbouring nodes which are sorted in the order of decreasing weights			
				dfsutil(G,items[0],d,visited)
				return
G=nx.Graph()
#list of list of 12-tupple array
dl=[]
with open("subj.txt") as f:
	for line in f:
		inner=[ int(elt.strip()) for elt in line.split(' ') ]
		dl.append(inner)
for list1 in range(len(dl)):
	for list2 in range(list1+1,len(dl)):
		weight=0
		for i in range(len(dl[0])):
#assigning weights according to the number of 1's that match on same index
			if ( dl[list1][i] == dl[list2][i] and dl[list2][i] == 1 and dl[list1][i] ==1 ):
				weight=weight+1
		if(weight):
			G.add_edge(dl[list1][0],dl[list2][0],weight=weight)

#print(G.edges(data=True)) -> uncommment  to check the correctness of the algorithm
#the loop will check for every combination of two nodes
for i in G.nodes():	
	for j in range(len(G.nodes())-1):
#since there is no node with index 0, so tweaked j with j+1		
#if source and destination is same, skip this iteration else resume for all iterations
		if(i==j+1):
			continue
		print("path between nodes",i ,j+1 ,"is")
		dfs(G,i,j+1)
#plotting the graph
nx.draw(G,with_labels=True)
plt.show()