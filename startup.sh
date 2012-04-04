#!/bin/bash
#
# Copyright 2011 James Thornton (http://jamesthornton.com)
# BSD License (see LICENSE for details)
#

# Modify this to point to your Rexster root dir and lib dir
REXSTER_DIR=/home/james/packages/tinkerpop/rexster
REXSTER_LIB="${REXSTER_DIR}/rexster-server/target/rexster-server-0.9-SNAPSHOT-standalone/lib/*"

# Modify this to point to your Jython dir
JYTHON_DIR=/home/james/packages/jython2.5.2

#
# You don't need to modify anyting past this point.
#

DIR="$( cd "$( dirname "$0" )" && pwd )"
export JYTHONPATH=$JYTHONPATH:$DIR;
export CLASSPATH=$CLASSPATH:$DIR:$REXSTER_LIB;

# TODO: catch CTRL-C and do server shutdown()

$JYTHON_DIR/bin/jython $DIR/init.py



