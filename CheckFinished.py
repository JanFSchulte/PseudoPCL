#!/usr/bin/env python

import sys, os

if os.path.exists('CurrentlyRunning.txt'):
    IsRunningFile=open('CurrentlyRunning.txt','r')
    Lines = IsRunningFile.readlines()
    IsRunningFile.close()

    LastLine = Lines[-1]
    if 'Job Finished' in LastLine:
        sys.exit(1)
    else:
        sys.exit(0)
else:
    IsRunningFile=open('CurrentlyRunning.txt','w')
    IsRunningFile.close()
    sys.exit(1)
