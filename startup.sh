#!/bin/bash
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

export CLASSPATH=$CLASSPATH:/home/hermann-local/src/jzmq/src/zmq.jar
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/google-gson-1.7.1/gson-1.7.1.jar
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/jackson/trunk/regression/*
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/rexster/target/rexster-0.7-SNAPSHOT-standalone/lib/*
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/blueprints/blueprints-core/target/blueprints-core-1.1-SNAPSHOT.jar
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/blueprints/blueprints-dex-graph/target/blueprints-dex-graph-1.1-SNAPSHOT.jar
export CLASSPATH=$CLASSPATH:/home/hermann-local/src/blueprints/blueprints-neo4jbatch-graph/target/blueprints-neo4jbatch-graph-1.1-SNAPSHOT.jar

# Modify this to point to your Rexster root dir and lib dir
REXSTER_DIR=/home/james/packages/tinkerpop/rexster
REXSTER_LIB="${REXSTER_DIR}/rexster-server/target/rexster-server-0.9-SNAPSHOT-standalone/lib/*"

# Modify this to point to your Jython dir
JYTHON_DIR=/home/james/packages/jython2.5.2

# Modify this to point to your lib dir with the jzmq libs
# (Dir not needed, when JZMQ libs are installed in regular sytem lib path)
JZMQ_LIB_DIR=/usr/local/lib

#
# You don't need to modify anyting past this point.
#

DIR="$( cd "$( dirname "$0" )" && pwd )"
export JYTHONPATH=$JYTHONPATH:$DIR;
export CLASSPATH=$CLASSPATH:$DIR:$REXSTER_LIB;

# TODO: catch CTRL-C and do server shutdown()

$JYTHON_DIR/bin/jython -Djava.library.path=$JZMQ_LIB_DIR $DIR/init.py

