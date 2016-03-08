#encoding: utf-8
import csv
import glob
import datetime
import sys
import os
import json
import time
reload(sys)
#中文错误
sys.setdefaultencoding( "utf-8" )
'''
@author l
    CSV批处理
    '''
name='shuziweiba'
inputfolder='data/'+name
outputfolder='data/'+name+'Tree'
evt=0
list_dirs=os.walk(inputfolder)
num=0
def addNode(parent, node, pid):
    if pid == parent['mid']:
        parent['dr']+=1
        # 
        #we can't merge the same child, miss the mid!!!!!!!!
        #
        # tag=False
        # node['dep']=parent['dep']+1
        # for child in parent['children']:
        #     if child['uid']==node['uid']:
        #         '''for evt in node['evtlist']:
        #             child['evtlist'].append(evt)'''
        #         child['evtlist']+=node['evtlist']
        #         child['times']+=1
        #         child['mid']+=node['mid']
        #         tag=True
        #         break
        # if not tag:
        parent['children'].append(node)
        parent['childnum']+=1
        return True
    else:
        for child in parent['children']:
            if addNode(child,node,pid):
                return True
    return False
def calChild(root):
    root['childnum']=len(root['children'])
    root['totalChildren']=0
    root['tr']=0
    for child in root['children']:
        cnt=calChild(child)
        root['totalChildren']+=1+cnt[0]
        root['tr']+=1+cnt[1]
    return [root['totalChildren'],root['tr']]
#time.struct_time(tm_year=2015, tm_mon=10, tm_mday=30, tm_hour=13, tm_min=52, tm_sec=46, tm_wday=4, tm_yday=303, tm_isdst=-1)
# 
evt=0
wronginfo=open('wrongfile','w')
wrongfile=0
for root, dirs, files in list_dirs:
    for ccfile in files:
        try:
            root={}
            evt+=1
            cfile=open(inputfolder+"/"+ccfile)
            jnodes=json.load(cfile)
            wrong=0
            crt=0
            if len(jnodes)<1:
                continue
            for jnode in jnodes:
                node={}
                node['mid']=jnode['mid']
                node['uid']=jnode['uid']
                node['dep']=0
                node['childnum']=0
                node['children']=[]
                # root['original_text']=jnode['original_text']
                node['evtlist']=[]
                node['dr']=0   # the number of direct repost
                node['tr']=0   # the number of all child drect repost
                #node['t']=time.mktime(time.strptime(jnode['t'], '%Y-%m-%d %H:%M:%S'))
                node['t']=jnode['t']
                node['text']=jnode['text']
                node['pid']=jnode['parent']
                node['evtlist'].append(evt)
                node['name']=jnode['username']
                node['times']=1
                if str(jnode['parent'])=='':
                    root=node
                    root['original_text']=jnode['original_text']

                else:
                    if not addNode(root,node,jnode['parent']):
                        wrong+=1
                    else:
                        crt+=1

            cfile.close() 
            if wrong>crt:
                print root['mid']
            root['totalChildren']=0
            root['tr']=0
            wronginfo.write('in '+str(crt)+' lost '+str(wrong)+'\n')
            # print 'wrong '+str(wrong)+' crt '+str(crt)
            calChild(root)
            output=open(outputfolder+'/'+ccfile[:ccfile.index('.')]+".json","w")         
            json.dump(root,output,ensure_ascii=False)
            output.close()
        except Exception as e:
            print str(e) + ' ' + ccfile
            wrongfile+=1
            continue

print wrongfile




                
