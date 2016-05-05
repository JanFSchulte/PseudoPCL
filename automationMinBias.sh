#!/bin/sh
RUN="$1"
COUNTER="$2"
CONFIG="$3"
workDir=`cat $CONFIG | grep workDir | cut -d \" -f2`

cd $workDir
eval `scram runtime -sh`
cd $workDir/PseudoPCL/Results$RUN/

python DoMINBIAS.py $RUN $COUNTER $CONFIG

