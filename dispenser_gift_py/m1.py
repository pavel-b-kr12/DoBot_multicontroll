import sys,threading,time
import DobotDllType as dType

from test_ui import *

def left_M1(dobotId):
	print("start_M1 id:", dobotId) #dobotId
	print("start_M1 id:",dType.GetQueuedCmdCurrentIndex(api, dobotId))
	
	dType.SetArmOrientation(api, dobotId, 0, 0)
	dType.SetQueuedCmdStartExec(api,dobotId)
	
	############################## paste script here:
	dType.SetQueuedCmdClear(api, dobotId) #could not work	https://forum.dobot.cc/t/clear-command-queue/250
	dType.SetPTPCmdEx(api, dobotId, 0, 200,  (-200),  230, 0, 1) #(api, dobotId, ptpMode, x, y, z, rHead, isQueued=0)
	dType.SetPTPCmdEx(api, dobotId, 0, 350,  0,  20, 0, 1)
	##############################
	print("start_M1 end")

