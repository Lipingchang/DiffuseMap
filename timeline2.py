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

def calEn2(mat,tot):
	ans=0
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if mat[i][j]>0:
				ans+=-1.0*mat[i][j]/tot*math.log(1.0*mat[i][j]/tot,math.e)
	return ans

def calEn1(arr,tot):
	ans=0
	for i in range(len(arr)):
		if arr[i]>0:
			ans+=-1.0*arr[i]/tot*math.log(1.0*arr[i]/tot,math.e)
	return ans

def entropy1(dta):
	# print dta
	tsize=1
	wsize=30
	left=0
	right=20
	ep=[]
	dlen=len(dta)
	
	for i in range(0,dlen-wsize,tsize):
		# mat=[[0 for k in range(10)] for k in range(10)]
		arr=[0 for k in range(10)]
		cnt=0
		for j in range(i,i+wsize):
			arr[dta[j][2]]+=1
			cnt+=1

		ep.append(calEn1(arr,cnt))
		# for j in range(i+1,i+wsize):
		# 	if j>=dlen:
		# 		break
		# 	cnt+=1
		# 	mat[dta[j][2]][dta[j-1][2]]+=1
			# if i==4:
			# 	print dta[j][2],dta[j-1][2]
		# print cnt
		# print mat
		#ep.append(calEn(mat,cnt))
	return ep
def entropy2(dta):
	# print dta
	tsize=1
	wsize=30
	left=0
	right=20
	ep=[]
	dlen=len(dta)

	for i in range(0,dlen-wsize,tsize):
		mat=[[0 for k in range(10)] for k in range(10)]
		cnt=0
		for j in range(i+1,i+wsize):
			if j>=dlen:
				break
			cnt+=1
			mat[dta[j][2]][dta[j-1][2]]+=1
			if i==4:
				print dta[j][2],dta[j-1][2]
		ep.append(calEn2(mat,cnt))
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

tdata=data[0]+data[1]+data[2]
tdata.sort(key=lambda x: x[0])
# print data[1]
print 'dlen',len(tdata)
ep1= entropy1(tdata)
ep2= entropy2(tdata)

plt.subplot(121)
plt.plot(ep1)
plt.subplot(122)
plt.plot(ep2)
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



