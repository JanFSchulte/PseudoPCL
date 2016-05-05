#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "No config provided"
  exit 1
fi

workDir=`cat $1 | grep workDir | cut -d \" -f2`

cd $workDir/PseudoPCL

python CheckFinished.py
if [ $? -ne 1 ]
then 
exit
fi

echo "New Job `date`" >> acronjobTestSTDOUT.txt
echo "New Job `date`" >> CurrentlyRunning.txt
python DoByRuns.py "$1" >> acronjobTestSTDOUT.txt
echo "Job Finished `date`" >> acronjobTestSTDOUT.txt
echo "Job Finished `date`" >> CurrentlyRunning.txt
