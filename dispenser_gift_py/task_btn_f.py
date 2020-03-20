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
#J angle  movJ( [ m1_pos_at_pack[0],  m1_pos_at_pack[1],  m1_pos_at_pack[2], m1_pos_at_pack[3]+dobotStates[id_m1].posPivot[3] ])

m1_pos_at_pivot=[0,0, 92,None]
m1_pos_at_mag_site=[180,  (-180),  5, (-10)] #!! must move CCW
m1_pos_at_pack_dx=-40
m1_pos_at_pack_Nx=0
m1_pos_at_pack_Ny=0

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
	m1_mov_before_pack0xy() #to don't get packet assidently
	m1.movJ([None, None, 222, None]) #abowe
	#m1.movJ([-5,	-5, None, None])

	dobotRailState.mov(0) #!or magL.home()
	
def t01_m1_find_pivot_f(): #115.3
	##!!if pos at pack - move before pack 
	print(f_nm())
	btn=window.t01_m1_find_pivot
	tskStart_mark(btn, id_magR)

	#safe pos
	mov_m1_before_pivot()
	#mov to pivot
	m1.movJ([-81.21,	-13.49,	186.00,	None]) #movJ

	'''
	if(m1.getPos()[7]>0):
		print('rotete to positive r')
		while(True):
			if(check_packet()): 
				break
			m1.movJ_relative([0,  0,  0, 2])
	'''
		
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
	
	m1.posPivot_set(m1.getPos())
	
	# firstly need mov out of pivot to use cartesian XYZ, because can't go for j 0,0 other way then movJ
	#m1.movJ([-14.221565246582031,	-47.71931838989258,	None,	None])
	
	mov_m1_before_pivot()
	
	tskEnd_mark(btn)
	if(bConnectTascs):
		queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)

#=============	
	
m1_r_pack_piv=-29
def t1_m1_pos_at_packet_h():
	print(f_nm())
	tskMarks_clear_all(False) #also clean queues
	#thread_m1.join(); #TODO  or wait thread_m1_queue empty
	
	queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
xx=32
yy=[-156, -191, -269, -341.5, -394] #before, pack 0, 1, 2, 3  #-397
zz=[110,31,41,54,55]
def m1_mov_before_pack0xy():
	m1.movJ([-11, -133, None, None]) #before packets, safe
	m1.mov([None, yy[0], None, m1_r_pack_piv]) #before packets, safe
	#[32.99159622192383, -153.87136840820312, 139.70315551757812, -7.699620246887207, -11.06596851348877, -133.66490173339844, 139.70315551757812, 137.03125]
	#for xx 25 m1.movJ([-21, -122.5, None, None]) #before packets, safe
	
def t1_m1_pos_at_packet_f():
	print(f_nm())
	btn=window.t1_m1_pos_at_packet
	tskStart_mark(btn, id_m1)
	
	
	l_1stPacket=31
	l_lastPacket=931  #780max to not hit
	dL=193-l_1stPacket
	
	l_lastPacket=l_lastPacket-dL #!! this skip last column to safe debug

	#m1_pos_at_pack_Nx=2
	#m1_pos_at_pack_Ny=0
	
	#print('mov m1 to y:', 25, yy[m1_pos_at_pack_Ny+1]);
	#print('mov rail to:' ,l_lastPacket-dL*m1_pos_at_pack_Nx);
	
	pos=m1.getPos()
	L=dobotRailState.getL()
	
	print("L from pos: ", abs(L - (l_lastPacket-dL*m1_pos_at_pack_Nx)))
	print(abs(pos[0]-xx))
	print(abs(pos[3]-zz[m1_pos_at_pack_Ny+1]))
	if( abs(L - (l_lastPacket-dL*m1_pos_at_pack_Nx)) >2 or  abs(pos[0]-xx) >3 or abs(pos[3]-zz[m1_pos_at_pack_Ny+1])>100  ):
		m1_mov_before_pack0xy()
		m1.movJ([None, None, zz[0], None]) #before packets, safe
		
		#==m1.mov([25, yy[0], None, None]) #before packets, safe
		
		m1.movJ([None, None, zz[m1_pos_at_pack_Ny+1], None]) 
		dobotRailState.mov(l_lastPacket-dL*m1_pos_at_pack_Nx)

	m1.mov([None, yy[m1_pos_at_pack_Ny+1], zz[m1_pos_at_pack_Ny+1], m1_r_pack_piv]) #before packets
	#m1.movJ([None,None,None,m1_r_pack_piv])
	
	

	
	dy_out=6 #33
	pack0Y=-164
	packY= pack0Y - m1_pos_at_pack_Ny*(-164-(-240))
	

	#m1.mov( [-23, packY+dy_out, 50, None]) #before row, before detect
	#m1.mov( [-23, packY, 50, None]) #at row, detect
	
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
	if(bConnectTascs):
		queue_put(thread_m1_queue, t2_m1_check_packet_f)



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
		if(bConnectTascs):
			queue_put(thread_m1_queue,t3_m1_get_packet_f)
		#time.sleep(2) ####
		pass
	else:
		m1_pos_at_pack_Ny+=1
		if(m1_pos_at_pack_Ny==4):
			m1_pos_at_pack_Ny=0
			m1_pos_at_pack_Nx+=1
			if(m1_pos_at_pack_Nx==5):
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
			
		if(bConnectTascs):
			queue_put(thread_m1_queue, t1_m1_pos_at_packet_f)
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
	m1.movJ([None, None, 232, None])
	
	m1_mov_before_pack0xy()
	
	m1.movJ([-0.34, -124.6, 232, None])
	dobotRailState.mov(835) #pos where cable don't interrupt movement

	m1.movJ([42.65,	-125.20, 232, None])
	m1.movJ([63.06,	-117.64, 232, None])




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
	
	#if(bConnectTascs):
	queue_put(thread_magL_queue,t5_magL_wait_m1_f)

	dobotRailState.mov(345)
	m1.movJ([80.67733001708984, -72.33910369873047, None, None]) #[230.28469848632812, 226.3616180419922, 233.01654052734375, -298.7320861816406, 80.67733001708984, -72.33910369873047, 233.01654052734375, -307.0703125]
	
	#wait place is free
	
	m1.movJ([82.94929504394531, -26.055644989013672, None, None]) #[133.78848266601562, 366.01922607421875, 233.01654052734375, -277.3055725097656, 82.94929504394531, -26.055644989013672, 233.01654052734375, -334.19921875]
	#m1.movJ([None, None, None, 90])
	#dobotStates[id_magR].mov([133.79,	366.02,	234.00,	64.89]) #movXYZ
	dobotStates[id_magR].movJ([None,	None,	None,	8.00]) #movJ
	
	#drop
	m1.movJ([None, None, 123, None])#[133.78848266601562, 366.01922607421875, 124.68587493896484, -277.3055725097656, 82.94929504394531, -26.055644989013672, 124.68587493896484, -334.19921875]
	
	dobotRailState.mov(265.0)

	#m1.mov([234.47,	278.99,	216.00,	65.78]) #movXYZ
	#dobotStates[id_magR].movJ([74.30,	-48.69,	216.00,	40.16]) #movJ
	#dobotRailState.mov(345.0)

	#out x
	dobotRailState.mov(242)
	#out y
	m1.movJ([74.30,	-48.69,	None,	None]) #movJ .mov([234.47,	278.99,	216.00,	149.78]) #movXYZ
	#m1.mov_relative([0, -90, 0, 0]
	#m1.movJ([0, 0, 200, None])
	

#r to left is
#dobotStates[id_magR].mov([133.79,	366.02,	123.00,	70.62]) #movXYZ
#dobotStates[id_magR].movJ([82.95,	-26.06,	123.00,	13.73]) #movJ
	
	
	#print("working long t4_m1_packet_to_mag_site_f")
	#time.sleep(2) ####
	
	#end thread. Next loop started from mag
	tskEnd_mark(btn)
	
	

	
def t5_magL_wait_m1_h():
	print(f_nm())
	tskMarks_clear_all(False)
	
	queue_put(thread_magL_queue,t5_magL_wait_m1_f)
	
def t5_magL_wait_m1_f():
	print(f_nm())
	btn=window.t5_magL_wait_m1
	
	
	#time.sleep(2)
	
	#dobotStates[id_magL].mov([186.09,	2.09,	-12.06,	-21.10]) #movXYZ
	magL.movJ([0.64,	27.26,	63.95,	-21.74]) #movJ #pos to wait

	
	tskWait_mark(btn, id_m1)
	print('t5_magL_wait_m1_f     wait join m1')
	thread_m1_queue.join()
	print('seems like M1 wokr done..')
	

		
	tskStart_mark(btn, id_m1)
	#time.sleep(1)
	
	if(bConnectTascs):
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

	
	#at packet
	#dobotStates[id_magL].mov([276.01,	1.00,	47.94,	-21.10]) #movXYZ
	magL.movJ([0.21,	37.32,	23.84,	-21.30]) #movJ 

	#get
	#dobotStates[id_magL].mov([256.67,	1.00,	161.26,	-21.10]) #movXYZ
	magL.movJ([0.22,	24.02,	-14.96,	-21.32]) #movJ

	#move
	#dobotStates[id_magL].mov([-0.00,	-259.64,	99.94,	-29.10]) #movXYZ
	magL.movJ([-90.00,	23.96,	9.17,	60.90]) #movJ
	
	#give
	#dobotStates[id_magL].mov([-0.00,	-298.42,	73.94,	-29.10]) #movXYZ
	magL.movJ([-90.00,	43.89,	9.14,	60.90]) #movJ

		

	tskEnd_mark(btn)

	tskMarks_clear_all(False)	###!!!
	
	queue_put(thread_m1_queue, t1_m1_pos_at_packet_f) #start next loop  ##!! move to  t5_magL_wait_m1_f
	
	
	
	
	# SetIOMultiplexingEx(api, dobotId, 2,  1, isQueued)
    # SetIOMultiplexingEx(api, dobotId, 4,  2, isQueued)
    # SetIODOEx(api, dobotId, 2, enableCtrl, isQueued)
    # SetIOPWMEx(api, dobotId, 4, 10000, power, isQueued)
	
	
