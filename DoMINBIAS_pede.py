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
sys.path.append("../cfg/")
config = sys.argv[2].split("/")[-1].split(".")[0]
configModule = __import__(config)
print configModule
pseudoPCLConfig = configModule.pseudoPCLConfig
sendEmailNotification = pseudoPCLConfig.sendMail
start = time.time()
print 'Start New Job ' + str(time.asctime())

#One inputfile
Inputfile=open('TkMinBias0','r')
InputFiles=Inputfile.readlines()
Inputfile.close()

# Binary Files
BinaryFiles=open('BinaryFiles.txt','r')
ListFiles=BinaryFiles.readlines()
BinaryFiles.close()

# Template alignment cfg
TemplateCfg=open('alignment_pede_minbias.py','r')
TemplateCfgLines=TemplateCfg.readlines()
TemplateCfg.close()

# New alignment cfg that will have the DAS query files input
NewCfg=open('alignment_pede.py','w')

# Go through the template configuration file (alignment_BASE.py) and add the file names for the run into a new file (alignment_New.py)
for cfgLine in TemplateCfgLines:
    if 'INSERTFILENAME' in cfgLine:
	newline=''
	for fileName in InputFiles:
	    newline = newline+cfgLine.replace('\'INSERTFILENAME\'','\''+fileName[:-1]+'\'')
    elif 'INSERT_BINARY_NAMES' in cfgLine:
        newline=''
        for fileName in ListFiles:
            newline = newline+cfgLine.replace('\'INSERT_BINARY_NAMES\'','\''+fileName[:-1]+'\'')
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
directory = "MinBias_2016"

if os.path.exists(directory):
    command = "rm -rf "+directory
    os.system(command)

command = "mkdir " + directory
os.system(command)
command = "mv alignment_pede.py " + directory + "/."
os.system(command)
command = "mv %s/PseudoPCL/Results"%pseudoPCLConfig.workDir+RUNNUM+"/milleBinary*.dat " + directory + "/."
os.system(command)
os.getcwd()
os.chdir(directory)
os.getcwd()

#Run alignment
os.system('cmsRun alignment_pede.py')
end = time.time()

#if os.path.exists("milleBinaryISN.dat"):
#    command = "rm milleBinaryISN.dat"
#    os.system(command)

os.chdir("..")

if sendEmailNotification:
               command = "echo \"New Alignment Pede\" | mail -s \"New Prompt Alignment Update\" %s"%pseudoPCLConfig.mail
               print command
               os.system(command)
