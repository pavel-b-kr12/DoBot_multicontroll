

#===================================================================== tst
def print_state_id(id):
	pos=dType.GetPose(api, id)
	print(" %5s %5s %5s %5s %5s %5s" % (id, pos[0], pos[1], pos[2], pos[3], dType.GetIODI(api, id, 17)[0]) )


lock1 = threading.Lock()
		

def tst():
	print('tst')
def testDelay():
	print(1)
	btn=window.btn_M1_gripperOpen
	rID=id_m1
	tskStart_mark(btn, rID)
	
	
	lock1.acquire()
	print("lock")
	time.sleep(5)
	
	print(2)
	tskEnd_mark(btn)
	keyboard.press(Key.scroll_lock)
	keyboard.release(Key.scroll_lock)
	


	
	gripperOff()
	
	#print(" GetQueuedCmdCurrentIndex:",dType.GetQueuedCmdCurrentIndex(api, id_m1))
	#dType.SetQueuedCmdClear(api, id_m1) #could not work	https://forum.dobot.cc/t/clear-command-queue/250
	
def unlock1():
	lock1.release()
	print("unlock")
	
def test_queue_empty_f():
	btn=window.t2
	rID=id_magL
	tskStart_mark(btn, rID)
	print(inspect.currentframe().f_code.co_name)

	'''
	while not thread_m1_queue.empty():
		time.sleep(0.5)
		print(1)
	'''
	
	tskEnd_mark(btn)


	#t = Timer(2, tskStart_mark)  # function will be called 2 sec later with [delay_in_sec] as *args parameter
	#t.start()  # returns None
	
#=====================================================================

def gripperOpen():
	#https://stackoverflow.com/questions/683542/how-to-put-a-function-and-arguments-into-python-queue
	# ttt = threading.Thread(target=testDelay) #,args=(result[3],)
	# ttt.setDaemon(True)
	# ttt.start()

	thread_m1_queue.put(gripperClose)
	#thread_m1_queue.put(gripperClose)
	thread_m1_queue.put(gripperOff)
	
	# dType.SetIODOEx(api, rID, 17, 0, 1)
	# dType.SetIODOEx(api, rID, 18, 0, 1)
	# dType.SetWAITCmdEx(api, rID, 500, 1)
	# dType.SetIODOEx(api, rID, 17, 1, 1)
	# dType.SetIODOEx(api, rID, 18, 1, 1)

def gripperClose():
	# ttt = threading.Thread(target=unlock1) #,args=(result[3],)
	# ttt.setDaemon(True)
	# ttt.start()

	
	btn=window.btn_M1_gripperClose
	rID=id_m1
	tskStart_mark(btn, rID)
	time.sleep(2)
	print(inspect.currentframe().f_code.co_name)
	#also caller  https://stackoverflow.com/questions/5067604/determine-function-name-from-within-that-function-without-using-traceback
	
	# dType.SetIODOEx(api, rID, 17, 1, 1)
	# dType.SetIODOEx(api, rID, 18, 0, 1)
	# dType.SetWAITCmdEx(api, rID, 500, 1)
	# dType.SetIODOEx(api, rID, 17, 1, 1)
	# dType.SetIODOEx(api, rID, 18, 1, 1)
	
	tskEnd_mark(btn)
	
def gripperOff():
	btn=window.btn_M1_gripperOff

	rID=id_m1
	tskStart_mark(btn, rID)
	time.sleep(2)
	print(inspect.currentframe().f_code.co_name)
	
	# dType.SetIODOEx(api, rID, 17, 1, 1)
	# dType.SetIODOEx(api, rID, 18, 1, 1)

	tskEnd_mark(btn)


def btn_rail_up_20_h():
	dType.SetPTPCmdEx(api, id_m1, 7, 0,  0,  5, 0, 1)
	dType.ClearAllAlarmsState(api, id_m1)

	#ClearAllAlarmsState(api, id_m1)

def btn_rail_down_h():
	#print(dType.GetAlarmsState(api, id_m1) ) ##!
	#dType.GetHOMEParams(api, id_m1)
	#dType.GetPose(api, id_m1)[0]
	
	dType.ClearAllAlarmsState(api, id_m1)
	dType.SetPTPCmdEx(api, id_m1, 7, 0,  0,  -5, 0, 1)


#================================================================================ IO

def getAll_In_draw():
	print("input for id %4s d:"%(window.id_selected))
	for i in range(11, 19):
		b=dType.GetIODI(api, window.id_selected,  i)[0] #GetIODO(api, dobotId,  addr)
		s=printColorizeStr(" "+str(i),b,["-","+"], [Fore.CYAN,Fore.GREEN])
		sys.stdout.write(s)
		#sys.stdout.flush()
	print()
	#print("input a:")
	#for i in range(0, 5):
	#	print(i, ": ", dType.GetIOADC(api, id_m1,  i)[0])

	#SetIODO(api, dobotId, address, level, isQueued=0)
	#dType.SetIODO(api, id_m1, 2, 1, 0)

def SetIODOEx_h(self, id_, N): # !! or window.id_selected
	btn=self
	#tskStart_mark(btn, id_)
	
	bex=dType.GetIODO(api, id_, N)
	print(type(bex))
	print(str(bex==1))
	
	bex= not (bex==1)
	print(str(bex))
	btn.setChecked(bex)
	
	#dType.SetIODOEx(api, id_, 2, bex2, 1) #TODO check

	#tskEnd_mark(btn)
