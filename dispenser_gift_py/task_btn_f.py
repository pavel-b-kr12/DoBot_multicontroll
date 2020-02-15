MOV_Relative=7 #to SetPTPCmdEx_mon(api, id_m1, MOV_Relative, x, y, z, rHead, 1)
MOV_Abs=2

################################### task_btn_f
'''
def t3_m1_get_packet_h():
	#
	btn=window.t3_m1_get_packet
	rID=id_m1
	tskStart_mark(btn, rID)


	rID=id_magL
	print(rID)
	dType.SetDeviceWithL(api, rID, 1)
	dType.SetWAITCmdEx(api, rID, 100, 1)
	current_pose = dType.GetPose(api, rID)
	dType.SetPTPWithLCmdEx(api, rID, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 100, 1)
	dType.SetPTPWithLCmdEx(api, rID, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 130, 1)

	rID=id_m1
	gripperOpen()
	
	current_pose = dType.GetPose(api, rID)
	dType.SetPTPCmdEx_mon(api, rID, 2, 50,  (-160),  233, 99, 1)
	current_pose = dType.GetPose(api, rID)
	dType.SetPTPCmdEx_mon(api, rID, 2, 50,  (-393),  233, 99, 1)
	dType.SetWAITCmdEx(api, rID, 2000, 1)
	current_pose = dType.GetPose(api, rID)
	dType.SetPTPCmdEx_mon(api, rID, 2, 50,  (-393),  200, 99, 1)


	
	gripperClose()
	
	#time.sleep(2)
	tskEnd_mark(btn)
'''

#################task

'''
@dataclass
class M1_pos_at_pack:
	x: float = 180
	y: float = -320
	z: float = 30
	r: float = -111
	dx: float = -80 #between packets
	N: int = 0
m1_pos_at_pack = M1_pos_at_pack()
'''



def f_nm():
	import traceback
	return traceback.extract_stack(None, 2)[0][2]

m1_pos_at_pack=[180,  (-320),  30, (-111)]
m1_pos_at_mag_site=[180,  (-180),  5, (-10)] #!! must move CCW
m1_pos_at_pack_dx=-40
m1_pos_at_pack_N=0;

#============= calibrate 0 at Dobot start
def t0_magR_rail_Home():
	print(f_nm())
	tskMarks_clear_all(False)
	
	queue_put(thread_magR_queue, t0_magR_rail_Home_f)
def t0_magR_rail_Home_f():
	print(f_nm())
	btn=window.t0_magR_rail_Home
	#tskStart_mark(btn, id_magR)
	btnHome_f(id_magR,btn)
	#tskEnd_mark(btn)
	queue_put(thread_m1_queue, t01_m1_find_pivot_f)
	
def t01_m1_find_pivot():
	print(f_nm())
	tskMarks_clear_all(False)
	queue_put(thread_magR_queue, t01_m1_find_pivot_f)
def t01_m1_find_pivot_f():
	print(f_nm())
	btn=window.t01_m1_find_pivot
	tskStart_mark(btn, id_magR)
	
	while(True):
		#dType.SetPTPCmdEx_mon(api, id_m1, MOV_Relative, None, None, None, 1, 1)# move a bit r-axis
	
		if(check_packet()): # check sensor
			break
	
	dobotStates[id_m1].posPivot=dType.GetPose(api, id_m1)
	
	tskEnd_mark(btn)
	queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
	
#=============	
	

def t1_m1_pos_at_packet_h():
	print(f_nm())
	tskMarks_clear_all(False) #also clean queues
	#thread_m1.join(); #TODO  or wait thread_m1_queue empty
	
	
	queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
def t1_m1_pos_at_packet_f():
	print(f_nm())
	btn=window.t1_m1_pos_at_packet
	tskStart_mark(btn, id_m1)

	#print_state_m1(id_m1)
	#dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0]+m1_pos_at_pack_dx*m1_pos_at_pack_N,  m1_pos_at_pack[1],  m1_pos_at_pack[2],  m1_pos_at_pack[3], 1)
	#print_state_id(id_m1)
	#time.sleep(3) ####
	dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0]+m1_pos_at_pack_dx*m1_pos_at_pack_N,  m1_pos_at_pack[1]-20,  m1_pos_at_pack[2],  m1_pos_at_pack[3], 1) #to IR sensor distance
	print_state_id(id_m1)
	#time.sleep(3) ####
	'''
	dType.SetPTPCmdEx_mon(api, 2, 180,  (-280),  30, 22, 1)
	
	current_pose = dType.GetPose(api, id_m1)
	dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0],  m1_pos_at_pack[1],  m1_pos_at_pack[2], current_pose[3], 1) #SetPTPCmdEx_mon(api, dobotId, ptpMode, x, y, z, rHead, isQueued=0)
	if(bDebug):
		time.sleep(1)
	#current_pose = dType.GetPose(api, id_m1)
	#dType.SetPTPCmdEx_mon(api, id_m1, 2, 257,  0,  136, current_pose[3], 1)

	print("m1_pos_at_packet", dType.GetPoseEx(api, id_m1, 1))
	'''
	tskEnd_mark(btn)
	
	queue_put(thread_m1_queue, t2_m1_check_packet_f)



def t2_m1_check_packet_h():
	print(f_nm())
	tskMarks_clear_all(False)

	queue_put(thread_m1_queue, t2_m1_check_packet_f)

def t2_m1_check_packet_f():
	print(f_nm())
	global m1_pos_at_pack_N
	btn=window.t2_m1_check_packet
	tskStart_mark(btn, id_m1)
	
	if(check_packet()):
		queue_put(thread_m1_queue,t3_m1_get_packet_f)
		time.sleep(2) ####
	else:
		print("no packet, so going to other pos")
		m1_pos_at_pack_N+= 1
		if(m1_pos_at_pack_N==3):
			m1_pos_at_pack_N=0;
		queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
		time.sleep(2) ####
	
	tskEnd_mark(btn)
	

	
def check_packet():
	bPacketFound= (dType.GetIODI(api, id_m1, 17)[0]==1) or window.checkBox_IR_debug.isChecked()
	#print("check_packet IR sensor:", bPacketFound, " ", end="") #!?? nw in thread
	dType.printPosNow(api, id_m1, bPrint=True)
	masgPacket=printColorizeStr("",bPacketFound, ["No","Yes"])
	sys.stdout.write("  check_packet IR sensor: %s   \r" % (masgPacket) )
	sys.stdout.flush()
	return bPacketFound
	
	
def t3_m1_get_packet_h():
	print(f_nm())
	tskMarks_clear_all(False)

	queue_put(thread_m1_queue,t3_m1_get_packet_f)
def t3_m1_get_packet_f():
	print(f_nm())
	btn=window.t3_m1_get_packet
	tskStart_mark(btn, id_m1)

	
	dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0]+m1_pos_at_pack_dx*m1_pos_at_pack_N,  m1_pos_at_pack[1],  m1_pos_at_pack[2]+10,  m1_pos_at_pack[3]+30, 1)
	print_state_id(id_m1)
	time.sleep(2) ####
	
	print("put t5_magL_wait_m1_f")
	queue_put(thread_magL_queue,t5_magL_wait_m1_f)

	tskEnd_mark(btn)
	
	queue_put(thread_m1_queue,t4_m1_packet_to_mag_site_f)
	
def t4_m1_packet_to_mag_site_h():
	print(f_nm())
	tskMarks_clear_all(False)
	queue_put(thread_m1_queue,t4_m1_packet_to_mag_site_f)
def t4_m1_packet_to_mag_site_f():
	print(f_nm())
	btn=window.t4_m1_packet_to_mag_site
	tskStart_mark(btn, id_m1)
	
	print("working long t4_m1_packet_to_mag_site_f")
	dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_mag_site[0],  m1_pos_at_mag_site[1],  m1_pos_at_mag_site[2],  m1_pos_at_mag_site[3], 1)
	print_state_id(id_m1)
	time.sleep(2) ####


	
	#dType.SetWAITCmdEx(api, id_m1, 1, 1) #api, dobotId, waitTime, isQueued
	#dType.SetQueuedCmdStartExec(api,dobotId)
	
	#current_pose = dType.GetPose(api, dobotId)
	#print("start_Mag current_pose:", current_pose)
	#dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 500, 1) #SetPTPWithLCmdEx(api, dobotId, ptpMode, x, y, z, rHead,  l, isQueued=0)
	
	#current_pose = dType.GetPose(api, dobotId)
	#print("start_Mag current_pose:", current_pose)
	#dType.SetPTPWithLCmdEx(api, dobotId, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 400, 1)
	
	#end thread. Next loop started from mag
	tskEnd_mark(btn)
	
	

	
def t5_magL_wait_m1_h():
	print(f_nm())
	tskMarks_clear_all(False)
	
	queue_put(thread_magL_queue,t5_magL_wait_m1_f)
	
def t5_magL_wait_m1_f():
	print(f_nm())
	btn=window.t5_magL_wait_m1
	
	dType.SetPTPCmdEx_mon(api, id_magL, 2, pos_gift_get[0],  pos_gift_get[1],  pos_gift_get[2], pos_gift_get[3], 1)
	print_state_id(id_magL)
	time.sleep(2) ####
	
	tskWait_mark(btn, id_m1)
	print('t5_magL_wait_m1_f     wait join m1')
	thread_m1_queue.join()
	tskStart_mark(btn, id_m1)
	#time.sleep(1)
	
	queue_put(thread_magL_queue,t6_magL_give_and_back_f)
	
	tskEnd_mark(btn)

pos_gift_get =[270,  53,  -58, 0]
pos_gift_place =[238,  -177,  91, -1]
	
def t6_magL_give_and_back_h():
	print(f_nm())
	tskMarks_clear_all(False)
	queue_put(thread_magL_queue,t6_magL_give_and_back_f)
	
def t6_magL_give_and_back_f(): #! re not back
	print(f_nm())
	btn=window.t6_magL_give_and_back
	tskStart_mark(btn, id_m1)


	dType.SetPTPCmdEx_mon(api, id_magL, 2, pos_gift_place[0],  pos_gift_place[1],  pos_gift_place[2], pos_gift_place[3], 1)
	print_state_id(id_magL)
	time.sleep(2) ####
	
		    # SetIOMultiplexingEx(api, dobotId, 2,  1, isQueued)
    # SetIOMultiplexingEx(api, dobotId, 4,  2, isQueued)
    # SetIODOEx(api, dobotId, 2, enableCtrl, isQueued)
    # SetIOPWMEx(api, dobotId, 4, 10000, power, isQueued)
	
			#dType.SetIODOEx(api, rID, 17, 1, 1)
			#dType.SetIODOEx(api, rID, 18, 0, 1)
			#dType.SetWAITCmdEx(api, rID, 500, 1)
		# dType.SetIODOEx(api, rID, 17, 1, 1)
		# dType.SetIODOEx(api, rID, 18, 1, 1)
		
	queue_put(thread_m1_queue, t2_m1_check_packet_f) #start next loop  ##!! move to  t5_magL_wait_m1_f
	
	tskEnd_mark(btn)
	tskMarks_clear_all(False)	
	
	
	
	
