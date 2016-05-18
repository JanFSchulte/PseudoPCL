#!/bin/sh
RUNNUM="$1"
NUMFILES="$2"
CONFIG="$3"
workDir=`cat $CONFIG | grep workDir | cut -d \" -f2`
cd $workDir
eval `scram runtime -sh`
cd $workDir/PseudoPCL/Results$RUNNUM/

bash findBinaries.sh $RUNNUM $NUMFILES $CONFIG
python DoMINBIAS_pede.py $RUNNUM $CONFIG
mv DQM_plots.py $workDir/PseudoPCL/Results$RUNNUM/MinBias_2016/
cd $workDir/PseudoPCL/Results$RUNNUM/MinBias_2016/
python DQM_plots.py $CONFIG $RUNNUM
