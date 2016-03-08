#encoding: utf-8

import community as cm
import networkx as nx
import matplotlib.pyplot as plt
import json
import csv
import time
import glob
import datetime
import sys
import os
import json
import copy
import numpy as np
import random

reload(sys)
#中文错误
sys.setdefaultencoding( "utf-8" )

def cal(evtlist,linklist,parent):
    global repost_num
    pid=parent['uid']
    pname=parent['name']
    idToN[pid]=pname
    cntuids[pid]=cntuids.get(pid,0)+1
    if pid not in evtlist:
        evtlist.append(pid)  # 避免重复出现
    if not pid in linklist:
        linklist[pid]=[]
    for child in parent['children']:
        repost_num+=1
        cid=child['uid']
        linklist[pid].append(cid)
        cal(evtlist,linklist,child)

def update(tree,uid_loc,uid_cls,p_evtlist,i):
    tree['loc']=uid_loc[tree['uid']]
    tree['category']=uid_cls[tree['uid']]
    p_evtlist[tree['uid']][i]+=1

    for child in tree['children']:
        update(child,uid_loc,uid_cls,p_evtlist,i)

def build_G(pnum,uids,matrix,layout_matrix):
    names=[]  # names of all users
    for uid in uids:
        names.append(idToN[uid])
    begin=time.time()
    for key in link_list.keys():
        pindex=uids.index(key)
        for cid in link_list[key]:
            cindex=uids.index(cid)
            a=min(pindex,cindex)
            b=max(pindex,cindex)
            layout_matrix[b][a]=layout_matrix[b].get(a,0)+100
            matrix[b][a]=matrix[b].get(a,0)+5             
    G=nx.Graph()
    edge_list=[]
    for i in xrange(len(names)):
        for j in matrix[i]:
            edge_list.append((i,j,matrix[i][j]))
    print 'repost_num '+str(repost_num)
    global enum
    enum=len(edge_list)
    print 'edges '+str(len(edge_list))
    #G.add_weighted_edges_from(edge_list)
    #G.add_weighted_edges_from(edge_list)
    G.add_weighted_edges_from(edge_list)
    return G

def build_layout_G(layout_matrix):
    evt_list_sq=[]  
    for i in xrange(len(evt_list)):
        evt_list_sq.append([])
        for j in xrange(len(evt_list[i])):
            evt_list_sq[i].append(uids.index(evt_list[i][j]))
    rootsq=uids.index(rootid)
    for i in xrange(len(evt_list_sq)):
        for j in xrange(len(evt_list_sq[i])):
            if evt_list_sq[i][j]==rootsq:
                continue
            for k in xrange(j+1,len(evt_list_sq[i])):
                if evt_list_sq[i][k]==rootsq:
                    continue
                factor=cntuids[evt_list[i][j]]*cntuids[evt_list[i][k]]
                # a=uids.index(evt_list[i][j])
                # b=uids.index(evt_list[i][k])
                a=evt_list_sq[i][j]
                b=evt_list_sq[i][k]
                a=min(a,b)
                b=max(a,b)
                if partition[a]==partition[b]:
                    if a in layout_matrix[b]:
                        layout_matrix[b][a]+=500/factor

                    else:
                        layout_matrix[b][a]=500/factor
    global cnum
    cnum = len(set(partition.values()))
    # cmem = [ [] for i in range(cnum)]
    # for i in range(pnum):
    #     cmem[partition[i]].append(i)
    # for i in range(pnum):
    #     for j in range(0,i):
    #         if partition[i]==partition[j]:
    #             if not j in layout_matrix[i]:
    #                 layout_matrix[i][j]=+200
    layout_edge_list=[]
    begin=time.time()
    global pnum
    for i in xrange(pnum):
        for j in layout_matrix[i]:
            layout_edge_list.append((i,j,layout_matrix[i][j]))
    layout_G=nx.Graph()
    layout_G.add_weighted_edges_from(layout_edge_list)
    return layout_G

evt_list=[]
link_list={}
idToN={}
treeArray=[]
repost_num=0
evt=0   
fnum=0
enum=0
cnum=0
rootid=''
cntuids={}
uids=[]
names=[]
pname='aikeke'
inputfolder='data/'+pname+'Tree'
# outputfolder='/home/shuaichen/Projects/DiffuseMap/data/community'
outputfolder='treeArray_community'
list_dirs=os.walk(inputfolder)
for root, dirs, files in list_dirs:
    for ccfile in files:
        fnum+=1
        cfile=open(inputfolder+'/'+ccfile)
        jfile=json.load(cfile)
        rootid=jfile['uid']
        treeArray.append(jfile)
        evt_list.append([])
        cal(evt_list[evt],link_list,jfile,)
        evt+=1  # can't be anoated
        if evt>0: 
            break                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

print 'fnum '+str(fnum) 
uids=cntuids.keys()  # id of all users
pnum=len(uids)
print 'pnum '+str(pnum)

matrix=[{} for i in xrange(pnum)]
layout_matrix=[{} for i in xrange(pnum)]
G=build_G(pnum,uids,matrix,layout_matrix)
dendo = cm.generate_dendogram(G)
partition=cm.partition_at_level(dendo, len(dendo)-1)



layout_G=build_layout_G(layout_matrix)
print 'nx.spring_layout'
begin=time.time()
pos = nx.spring_layout(layout_G,iterations=30) # default 50
print 'pos '+(str(time.time()-begin))

uid_loc={}
uid_cls={}
cat_cnt=[0 for i in xrange(cnum)]
group={}
for i in xrange(len(uids)):
    cat_cnt[partition[i]]+=1
    uid_loc[uids[i]]=[float(pos[i][0]),float(pos[i][1])]
    uid_cls[uids[i]]=partition[i]

  
begin=time.time()
# K=10
# clusters=tree_clustering(trees=treeArray,uids=uids,k=K)
# cls_cnt=[0 for i in range(K)]
# for i in range(fnum):
#     cls_cnt[clusters[i]]+=1
# print cls_cnt
# print 'clusters '+str(time.time()-begin)

p_evtlist={}
for uid in uids:
    p_evtlist[uid]=[ 0 for i in range(len(treeArray))]
for i,jt in enumerate(treeArray):
    update(jt,uid_loc,uid_cls,p_evtlist,i)
    # jt['group']=str(clusters[i])
print 'cnum'+str(cnum)
output=open(outputfolder+'/'+pname+'treeArray'+str(evt)+ ' pnum'+str(pnum)+\
    ' cnum'+str(cnum)+' edges'+str(enum)+' rpnum'+str(repost_num)+' com'+'.json','w')
json.dump({'treeArray':treeArray,'cat_cnt':cat_cnt},output,ensure_ascii=False,encoding='utf8')
output.close()
# for i in xrange(cnum):
#     print str(i)+' '+str(cat_cnt[i])


# for (u,v,d) in G.edges(data='weight'):
#     print (u,v,d)
cmap = plt.get_cmap('gnuplot')
# plt.subplot(1,2,1)
colors = [cmap(i) for i in np.linspace(0, 1, cnum)]
count=0
tag=0
for com in set(partition.values()):
    count = count + 1
    list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]

    # if len(list_nodes)==4:
    nx.draw_networkx_nodes(layout_G, pos, list_nodes, node_size = 40, \
        node_color = [colors[com] for i in range(len(list_nodes))],cmap=cmap, \
        label='$cnum: {k}$'.format(k=len(list_nodes)))
nx.draw_networkx_edges(G,pos,alpha=0.5)
plt.legend(loc=2,prop={'size':6})
plt.title(pname+'treeArray'+str(evt)+ ' pnum'+str(pnum)+\
    ' cnum'+str(cnum)+' edges'+str(enum)+' rpnum'+str(repost_num)+' com'+' norooid factor'+'.json')
plt.show()




