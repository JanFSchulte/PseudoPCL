#!/bin/sh
RUNNUM="$1"
NUMFILES="$2"
CONFIG="$3"
workDir=`cat $CONFIG | grep workDir | cut -d \" -f2`
COUNTER=0
while [ $COUNTER -lt $NUMFILES ]; do
	find $workDir/PseudoPCL/Results$RUNNUM/MinBias_2016_$COUNTER/ -name 'milleBinary*' ! -empty -type f -exec mv -vv {} ./ \;
	let COUNTER=COUNTER+1
done

ls -1 milleBinary_* > BinaryFiles.txt
