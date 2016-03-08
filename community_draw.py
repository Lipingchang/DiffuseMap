#encoding: utf-8
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
from graph_tool.all import *
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

def update(tree,uid_loc,uid_cls):
    tree['loc']=uid_loc[tree['uid']]
    tree['category']=uid_cls[tree['uid']]
    # p_evtlist[tree['uid']][i]+=1

    for child in tree['children']:
        update(child,uid_loc,uid_cls)

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
    G=Graph()
    G.set_directed(False)
    global enum
    # G.add_vertex(len(uids))
    v_list=G.add_vertex(len(uids))
    for v1 in xrange(len(uids)):
    	for v2 in matrix[v1]:
            G.add_edge(G.vertex(v1),G.vertex(v2))
            enum+=1
    return G

def build_layout_G(layout_matrix,rootid):
    evt_list_sq=[]

    for i in xrange(len(evt_list)):
        evt_list_sq.append([])
        for j in xrange(len(evt_list[i])):
            evt_list_sq[i].append(uids.index(evt_list[i][j]))
    rootsq=uids.index(rootid)
    # print evt_list_sq
    # print rootsq
    begin=time.time()
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
                a=min(evt_list_sq[i][j],evt_list_sq[i][k])
                b=max(evt_list_sq[i][j],evt_list_sq[i][k])
                # if a==b:
                #     continue
                # print a,b,partitions[a],partitions[b]
                if partitions[a]==partitions[b]:
                    if a in layout_matrix[b]:
                        layout_matrix[b][a]+=500/factor

                    else:
                        layout_matrix[b][a]=500/factor
    print "l1",str(time.time()-begin)
    layout_G=Graph()
    layout_G.set_directed(False)
    layout_G.add_vertex(len(cntuids))
    print 's'
    tmp=len(cntuids)
    for v1 in xrange(tmp):
    	for v2 in layout_matrix[v1]:
    	    layout_G.add_edge(G.vertex(v1),G.vertex(v2))

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
pname='aikeke2298'
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
        # if evt>300: 
        #     break                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              

print 'fnum '+str(fnum) 
uids=cntuids.keys()  # id of all users
pnum=len(uids)
print 'pnum '+str(pnum)

matrix=[{} for i in xrange(pnum)]
layout_matrix=[{} for i in xrange(pnum)]
G=build_G(pnum,uids,matrix,layout_matrix)
# pos1=sfdp_layout(G)
begin=time.time()
cnum=20
part= minimize_blockmodel_dl(G, 1000,cnum,t_range=(5, 0.1))
partitions=[0 for i in range(pnum)]

for v in G.vertices():
    partitions[int(v)]=part[v]

print 'partition',str(time.time()-begin)

begin=time.time()
layout_G=build_layout_G(layout_matrix,rootid)
print 'layout_G',str(time.time()-begin)
# print len(list(layout_G.edges()))
begin=time.time()
pos=sfdp_layout(layout_G)
print 'pos',str(time.time()-begin)


graph_draw(G, pos=pos,vertex_fill_color=part, output_size=(800, 800),output= \
    pname+'treeArray'+str(evt)+ ' pnum'+str(pnum)+\
    ' cnum'+str(cnum)+' edges'+str(enum)+' rpnum'+str(repost_num)+".png")
# graph_draw(G, pos1, output_size=(1000, 1000), vertex_color=[1,1,1,0],
#             vertex_size=10, edge_pen_width=1.2,
#             vcmap=plt.cm.gist_heat_r)
# print type(pos[0])
uid_loc={}
uid_cls={}
cat_cnt=[0 for i in xrange(cnum)]
err=0
for v in G.vertices():
    try:
        i=int(v)
        cat_cnt[partitions[i]]+=1
        uid_loc[uids[i]]=[pos[v][0],pos[v][1]]
        uid_cls[uids[i]]=partitions[i]
        cat_cnt[partitions[i]]+=1
    except Exception as e:
        err+=1
print err  

# p_evtlist={}
# for uid in uids:
#     p_evtlist[uid]=[ 0 for i in range(len(treeArray))]
for i,jt in enumerate(treeArray):
    update(jt,uid_loc,uid_cls)
#     # jt['group']=str(clusters[i])
# # print 'cnum'+str(cnum)
output=open(outputfolder+'/'+pname+'treeArray'+str(evt)+ ' pnum'+str(pnum)+\
    ' cnum'+str(cnum)+' edges'+str(enum)+' rpnum'+str(repost_num)+'.json','w')
json.dump({'treeArray':treeArray,'cat_cnt':cat_cnt},output,ensure_ascii=False,encoding='utf8')

print cat_cnt



