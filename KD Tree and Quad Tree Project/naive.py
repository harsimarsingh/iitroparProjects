class point:
	def __init__(self,x,y):
		self.x=x
		self.y=y
	
	def __repr__(self):
		return "".join(["(",str(self.x),",",str(self.y),")"])

class Region:
	def __init__ (self,xmin,ymin,xmax,ymax): #default_region = Region(a,b,c,d) Replace a,b,c,d with our points data
		self.x_min=xmin
		self.y_min=ymin
		self.x_max=xmax
		self.y_max=ymax
		
	def copy(self):
		return Region(self.x_min,self.y_min,self.x_max,self.y_max)

def PointInside(point,reg): 
	x=int(point.x)
	y=int(point.y)
	if( x >= reg.x_min and x <= reg.x_max and y >= reg.y_min and y <= reg.y_max  ):
		return 1
	'''
	check karan lyi 
	default_region = Region(2,1,6,7) 
	print(PointInside(point(5,6),default_region))
	'''	

dictline={}
pointlist=[]
regi=Region(3,5,13,9)
with open("points.txt") as f:
	data=f.readlines() 				
	if (len (data)==0):
		sys.exit()
	for item in data:
		id, x, y = item.split()
		if( PointInside(point(x,y),regi)): 	
			print(str(id)+' '+str(x)+ ',' + str(y))

