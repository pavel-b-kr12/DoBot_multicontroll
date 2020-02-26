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


def movJ(id_, posJ): #relative to pivot r-axis
	print("posJ:",posJ)
	dType.SetPTPCmdEx_mon(api, id_, 4, posJ[0],  posJ[1],  posJ[2], posJ[3]+dobotStates[id_].posPivot[3], 1)
	print("now:",dType.GetPose(api, id_))
def movJ_def(id_, j1,j2,j3,j4): #set None to stay current
	pos_now=dType.GetPose(api, id_)
	if(j1 is None):
		j1=pos_now[4]
	if(j2 is None):
		j2=pos_now[5]
	if(j3 is None):
		j3=pos_now[6]
	if(j4 is None):
		j4=pos_now[7]
	else:
		j4+=dobotStates[id_].posPivot[3]
		
	#print("posJ:",[j1,j2,j3,j4])
	dType.SetPTPCmdEx_mon(api, id_, 4, j1, j2, j3, j4, 1)
	print("now:",dType.GetPose(api, id_))
def movRail(id_, L):
	current_pose = dType.GetPose(api, id_)
	dType.SetPTPLParamsEx(api, id_,200,30,1)
	dType.SetPTPWithLCmdEx(api, id_, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], L, 1)
	
	
m1_pos_at_pack=[-2.8,-45.88,25.5,37.22+6,1133]
m1_pos_before_pack=[23,8,-66,25.5,30+6,1133]
#J angle  movJ( m1_pos_at_pack[0],  m1_pos_at_pack[1],  m1_pos_at_pack[2], m1_pos_at_pack[3]+dobotStates[id_m1].posPivot[3], 1)

m1_pos_at_mag_site=[180,  (-180),  5, (-10)] #!! must move CCW
m1_pos_at_pack_dx=-40
m1_pos_at_pack_Nx=0
m1_pos_at_pack_Ny=0
pos_rail_pivot=760  #780max to not hit 
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
	##!!if pos at pack - move before pack 
	print(f_nm())
	btn=window.t01_m1_find_pivot
	tskStart_mark(btn, id_magR)
	
	#move to target pos
	movRail(id_magR, pos_rail_pivot)
	#movJ_def(id_m1, None,None, 84,None) #z 37
	movJ_def(id_m1, 0,0, 84,None) #z 37
	
	pos_m1 = dType.GetPose(api, id_m1)
	print(pos_m1)
	
	#rot CCW
	#check sensor until 1
	while(True):
		if(check_packet()): 
			break
		dType.SetPTPCmdEx(api, id_m1, 6, 0,  0,  0, 2, 1)
		
	#rot CW
	#check sensor until 0
	while(True):
		dType.SetPTPCmdEx(api, id_m1, 6, 0,  0,  0, -1, 1)
		if(not check_packet()): 
			break
	pos_m1 = dType.GetPose(api, id_m1)
	print(pos_m1)
	#rot CCW
	#check sensor until 1
	while(True):
		dType.SetPTPCmdEx(api, id_m1, 6, 0,  0,  0, 0.1, 1)
		#move CCW
		#dType.SetPTPCmdEx_mon(api, id_m1, MOV_Relative, None, None, None, 1, 1)# move a bit r-axis
		
		# check sensor until 1
		if(check_packet()): 
			break
			
	pos_m1 = dType.GetPose(api, id_m1)
	print("find target at: ",pos_m1[0:4],"  r:", pos_m1[7])
	
	#repeat for avg
	
	dobotStates[id_m1].posPivot=dType.GetPose(api, id_m1)
	
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
	
	dType.SetArmOrientation(api, id_m1, 0, 1) #!! SetArmOrientationEx -> SetArmOrientation
	
	movJ(id_m1, [8,  -48,  30, 30.2-20.7]) #m1_pos_before_pack
	movRail(id_magR, pos_rail_pivot-m1_pos_at_pack_Nx*175)
	movJ(id_m1, [-4.5, -35, 30, 30.2-20.7] ) #check
	#movJ(id_m1,[-14,  (-25),  27, 31]) #m1_pos_at_pack at this pos sensor can check, and Z up can pick packet. But cant move Y
	
	#print(dobotStates[id_m1])
	#print(dobotStates[id_m1].posPivot[3])
	#print("m1 pos:", dType.GetPose(api, id_m1))
	#print(m1_pos_at_pack[0],  m1_pos_at_pack[1],  m1_pos_at_pack[2], m1_pos_at_pack[3]+dobotStates[id_m1].posPivot[3])
	
	#print_state_id(id_m1)
	#dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0]+m1_pos_at_pack_dx*m1_pos_at_pack_N,  m1_pos_at_pack[1],  m1_pos_at_pack[2],  m1_pos_at_pack[3], 1)
	#print_state_id(id_m1)
	#time.sleep(3) ####
	
	#dType.SetPTPCmdEx_mon(api, id_m1, 2, m1_pos_at_pack[0]+m1_pos_at_pack_dx*m1_pos_at_pack_N,  m1_pos_at_pack[1]-20,  m1_pos_at_pack[2],  m1_pos_at_pack[3], 1) #to IR sensor distance
	#print_state_id(id_m1)
	
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
		print("no packet, so going to other pos")
		m1_pos_at_pack_Nx+= 1
		if(m1_pos_at_pack_Nx==3):
			m1_pos_at_pack_Nx=0
			m1_pos_at_pack_Ny+=1
			if(m1_pos_at_pack_Ny==5):
				print("!! out of packets") #TODO
				m1_pos_at_pack_Ny=0
				m1_pos_at_pack_Nx=0
				pass
			
			
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

	movJ(id_m1,[-9.495, -41,	228,	38.96]) #pack get
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
	
	#get packet TODO slower pick
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	-9.494999885559082,	-41.0,	228.0,	38.959999084472656, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 2,	324.4891052246094,	-187.30612182617188,	228.0,	-11.535000801086426, 1) #movXYZ

	#move w packet
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	9.548895835876465,	-60.791259765625,	228.0,	39.707359313964844, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 2,	322.4343566894531,	-122.78236389160156,	228.0,	-11.535004615783691, 1) #movXYZ

	dType.SetPTPCmdEx_mon(api, id_m1, 4,	38.217063903808594,	-83.2728042602539,	228.0,	33.52074432373047, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 2,	298.4182434082031,	-17.83038902282715,	228.0,	-11.534996032714844, 1) #movXYZ

	current_pose = dType.GetPose(api, id_magR)
	dType.SetPTPWithLCmdEx(api, id_magR, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], 550, 1)

	dType.SetPTPCmdEx_mon(api, id_m1, 4,	55.90485382080078,	-29.299684524536133,	230,	-11.439573287963867, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	55.90485382080078,	-29.299684524536133,	230,	70-20.7, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	71.00940704345703,	-30.350120544433594,	230,	56.18449783325195, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	71.00940704345703,	-30.350130081176758,	230,	56.18450164794922, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	50,	4,	230,	24.7-20.7, 1) #movJ
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	50,	4,	150,	24.7-20.7, 1) #movJ drop
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	64,	11,	150,	27.7-20.7, 1) #movJ out
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	64,	11,	200,	27.7-20.7, 1) #movJ out
	dType.SetPTPCmdEx_mon(api, id_m1, 4,	40,	-28,200,	27.7-20.7, 1) #movJ ret
	
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
	
	
	
	
