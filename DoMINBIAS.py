#!/usr/bin/env python
import sys
import subprocess
import os
from ROOT import TH1F, TFile, TH1
from subprocess import *
import time
import shlex
import stat

RUNNUM = sys.argv[1]
runNumber = sys.argv[2]
sys.path.append("../cfg/")
config = sys.argv[3].split("/")[-1].split(".")[0]
configModule = __import__(config)
print configModule
pseudoPCLConfig = configModule.pseudoPCLConfig

sendEmailNotification = False
start = time.time()
print 'Start New Job ' + str(time.asctime())

FileNames=open('TkMinBias'+runNumber,'r')
ListFiles = FileNames.readlines()
FileNames.close()

print 'Run Number ' + runNumber

# Template alignment cfg
TemplateCfg=open('alignment_mille_minbias.py','r')
TemplateCfgLines=TemplateCfg.readlines()
TemplateCfg.close()

# New alignment cfg that will have the DAS query files input
NewCfg=open('alignment_mille_%s.py'%str(runNumber),'w')

# Go through the template configuration file (alignment_BASE.py) and add the file names for the run into a new file (alignment_New.py)
for cfgLine in TemplateCfgLines:
    if 'INSERTFILENAME' in cfgLine:
        newline=''
        for fileName in ListFiles:
            newline = newline+cfgLine.replace('INSERTFILENAME',fileName[:-1])
    elif 'INSERT_NUM' in cfgLine:
    	newline = cfgLine.replace('INSERT_NUM',str(runNumber))
    elif 'RUN_NUMBER' in cfgLine:
	newline = cfgLine.replace('RUN_NUMBER',str(RUNNUM))
    elif 'INSERTGT' in cfgLine:
    	newline = cfgLine.replace('INSERTGT',str(pseudoPCLConfig.globalTag))
    elif 'INSERTMAGNETSTATUS' in cfgLine:
    	newline = cfgLine.replace('INSERTMAGNETSTATUS',str(pseudoPCLConfig.magnetOn))
    elif 'INSERTCOSMICSSTATUS' in cfgLine:
    	newline = cfgLine.replace('INSERTCOSMICSSTATUS',str(pseudoPCLConfig.cosmics))
    else:
        newline=cfgLine
    NewCfg.write(newline)


NewCfg.close()

#Make directory for specific run and move files into there
directory = "MinBias_2016_" + runNumber

if os.path.exists(directory):
    command = "rm -rf "+directory
    os.system(command)

command = "mkdir " + directory
os.system(command)
command = "mv alignment_mille_%s.py "%str(runNumber) + directory + "/."
os.system(command)
command = "cp TkMinBias"+runNumber+" " + directory + "/."
os.system(command)
os.getcwd()
os.chdir(directory)
os.getcwd()

#Run alignment
os.system('cmsRun alignment_mille_%s.py'%str(runNumber))
end = time.time()

#if os.path.exists("milleBinaryISN.dat"):
#    command = "rm milleBinaryISN.dat"
#    os.system(command)

os.chdir("..")

if sendEmailNotification:
               command = "echo \"New Alignment Mille File for Run " + runNumber + "\" | mail -s \"New Prompt Alignment Update\" %s"%pseudoPCLConfig.mail
               print command
               os.system(command)
