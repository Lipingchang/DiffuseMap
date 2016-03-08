#! /usr/bin/env python

import sys
if sys.version_info < (3,):
    range = xrange
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
import math

def tran(dt,tree,dep):
	dt.append([tree['t'],dep,tree['category']])
	groups[tree['category']]=groups.get(tree['category'],0)+1
	for child in tree['children']:
		tran(dt,child,dep+1)

def calEn(each,group):
	ans=0
	t=0
	for key in each.keys():
		x=each[key]
		t+=x
		y=group[key]
		ans+=-1.0*x/y*math.log(1.0*x/y,math.e)
	# print t
	return ans

def entropy(dta):
	# print dta
	tsize=250
	wsize=2500
	left=dta[0][0]-wsize
	right=dta[0][0]
	ep=[]
	i=0
	group={}
	for i in range(len(dta)):
		group[dta[i][2]]=group.get(dta[i][2],0)+1

	while True:
		# i+=1
		# if i>100:
		# 	break
		each={}
		s=0
		while True:
			if dta[s][0]<=right and dta[s][0]>=left:
				each[dta[s][2]]=each.get(dta[s][2],0)+1
				s+=1
			elif dta[s][0]<left:
				s+=1
			if s>=len(dta) or dta[s][0]>right:
				break
		ep.append(calEn(each,group))
		# print 'left',left
		# print 'right',right
		left+=tsize
		right+=tsize
		if left>=dta[-1][0]:
			break
		# if s>=len(dta)/2:
		# 	break
	print 'group',group
	return ep

inputfolder='treeArray_community'
filename='aikeke2298treeArray2298 pnum10209 cnum10 edges19338 rpnum79013 sto.json'
f=open(inputfolder+'/'+filename)
trees=json.load(f)['treeArray']
tnum=len(trees)

data=[[] for i in range(tnum)]
groups={}
for i in range(tnum):
	tran(data[i],trees[i],1)

tmp=0
tdata=[]

data.sort(key=lambda x: -len(x))
for i in range(len(data)):
	data[i].sort(key=lambda x: x[0])

print 'dlen',len(data[10])
ep= entropy(data[10])
print 'ep',len(ep)
print 'groups',groups
plt.plot(ep)
plt.show()


# colors=matplotlib.colors.cnames.keys()

# ndata=[[] for i in range(len(data))]
# for i in range(len(data)):
# 	ndata[i].append(data[i][0]+[1])
# 	for j in range(1,len(data[i])):
# 		if data[i][j][2]==ndata[i][-1][2]:
# 			ndata[i][-1][3]+=1
# 		else:
# 			ndata[i].append(data[i][j]+[1])

# for j in range(10):
# 	for i,p in enumerate(ndata[j]):
# 		plt.scatter(x=i+1,y=10*j,c=colors[p[2]],s=p[3]*10)
# plt.show()



