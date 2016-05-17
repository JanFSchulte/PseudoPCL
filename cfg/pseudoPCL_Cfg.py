class pseudoPCLConfig:

	#millepde config:
	globalTag = "80X_dataRun2_Express_v7"
	cosmics = False
	magnetOn = True

	#data config
	dataset = "/StreamExpress/Run2016B-TkAlMinBias-Express-v2/ALCARECO"
	minNumEv = 20000

	#user config
	mail = "kiesel@cern.ch"
	workDir = "/afs/cern.ch/work/k/kiesel/alignment/CMSSW_8_0_8/src/"
	pubDir = "/afs/cern.ch/user/k/kiesel/public"
	sendMail = True

	#PCL config
	uploadToDropBox = False
	skipExpressStreamFinishedCheck = False # check if stream exprepss is complete: False:= do check, True:= Process nevertheless

