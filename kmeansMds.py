#encoding: utf-8
from sklearn.manifold import MDS
import numpy as np  
import copy
import codecs
import matplotlib.pyplot as plt
import matplotlib
import Image
import os
import sys
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
import time
import json
reload(sys)
#中文错误
sys.setdefaultencoding( "utf-8" )


def tran(arr,m):
	m[arr['category']]+=1
	for child in arr['children']:
		tran(child,m)

inputfolder='treeArray_community'
outputfolder='kmeansMds'
list_dirs=os.walk(inputfolder)
fcnt=0
K=5
for root, dirs, files in list_dirs:
    for filename in files:
    	fcnt+=1
    	print filename
    	efile=open(inputfolder+'/'+filename)
        jfile=json.load(efile)
        arrays=jfile['treeArray']
        cnum=len(jfile['cat_cnt'])
        mat=[[0 for i in range(cnum)] for i in xrange(len(arrays))]
        for i in xrange(len(arrays)):
        	tran(arrays[i],mat[i])
        for i in xrange(len(mat)):
        	for j in xrange(len(mat[i])):
        		mat[i][j]=1.0*mat[i][j]/sum(mat[i])
        mat=np.array(mat)
        km=KMeans(init='k-means++', n_clusters=K, n_init=10)
        km.fit(mat)
        labels=km.labels_

        disM=euclidean_distances(mat.astype(np.float64))
        mds = MDS(n_components=2, max_iter=3000,eps=1e-9,dissimilarity="precomputed")
        pos=mds.fit(disM.astype(np.float64)).embedding_

        for i in xrange(len(arrays)):
			arrays[i]['kPos']=[float(pos[i,0]),float(pos[i,1])]
			arrays[i]['kGroup']=int(labels[i])
        output=open(outputfolder+'/k_'+filename,'w')
        json.dump({'treeArray':arrays},output,ensure_ascii=False,encoding='utf8')
        
        each=[0 for i in range(K)]
        for i in range(len(labels)):
        	each[labels[i]]+=1
        	
        colors=matplotlib.colors.cnames.keys()
        for i in range(len(arrays)):
			plt.scatter(x=pos[i,0],y=pos[i,1],c=colors[labels[i]])
        plt.show()
        print each
        efile.close()
        # if fcnt>0:
        # 	break
