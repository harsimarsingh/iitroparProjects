'''
By- Harsimar Singh
	2018CSM1010
'''

import math
import sys
from pathlib import Path
import os
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
		if(not isinstance (root,Node_leaf)):
			print ("line in x axis is " ,root.linex ,"line in y axis is " ,root.liney)
	elif level > 1 : 
		printGivenLevel(root.sw , level-1) 
		printGivenLevel(root.se , level-1) 
		printGivenLevel(root.ne , level-1) 
		printGivenLevel(root.nw , level-1) 
		
def height(node): 
	if node is None: 
		return 0 
	elif isinstance(node,Node_leaf):
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
	print ("Height is ", h)

def PointInside(point,reg): 
	x=int(point.x)
	y=int(point.y)
	if( x >= int(reg.x_min) and x <= int(reg.x_max) and y >= int(reg.y_min) and y <= int(reg.y_max)  ):
		return True

def Inside(reg1,reg2): 			#to check whether reg1 is inside reg2
	if(reg1 and reg2):
		low=point(int(reg1.x_min),int(reg1.y_min) )
		high=point(int(reg1.x_max),int(reg1.y_max) )
		if(PointInside(low,reg2) and PointInside(high,reg2)):
			return True
	else:
		return False
		
def TestIntersect(reg1,reg2):   # region2 should always be greater than region1 
	if(reg1 and reg2):
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

def SubtreePoints(node):
	#print("in SubtreePoints")
	if(isinstance(node,Node_leaf)):
		with open(node.filename,'r') as f:
			data=f.readlines()
			#print("\n" , node.filename) 			
		if(len(data)):
			for item in data:
				id, x, y = item.split()
				print(str(id)+' '+str(x)+ ',' +str(y) )
	else: 
		if(node.sw):
			SubtreePoints(node.sw)
		if(node.se):
			SubtreePoints(node.se)
		if(node.ne):
			SubtreePoints(node.ne)
		if(node.nw):
			SubtreePoints(node.nw)

def findRegion(node):
	if( not isinstance(node,Node_leaf)):
		x1=0
		x2=0
		y1=0
		y2=0
		while( not isinstance(node,Node_root)):
			nodestack.append( (node.par.linex,node.par.liney,node.status)  )
			node=node.par
		x1=node.xmin
		x2=node.xmax
		y1=node.ymin
		y2=node.ymax
		for i in range(len(nodestack)):
			item=nodestack.pop()
			if(item[2])==1: #sw child
				x2=item[0]
				y2=item[1]			
			if(item[2])==2: #se child
				x1=item[0]
				y2=item[1]
			if(item[2])==3: #ne child
				x1=item[0]
				y1=item[1]
			if(item[2])==4: #nw child
				x2=item[0]
				y1=item[1]
		return (Region(xmin=x1,ymin=y1,xmax=x2,ymax=y2))

	else:
		#find region of leaf node and return
		lx=[]
		ly=[]
		my_file = Path(node.filename)
		if(my_file):
			with open(node.filename,'r') as f:		
				data=f.readlines()
			if(data):
				for item in data:
					id, x, y = item.split()
					lx.append(int(x))
					ly.append(int(y))
					#print(min(lx),min(ly),max(lx),max(ly))
				return ( Region(xmin=min(lx),ymin=min(ly),xmax=max(lx),ymax=max(ly) ))		

def searchQuadTree(node,regi):
	global countinternal
	if( isinstance(node,Node_int) ):
		countinternal=countinternal+1
	if(isinstance(node,Node_leaf)):
		with open(node.filename,'r') as f:
			data=f.readlines() 				#read().split()
		if(data):	
			for item in data:
				id, x, y = item.split()
				if( PointInside(point(x,y),regi) ): 	
					for key in dictpoints:				#search points in dictionary
						x1=(dictpoints[key].x)
						y1=(dictpoints[key].y)
						if (x1==x and y1==y):
							print(str(key)+' '+str(x)+','+str(y) )
	else:
		if ( Inside ( findRegion(node.sw), regi) ):
		 	SubtreePoints(node.sw)	
		elif (TestIntersect(findRegion(node.sw),regi)):
			searchQuadTree(node.sw,regi)

		if ( Inside ( findRegion(node.se), regi) ):
		 	SubtreePoints(node.se)	
		elif (TestIntersect(findRegion(node.se),regi)):
			searchQuadTree(node.se,regi)
		
		if ( Inside ( findRegion(node.ne), regi) ):
		 	SubtreePoints(node.ne)	
		elif (TestIntersect(findRegion(node.ne),regi)):
			searchQuadTree(node.ne,regi)

		if ( Inside ( findRegion(node.nw), regi) ):
		 	SubtreePoints(node.nw)	
		elif (TestIntersect(findRegion(node.nw),regi)):
			searchQuadTree(node.nw,regi)

def rangequerygen(area):
	if area == 50:
		length=10
		breadth=5
		x_min=r.randint(0,90-length)
		y_min=r.randint(0,90-breadth)
		x_max=x_min+length
		y_max=y_min+breadth
		#print(x_min,x_max,y_min,y_max)
	if area == 100:
		length=10
		breadth=10
		x_min=r.randint(0,90-length)
		y_min=r.randint(0,90-breadth)
		x_max=x_min+length
		y_max=y_min+breadth
		#print(x_min,x_max,y_min,y_max)
	if area == 150:
		length=15
		breadth=10
		x_min=r.randint(0,90-length)
		y_min=r.randint(0,90-breadth)
		x_max=x_min+length
		y_max=y_min+breadth
		#print(x_min,x_max,y_min,y_max)
	if area == 200:
		length=20
		breadth=10
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

	time_lista=[]
	start_time=time.time()
	for i in range (8):
		x_min,x_max,y_min,y_max=rangequerygen(50)
		#print(x_min,x_max,y_min,y_max)
		#print("iteration number ", i )
		#print("region is",x_min,y_min,x_max,y_max )
		regi=Region(x_min,y_min,x_max,y_max)
		searchQuadTree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
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
		searchQuadTree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
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
		searchQuadTree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
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
		searchQuadTree(root,Region(x_min,y_min,x_max,y_max)) #region -> xmin,ymin,xmax,ymax
		#visualize(root)
		#naive(regi)
		time_listd.append(time.time()-start_time)
		start_time=time.time()
	countlist.append(countinternal/8)


	visualize(root)
	
	print ("for 50",np.mean(time_lista))
	print ("for 100",np.mean(time_listb))
	print ("for 150",np.mean(time_listc))
	print ("for 200",np.mean(time_listd))
	X=[50,100,150,200]
	Y=countlist
	#plt.xlim=(50,200)
	print(X,Y)
	#plt.scatter(X,Y)
	#plt.show()
	with open('output.txt', 'a') as f:
		for item in Y:
			f.write("%s\n" % item)	
	

if __name__ == '__main__':
	main()			