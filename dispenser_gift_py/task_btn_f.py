MOV_Relative=7 #to SetPTPCmdEx_mon(api, id_m1, MOV_Relative, x, y, z, rHead, 1)
MOV_Abs=2

################################### task_btn_f

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


import traceback
def f_nm():
	return traceback.extract_stack(None, 2)[0][2]


	
m1_pos_at_pack=[-2.8,-45.88,25.5,37.22+6,1133]
m1_pos_before_pack=[23,8,-66,25.5,30+6,1133]
#J angle  movJ( m1_pos_at_pack[0],  m1_pos_at_pack[1],  m1_pos_at_pack[2], m1_pos_at_pack[3]+dobotStates[id_m1].posPivot[3], 1)

m1_pos_at_pivot=[0,0, 92,None]
m1_pos_at_mag_site=[180,  (-180),  5, (-10)] #!! must move CCW
m1_pos_at_pack_dx=-40
m1_pos_at_pack_Nx=0
m1_pos_at_pack_Ny=0
pos_rail_pivot=638  #780max to not hit 
#============= calibrate 0 at Dobot start
def t0_magR_rail_Home():
	print(f_nm())
	tskMarks_clear_all(False)
	
	queue_put(thread_magR_queue, t0_magR_rail_Home_f)
def t0_magR_rail_Home_f():
	print(f_nm())
	btn=window.t0_magR_rail_Home
	#tskStart_mark(btn, id_magR)
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	-81.21,	-13.49,	186.00,	-7.81, 1) #movJ
	dobotRailState.dobotSt.home_mon(btn)
	#tskEnd_mark(btn)
	#queue_put(thread_m1_queue, t01_m1_find_pivot_f)
	
def t01_m1_find_pivot():
	print(f_nm())
	tskMarks_clear_all(False)
	queue_put(thread_magR_queue, t01_m1_find_pivot_f)
	
def mov_m1_before_pivot():
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	-5,	-5,	186.00,	None, 1) #movJ
	dobotRailState.mov(0)
	
def t01_m1_find_pivot_f(): #115.3
	##!!if pos at pack - move before pack 
	print(f_nm())
	btn=window.t01_m1_find_pivot
	tskStart_mark(btn, id_magR)

	#safe pos
	mov_m1_before_pivot()
	#mov to pivot
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	-81.21,	-13.49,	186.00,	None, 1) #movJ


	if(m1.getPos()[3]>0):
		print('rotete to positive r')
		while(True):
			if(check_packet()): 
				break
			m1.movJ_relative([0,  0,  0, 2])
		
	#!@@ TODO replace w dType SetTRIGCmd		#TODO repeat for avg
	bFIndCCW_incr=-1
	#rot CCW	#check sensor until 1
	while(True):
		if(check_packet()): 
			break
		m1.movJ_relative([0,  0,  0, 2*bFIndCCW_incr]) #can't do mov_relative from J 0,0 even w only r 
		
	#rot CW		#check sensor until 0
	while(True):
		m1.movJ_relative([0,  0,  0, -1*bFIndCCW_incr])
		if(not check_packet()): 
			break

	#rot CCW	#check sensor until 1
	while(True):
		m1.movJ_relative([0,  0,  0, 0.1*bFIndCCW_incr])
		if(check_packet()): 
			break

	pos_m1 = m1.getPos()
	print("find target at: ",pos_m1)
	#print("find target at: ",pos_m1[0:4],"  r:", pos_m1[7])
	
	m1.posPivot=dType.GetPose(api, id_m1) #TODO draw it
	
	# firstly need mov out of pivot to use cartesian XYZ, because can't go for j 0,0 other way then movJ
	#m1.movJ([-14.221565246582031,	-47.71931838989258,	None,	None])
	
	mov_m1_before_pivot()
	
	tskEnd_mark(btn)
	if(bConnectTascs):
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
	#dType.SetArmOrientation(api, id_m1, 0, 1) #!! SetArmOrientationEx -> SetArmOrientation
	
	#pos=m1.getPos()
	
	pack0Y=-164
	packY= pack0Y - m1_pos_at_pack_Nx*(-164-(-240))
	
	m1.mov( [-23, pack0Y+33, 50, None]) #safe before all pack

	l_1stPacket=31
	l_lastPacket=838
	dL=193-l_1stPacket
	
	dobotRailState.mov(31+dL*m1_pos_at_pack_Nx) #right to left
	dobotRailState.mov(l_lastPacket-dL*m1_pos_at_pack_Nx) #left to right
	m1.mov( [-23, packY+33, 50, None]) #before row, before detect
	m1.mov( [-23, packY, 50, None]) #at row, detect
	
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
	#if(bConnectTascs):
	#queue_put(thread_m1_queue, t2_m1_check_packet_f)



def t2_m1_check_packet_h():
	print(f_nm())
	tskMarks_clear_all(False)

	queue_put(thread_m1_queue, t2_m1_check_packet_f)

def t2_m1_check_packet_f():
	print(f_nm())
	global m1_pos_at_pack_Nx
	global m1_pos_at_pack_Ny
	btn=window.t2_m1_check_packet
	tskStart_mark(btn, id_m1)
	
	if(check_packet()):
		#if(bConnectTascs):
		#queue_put(thread_m1_queue,t3_m1_get_packet_f)
		#time.sleep(2) ####
		pass
	else:
		m1_pos_at_pack_Ny+=1
		if(m1_pos_at_pack_Ny==5):
			m1_pos_at_pack_Ny=0
			m1_pos_at_pack_Nx+=1
			if(m1_pos_at_pack_Nx==4):
				m1_pos_at_pack_Nx=0
				m1_pos_at_pack_Ny=0
				print("!! out of packets") #TODO
		print("no packet, so going to other pos Nx: %1s, Ny: %1s"%(m1_pos_at_pack_Nx,m1_pos_at_pack_Ny))
			
		
		''' #x first
		m1_pos_at_pack_Nx+= 1
		if(m1_pos_at_pack_Nx==4):
			m1_pos_at_pack_Nx=0
			m1_pos_at_pack_Ny+=1
			if(m1_pos_at_pack_Ny==5):
				print("!! out of packets") #TODO
				m1_pos_at_pack_Ny=0
				m1_pos_at_pack_Nx=0
		'''	
			
		#if(bConnectTascs):
		#queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
		#time.sleep(2) ####
	
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

	#!!slow
	m1.mov([None, None, 232, None]) #pack get
	m1.mov_relative([0, 33, 0, 0])
	'''
	movJ(id_m1,[38.7,	-75.1,	228,	27.8]) #move
	movJ(id_m1,[56.8,	-84.6,	228,	22]) #
	movJ(id_m1,[84,		-81.6,	228,	-2]) #
	#move rail
	current_pose = dType.GetPose(api, id_magR)
	dType.SetPTPWithLCmdEx(api, id_magR, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 580, 1)
	
	movJ(id_m1,[83.7,	-29,	228,	27]) #place
	movJ(id_m1,[83.7,	-29,	145,	27]) #
	
	movJ(id_m1,[83.7,	8.8,	152,	2]) #out from it
	movJ(id_m1,[83.7,	8.8,	160,	2]) #
	
	movJ(id_m1,[60,		-38,	200,	2]) #
	movJ(id_m1,[31,		-48,	140,	2]) #
	
	#move rail
	current_pose = dType.GetPose(api, id_magR)
	dType.SetPTPWithLCmdEx(api, id_magR, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], pos_rail_pivot, 1)
	'''

	#print_state_id(id_m1)

	
	print("put t5_magL_wait_m1_f")
	#queue_put(thread_magL_queue,t5_magL_wait_m1_f)

	tskEnd_mark(btn)
	
	if(bConnectTascs):
		queue_put(thread_m1_queue,t4_m1_packet_to_mag_site_f)
	
def t4_m1_packet_to_mag_site_h():
	print(f_nm())
	tskMarks_clear_all(False)
	queue_put(thread_m1_queue,t4_m1_packet_to_mag_site_f)
def t4_m1_packet_to_mag_site_f():
	print(f_nm())
	btn=window.t4_m1_packet_to_mag_site
	tskStart_mark(btn, id_m1)
	
	m1.mov([145.73712158203125, -55.97725296020508, None, None])
	dobotRailState.mov(790) #обход кабельканала
	m1.mov([207.6950225830078, -15, None, None])
	dobotRailState.mov(345)
	m1.movJ([80.67733001708984, -72.33910369873047, None, None]) #[230.28469848632812, 226.3616180419922, 233.01654052734375, -298.7320861816406, 80.67733001708984, -72.33910369873047, 233.01654052734375, -307.0703125]
	m1.movJ([82.94929504394531, -26.055644989013672, None, None]) #[133.78848266601562, 366.01922607421875, 233.01654052734375, -277.3055725097656, 82.94929504394531, -26.055644989013672, 233.01654052734375, -334.19921875]
	
	#drop
	m1.movJ([None, None, 123, None])#[133.78848266601562, 366.01922607421875, 124.68587493896484, -277.3055725097656, 82.94929504394531, -26.055644989013672, 124.68587493896484, -334.19921875]
	#out
	dobotRailState.mov(242)
	m1.movJ([0, 0, 200, None])
	
	#print("working long t4_m1_packet_to_mag_site_f")
	#time.sleep(2) ####
	#print_state_id(id_m1)


	
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
	
	
	
	
