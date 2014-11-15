#eric.mourgaya@gmail.com
#licence MIT
# Generate a graph between caches and pools, this script request ceph-rest-api to get informations.
# also generate the  dot file.

#sudo easy_install python-graph-core
#sudo apt-get install libgv-python
#sudo easy_install python-graph-dot
#sudo apt-get install libgraphviz-dev
#sudo easy_install pygraphviz

import json
from StringIO import StringIO
import json
import httplib
import gv
import pydot
import pygraphviz as pgv


# variables:
cephrestapi="radosgw1-r:5000"


#manage options

# dictionnary contained all  objet  in the cluster map
#crushobjdict={}

def load_conf(jfile):
    '''
        load the json file and return the json object
    '''
    datasource = open(jfile, "r")
    data = json.load(datasource)
    datasource.close()
    return data

# define the  cephrestapi target

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


#poolosddump=getjosddump(cephrestapi)
# uncomment  the previous line  and comment the  following oneto take  jason from dump.json file input from a file
poolosddump=load_conf('dump.json')

id_pool={}


# create an empty the graph
gr=pgv.AGraph(strict=False,directed=True)


def  addnode2graph(graph,list_nodes):
    '''
        graph: is the name of graph
        list_nodes: list of nodes to add on the graph
        add all nodes in lis_nodes in the graph
    '''
    graph.add_nodes_from(list_nodes)


list_node=[]
# add  nodes in  list_node
for item in poolosddump['output']['pools']:
    id_pool[item['pool']]=item['pool_name'] 
    list_node.append(item['pool_name'])

# add node to graph
addnode2graph(gr,list_node)

# create edges and add it to graph
for item in poolosddump['output']['pools']:
    id_pool[item['pool']]=item['pool_name'] 
    if item['tiers'] !=[]:
        gr.add_edge((id_pool[item['tiers'][0]],item['pool_name']))

# create the  dot file
gr.write("cache_relationship.dot")

# create a  png
gr.layout()
gr.draw('cache_relationship.png')

