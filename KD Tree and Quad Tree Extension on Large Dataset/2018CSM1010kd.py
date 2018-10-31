'''
By- Harsimar Singh
	2018CSM1010

'''

import math
import sys
import statistics as stat
import random as r
import numpy as np
import time
import matplotlib.pyplot as plt
alpha=150 			#this will be our threshhold #default is 3
xpoints=[]
ypoints=[]
dictpoints={}	 	#dictionary to map points
countleaf=0
nodestack=[]
my_file="DatasetC.txt"
countinternal=0

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

def naive(regi):
	dictline={}
	pointlist=[]
	#regi=Region(3,5,13,9)
	with open(my_file) as f:
		data=f.readlines() 				
		if (len (data)==0):
			sys.exit()
		for item in data:
			id, x, y = item.split()
			if( PointInside(point(x,y),regi)): 	
				print(str(id)+' '+str(x)+ ',' + str(y))

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
	if node is None : 
		return 0
	elif  isinstance(node,Node_leaf):
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
	if level == 1 : 
			if(not isinstance (root,Node_leaf)):
				print ("line is " ,root.line ,"axis is " ,root.axis)
	elif isinstance(root,Node_leaf):
		print("\n")
		return 		
	elif level > 1 : 
		printGivenLevel(root.left , level-1) 
		printGivenLevel(root.right , level-1) 

def visualize(root): 
	h = height(root) 
	for i in range(1, h+1):
		print("\n")
		print("height of level is " + str(i))
		printGivenLevel(root, i)
	print ("Height is ", h)

def PointInside(point,reg): 
	x=int(point.x)
	y=int(point.y)
	if( x >= int(reg.x_min) and x <= int(reg.x_max) and y >= int(reg.y_min) and y <= int(reg.y_max)  ):
		return True

def Inside(reg1,reg2): #to check whether reg1 is inside reg2
	if(reg1 and reg2):
		low=point(int(reg1.x_min),int(reg1.y_min) )
		high=point(int(reg1.x_max),int(reg1.y_max) )
		if(PointInside(low,reg2) and PointInside(high,reg2)):
			return True
	else:
		return False

def TestIntersect(reg1,reg2):   # region2 should always be greater than region1 
	area1= ((int(reg1.x_max)-int(reg1.x_min) ) * (int(reg1.y_max)-int(reg1.y_min) )) 
	area2= ((int(reg2.x_max)-int(reg2.x_min) ) * ( int(reg2.y_max)-int(reg2.y_min) )) 
	if(area1 > area2): 			#swapping regions if region1 is given bigger than region2 by logic of area
		reg1,reg2=reg2,reg1
	cor1=point(reg1.x_min,reg1.y_min)
	cor2=point(reg1.x_min,reg1.y_max)
	cor3=point(reg1.x_max,reg1.y_min)
	cor4=point(reg1.x_max,reg1.y_max)
	if ( PointInside(cor1,reg2) or PointInside(cor2,reg2) or PointInside(cor3,reg2) or PointInside(cor4,reg2) ):
		return True
	else:
		return False	

def findRegion(node):
	if( not isinstance(node,Node_leaf)):
		x1=0
		x2=0
		y1=0
		y2=0
		while( not isinstance(node,Node_root)):
			nodestack.append( (node.par.line,node.par.axis,node.status)  )
			node=node.par
		x1=node.xmin
		x2=node.xmax
		y1=node.ymin
		y2=node.ymax
		#print(x1,y1,x2,y2)
		for i in range(len(nodestack)):
			item=nodestack.pop()
			if(item[2]==0):
				if(item[1]==0):
					x2=item[0]	
				else:	
					y2=item[0]	
			if(item[2]==1):
				if(item[1]==0):
					x1=item[0]	
				else:	
					y1=item[0]	
		return (Region(xmin=x1,ymin=y1,xmax=x2,ymax=y2)) #xmin,ymin,xmax,ymax	
	else:
		#find region of leaf node and return
		lx=[]
		ly=[]
		with open(node.filename,'r') as f:		
			#print(node.filename)
			data=f.readlines()
		for item in data:
			#print(item)
			id, x, y = item.split()
			lx.append(int(x))
			ly.append(int(y))
		return ( Region(xmin=min(lx),ymin=min(ly),xmax=max(lx),ymax=max(ly) )) 

def SubtreePoints(node):
	#print("in SubtreePoints")
	if(isinstance(node,Node_leaf)):
		with open(node.filename,'r') as f:
			data=f.readlines() 			
			if (len (data)==0):
				sys.exit()
		for item in data:
			id, x, y = item.split()
			print(str(id)+' '+str(x)+ ',' +str(y) )
	
	else: 
		if(node.left):
			SubtreePoints(node.left)
		if(node.right):
			SubtreePoints(node.right)

def searchKDtree(node,regi):
	global countinternal
	if( isinstance(node,Node_int) ):
		countinternal=countinternal+1
	if(isinstance(node,Node_leaf)):
		with open(node.filename,'r') as f:
			data=f.readlines() 				#read().split()
		for item in data:
			id, x, y = item.split()
			if( PointInside(point(x,y),regi) ): 	
				for key in dictpoints:				#search points in dictionary
					x1=(dictpoints[key].x)
					y1=(dictpoints[key].y)
					if (x1==x and y1==y):
						print(str(key)+' '+str(x)+','+str(y) )
	else:
		if ( Inside ( findRegion(node.left), regi) ):
		 	SubtreePoints(node.left)	#report points inside that regions subtree that intersect with r
		elif (TestIntersect(findRegion(node.left),regi)):
			searchKDtree(node.left,regi)
		if (Inside(findRegion(node.right),regi)):
			SubtreePoints(node.right)	#reports all points in subtree that intersect with r
		elif(TestIntersect(findRegion(node.right),regi)):
			searchKDtree(node.right,regi)
		return None

def rangequerygen(area):
	if area == 50:
		case=r.random()	
		if(case>0.5):
			length=10
			breadth=5
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)
		
		else:
			length=25
			breadth=2
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)
				

	if area == 100:
		case=r.random()
		if(case>0 and case<0.33):
			length=10
			breadth=10
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)
		elif(case>0.33 and case < 0.66):
			length=20
			breadth=5
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)
		elif(case>0.66):
			length=25
			breadth=4
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)		
	
	if area == 150:
		case=r.random()
		if(case>0 and case<0.33):
			length=15
			breadth=10
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
			#print(x_min,x_max,y_min,y_max)
		elif(case>0.33 and case < 0.66):
			length=30
			breadth=5
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth	
		elif(case>0.66):
			length=75
			breadth=2
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth

	if area == 200:
		case=r.random()
		if(case>0 and case<0.33):	
			length=20
			breadth=10
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
		elif(case>0.33 and case < 0.66):
			length=40
			breadth=5
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth
		elif(case>0.66):
			length=25
			breadth=8
			x_min=r.randint(0,90-length)
			y_min=r.randint(0,90-breadth)
			x_max=x_min+length
			y_max=y_min+breadth		
	
	return x_min,x_max,y_min,y_max

def main():
	global countinternal
	countlist=[]
	dictline={}
	pointlist=[]
	with open(my_file) as f:
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
	if( (max(ypoints)-min(ypoints)) > (max(xpoints)-min(xpoints)) ):
		axis=1 			
		median = med(ypoints)
		#print (median)
	else:
		axis=0 			
		median = med(xpoints)
	#print (median,axis)
	if(len(pointlist)<=alpha):
		print("the region of node defined at root node contains all the nodes")
		root=Node_leaf(filename=countleaf,pointlist=pointlist,depth=0)
		print(dictpoints)
	else:
		root=Node_root(ymax=max(ypoints),ymin=min(ypoints),xmax=max(xpoints),xmin=min(xpoints),left=None,right=None,line=median,axis=axis) #(self,ymax,ymin,xmax,xmin,left,right,cord,axis)
		kdtree(node=root,pointlist=pointlist,line=median,axis=axis,depth=0)
	
	time_lista=[]
	start_time=time.time()
	for i in range (8):
		x_min,x_max,y_min,y_max=rangequerygen(50)
		#print(x_min,x_max,y_min,y_max)
		#print("iteration number ", i )
		#print("region is",x_min,y_min,x_max,y_max )
		regi=Region(x_min,y_min,x_max,y_max)
		searchKDtree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
		time_lista.append(time.time()-start_time)
		start_time=time.time()
		#visualize(root)
		#naive(regi)
	countlist.append(countinternal/8)
	countinternal=0
			
	time_listb=[]
	start_time=time.time()	
	for i in range (8):
		x_min,x_max,y_min,y_max=rangequerygen(100)
		#print(x_min,x_max,y_min,y_max)
		#print("iteration number ", i )
		#print("region is",x_min,y_min,x_max,y_max )
		regi=Region(x_min,y_min,x_max,y_max)
		searchKDtree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
		#visualize(root)
		#naive(regi)
		time_listb.append(time.time()-start_time)
		start_time=time.time()
	countlist.append(countinternal/8)
	countinternal=0
		

	time_listc=[]
	start_time=time.time()	
	for i in range (8):
		x_min,x_max,y_min,y_max=rangequerygen(150)
		#print(x_min,x_max,y_min,y_max)
		#print("iteration number ", i )
		#print("region is",x_min,y_min,x_max,y_max )
		regi=Region(x_min,y_min,x_max,y_max)
		searchKDtree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
		#visualize(root)
		#naive(regi)
		time_listc.append(time.time()-start_time)
		start_time=time.time()
	countlist.append(countinternal/8)
	countinternal=0		
	
	time_listd=[]
	start_time=time.time()	
	for i in range (8):
		x_min,x_max,y_min,y_max=rangequerygen(200)
		#print(x_min,x_max,y_min,y_max)
		#print("iteration number ", i )
		#print("region is",x_min,y_min,x_max,y_max )
		regi=Region(x_min,y_min,x_max,y_max)
		searchKDtree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
		#visualize(root)
		#naive(regi)
		time_listd.append(time.time()-start_time)
		start_time=time.time()
	countlist.append(countinternal/8)
	countinternal=0	

	visualize(root)
	
	print ("for 50",np.mean(time_lista))
	print ("for 100",np.mean(time_listb))
	print ("for 150",np.mean(time_listc))
	print ("for 200",np.mean(time_listd))
	
	X=[50,100,150,200]
	Y=countlist
	plt.xlim=(50,200)
	print(X,Y)
	#plt.scatter(X,Y)
	#plt.show()
	with open('output.txt', 'w') as f:
		for item in Y:
			f.write("%s\n" % item)


if __name__ == '__main__':
	main()

