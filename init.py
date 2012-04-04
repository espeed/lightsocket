from lightsocket.server import Server
from lightsocket.resources.example import Example
from lightsocket.resources.blueprints import Neo4jGraph, Neo4jBatchGraph

#
# Modify this init script by adding your own custom Resources
#

# Example Resource
example = Example()

# WordGraph Resource
#wordgraph = Neo4jGraph("/home/james/data/wordgraph")
#wordgraph.graph.setMaxBufferSize(1000)

# Initialize the server, add your resources, and start the server
server = Server()
server.add_resource("example",example)
#server.add_resource("wordgraph",wordgraph)
server.start()

