def show_exception_and_exit(exc_type, exc_value, tb):
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)

import sys
sys.excepthook = show_exception_and_exit

import threading,time
import DobotDllType as dType


  
api = dType.load()

errorString = ['Success','NotFound','Occupied']
maxDobotConnectCount = 10

Magic_id = -1
M1_id = -1

if __name__ == '__main__':
	try:
		Magic_id = dType.ConnectDobot(api, "COM4",115200)[3]
		M1_id = dType.ConnectDobot(api, "COM3",115200)[3]
		print("Magic_id : ", Magic_id)
		print("M1_id : ", M1_id)
		
		dobotId = Magic_id
		dType.SetQueuedCmdStartExec(api,dobotId)
		
		dType.SetDeviceWithL(api, dobotId, 1) #!!!! set 1
		##dType.GetDeviceWithL(api, dobotId)
		#dType.SetWAITCmdEx(api, dobotId, 1, 1) #api, dobotId, waitTime, isQueued
		####################################### paste script here:
		current_pose = dType.GetPose(api, dobotId)
		print("start_Mag current_pose:", current_pose)
		dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 500, 1) #SetPTPWithLCmdEx(api, dobotId, ptpMode, x, y, z, rHead,  l, isQueued=0)
	
		current_pose = dType.GetPose(api, dobotId)
		print("start_Mag current_pose:", current_pose)
		dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 400, 1)
		#######################################
		#dType.SetQueuedCmdStartExec(api,dobotId)
		#dType.SetWAITCmdEx(api, dobotId, 1, 1)
		dType.DisconnectDobot(api, dobotId)



		dobotId = M1_id
		#dType.SetQueuedCmdStartExec(api,dobotId)
		####################################### paste script here:
		dType.SetPTPCmdEx(api, dobotId, 0, 200,  (-200),  230, 0, 1) #(api, dobotId, ptpMode, x, y, z, rHead, isQueued=0)
		dType.SetPTPCmdEx(api, dobotId, 0, 350,  0,  20, 0, 1)
		#######################################
		dType.DisconnectDobot(api, dobotId)
		
		#dType.SetPTPCmd(

		#SetQueuedCmdStopExec
		print("end")
		#dType.DobotExec(api)
		#print("end after DobotExec ")
	except Exception as ex:
		print(ex)
