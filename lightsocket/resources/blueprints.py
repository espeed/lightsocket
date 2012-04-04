# -*- coding: utf-8 -*-
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

from java.lang import Long

from com.tinkerpop.rexster.util import ElementHelper
from com.tinkerpop.blueprints.pgm.impls.neo4j import Neo4jGraph
from com.tinkerpop.blueprints.pgm.impls.neo4jbatch import Neo4jBatchGraph
#from com.tinkerpop.pipes.util import FluentPipeline


from lightsocket.server import Resource, Response, Router

class VertexProxy(Resource):

    _type = "vertex"
    
    def __init__(self,graph):
        self.router = Router(self)
        self.graph = graph
        self.method_map = dict(create=self.create,
                               get=self.get,
                               get_all=self.get_all)

    def create(self,request):
        vertex = self.graph.addVertex(None)
        for key, value in request.data.items():
            if key == "element_type":
                element_type = value
            try:
                vertex.setProperty(key,value)
            except:
                print "WOULDN'T SET: ", element_type, key, value
                
        data = dict(_id=vertex.id,_type=self._type)
        return Response(201,data)
        
    def get(self,request):
        eid = request.params['eid']
        vertex = self.graph.getVertex(long(eid))
        return Response(200,vertex)

    def get_all(self,request):
        results = []
        for vertex in self.graph.getVertices():
            results.append(vertex.id)
        data = dict(_results=results,_type=self._type)
        return Response(200,data)

    def remove(self,request):
        raise NotImplementedError

class EdgeProxy(Resource):

    _type = "edge"

    def __init__(self,graph):
        self.router = Router(self)
        self.graph = graph
        self.method_map = dict(create=self.create)

    def create(self,request):
        outV_id = Long(request.params['outV'])
        inV_id = Long(request.params['inV'])
        label = request.params['label']
        data = request.data
        outV = self.graph.getVertex(outV_id)
        inV = self.graph.getVertex(inV_id)
        edge = self.graph.addEdge(data,outV,inV,label)
        data = dict(_id=edge.id,_outV=outV.id,label=label,_inV=inV.id,_type=self._type)
        return Response(201,data)
    
    def get(self,eid):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

class IndexProxy(Resource):

    def __init__(self,graph):
        self.router = Router(self)
        self.graph = graph
        self.method_map = dict(flush=self.flush,
                               create_manual=self.create_manual,
                               create_automatic=self.create_automatic,
                               get=self.get,
                               get_all=self.get_all,
                               drop=self.drop)

    def flush(self):
        # This is necessary prior to using indices to ensure that indexed data 
        # is available to index queries. This method is not part of the 
        # Blueprints Graph or IndexableGraph API.
        self.graph.flushIndices()

    def create_manual(self,index_name,index_class):
        index = self.graph.createManualIndex(index_name,index_class)
        return Response(201,index.getPropertyMap())

    def create_automatic(self,index_name,index_class,index_keys):
        index = self.graph.createAutomaticlIndex(index_name,index_class,index_keys)
        return Response(201,index.getPropertyMap())

    def get(self,index_name,index_class):
        index = self.graph.getIndex(index_name,index_class)
        return Response(200,index.getPropertyMap())

    def get_all(self):
        indices = self.graph.getIndices()
        return Response(200,indices.getPropertyMap())

    def drop(self,index_name):
        self.graph.dropIndex(index_name)


class Gremlin(Resource):
    pass
    

class Blueprints(Resource):
    """Abstract method"""

    def __init__(self,db_dir):
        self.db_dir = db_dir
        self._startup()
        self.router = Router(self)
        self.router.add("vertices", VertexProxy(self.graph))
        self.router.add("edges", EdgeProxy(self.graph))
        self.router.add("indices", IndexProxy(self.graph))
        #self.router.add("gremlin", Gremlin(self.graph))
        self.method_map = dict(startup=self.startup,
                               shutdown=self.shutdown) 
        
    def _startup(self):
        self.graph = self.graph_class(self.db_dir)

    def startup(self,request):
        self._startup()
        return Response(200)

    def shutdown(self,request):
        print "Shutting down graph..."
        self.graph.shutdown()
        return Response(200)
    #
    # Resource-specific methods
    #

    def clear(self):
        raise NotImplementedError

        
class Neo4jGraph(Blueprints):
    
    graph_class = Neo4jGraph

class Neo4jBatchGraph(Blueprints):

    graph_class = Neo4jBatchGraph
