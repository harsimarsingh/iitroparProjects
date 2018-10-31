import networkx as nx
import matplotlib.pyplot as plt
import random
import itertools

def get_signs_of_tris(triangle_list,G):
	#triangle_list=[[1,2,3][4,5,6][7,8,9]]
	#all_signs=[[1,2->'+',2,3->'-',1,3->'-'][][]]
	all_signs=[]
	for i in range(len(triangle_list)):
		temp=[]
		temp.append(G[ triangle_list[i][0]] [triangle_list[i][1]] ['sign'] )
		temp.append(G[ triangle_list[i][1]] [triangle_list[i][2]] ['sign'] )
		temp.append(G[ triangle_list[i][0]] [triangle_list[i][2]] ['sign'] )
		all_signs.append(temp)
	return all_signs

def count_unstable(all_signs):
	stable=0
	unstable=0
	for i in range(len(all_signs)):
		if all_signs[i].count('+') == 3 or all_signs[i].count('+') == 1:
			stable +=1
		elif all_signs[i].count('+') == 2 or all_signs[i].count('+') == 0:
			unstable +=1
	print ("total trianlges =" ,stable+unstable)
	print ("total unstable trianlges =", unstable)
	print ("total stable trianlges =", stable)
	return stable,unstable
#1. create a graph with 'n' nodes where nodes are game of thrones characters

def move_to_stable(G,triangle_list,all_signs):
	found_stable = False
	while(found_stable == False):
		index=random.randint(0,len(triangle_list)-1)
		if all_signs[index].count('+') == 2 or all_signs[index].count('+') == 0:
			found_stable = True
		else:
			continue
	#move unstable triangle to stable state
	r=random.randint(1,3)
	if all_signs[index].count('+') == 2:
	 	if r == 1:
	 		if (G[triangle_list[index][0]][triangle_list[index][1]]['sign']) == '+':
	 			G[triangle_list[index][0]][triangle_list[index][1]]['sign'] = '-'
	 		elif G[triangle_list[index][0]][triangle_list[index][1]]['sign'] == '-':
	 			G[triangle_list[index][0]][triangle_list[index][1]]['sign'] = '+'
	 	elif r==2:
	 		if G[triangle_list[index][1]][triangle_list[index][2]]['sign'] =='+':
	 			G[triangle_list[index][1]][triangle_list[index][2]]['sign'] ='-'
	 		elif G[triangle_list[index][1]][triangle_list[index][2]]['sign'] =='-':
	 			G[triangle_list[index][1]][triangle_list[index][2]]['sign'] ='+'
	 	else:
	 		if G[triangle_list[index][0]][triangle_list[index][2]]['sign'] =='+':
	 			G[triangle_list[index][0]][triangle_list[index][2]]['sign'] ='-'
	 		elif G[triangle_list[index][0]][triangle_list[index][2]]['sign'] =='-':
	 			G[triangle_list[index][0]][triangle_list[index][2]]['sign'] ='+'
	elif all_signs[index].count('+') == 0:
		if r==1:
			G[triangle_list[index][0]][triangle_list[index][1]]['sign'] ='+'
		elif r==2:
			G[triangle_list[index][1]][triangle_list[index][2]]['sign'] ='+'
		elif r==3:
			G[triangle_list[index][0]][triangle_list[index][2]]['sign'] ='+'
	return G

def see_coalitions(G):
	first_coalition = []
	second_coalition =[]
	node = G.nodes()
	r = random.choice(node)
	first_coalition.append(r)
	processed_nodes=[]
	to_be_processed =[r]

	# BFS STARTS HERE
	for each in to_be_processed:

		if each not in processed_nodes:
			neigh = G.neighbors(each)
			#print (neigh)

			for i in range(len(neigh)):
				if G[each][neigh[i]]['sign']=='+':
					if neigh[i] not in first_coalition:
						first_coalition.append(neigh[i])
					if neigh[i] not in to_be_processed:
						to_be_processed.append(neigh[i])
				elif G[each][neigh[i]]['sign']=='-':
					if neigh[i] not in second_coalition:
						second_coalition.append(neigh[i])
						processed_nodes.append(neigh[i])
			processed_nodes.append(each)
	return first_coalition,second_coalition

G = nx.Graph()
n=5
G.add_nodes_from([i for i in range(1 , n+1)])
mapping = {1:'Jon',2:'Cersai',3:'Tyrion',4:'Danny',5:'Jamie',6:'Sam'}
G = nx.relabel_nodes(G , mapping) #first one is list and second param is Graph

#2. make it a complete graph by adding all the possible edges.assign +ve or -ve edge weights

signs =[ '+','-']
for i in G.nodes():
	for j in G.nodes():
		if i!=j:
			G.add_edge(i,j, sign = random.choice(signs)) #random.choice randomly chooses one value

#3.display the network

edge_labels =nx.get_edge_attributes(G,'sign')
pos = nx.circular_layout(G)
nx.draw(G , pos ,node_size=3000,with_labels=True)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=20,font_color='red')
plt.show()


#4
	#1. get all triangles

nodes = G.nodes()
tri_list = [list(x) for x in itertools.combinations(nodes,3)]

	#2. store all their details

all_signs = get_signs_of_tris(tri_list, G) #list of lists [ [] ,[] ,[]]

	#3. count number of unstable triangles

stable,unstable = count_unstable(all_signs) 	#count the number of triangles using the list and then count the number of all unstable triangles and return them

#5 while number of unstable triangles is not 0
total=stable+unstable
while(unstable !=0 ):
	#1. choose a triangle in a graph that is unstable
	#2. make that triangle stable
	#3. count that number of unstable triangles
	G = move_to_stable(G,tri_list,all_signs)
	all_signs = get_signs_of_tris(tri_list,G)
	stable,unstable = count_unstable(all_signs)

edge_labels =nx.get_edge_attributes(G,'sign')
pos = nx.circular_layout(G)
nx.draw(G , pos ,node_size=3000,with_labels=True)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=20,font_color='red')
plt.show()
#6 here no unstable triangle, partition it into two clusters
	#1. choose a random node. add it to first coalition
	#2. Also put all the 'friends' of this node in first coalition
	#3. put all the enemies of this node in the second coalition

first,second = see_coalitions(G)
print (first)
print (second)
edge_labels =nx.get_edge_attributes(G,'sign')
pos = nx.circular_layout(G)
nx.draw(G , pos ,node_size=3000,with_labels=True)
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_size=20,font_color='red')
plt.show()
