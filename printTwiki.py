from sys import argv
import os


dir = os.getcwd()

for i in os.listdir(os.getcwd()):
	
	if "Results" in i:

		run = i.split("Results")[-1]

		logFile = open(i+"/MinBias_2016/pede.dump",'r')
		chi2Counter = 999
		for lineNumber, line in enumerate(logFile,1):
			if 'NREC =' in line:
			    records = line.split()
			    Nrec = int(records[2])	
			if 'Fraction of rejects' in line:
			    records = line.split("%")
			    fraction = float(records[0].split("=")[1])	
			if 'Sum(Chi^2)/Sum(Ndf)' in line:
			    chi2Counter = lineNumber
			if lineNumber == chi2Counter+2:
			   chi2 = float(line.split("=")[-1])					
		
		txt = '''
---++++ Run {0}
Further results can be found at /afs/cern.ch/user/j/jschulte/public/pp3.8T_PCL_Alignment/Results{0}

DB object can be found at /afs/cern.ch/user/j/jschulte/public/pp3.8T_PCL_Alignment/Results{0}/MinBias_2016/TkAlignment.db (Tag: testTag)
   * <verbatim>Tracks used by Pede...........{1}</verbatim>  
   * <verbatim>Chi^2/Ndof....................{2}</verbatim>
   * <verbatim>Fraction of rejects...........{3} %</verbatim>
   * PCL_SiPixAl_{0}.png: <br />   
    <img alt="PCL_SiPixAl_{0}.png" height="575" src="%ATTACHURLPATH%/PCL_SiPixAl_{0}.png" width="998" ><br />  
   * PCL_SiPixAl_Expert_{0}.png: <br />
     <img alt="PCL_SiPixAl_Expert_{0}.png" height="730" src="%ATTACHURLPATH%/PCL_SiPixAl_Expert_{0}.png" width="1246" >
		'''

		print txt.format(run,Nrec,chi2,fraction)
