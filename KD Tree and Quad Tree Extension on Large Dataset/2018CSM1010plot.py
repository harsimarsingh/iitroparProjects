'''Submitted by 
Harsimar Singh
2018CSM1010
'''
import matplotlib.pyplot as plt
filename="output.txt"
count=0
line1=[]
line2=[]
xline=[50,100,150,200]
with open (filename) as f:
	data=f.readlines()
	for item in data:
		count=count+1
		if(count <= 4):
			line1.append(item)
		else:
			line2.append(item)
plt.plot(xline,line1,label ="kdline")
plt.plot(xline,line2,label ="quadline")
plt.title("KD vs Quad")
plt.legend()
plt.xlabel('area of query rectangle')
plt.ylabel('number of internal nodes')
plt.show()
