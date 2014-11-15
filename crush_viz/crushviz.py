#!/bin/sh
#eric.mourgaya@gmail.com
#licence MIT
#generate a graph  from crushmap informations

import json
from StringIO import StringIO
import json
import httplib
import gv
import pydot
import pygraphviz as pgv

#import pydot
# dictionnary contained all  objet  in the cluster map
crushobjdict={}
# hastable for id and  name of object
idhash={}
# ceph-rest-api link
cephrestapi="radosgw1-r:5000"

colortype={"osd":"blue","host":"red","rack":"grey","row":"black","room":"green","datacenter":"orange","root":"purple"}


def load_conf(jfile):
    '''
        load the json file and return the json object
    '''
    datasource = open(jfile, "r")
    data = json.load(datasource)
    datasource.close()
    return data


def getjosddump(cephapi):
    '''
        get json file from ceph-rest-api
    '''
    restapi = httplib.HTTPConnection(cephapi)
    restapi.request("GET", "/api/v0.1/osd/dump.json")
    response=restapi.getresponse()
    if (response.status == 200) :
        data = response.read()
        io = StringIO(data)
        josddump = json.load(io)
    return josddump

#crushjobj=getjosddump(cephrestapi)
# uncomment  the previous line  and comment the  following oneto take  jason from dump.json file input from a file

crushjobj=load_conf('dump.json')

# create a dictionnary  of object with a structure {type-name, id, name} for devices section  so it refer to device

for item in crushjobj['output']['devices']:
    idhash[item['id']]=item['name']
    item['type_name']="osd"
    item['items']=[]
    crushobjdict[item['id']]=item

for item in crushjobj['output']['buckets']:
     buckdict={}
     idhash[item['id']]=item['name']
     buckdict['type_name']=item['type_name']
     buckdict['id']=item['id']
     buckdict['name']=item['name']
     buckdict['items']=item["items"]
     crushobjdict[item['id']]=buckdict


# create an empty the graph
gr=pgv.AGraph(strict=False,directed=True)

# create the file dot and all the  rules.
for  obj in crushobjdict:
    if crushobjdict[obj]['type_name'] != "osd":
            gr.add_node(crushobjdict[obj]['name'],color=colortype[crushobjdict[obj]['type_name']])   
             #gr.add_node(crushobjdict[obj],color='blue')   
            for item in crushobjdict[obj]['items']:
                gr.add_edge((crushobjdict[obj]['name'],idhash[item['id']]))
    elif  crushobjdict[obj]['type_name'] == "osd":
        gr.add_node(crushobjdict[obj]['name'],color=colortype[crushobjdict[obj]['type_name']])   
        
gr.write("cache_relationship.dot")

        
gr.layout()
gr.draw('cache_relationship.png')


