#! /usr/bin/env python

import sys
if sys.version_info < (3,):
    range = xrange
import os
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json

def tran(dt,tree,dep):
	dt.append([tree['t'],dep,tree['category']])
	for child in tree['children']:
		tran(dt,child,dep+1)

inputfolder='treeArray_community'
filename='aikeke2298treeArray2298 pnum10209 cnum10 edges19338 rpnum79013 sto.json'
f=open(inputfolder+'/'+filename)
trees=json.load(f)['treeArray']
tnum=len(trees)

data=[[] for i in range(tnum)]

for i in range(tnum):
	tran(data[i],trees[i],1)

tmp=0
tdata=[]

data.sort(key=lambda x: -len(x))
for i in range(len(data)):
	data[i].sort(key=lambda x: x[0])

colors=matplotlib.colors.cnames.keys()

ndata=[[] for i in range(len(data))]
for i in range(len(data)):
	ndata[i].append(data[i][0]+[1])
	for j in range(1,len(data[i])):
		if data[i][j][2]==ndata[i][-1][2]:
			ndata[i][-1][3]+=1
		else:
			ndata[i].append(data[i][j]+[1])

for j in range(10):
	for i,p in enumerate(ndata[j]):
		plt.scatter(x=i+1,y=10*j,c=colors[p[2]],s=p[3]*10)
plt.show()



