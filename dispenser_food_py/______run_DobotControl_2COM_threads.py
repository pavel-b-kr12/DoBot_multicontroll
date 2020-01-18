import sys,threading,time
import DobotDllType as dType
api = dType.load()

def start_Mag(dobotId):
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



def start_M1(dobotId):
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

threads = []
	
def connectCOM(COMName, functionName):
	result = dType.ConnectDobot(api, COMName,115200)
	print("Connect : ", COMName)
	print("Connect : ", errorString[result[0]])
	if result[0] == 0:
		print("Connect got id: ", result[3])
		t1 = threading.Thread(target=functionName,args=(result[3],))
		threads.append(t1)
		t1.setDaemon(True)
		t1.start()
		#return id
	#else:
	#	return -1

#start_com("COM3")



maxDobotConnectCount = 10
errorString = ['Success','NotFound','Occupied']

if __name__ == '__main__':
	#print("Start search dobot, max:", maxDobotConnectCount)
	#for i in range(0, maxDobotConnectCount):
	#	result = dType.ConnectDobot(api, "",115200)
	id = connectCOM("COM3", start_M1)
	id = connectCOM("COM4", start_Mag)

	for t in threads:
		t.join()

	dType.DobotExec(api)
