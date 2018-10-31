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
