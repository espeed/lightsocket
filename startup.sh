#!/bin/bash
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

# These are only hints on the needed jars.
#export CLASSPATH=$CLASSPATH:/home/user/src/jzmq/src/zmq.jar                   
#export CLASSPATH=$CLASSPATH:/home/user/src/google-gson-1.7.1/gson-1.7.1.jar
#export CLASSPATH=$CLASSPATH:/home/user/src/jackson/trunk/regression/*
#export CLASSPATH=$CLASSPATH:/home/user/src/rexster/target/rexster-0.7-SNAPSHOT-standalone/lib/*
#export CLASSPATH=$CLASSPATH:/home/user/src/blueprints/blueprints-core/target/blueprints-core-1.1-SNAPSHOT.jar
#export CLASSPATH=$CLASSPATH:/home/user/src/blueprints/blueprints-dex-graph/target/blueprints-dex-graph-1.1-SNAPSHOT.jar
#export CLASSPATH=$CLASSPATH:/home/user/src/blueprints/blueprints-neo4jbatch-graph/target/blueprints-neo4jbatch-graph-1.1-SNAPSHOT.jar

# Modify this to point to your Rexster root dir and lib dir
REXSTER_DIR=/home/james/projects/whybase/rexster
REXSTER_LIB="${REXSTER_DIR}/target/rexster-0.7-SNAPSHOT-standalone/lib/*"

# Modify this to point to your Jython dir
JYTHON_DIR=/home/james/jython2.5.2

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


