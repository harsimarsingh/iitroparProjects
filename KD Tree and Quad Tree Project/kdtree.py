import math
import sys
import statistics as stat
alpha=3 			#this will be our threshhold #default is 3
xpoints=[]
ypoints=[]
dictpoints={}	 	#dictionary to map points
countleaf=0
nodestack=[]

class point:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	
	def __repr__(self):
		return "".join(["(",str(self.x),",",str(self.y),")"])

class Node_root:
	def __init__(self,left,right,line,axis,ymax,ymin,xmax,xmin):
		self.left=None
		self.right=None
		self.line=line
		self.axis=axis
		self.ymax=ymax
		self.ymin=ymin
		self.xmax=xmax
		self.xmin=xmin

class Node_int:
	def __init__(self,left,right,line,axis,status,par):
		self.left=None
		self.right=None
		self.line=line
		self.axis=axis
		self.par=par
		self.status=status #right child or left (0,1 boolean values)

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
						f.write(str(key) +' '+ str(x) +' ' + str(y) + '\n' )
				
		#print("At depth: ",depth)
		#print(pointlist)	

class Region:
	def __init__ (self,xmin,ymin,xmax,ymax): #default_region = Region(a,b,c,d) Replace a,b,c,d with our points data
		self.x_min=xmin
		self.y_min=ymin
		self.x_max=xmax
		self.y_max=ymax
		
	def copy(self):
		return Region(self.x_min,self.y_min,self.x_max,self.y_max)

def med(li):
	li.sort()
	#print(stat.median(li))
	return (stat.median(li))		

def kdtree(node,pointlist,line,axis, depth):
	global countleaf
	leftl=[] 				#left list
	rightl=[]				#right list
	if (axis == 0):
		for i in range( len(pointlist) ):
			if( int(pointlist[i].x) <= line):
				leftl.append(pointlist[i])
			else:
				rightl.append(pointlist[i])
	else:	
		for i in range( len(pointlist) ):
			if( int(pointlist[i].y) <= line):
				leftl.append(pointlist[i])
			else:
				rightl.append(pointlist[i])	
	
	if( len(leftl) <= alpha):
		countleaf = countleaf+1
		node.left=Node_leaf(filename=countleaf,pointlist=leftl,depth=depth+1)

	else:
		#find spread in left list
		xpoints=[]
		ypoints=[]
		for i in range(len(leftl)):
			xpoints.append(int(leftl[i].x))
			ypoints.append(int(leftl[i].y))
		if( (max(ypoints)-min(ypoints)) > (max(xpoints)-min(xpoints)) ):
			axis=1 			#value for axis is 1 for y axis split
			median = med(ypoints)
		else:
			axis=0 			#value of axis is 0 for x axis split
			median = med(xpoints)
		#print(median,axis)
		node.left=Node_int(left=None,right=None,line=median,axis=axis,status=0,par=node)		
		#print("left node of tree created")
		kdtree(node=node.left,pointlist=leftl,line= median,axis= axis, depth=depth+1)

	if (len(rightl) <= alpha):
		countleaf =countleaf+1
		node.right=Node_leaf(filename=countleaf,pointlist=rightl,depth=depth+1)

	else:
		#find spread in right list
		xpoints=[]
		ypoints=[]
		for i in range(len(rightl)):
			xpoints.append(int(rightl[i].x))
			ypoints.append(int(rightl[i].y))
		if( (max(ypoints)-min(ypoints)) > (max(xpoints)-min(xpoints)) ):
			axis=1 			#value for axis is 1 for y axis split
			median = med(ypoints)
		else:
			axis=0 			#value of axis is 0 for x axis split
			median = med(xpoints)
		#print(median,axis)	
		node.right=Node_int(left=None,right=None,line=median,axis=axis,status=1,par=node)		
		#print("right node of tree created")
		kdtree(node=node.right,pointlist=rightl,line= median,axis= axis,depth=depth+1) #recursion

def height(node): 
	if node is None: 
		return 0 
	if isinstance(node,Node_leaf):
		print("\n")
		with open(node.filename,'r') as f:		
			print("node is ", node.filename, "depth of node is ", node.depth )
			data=f.readlines()
		for item in data:
			id, x, y = item.split()
			print(id, x, y )   
		return 0
	else : 
		# Compute the height of each subtree  
		lheight = height(node.left) 
		rheight = height(node.right) 
		#Use the larger one 
		if lheight > rheight : 
			return lheight+1
		else: 
			return rheight+1

def printGivenLevel(root , level): 
	if root is None: 
		return
	if level == 1: 
		if(not isinstance(root,Node_root) and root.left is not None or root.right is not None ):
			print ("line is " ,root.line ,"axis is " ,root.axis)
	elif level > 1 : 
		printGivenLevel(root.left , level-1) 
		printGivenLevel(root.right , level-1) 

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
		data=f.readlines() 				#read().split()
		if (len (data)==0):
			print("no file exist")
			sys.exit()
	for item in data:
		id, x, y = item.split()
		dictpoints[id]=point(x,y) 	#points inserted in dictionary
	pointlist=list(dictpoints.values())
	for i in range(len(pointlist)):
		xpoints.append(int(pointlist[i].x))
		ypoints.append(int(pointlist[i].y))
	if( (max(ypoints)-min(ypoints)) > (max(xpoints)-min(xpoints)) ):
		axis=1 			#value for axis is 1 for y axis split
		median = med(ypoints)
		#print (median)
	else:
		axis=0 			#value of axis is 0 for x axis split
		median = med(xpoints)
	#print (median,axis)
	if(len(pointlist)<=alpha):
		print("the region of node defined at root node contains all the nodes")
		root=Node_leaf(filename=countleaf,pointlist=pointlist,depth=0)
		print(dictpoints)
	else:
		root=Node_root(ymax=max(ypoints),ymin=min(ypoints),xmax=max(xpoints),xmin=min(xpoints),left=None,right=None,line=median,axis=axis) #(self,ymax,ymin,xmax,xmin,left,right,cord,axis)
		kdtree(node=root,pointlist=pointlist,line=median,axis=axis,depth=0)
	
	#searchKDtree(root,Region(0,0,4,4))
	#visualize(root)

if __name__ == '__main__':
	main()

