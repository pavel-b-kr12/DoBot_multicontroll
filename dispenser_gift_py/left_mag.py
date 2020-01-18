import sys,threading,time
import DobotDllType as dType

from test_ui import *

def left_mag_1(dobotId):
	print("start_Mag id:", dobotId)
	print("start_Mag GetQueuedCmdCurrentIndex:",dType.GetQueuedCmdCurrentIndex(api, dobotId))
	dType.SetQueuedCmdClear(api, dobotId) #could not work	https://forum.dobot.cc/t/clear-command-queue/250
	
	
	dType.SetDeviceWithL(api, dobotId, 1) #! 1
	dType.SetWAITCmdEx(api, dobotId, 1, 1) #api, dobotId, waitTime, isQueued
	
	dType.SetQueuedCmdStartExec(api,dobotId)
	############################## paste script here:
	current_pose = dType.GetPose(api, dobotId)
	#print("start_Mag current_pose:", current_pose)
	dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 500, 1) #SetPTPWithLCmdEx(api, dobotId, ptpMode, x, y, z, rHead,  l, isQueued=0)
	
	current_pose = dType.GetPose(api, dobotId)
	#print("start_Mag current_pose:", current_pose)
	dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 400, 1)
	##############################
	
	
	#dType.SetQueuedCmdStartExec(api, dobotId)
	#dType.SetDeviceWithL(api, dobotId, 0)
	#dType.SetWAITCmdEx(api, dobotId, 5, 1)
	#while(True):

	#dType.SetPTPCmd(api, dobotId, 1, pos[0], pos[1], pos[2], pos[3])

	#dType.dSleep(111)
	
	# dType.SetEndEffectorParamsEx(api, 59.7, 0, 0, 1)
	# for count in range(10):
		# current_pose = dType.GetPose(api)
		# dType.SetPTPCmdEx(api, 2, 200, 0, 0, current_pose[3], 1)
		# dType.SetEndEffectorGripperEx(api, 1, 1)
		# dType.SetWAITCmdEx(api, 1, 1)
		# current_pose = dType.GetPose(api)
		# dType.SetPTPCmdEx(api, 2, 200, 0, 0, current_pose[3], 1)
		# dType.SetEndEffectorGripperEx(api, 1, 0)
		# dType.SetWAITCmdEx(api, 1, 1)
		#while(True):
	
	print("start_Mag end")