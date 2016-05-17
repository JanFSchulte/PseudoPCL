#!/usr/bin/python
#-------------------------------
# Latest update: 2016.05.17
# by Jan for PCL Alignment
#-------------------------------
import sys, os, pwd, commands
import optparse, shlex, re
import math
from ROOT import *
import ROOT

from sys import argv

if len(argv) < 3:
	print "No Config File or run number given"
	sys.exit(0)
path = argv[1].split("/cfg")[0]
sys.path.append(path+"/cfg/")
config = argv[1].split("/")[-1].split(".")[0]
configModule = __import__(config)

pseudoPCLConfig = configModule.pseudoPCLConfig

runNumber = argv[2]


PedeSucess = False
Nrec = 0
Movements = False
Error = False
Significant = False
DBupdated = False

#Significance of movement must be above
SigCut = 2.5

#Cutoff in micro-meter & micro-rad
Xcut = 5.0
tXcut = 30.0 #thetaX
Ycut = 10.0
tYcut = 30.0 #thetaY
Zcut = 15.0
tZcut = 30.0 #thetaZ

#maximum movement in micro-meter/rad
MaxMoveCut = 200
MaxErrorCut = 10
HitMax = False
HitErrorMax = False

#Order same as "Bins" List
Xobs = [0.,0.,0.,0.,0.,0.]
XobsErr = [0.,0.,0.,0.,0.,0.]
tXobs = [0.,0.,0.,0.,0.,0.]
tXobsErr = [0.,0.,0.,0.,0.,0.]
Yobs = [0.,0.,0.,0.,0.,0.]
YobsErr = [0.,0.,0.,0.,0.,0.]
tYobs = [0.,0.,0.,0.,0.,0.]
tYobsErr = [0.,0.,0.,0.,0.,0.]
Zobs = [0.,0.,0.,0.,0.,0.]
ZobsErr = [0.,0.,0.,0.,0.,0.]
tZobs = [0.,0.,0.,0.,0.,0.]
tZobsErr = [0.,0.,0.,0.,0.,0.]

Bins = ["FPIX(x+,z-)", "FPIX(x-,z-)", "BPIX(x+)", "BPIX(x-)", "FPIX(x+,z+)", "FPIX(x-,z+)"]

Cutoffs = [Xcut, Ycut, Zcut, tXcut, tYcut, tZcut]
Multiplier = [10000.,10000.,10000.,1000000.,1000000.,1000000.]


logFileName = "millepede.log"

if not os.path.exists(logFileName):
    PedeSucess = False
    Nrec = 0
    Movements = False
    Error = False
    Significant = False
    DBupdated = False
    
else:

    logFile = open(logFileName,'r')
    for line in logFile:
        if 'NREC =' in line:
            records = line.split()
            Nrec = int(records[2])
            if Nrec < 25000:
                PedeSucess = False
                Movements = False
                Error = False
                Significant = False
                DBupdated = False

fileName = "millepede.res"

if not os.path.exists(fileName):
    PedeSucess = False
    Nrec = 0
    Movements = False
    Error = False
    Significant = False
    DBupdated = False
else:
    resFile = open(fileName,'r')
    resLines = resFile.readlines()
    resLines.pop(0)
    for line in resLines:
	#print line
	movement = line.split()
        if len(movement) > 3:
            PedeSucess = True
            alignable = int(movement[0])%10-1
            ObsMove = float(movement[3])*Multiplier[alignable]
            ObsErr = float(movement[4])*Multiplier[alignable]
            det = -1
            if int(movement[0]) >= 60 and int(movement[0]) <= 69:
                det = 2 #TPBHalfBarrel (x+)
            elif int(movement[0]) >= 8780 and int(movement[0]) <= 8789:
                det = 3 #TPBHalfBarrel (x-)
            elif int(movement[0]) >= 17520 and int(movement[0]) <= 17529:
                det = 4 #TPEHalfCylinder (x+,z+)
            elif int(movement[0]) >= 22380 and int(movement[0]) <= 22389:
                det = 5 #TPEHalfCylinder (x-,z+)
            elif int(movement[0]) >= 27260 and int(movement[0]) <= 27269:
                det = 0 #TPEHalfCylinder (x+,z-)
            elif int(movement[0]) >= 32120 and int(movement[0]) <= 32129:
                det = 1 #TPEHalfCylinder (x-,z-)
            else:
                continue
            
            if alignable == 0 and det >= 0 and det <= 5:
                Xobs[det] = ObsMove
                XobsErr[det] = ObsErr
            elif alignable == 1 and det >= 0 and det <= 5:
                Yobs[det] = ObsMove
                YobsErr[det] = ObsErr
            elif alignable == 2 and det >= 0 and det <= 5:
                Zobs[det] = ObsMove
                ZobsErr[det] = ObsErr
            elif alignable == 3 and det >= 0 and det <= 5:
                tXobs[det] = ObsMove
                tXobsErr[det] = ObsErr
            elif alignable == 4 and det >= 0 and det <= 5:
                tYobs[det] = ObsMove
                tYobsErr[det] = ObsErr
            elif alignable == 5 and det >= 0 and det <= 5:
                tZobs[det] = ObsMove
                tZobsErr[det] = ObsErr
       	    
            if abs(ObsMove) > MaxMoveCut:
                Movements = False
                Error = False
                Significant = False
                DBupdated = False
                HitMax = True
		continue
            elif abs(ObsMove) > Cutoffs[alignable]:
                Movements = True
                if abs(ObsErr) > MaxErrorCut:
                    Error = False
                    Significant = False
                    DBupdated = False
                    HitErrorMax = True
		    continue
                else:
                    Error = True
                    if abs(ObsMove/ObsErr) > SigCut:
                        Significant = True
			DBupdated = True
           
#print "Xpos: ", Xobs
#print "XposErr: ", XobsErr
ROOT.gStyle.SetOptStat(0)
#ROOT.gStyle.SetTitleFontSize(0.05)

c = ROOT.TCanvas("PCL_SiPixAl_Expert","PCL_SiPixAl_Expert",1500,800)
c.Divide(3,2)
c_1 = c.cd(1)
Xpos = ROOT.TH1F("Xpos","Xpos",6,0.,6.)
Xpos.SetTitle("#Delta X;;#mu m")
Xpos.SetMinimum(-MaxMoveCut)
Xpos.SetMaximum(MaxMoveCut)
Xpos.SetLabelSize(0.06)
Xpos_1 = ROOT.TH1F("Xpos_1","Xpos_1",6,0.,6.)
Xpos_2 = ROOT.TH1F("Xpos_2","Xpos_2",6,0.,6.)
Xpos_3 = ROOT.TH1F("Xpos_3","Xpos_3",6,0.,6.)
for bin in Bins:
    Xpos.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
    Xpos.SetBinContent(Bins.index(bin)+1,Xobs[Bins.index(bin)])
    Xpos.SetBinError(Bins.index(bin)+1,XobsErr[Bins.index(bin)])
    Xpos_1.SetBinContent(Bins.index(bin)+1,Xobs[Bins.index(bin)])
    Xpos_1.SetBinError(Bins.index(bin)+1,(Xpos_1.GetBinContent(Bins.index(bin)+1)/SigCut))
    Xpos_2.SetBinContent(Bins.index(bin)+1,Xcut)
    Xpos_3.SetBinContent(Bins.index(bin)+1,-Xcut)
Xpos_2.SetLineWidth(2)
Xpos_3.SetLineWidth(2)
Xpos_1.SetLineWidth(2)
Xpos.SetLineWidth(2)
Xpos_2.SetLineColor(kRed+2)
Xpos_3.SetLineColor(kRed+2)
Xpos.SetLineColor(kBlack)
Xpos.SetFillColor(kGreen+3)
Xpos.Draw("HIST")
Xpos_1.SetLineColor(kRed+2)
Xpos_1.Draw("E1 SAME")
Xpos.Draw("AE1 SAME") 
Xpos_2.Draw("HIST same")
Xpos_3.Draw("HIST same")
c_4 = c.cd(4)
Xrot = ROOT.TH1F("Xrot","Xrot",6,0.,6.)
Xrot.SetTitle("#Delta #theta_{X};;#mu rad")
Xrot.SetMinimum(-MaxMoveCut)
Xrot.SetMaximum(MaxMoveCut)
Xrot.SetLabelSize(0.06)
Xrot_1 = ROOT.TH1F("Xrot_1","Xrot_1",6,0.,6.)
Xrot_2 = ROOT.TH1F("Xrot_2","Xrot_2",6,0.,6.)
Xrot_3 = ROOT.TH1F("Xrot_3","Xrot_3",6,0.,6.)
for bin in Bins:
        Xrot.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
        Xrot.SetBinContent(Bins.index(bin)+1,tXobs[Bins.index(bin)])
        Xrot.SetBinError(Bins.index(bin)+1,tXobsErr[Bins.index(bin)])
        Xrot_1.SetBinContent(Bins.index(bin)+1,tXobs[Bins.index(bin)])
        Xrot_1.SetBinError(Bins.index(bin)+1,(Xrot_1.GetBinContent(Bins.index(bin)+1)/SigCut))
        Xrot_2.SetBinContent(Bins.index(bin)+1,tXcut)
        Xrot_3.SetBinContent(Bins.index(bin)+1,-tXcut)
Xrot_2.SetLineWidth(2)
Xrot_3.SetLineWidth(2)
Xrot_1.SetLineWidth(2)
Xrot.SetLineWidth(2)
Xrot_2.SetLineColor(kRed+2)
Xrot_3.SetLineColor(kRed+2)
Xrot.SetLineColor(kBlack)
Xrot.SetFillColor(kGreen+3)
Xrot.Draw("HIST")
Xrot_1.SetLineColor(kRed+2)
Xrot_1.Draw("E1 SAME")
Xrot.Draw("AE1 SAME")
Xrot_2.Draw("HIST same")
Xrot_3.Draw("HIST same")

c_2 = c.cd(2)
Ypos = ROOT.TH1F("Ypos","Ypos",6,0.,6.)
Ypos.SetTitle("#Delta Y;;#mu m")
Ypos.SetMinimum(-MaxMoveCut)
Ypos.SetMaximum(MaxMoveCut)
Ypos.SetLabelSize(0.06)
Ypos_1 = ROOT.TH1F("Ypos_1","Ypos_1",6,0.,6.)
Ypos_2 = ROOT.TH1F("Ypos_2","Ypos_2",6,0.,6.)
Ypos_3 = ROOT.TH1F("Ypos_3","Ypos_3",6,0.,6.)
for bin in Bins:
    Ypos.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
    Ypos.SetBinContent(Bins.index(bin)+1,Yobs[Bins.index(bin)])
    Ypos.SetBinError(Bins.index(bin)+1,YobsErr[Bins.index(bin)])
    Ypos_1.SetBinContent(Bins.index(bin)+1,Yobs[Bins.index(bin)])
    Ypos_1.SetBinError(Bins.index(bin)+1,(Ypos_1.GetBinContent(Bins.index(bin)+1)/SigCut))
    Ypos_2.SetBinContent(Bins.index(bin)+1,Ycut)
    Ypos_3.SetBinContent(Bins.index(bin)+1,-Ycut)
Ypos_2.SetLineWidth(2)
Ypos_3.SetLineWidth(2)
Ypos_1.SetLineWidth(2)
Ypos.SetLineWidth(2)
Ypos_2.SetLineColor(kRed+2)
Ypos_3.SetLineColor(kRed+2)
Ypos.SetLineColor(kBlack)
Ypos.SetFillColor(kGreen+3)
Ypos.Draw("HIST")
Ypos_1.SetLineColor(kRed+2)
Ypos_1.Draw("E1 SAME")
Ypos.Draw("AE1 SAME") 
Ypos_2.Draw("HIST same")
Ypos_3.Draw("HIST same")
c_5 = c.cd(5)
Yrot = ROOT.TH1F("Yrot","Yrot",6,0.,6.)
Yrot.SetMinimum(-MaxMoveCut)
Yrot.SetMaximum(MaxMoveCut)
Yrot.SetLabelSize(0.06)
Yrot.SetTitle("#Delta #theta_{Y};;#mu rad")
Yrot_1 = ROOT.TH1F("Yrot_1","Yrot_1",6,0.,6.)
Yrot_2 = ROOT.TH1F("Yrot_2","Yrot_2",6,0.,6.)
Yrot_3 = ROOT.TH1F("Yrot_3","Yrot_3",6,0.,6.)
for bin in Bins:
        Yrot.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
        Yrot.SetBinContent(Bins.index(bin)+1,tYobs[Bins.index(bin)])
        Yrot.SetBinError(Bins.index(bin)+1,tYobsErr[Bins.index(bin)])
        Yrot_1.SetBinContent(Bins.index(bin)+1,tYobs[Bins.index(bin)])
        Yrot_1.SetBinError(Bins.index(bin)+1,(Yrot_1.GetBinContent(Bins.index(bin)+1)/SigCut))
        Yrot_2.SetBinContent(Bins.index(bin)+1,tYcut)
        Yrot_3.SetBinContent(Bins.index(bin)+1,-tYcut)
Yrot_2.SetLineWidth(2)
Yrot_3.SetLineWidth(2)
Yrot_1.SetLineWidth(2)
Yrot.SetLineWidth(2)
Yrot_2.SetLineColor(kRed+2)
Yrot_3.SetLineColor(kRed+2)
Yrot.SetLineColor(kBlack)
Yrot.SetFillColor(kGreen+3)
Yrot.Draw("HIST")
Yrot_1.SetLineColor(kRed+2)
Yrot_1.Draw("E1 SAME")
Yrot.Draw("AE1 SAME")
Yrot_2.Draw("HIST same")
Yrot_3.Draw("HIST same")
c_3 = c.cd(3)
Zpos = ROOT.TH1F("Zpos","Zpos",6,0.,6.)
Zpos.SetTitle("#Delta Z;;#mu m")
Zpos.SetMinimum(-MaxMoveCut)
Zpos.SetMaximum(MaxMoveCut)
Zpos.SetLabelSize(0.06)
Zpos_1 = ROOT.TH1F("Zpos_1","Zpos_1",6,0.,6.)
Zpos_2 = ROOT.TH1F("Zpos_2","Zpos_2",6,0.,6.)
Zpos_3 = ROOT.TH1F("Zpos_3","Zpos_3",6,0.,6.)
for bin in Bins:
    Zpos.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
    Zpos.SetBinContent(Bins.index(bin)+1,Zobs[Bins.index(bin)])
    Zpos.SetBinError(Bins.index(bin)+1,ZobsErr[Bins.index(bin)])
    Zpos_1.SetBinContent(Bins.index(bin)+1,Zobs[Bins.index(bin)])
    Zpos_1.SetBinError(Bins.index(bin)+1,(Zpos_1.GetBinContent(Bins.index(bin)+1)/SigCut))
    Zpos_2.SetBinContent(Bins.index(bin)+1,Zcut)
    Zpos_3.SetBinContent(Bins.index(bin)+1,-Zcut)
Zpos_2.SetLineWidth(2)
Zpos_3.SetLineWidth(2)
Zpos_1.SetLineWidth(2)
Zpos.SetLineWidth(2)
Zpos_2.SetLineColor(kRed+2)
Zpos_3.SetLineColor(kRed+2)
Zpos.SetLineColor(kBlack)
Zpos.SetFillColor(kGreen+3)
Zpos.Draw("HIST")
Zpos_1.SetLineColor(kRed+2)
Zpos_1.Draw("E1 SAME")
Zpos.Draw("AE1 SAME") 
Zpos_2.Draw("HIST same")
Zpos_3.Draw("HIST same")
c_6 = c.cd(6)
Zrot = ROOT.TH1F("Zrot","Zrot",6,0.,6.)
Zrot.SetTitle("#Delta #theta_{Z};;#mu rad")
Zrot.SetMinimum(-MaxMoveCut)
Zrot.SetMaximum(MaxMoveCut)
Zrot.SetLabelSize(0.06)
Zrot_1 = ROOT.TH1F("Zrot_1","Zrot_1",6,0.,6.)
Zrot_2 = ROOT.TH1F("Zrot_2","Zrot_2",6,0.,6.)
Zrot_3 = ROOT.TH1F("Zrot_3","Zrot_3",6,0.,6.)
for bin in Bins:
        Zrot.GetXaxis().SetBinLabel(Bins.index(bin)+1,bin)
        Zrot.SetBinContent(Bins.index(bin)+1,tZobs[Bins.index(bin)])
        Zrot.SetBinError(Bins.index(bin)+1,tZobsErr[Bins.index(bin)])
        Zrot_1.SetBinContent(Bins.index(bin)+1,tZobs[Bins.index(bin)])
        Zrot_1.SetBinError(Bins.index(bin)+1,(Zrot_1.GetBinContent(Bins.index(bin)+1)/SigCut))
        Zrot_2.SetBinContent(Bins.index(bin)+1,tZcut)
        Zrot_3.SetBinContent(Bins.index(bin)+1,-tZcut)
Zrot_2.SetLineWidth(2)
Zrot_3.SetLineWidth(2)
Zrot_1.SetLineWidth(2)
Zrot.SetLineWidth(2)
Zrot_2.SetLineColor(kRed+2)
Zrot_3.SetLineColor(kRed+2)
Zrot.SetLineColor(kBlack)
Zrot.SetFillColor(kGreen+3)
Zrot.Draw("HIST")
Zrot_1.SetLineColor(kRed+2)
Zrot_1.Draw("E1 SAME")
Zrot.Draw("AE1 SAME")
Zrot_2.Draw("HIST same")
Zrot_3.Draw("HIST same")

c.Print("PCL_SiPixAl_Expert_%s.pdf"%runNumber)
c.Print("PCL_SiPixAl_Expert_%s.png"%runNumber)

c1 = ROOT.TCanvas("PCL_SiPixAl","PCL_SiPixAl",1000,600)
c1.Divide(1,3)
Text_DB = ROOT.TPaveText(.0,.0,1.,1.)
Text_DB.SetBorderSize(1)
Text_DB.AddText("DB updated")
Text_Pede = ROOT.TPaveText(.0,.0,1.,1.)
Text_Pede.SetBorderSize(1)
Text_Pede.AddText("Alignment Performed Nrec = {0}".format(Nrec)) 
Text_DB.SetTextSize(0.15)
Text_Pede.SetTextSize(0.15)
if PedeSucess :
    Text_Pede.SetFillColor(kGreen)
else :
    Text_Pede.SetFillColor(kRed)

Text_DB.SetFillColor(kGray)
if HitMax or HitErrorMax:
    Text_DB.SetFillColor(kRed)
    command = "echo \"New Alignment to be Updated "+os.getcwd()+" Nrec={0}\" | mail -s \"New Prompt Unreasonable Alignment Update\" {1}".format(Nrec,pseudoPCLConfig.mail)
    os.system(command)
elif DBupdated:
    Text_DB.SetFillColor(kOrange)
    command = "echo \"New Alignment to be Updated "+os.getcwd()+" Nrec={0}\" | mail -s \"New Prompt Reasonable Alignment Update\" {1}".format(Nrec,pseudoPCLConfig.mail)
    os.system(command)
c1.cd(1)
Text_DB.Draw()
c1.cd(3)
Text_Pede.Draw()
c1_2 = c1.cd(2)
c1_2.Divide(4,1)
c1_2.cd(1)
Text_Move = ROOT.TPaveText(.0,.0,1.,1.)
Text_Move.SetBorderSize(1)
Text_Move.AddText("Movement Seen")
Text_Move.SetTextSize(0.15)
if Movements: 
        Text_Move.SetFillColor(kOrange) 
else : 
        Text_Move.SetFillColor(kGray)
Text_Move.Draw()
c1_2.cd(2)
Text_Move2 = ROOT.TPaveText(.0,.0,1.,1.)
Text_Move2.SetBorderSize(1)
Text_Move2.AddText("#splitline{Movement}{Reasonable}")
Text_Move2.SetTextSize(0.15)
Text_Move2.SetFillColor(kGray)
if HitMax: 
        Text_Move2.SetFillColor(kRed) 
elif Movements : 
        Text_Move2.SetFillColor(kGreen)
Text_Move2.Draw()
c1_2.cd(3)
Text_Error = ROOT.TPaveText(.0,.0,1.,1.)
Text_Error.SetBorderSize(1)
Text_Error.AddText("#splitline{Uncertainty}{Reasonable}")
Text_Error.SetTextSize(0.15)
Text_Error.SetFillColor(kGray)
if HitErrorMax :
        Text_Error.SetFillColor(kRed)
elif Error :
	Text_Error.SetFillColor(kGreen)
Text_Error.Draw()
c1_2.cd(4)
Text_Signif = ROOT.TPaveText(.0,.0,1.,1.)
Text_Signif.SetBorderSize(1)
Text_Signif.AddText("#splitline{Movement}{Significant}")
Text_Signif.SetTextSize(0.15)
if Significant :
        Text_Signif.SetFillColor(kGreen)
else :
        Text_Signif.SetFillColor(kGray)
Text_Signif.Draw()

c1.Print("PCL_SiPixAl_%s.pdf"%runNumber)
c1.Print("PCL_SiPixAl_%s.png"%runNumber)

file = ROOT.TFile("PCL_SiPixAl_DQM.root","RECREATE")
c1.Write()
c.Write()
file.Close()
