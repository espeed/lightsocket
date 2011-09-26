# -*- coding: utf-8 -*-
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

import random
from lightsocket.server import Resource, Response, Router

class ExampleProxy(Resource):

    # This example class is used in composition of the primary resource (below). 
    # Each resource has the same structure and required methods.
    def __init__(self):
        self.router = Router(self)
        self.method_map = dict(yep=self.yep)

    # This is the default request handler. 
    # A request handler is required in each class.
    def handle_request(self,request):
        method = self.get_method(request)
        return method(request)

    # This method is public because it has been added to method_map.
    def yep(self,request):
        data = "yep: " + str(random.random())
        return Response(200,data)


class Example(Resource):

    def __init__(self):
        # The router is required in each object.
        # It taks one arg for the container, which will always be self.
        self.router = Router(self)

        # Add any objects you want to include in this resource
        # the name will be the path segment
        # e.g. /example/proxy
        self.router.add("proxy",ExampleProxy())

        # Add this object's public methods
        self.method_map = dict(test=self.test)

    # This is the default request handler. 
    # A request handler is required in each class.
    def handle_request(self,request):
        method = self.get_method(request)
        return method(request)

    # This method is not public because it's not in method_map.
    def shutdown(self,params):
        return Response(200,None)

    # This method is public because it has been added to method_map.
    def test(self,request):
        data = "test: " + str(random.random())
        return Response(200,data)



        
