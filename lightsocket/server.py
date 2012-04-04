# -*- coding: utf-8 -*-
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

from org.zeromq import ZMQ
from java.util import HashMap
from org.codehaus.jackson.map import ObjectMapper
from com.google.gson import Gson

#from org.msgpack import MessagePack
#from org.msgpack.annotation import MessagePackMessage

STATUS_CODES = {200:"OK",
                201:"Created",
                202:"Accepted",
                204:"No Content",
                400:"Bad Request",
                401:"Unauthorized",
                403:"Forbidden",
                404:"Not Found",
                405:"Method Not Allowed",
                408:"Request Timeout",
                500:"Internal Server Error",
                501:"Not Implemented",
                502:"Bad Gateway",
                503:"Service Unavailable"}

class Router(object):

    def __init__(self,container):
        self.container = container
        self.route_map = {}

    def add(self,name,resource):
        resource.container = self.container
        self.route_map.update({name:resource})

    def get(self,request):
        path_segment = self._get_path_segment(request)
        resource = self.route_map.get(path_segment)
        if resource:
            resp = resource.router.get(request)
        else: 
            # either we're at the end of the path so path_segment is None
            # e.g. wordgraph/vertices (self.container is "vertices")
            # or the last path_segment is not a resource so we must have found a method or param
            # e.g. worgraph/indices/people (path_segment is "people", a param to indices)
            # so call the current container's request handler
            request.path_pos = request.path_pos - 1
            resp = self.container.handle_request(request)
        return resp
            
    def remove(self,name):
        self.route_map.pop(name)


    def _get_path_segment(self,request):
        path_segment = None
        if request.path_pos < len(request.path_list):
            path_segment = request.path_list[request.path_pos]
            request.path_pos = request.path_pos + 1
        return path_segment


class Request(object):
    
    def __init__(self,request):
        self.path = request['path'] 
        self.params = request['params'] if request['params'] else {} 
        self.data = dict(request['data'])
        self.path_list = self.path.split("/")
        self.path_pos = 0

class Resource(object):
    
    # what about making the router a class var so that it's shared?

    def handle_request(self,request):
        # default request handler
        method = self.get_method(request)
        return method(request)
    
    def add_method(self,name,method):
        self.method_map.update({name:method})

    def get_method(self,request):
        path_segment = self.router._get_path_segment(request)
        return self.method_map.get(path_segment,self.not_found)

    def shutdown(self):
        raise NotImplementedError

    def log_status(self,request,response):
        path = request.path
        print "%s: %s" % (path, STATUS_CODES[response.status])
        
    def not_found(self,request):
        resp = Response(404)
        self.log_status(request,resp)
        #self.send_response(resp)
        return resp

class Response(object):

    def __init__(self,status,data=None):
        # convert data to Java Map
        self.data = data
        #self.mapper = ObjectMapper()
        self.status = status
        self.gson = Gson()

    def to_json(self,return_data):
        if return_data is True:
            data = self.data
            # or writeValueAsBytes() to serialize to a byte array
            response = dict(status=self.status,results=self.data)
            #writer = self.mapper.writer()
            #json = writer.writeValueAsString(response)
            json = self.gson.toJson(response)
        else:
            json = str(self.status)
        return json

class Server(Resource):

    # the server itself is a resource because 
    # it could have it's own methods
    
    def __init__(self,proto="tcp",host="*",port="5555"):
        self.address = "%s://%s:%s" % (proto,host,port)
        self.up = False
        self.socket = None
        #self.resource_map = {}
        self.mapper = ObjectMapper()
        self.return_data = True     
        self.router = Router(self)
    
        #self.gson = Gson()

    def handle_request(self,request):
        # you may want to add server methods someday
        return self.not_found(request)

    def shutdown(self):
        self.stop()

    #
    # Resource-specific methods
    #

    def get_resource_map(self):
        # TODO: traverse resources and build map
        pass

    def add_resource(self,name,resource):
        self.router.add(name,resource)

    def get_resource(self,name):
        return self.router.get(name)
        
    def start(self):
        print "Starting Lightsocket..."
        context = ZMQ.context(4)  # number of IO threads to use
        self.socket = context.socket(ZMQ.REP)
        self.socket.bind(self.address)
        self.up = True
        self.receive_requests()

    def receive_requests(self):
        print "Ready to receive requests..."
        while self.up:
            raw = self.socket.recv(0)
            # max req/sec with one python client: 10174 req/sec
            # python client json serialization drops 10174 to 8153
            # jython server json read drops it from 8153 to 6302
            request = Request(self.mapper.readValue(raw.tostring(),HashMap))
            # router drops is from 6302 to 4600 (this is the only thing to optimize)
            resp = self.router.get(request)
            # re-serialization drops it from 4600 to 4282 (you don't have to serialize)
            self.send_response(resp)
            #self.socket.send(str(dict()), 0)        

            # evidently pickle with zlib is not faster than json
            #decomp = zlib.decompress(raw)
            #data = cPickle.loads(decomp)
            #request = Request(data)

    def send_response(self,resp):
        self.socket.send(resp.to_json(self.return_data), 0)
        #self.socket.send("OK", 0)
                    
    def stop(self):
        self.up = False
        for resource in self.resource_map.values():
            resource.shutdown()


    




        
    
