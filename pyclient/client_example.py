# -*- coding: utf-8 -*-
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#
# This is an example Python client (not Jython) for Lightsocket.
#
# You need to install the ZeroMQ Python binding before you run it.
# Get pyzmq here https://github.com/zeromq/pyzmq or install via: 
# $ easy_install pyzmq
#
# Then startup the lightsocket server, and then run this client via:
# $ python client_example.py
#

import zmq
import json
import time

class ClientExample(object):

    def __init__(self,server="tcp://localhost:5555"):
        self.server = server
        self.socket = self._connect()
        self.count = 0
        self.start_time = None

    def _connect(self):        
        print "Connecting to Lightsocket..."
        context = zmq.Context(8)
        socket = context.socket(zmq.REQ)
        socket.connect(self.server)
        return socket

    def send_request(self,path,params,data):
        request = dict(path=path,params=params,data=data)
        message = json.dumps(request)
        self.socket.send(message)
        raw = self.socket.recv()
        resp = json.loads(raw)        
        return resp

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        end_time = time.time()
        run_time = end_time - self.start_time
        print "Requests Per Second: ", self.count / run_time

    def display_progress(self):
        if self.start_time:
            self.count = self.count + 1
            if (self.count % 1000) == 0:
                elapsed = time.time() - self.start_time
                print self.count, elapsed, elapsed / self.count, self.count / elapsed

    def run_test(self,requests=30000):
        path = "example/test"
        self.start_timer()
        for x in range(0,requests):
            self.send_request(path,params={},data={})
            self.display_progress()
        self.stop_timer()

    # Example how to add node to the wordgraph DB
    def create_node(self):
        path = "wordgraph/vertices/create"
        data = dict(name="James",city="Dallas")
        params = None
        resp = self.send_request(path,params,data)
        print resp
        node_id = resp['results']['_id']
        return node_id


client = ClientExample()
client.run_test()
#client.create_node()
