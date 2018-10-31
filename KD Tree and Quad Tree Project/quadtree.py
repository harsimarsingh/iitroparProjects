import math
import sys
from pathlib import Path
import os
alpha=3 			#this will be our threshhold #default is 3
xpoints=[]
ypoints=[]
dictpoints={}	 	#dictionary to map points
countleaf=0
nodestack=[]

#	Quad Tree Representation
#			N
#		nw	|   ne
#		 4	|	3
#    W--------------- E
#		 1	|   2
#		sw	|   se
#			S

class point:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	
	def __repr__(self):
		return "".join(["(",str(self.x),",",str(self.y),")"])

class Node_root:
	def __init__(self,sw,se,ne,nw,linex,liney,ymax,ymin,xmax,xmin):
		self.sw=None
		self.se=None
		self.ne=None
		self.nw=None
		self.linex=linex
		self.liney=liney
		self.ymax=ymax
		self.ymin=ymin
		self.xmax=xmax
		self.xmin=xmin

class Node_int:
	def __init__(self,sw,se,ne,nw,linex,liney,status,par):
		self.sw=None
		self.se=None
		self.ne=None
		self.nw=None
		self.linex=linex
		self.liney=liney
		self.par=par
		self.status=status

class Node_leaf:
	def __init__ (self,filename,pointlist,depth): 
		filename = str(filename)+'.txt'
		self.filename=filename
		self.pointlist=pointlist
		self.depth=depth
		with open (filename,'w') as f:
			for point in pointlist:
				for key in dictpoints:
					x=(dictpoints[key].x)
					y=(dictpoints[key].y)
					if (point.x==x and point.y==y):
						f.write(str(key) +' '+ str(x) +' ' + str(y) + '\n') 

class Region:
	def __init__ (self,xmin,ymin,xmax,ymax): #default_region = Region(a,b,c,d) Replace a,b,c,d with our points data
		self.x_min=xmin
		self.y_min=ymin
		self.x_max=xmax
		self.y_max=ymax
		
	def copy(self):
		return Region(self.x_min,self.y_min,self.x_max,self.y_max)

def med(li):
	#print(((max(li)-min(li))/2)+min(li))
	return (((max(li)-min(li))/2)+min(li))

def quadtree(node,pointlist,linex,liney,depth):
	#print("hi this is quadtree")
	global countleaf
	swl=[]
	sel=[]
	nel=[]
	nwl=[]
	#print("lines are",linex,liney )
	for i in range( len(pointlist) ):
		if(int(pointlist[i].x) == linex and int(pointlist[i].y) == liney ):
			nwl.append(pointlist[i])
		elif( int(pointlist[i].x) <= linex and int(pointlist[i].y) <= liney ):
			swl.append(pointlist[i])			
		elif( int(pointlist[i].x) > linex and int(pointlist[i].y) <= liney ):
			sel.append(pointlist[i])			
		elif( int(pointlist[i].x) > linex and int(pointlist[i].y) > liney ):
			nel.append(pointlist[i])			
		else:
			nwl.append(pointlist[i])
	#print("list of swl is ",swl)		
	#print("list of sel is ",sel)		
	#print("list of nwl is ",nwl)		
	#print("list of nel is ",nel)		
			
	if( len(swl) <= alpha):
		countleaf = countleaf+1
		node.sw=Node_leaf(filename=countleaf,pointlist=swl,depth=depth+1)
	else:
		xpoints=[]
		ypoints=[]
		for i in range(len(swl)):
			xpoints.append(int(swl[i].x))
			ypoints.append(int(swl[i].y))
		medx=med(xpoints)
		medy=med(ypoints)
		node.sw=Node_int(sw=None,se=None,ne=None,nw=None,linex=medx,liney=medy,status=1,par=node)
		quadtree(node=node.sw,pointlist=swl,linex=medx,liney=medy,depth=depth+1)		
	
	if( len(sel) <= alpha):
		countleaf = countleaf+1
		node.se=Node_leaf(filename=countleaf,pointlist=sel,depth=depth+1)
	else:
		xpoints=[]
		ypoints=[]
		for i in range(len(sel)):
			xpoints.append(int(sel[i].x))
			ypoints.append(int(sel[i].y))
		medx=med(xpoints)
		medy=med(ypoints)
		node.se=Node_int(sw=None,se=None,ne=None,nw=None,linex=medx,liney=medy,status=2,par=node)
		quadtree(node=node.se,pointlist=sel,linex=medx,liney=medy,depth=depth+1)

	if( len(nel) <= alpha):
		countleaf = countleaf+1
		node.ne=Node_leaf(filename=countleaf,pointlist=nel,depth=depth+1)
	else:
		xpoints=[]
		ypoints=[]
		for i in range(len(nel)):
			xpoints.append(int(nel[i].x))
			ypoints.append(int(nel[i].y))
		medx=med(xpoints)
		medy=med(ypoints)
		node.ne=Node_int(sw=None,se=None,ne=None,nw=None,linex=medx,liney=medy,status=3,par=node)
		quadtree(node=node.ne,pointlist=nel,linex=medx,liney=medy,depth=depth+1)						

	if( len(nwl) <= alpha):
		countleaf = countleaf+1
		node.nw=Node_leaf(filename=countleaf,pointlist=nwl,depth=depth+1)
	else:
		xpoints=[]
		ypoints=[]
		for i in range(len(nwl)):
			xpoints.append(int(nwl[i].x))
			ypoints.append(int(nwl[i].y))
		medx=med(xpoints)
		medy=med(ypoints)
		node.nw=Node_int(sw=None,se=None,ne=None,nw=None,linex=medx,liney=medy,status=4,par=node)
		quadtree(node=node.nw,pointlist=nwl,linex=medx,liney=medy,depth=depth+1)	

def printGivenLevel(root , level): 
	if root is None: 
		return
	if level == 1: 
		if(not isinstance(root,Node_root) and root.se is not None ):
			print ("line in x axis is " ,root.linex ,"line in y axis is " ,root.liney)
	elif level > 1 : 
		printGivenLevel(root.sw , level-1) 
		printGivenLevel(root.se , level-1) 
		printGivenLevel(root.ne , level-1) 
		printGivenLevel(root.nw , level-1) 
		
def height(node): 
	if node is None: 
		return 0 
	if isinstance(node,Node_leaf):
		with open(node.filename,'r') as f:		
			data=f.readlines()
		if (data):	
			print("node is ", node.filename, "depth of node is ", node.depth )
			for item in data:
				id, x, y = item.split()
				print(id, x, y )   
		return 0
	else : 
		# Compute the height of each subtree  
		swh = height(node.sw) 
		seh = height(node.se) 
		neh = height(node.ne) 
		nwh = height(node.nw) 
		#Use the larger one 
		if swh > seh and swh > neh and swh > nwh:
			return swh+1
		elif seh > swh and seh > neh and seh > nwh:
			return seh+1
		elif neh > swh and neh > seh and neh > nwh:
			return neh+1
		else:	
			return swh+1
		
def visualize(root): 
	h = height(root) 
	for i in range(1, h+1):
		print("\n")
		print("height of level is " + str(i))
		printGivenLevel(root, i)

def main():
	dictline={}
	pointlist=[]
	with open("points.txt") as f:
		data=f.readlines() 				
		if (len (data)==0):
			print("no file exist")
			sys.exit()
	for item in data:
		id, x, y = item.split()
		dictpoints[id]=point(x,y) 	
	pointlist=list(dictpoints.values())
	for i in range(len(pointlist)):
		xpoints.append(int(pointlist[i].x))
		ypoints.append(int(pointlist[i].y))
	
	medx=med(xpoints)
	medy=med(ypoints)
	#print("at root", medx,medy)
	if(len(pointlist)<=alpha):
		print("the region of node defined at root node contains all the nodes")
		root=Node_leaf(filename=countleaf,pointlist=pointlist,depth=0)
		print(dictpoints)
	else:	
		root=Node_root(ymax=max(ypoints),ymin=min(ypoints),xmax=max(xpoints),xmin=min(xpoints),sw=None,se=None,ne=None,nw=None,linex=medx,liney=medy)
		quadtree(node=root,pointlist=pointlist,linex=medx,liney=medy,depth=0)


	#searchQuadTree(root,Region(0,0,1,0))	
	#visualize(root)

if __name__ == '__main__':
	main()			