#TODO fix 2nd loop

#F4 to toggle prog panel

#int ClearAllAlarmsState(api, id_)

from ui_print import *
		

bDebug=False # print
bConnectTascs=False	#!!TODO

bKeyboardLeds=False
bMainBtns=False
xy_scale=0.94 #plot pos
bBtnStyle=True
bIDLE=False #False True to run from IDLE
#TODO:
bDobot_to_Queue_internal=True # isQueued for internal dobot MCU SetPTPCmdEx(api, dobotId, ptpMode, x, y, z, rHead, isQueued=0)
bDobot_to_Queue_external=False #push to thread thread_m1_queue thread_magL_queue thread_magR_queue

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QApplication,QDialog, QMessageBox, QPushButton)
from PySide2.QtCore import (QFile,QPoint,QPointF,QObject)
from PySide2.QtGui import (QPen, QPainter, QColor)
from PySide2 import (QtGui,QtCore,QtWidgets)


import sys, threading,time, os, random
import re
from os.path import dirname, join, isdir, abspath, basename
from threading import Timer
from functools import partial
import queue
import inspect
from math import *

#from dataclasses import dataclass

from ui import *
exec(open("./dobot_f.py").read()) #from dobot_f import *		# common scripts		#TODO2 set as https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
exec(open("./task_btn_f.py").read()) #from task_btn_f import *		# task scripts

import DobotDllType as dType
api = dType.load()

#===================================================================== Dobot start
def doTask(que, k):
	fitem = que.get()
	if(bKeyboardLeds):
		keyboard.press(k)
		keyboard.release(k)
	fitem()
	if(bKeyboardLeds):
		keyboard.press(k)
		keyboard.release(k)
	# func = items[0]
	# args = items[1:]
	# func(*args)
	que.task_done()

thread_m1_queue = queue.Queue()
def thread_m1_f(  ) :
	while True :
		if thread_m1_queue.empty():
			time.sleep(1)
			#print('wait m1 tasks','')
			continue
		doTask(thread_m1_queue, Key.caps_lock)
		
thread_magL_queue = queue.Queue()
def thread_magL_f(  ) :
	while True :
		if thread_magL_queue.empty():
			time.sleep(1)
			#print('wait mL tasks','')
			continue
		doTask(thread_magL_queue, Key.num_lock)
		
thread_magR_queue = queue.Queue()
def thread_magR_f(  ) :
	while True :
		if thread_magR_queue.empty():
			time.sleep(1)
			#print('wait mR tasks','')
			continue
		doTask(thread_magR_queue, Key.scroll_lock)

#=================================== COM port
id_m1=-2 #also in dobotStates[id_m1]
id_magL=-2
id_magR=-2
errorString = ['Success','NotFound','Occupied']

def checkBox_ConnectAll_click(state):
	print("checkBox_ConnectAll_click: ",state)
	if state == 2:
		connectDobots()
	else: #0
		disconnectDobots()

def connectDobots():
	global id_m1 #also in dobotStates[id_m1]
	global id_magL
	global id_magR
	global m1
	global magL
	global magR

	m1,id_m1=connectDobot("COM3", "m1", QColor(0,111,255,166), window.checkBox_M1, window.label_M1_id) #0   # QtCore.Qt.green QColor(0, 0, 255) Qt.darkYellow
	magL,id_magL=connectDobot("COM4", "magL", QColor(255,177,0,166), window.checkBox_MagL, window.label_MagL_id) #1 # rail connected
	magR,id_magR=connectDobot("COM16", "magR", QColor(0,255,0,166), window.checkBox_MagR, window.label_MagR_id, True)  #2 
	

id_nms_default=["id_m1","id_magL","id_magR"] # for 0, 1 , 2
def id_default(i):
	switcher={
			"m1":0,
			"magL":1,
			"magR":2
		}
	return switcher.get(i,2) #default 2
		 
def connectDobot(com_nm, id_nm, c, checkbox, label, bRail=False):
	id_ = connectCOM(com_nm)  # 0
	
	checkbox.setChecked(id_ != -1)  # TODO mark red if fail connect COM
	label.setText(str(id_))  # f'{10}'
	
	onNow=False
	if id_ > -1:
		onNow=True
		dType.SetQueuedCmdClear(api, id_)
		dType.SetQueuedCmdStartExec(api, id_)
		dType.ClearAllAlarmsState(api, id_)
		dType.SetPTPCommonParams(api, id_,40,30,1)  #??Ex #speed, acceleration max is 100, 1000
	
	if(id_ == -1):
		id_=id_default(id_nm) #initial id, for debug or create functions w.o robots
	
	dobotStates[id_] = DobotState(id_nm, id_, c, bRail)
	dobotStates[id_].bOn=onNow
	'''
	   
    dType.SetQueuedCmdClear(api)  #Clean Command Queued

    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    dType.SetHOMECmd(api, temp = 0, isQueued = 1)
	
	dType.DisconnectDobot(api)
	'''

	return dobotStates[id_], id_
			
def disconnectDobots():
	global id_m1
	global id_magL
	global id_magR
	
	print("DISconnecting all Dobots")
	dType.DisconnectDobot(api,id_m1)	# dType.DisconnectDobot(self.DobotAPI)
	dType.DisconnectDobot(api,id_magL)
	dType.DisconnectDobot(api,id_magR)
	print("DISconnecting probably not working") #? bug. ports left occupied

def connectCOM(COMName):
	result = dType.ConnectDobot(api, COMName,115200)

	if(bDebug):
		print("Connect : {}, err?: {}, id: {}".format(COMName, errorString[result[0]], result[3]))
	if result[0] == 0:
		return result[3]
	else:
		return -1

#===================================================================== GUI
def btn_alarm_check_clear_f(id_, btn):
	print(dType.GetAlarmsState(api, id_))
	#TODO 1st: check AlarmsState, mark color btn, 2nd press if marked red - clear
	#btn.setStyleSheet("background-color: #00ff00")
	dType.ClearAllAlarmsState(api, id_)
	
	print("after clear",dType.GetAlarmsState(api, id_))
def btnHome_f(id_,btn=None):
	if(id_==id_m1): #do not home m1, only clear err !!TODO and goto initial
		dType.ClearAllAlarmsState(api, id_)
		return
		
	if(btn is not None):
		tskStart_mark(btn, id_)
	dType.ClearAllAlarmsState(api, id_)
	dType.SetQueuedCmdClear(api, id_)
	dType.SetHOMECmdEx_mon(api, id_, 1,1)
	dobotStates[id_].posHome=dType.GetPose(api, id_)
	#dType.printPos(api, id_,0, 0, 0, 0, True)
	if(btn is not None):
		tskEnd_mark(btn)
	

def btnHome_h(id_,btn):
	tskMarks_clear_all(False)
	threading.Thread(target=btnHome_f, args=[id_,btn]).start()

	
def btnStop_f(id_):
	tskMarks_clear_all(True)
	
	queue_clear(thread_m1_queue)
	queue_clear(thread_magL_queue)
	queue_clear(thread_magR_queue)
	
	dType.SetQueuedCmdForceStopExec(api, id_)
	dType.ClearAllAlarmsState(api, id_)
def queue_clear(q):
	with q.mutex:
		q.queue.clear()
	
def queue_put(q, f): #TODO2 mark enqueued
	#print("bStopEnqueue: ", bStopEnqueue)
	if(not bStopEnqueue):
		q.put(f)
#===================================================================== GUI
bStopEnqueue=False

tskMarks=[]
def tskStart_mark(elem, id):
	#print("tskStart_mark id: ", id)
	tskMarks.append(elem)
	
	if(bBtnStyle):
		time.sleep(0.001)
		if id==id_m1:
			elem.setStyleSheet("background-color: #ffffaa") #yellow rgb(255,255,55) 
		if id==id_magL:
			elem.setStyleSheet("background-color: #eeffaa")
		if id==id_magR:
			elem.setStyleSheet("background-color: #ffeeaa")
		
	#elem.update()
	elem.setEnabled(False) #disable buttons input before task end. Alternate: clear queue or/and stop
	#elem.hide()
	#window.update()
	
	QApplication.processEvents()
	#window.update()
	
def tskWait_mark(elem, id):
	if(bBtnStyle):
		elem.setStyleSheet("background-color: #aaaaff") #blue
	pass
	
def tskEnd_mark(elem):
	#print(elem.styleSheet())
	
	if(bBtnStyle):
		time.sleep(0.001) #! bug without this delay random cause:  Could not parse stylesheet of object QPushButton(0x6f17de8, name = "my_btn_handler_function")
		#@ https://stackoverflow.com/questions/32313469/stylesheet-in-pyside-not-working https://stackoverflow.com/questions/20908370/styling-with-classes-in-pyside-python
		elem.setStyleSheet("background-color: #aaff88") #green
	elem.setEnabled(True)
	QApplication.processEvents()

def tskMarks_clear_all(bStopEnque):
	global bStopEnqueue
	bStopEnqueue=bStopEnque
	#print("tskMarks_clear_all", bStopEnqueue)
	if(bBtnStyle):
		for elem in tskMarks:
			elem.setStyleSheet("background-color: #cccccc") #!!default
	tskMarks.clear()
	
	queue_clear(thread_m1_queue) #to not start 2nd loop #TODO stop current
	queue_clear(thread_magL_queue)
	queue_clear(thread_magR_queue)
	
def resetProgressView():
	pass

#==================== order btns

def btn_redraw_act(btn):
	btn.txt=btn.text()
	btn.setText("..чекайте  wait  ждите..")
	btn.setStyleSheet(style_order_btn_act)
	#nwp TODO change bg, same style
	#palette = btn.palette()
	#role = btn.backgroundRole() #choose whatever you like
	#palette.setColor(role, QtGui.QColor('red'))
	#btn.palette=palette
	#btn.setPalette(palette)
	#btn.setAutoFillBackground(True)

	btn.setEnabled(False) # setEnabled =! setDisabled https://stackoverflow.com/questions/33954886/how-to-make-push-button-immediately-disabled
def btn_redraw_end(btn):
	btn.setText(btn.txt)
	btn.setStyleSheet(style_order_btn)
	btn.setEnabled(True)
	
#==================== fill btns
fill=100 # global setting that can be set with left bar in GUI

def setSpeed(val):
	if(m1.bOn):
		dType.SetPTPCommonParams(api, id_m1, 60*val/100, 30*val/100, 1) #DOTO all dobots
def btn_fill_redraw():
	window.btn_fill10.setStyleSheet(style_fill_btn)
	window.btn_fill50.setStyleSheet(style_fill_btn)
	window.btn_fill100.setStyleSheet(style_fill_btn)
	window.btn_fill110.setStyleSheet(style_fill_btn)
	setSpeed(fill)

def btn_fill_redraw_selected(btn):
	btn.setStyleSheet(style_fill_btn_selected)

def btn_handler_btn_fill10():
	global fill
	fill=10
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill50():
	global fill
	fill=50
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill50)
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill100():
	global fill
	fill=100
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill100)
	btn_fill_redraw_selected(window.btn_fill50)
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill110():
	global fill
	fill=110
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill110)
	btn_fill_redraw_selected(window.btn_fill100)
	btn_fill_redraw_selected(window.btn_fill50)
	btn_fill_redraw_selected(window.btn_fill10)

#===================================================================== style
style_order_btn="""
QPushButton
{
 font-size:22px;
 font-weight:bold;
 background-color: #dddddd
}
"""
style_order_btn_act="""
QPushButton
{
 font-size:22px;
 font-weight:bold;
 background-color: #ffaa88
}
"""
#aaff88

style_fill_btn="""
QPushButton
{
 font-size:22px;
 font-weight:bold;
 background-color: #dddddd
}
"""
style_fill_btn_selected="""
QPushButton
{
 font-size:22px;
 font-weight:bold;
 background-color: #aaaaff
}
"""


'''
"""
	   QPushButton {
			margin: 1px;
			border-color: #0c457e;
			border-style: outset;
			border-radius: 3px;
			border-width: 1px;
			color: black;
			background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2198c0, stop: 1 #0d5ca6);
		}
		QPushButton:pressed {
			background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #0d5ca6, stop: 1 #2198c0);
		}"""
'''
#===================================================================== generate GUI
ffthread_nm_N=0
#tst:
#dirs = [f for f in os.scandir('.\script') if os.path.isdir(f)]
#path=dirs[0].path
#imgs = [os.path.join(path, f) for f in os.listdir(path) if f.endswith((".png",".jpg",".gif"))]
#gen_btn_order(dirs[0].name, imgs[0])
'''! scripting part of this function is funny and possible could be complately replaced with loading py file'''
def gen_btn_order_fromDir(d):
	path=d.path
	imgs = [os.path.join(path, f) for f in os.listdir(path) if f.endswith((".png",".jpg",".gif"))]
	img=None
	if len(imgs) >0:
		img=imgs[0]
	
	txts = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".txt")]

	elem=gen_btn_order(d.name, img)

	global ffthread_nm_N
	ffthread_nm_N=ffthread_nm_N+1
	ffnm="ff"+str(ffthread_nm_N)
	#it is not working without `global` ffnm and global """+ffthread_nm+"""
	#it is working with same names only without exec so possible elem.clicked.connect(ff).
	#Buth with Thred function both func names need to be numbered/unique
	for txt in txts:
		txt_str=open(txt, 'r').read()
		exe_str="global "+ffnm+"\r\n"
		exe_str+="def "+ffnm+"():\r\n"+txt_str+"""\r\n\tbtn_redraw_end(window.findChild(QtWidgets.QPushButton, '"""+elem.objectName()+"""'))""" #!! fix indent
		#print(exe_str)
		exec(exe_str)
				#cc=compile(exe_str,"tmp.txt",'exec') #nw
				#exec(cc)
		
		
		ffthread_nm="ffthread"+str(ffthread_nm_N)
		exe_str_th="""
global """+ffthread_nm+"""
def """+ffthread_nm+"""():
	btn_redraw_act(window.findChild(QtWidgets.QPushButton, '"""+elem.objectName()+"""'))
	th = threading.Thread(target="""+ffnm+""")
	th.setDaemon(True)
	th.start()
print('"""+ffthread_nm+"""')
elem.clicked.connect("""+ffthread_nm+""")
"""
		exec(exe_str_th)
		#exec("""elem.clicked.connect("""+ffthread_nm+""")""")
		#elem.clicked.connect(ffthread_nm)
		break #multiple connect probably cause GUI freeze after click. But all connected to their job

"""
	global exe_str
	if len(txts) >0:
		txt_str=open(txts[0], 'r').read()
		exe_str="global ff\r\n"
		exe_str+="def ff():\r\n"+txt_str
		print(exe_str)
		exec(exe_str)
		#cc=compile(exe_str,"tmp.txt",'exec') #nw
		#exec(cc)
		elem.clicked.connect(ff)
	"""
	
btn_order_row_ico=0
btn_order_row2=0
def gen_btn_order(nm, img):
	global btn_order_row_ico
	global btn_order_row2
	#print(nm, img)
	#global btn_order_
	btn_order_ = QtWidgets.QPushButton(window)
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(0)
	sizePolicy.setHeightForWidth(btn_order_.sizePolicy().hasHeightForWidth())
	btn_order_.setSizePolicy(sizePolicy)
	btn_order_.setMinimumSize(QtCore.QSize(220, 144))
	btn_order_.setCursor(QtCore.Qt.PointingHandCursor)
	btn_order_.setObjectName(nm)
	''' name for css:
QPushButton#exit_button {
	border-image: url(resources/icons/64/exit.png);
}
QPushButton#config_button {
	border-image: url(resources/icons/64/config.png);
}
	'''
	window.QGridLayout_order.addWidget(btn_order_, btn_order_row2, 1, 1, 1)
	btn_order_row2 += 1
	#window.btn_order_.setText(QtWidgets.QApplication.translate("mainWindow", "  Кава2	   Coffe	   Кофе	der Kaffee", None, -1))
	btn_order_.setText(nm)
	
	#global img_elem
	#global pixmap
	#img_elem = QtWidgets.QPushButton(window)
	img_elem = QtWidgets.QLabel(window)
	#^nw img_elem.setStyleSheet("background-image: url(:/"+img+")")
	pixmap = QtGui.QPixmap(img).scaled(btn_order_.height(),btn_order_.height())
		#pixmap.scaledToHeight(btn_order_.height())
	img_elem.setPixmap(pixmap)
		#img_elem.setScaledContents(True) #resize to label
		#img_elem.resize(10,btn_order_.height())
	
	img_elem.setMask(pixmap.mask())
	sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
	sizePolicy.setHeightForWidth(img_elem.sizePolicy().hasHeightForWidth())
	img_elem.setSizePolicy(sizePolicy)
	img_elem.setMinimumSize(QtCore.QSize(btn_order_.height(), btn_order_.height()))
	img_elem.setCursor(QtCore.Qt.PointingHandCursor)
	window.QGridLayout_order.addWidget(img_elem, btn_order_row_ico, 0, 1, 1)
	btn_order_row_ico += 1
	'''
	if img is not None:
		setIcon(img_elem, img)
	'''
	effShadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=12 ) # xOffset=3, yOffset=3
	btn_order_.eff=effShadow
	btn_order_.setGraphicsEffect( effShadow )
	btn_order_.setStyleSheet(style_order_btn)
	return btn_order_

'''
def setIcon(elem, path):
#@ Making Classes that Use QIcon https://srinikom.github.io/pyside-docs/PySide/QtGui/QIcon.html
	
	icon=QtGui.QIcon(path)
	elem.setIcon(icon)
	#elem.setIconSize(QtCore.QSize(24,24))
	#elem.setIconSize(icon.availableSizes()[0])
	elem.setIconSize(QtCore.QSize(elem.height(),elem.height()))
	
	#elem.setIconSize(QtCore.QSize(window.btn_order_Wine.iconSize().width(),window.btn_order_Wine.size().height()))
	#elem.setStyleSheet("background-image: url('logo.png'); background-repeat: no-repeat; border: none;")
'''

import pkgutil
class funcToUIGen:
	id_nm=None
	
	'''	----------------- load modules
	@staticmethod
	def searchModulesAndGenUI():
		#dynamically load all py files (packegas). And also run it
		for loader, module_name, is_pkg in  pkgutil.walk_packages([dirname(__file__)+"\\script"]):
			#__all__.append(module_name)
			_module = loader.find_module(module_name).load_module(module_name)
			#ffs1.ff=_module.gg
			globals()[module_name] = _module
			print(module_name)
			print(dir(_module))
			funcList.append( initFromFile(_module, window, module_name) )
	@classmethod
	def initFromFile(cls, modul, window, module_name):
		cls.modul = modul
		return cls(modul.id_nm, window, module_name, None)
	'''	
	# ------------------ load string
	@staticmethod
	def loadStringsAndGenUI():
		path=exepath+"script\\"
		txt_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".txt")]
		#print(txt_files)

		for txt_file in txt_files:
			stri=open(txt_file, 'r').read()
			nmFunction=basename(txt_file)[:-4]
			fileNm_strArr=nmFunction.split('_')
			if len(fileNm_strArr)<3:
				continue
			N=fileNm_strArr[0][1] #TODO sort by N, inserting to layout

			id_nm=fileNm_strArr[1]
			# id_exec='id=id_'+fileNm_strArr[1]
			# exec(id_exec) #! TST
			# print(id)
			
			if(bDebug):
				print("read file nm")
				print(fileNm_strArr)
				print("nmFunction:"+nmFunction)

			

			funcList.append( funcToUIGen.createFromFile(id_nm, window, nmFunction, stri) )	
	
	@classmethod
	def createFromFile(cls, id_nm, window, nmFunction, stri):
		cls.id_nm = id_nm
		cls.window = window
		cls.nmFunction = nmFunction
		#cls.btn = cls.createBtn(cls)
		cls.exec_str=stri
		cls.btn = funcToUIGen.createBtn(nmFunction, id_nm, stri)
		cls.fn = funcToUIGen.createFunctionFromStr(nmFunction)
		return cls()
	
	@classmethod
	def createAndSave(cls, id_nm, window, nmFunction, stri):
		cls.id_nm = id_nm
		cls.window = window
		cls.nmFunction = nmFunction
		cls.nmFile = nmFunction
		#cls.btn = cls.createBtn(cls)
		stri="id = '"+id_nm+"'\r\nnmFunction = '"+cls.nmFile+"'\r\n"+stri
		cls.exec_str=stri	#"print('TODO exec_str')"
		if(bDebug):
			print("save file "+cls.nmFile)
			print(stri)
		with open(exepath+"script\\"+cls.nmFile+".txt", "w") as text_file:
			text_file.write(stri)
		return cls()
		
	def __init__(self):
		if(bDebug):
			print("init funcToUIGen")
		#self.btn = self.createBtn()
		#self.fn = self.createFunctionFromStr()
		
		
	
	def createFunctionFromStr(nmFunction):
		exec_strf="global "+nmFunction+"\r\ndef "+nmFunction+"():\r\n" + '\t'.join(('\n'+funcToUIGen.exec_str.lstrip()).splitlines(True))
		# exec_strf="def fn():\r\n" + '\t'.join(('\n'+self.exec_str.lstrip()).splitlines(True))
		if(bDebug):
			print("create f: "+exec_strf)
		exec(exec_strf)
		if nmFunction == 'functionNameAt0': #!tst
			functionNameAt0()
			if(bDebug):
				print("?functionNameAt0?")
		# self.fn=fn
		# fn()
		 
	def createBtn(nmFunction, id_nm, stri):

		
		#window.xx = QtWidgets.QPushButton(window.verticalLayout_debug_2)
		btn = QtWidgets.QPushButton(window.verticalLayout_debug_2)
		
		btn.nmFunction = nmFunction
		btn.id_nm = id_nm
		btn.exec_str=stri
		
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setWeight(50)
		font.setItalic(False)
		font.setBold(False)
		btn.setFont(font)
		btn.setStyleSheet("font: 12pt ;")
		if(bDebug):
			print("create btn: "+nmFunction)
		btn.setObjectName(nmFunction)
		btn.setText(nmFunction)
		if id_nm=="m1":
			parentElem=window.verticalLayout_m1
		elif  id_nm=="magL":
			parentElem=window.verticalLayout_magL
		else:
			parentElem=window.verticalLayout_magR
		
		parentElem.addWidget(btn)	#btn_order_, btn_order_row2, 1, 1, 1)
		
		#btn.clicked.connect(funcToUIGen.btnHandler) #this send False to Handler
		btn.clicked.connect(partial(funcToUIGen.btnHandler, btn))
		#print(__name__) ##==__main__
		return btn

	#thread to not freeze GUI
	def btnHandler(btn):
		if(bDebug):
			print("run btnHandler: "+btn.nmFunction)
		th = threading.Thread(target=funcToUIGen.btnThr, args=[btn], daemon=True) #?is need daemon
		th.start()
		
	#wram worker function with UI signaling
	def btnThr(btn):
		if(bDebug):
			print(btn.nmFunction)

		#btn=window.findChild(QtWidgets.QPushButton, self.nmFunction)

		rID=btn.id_nm
		tskStart_mark(btn, rID)
		#if self.modul is None:
		exec(btn.exec_str)
		#else:
		#	self.modul.run()
		tskEnd_mark(btn)


funcList = []
import win32clipboard
def convertClipboard(id):
	if(bDebug):
		print("convertClipboard id: "+id)
	N=window.spinBox_N.value()
	window.spinBox_N.setValue(N+1)
	nm=window.lineEdit_nm.text()

	nmFunction='n'+str(N)+"_"+id+"_"+nm
	#nmFile=str(N)+" "+id+" "+nm+str(N)
	#nmBtn="btn"+nmFunction #? is need

	global str_buf
	# get clipboard data
	win32clipboard.OpenClipboard()
	str_buf = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	'''	
	#print(   '\t'.join(str_buf.splitlines(True)))
	#print(   '\t'.join(('\n'+str_buf.lstrip()).splitlines(True)))
	#str_buf='\t'.join(('\n'+str_buf.lstrip()).splitlines(True))
	'''
	
	'''
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardText(exec_str, win32clipboard.CF_TEXT)
	win32clipboard.CloseClipboard()
	'''

	#str_buf = re.sub(r"exec_str(.*?\r\n)", r"\1 xxx %s" % 1, str_buf)
	#str_buf = re.sub(r"(nc_str\)\r\n)", r"%s" % 1, str_buf)
	
	str_buf = re.sub(r"SetQueuedCmdClear\(api\,", r"SetQueuedCmdClear(api, %s" % id, str_buf)
	str_buf = re.sub(r"SetHOMECmdEx\(api, 1\)", r"SetHOMECmdEx(api, %s, 1)" % id, str_buf)
	str_buf = re.sub(r"SetQueuedCmdForceStopExec(api)\(api, 1\)", r"SetQueuedCmdForceStopExec(api, %s)" % id, str_buf)
	str_buf = re.sub(r"GetPoseEx\(api\)", r"GetPoseEx(api, %s)" % id, str_buf)
	str_buf = re.sub(r"GetPose\(api\)", r"GetPose(api, %s)" % id, str_buf)
	str_buf = re.sub(r"SetPTPCmdEx\(api\,", r"SetPTPCmdEx(api, %s" % id, str_buf) #not exactly match
	str_buf = re.sub(r"GetIODI\(api\,", r"GetIODI(api, %s" % id, str_buf) #not exactly match
	str_buf = re.sub(r"SetHOMECmdEx\(api\,", r"SetHOMECmdEx(api, %s" % id, str_buf) #not exactly match
	

	
	global exec_str
	exec_str="global "+nmFunction+"\r\n"
	exec_str+="def "+nmFunction+"():"+str_buf
	exec(exec_str)
	newBtn=funcToUIGen.createBtn(nmFunction, id, str_buf)
	newBtn.clicked.connect(globals()[nmFunction])
	
	print(exec_str,  file=open(nmFunction+".py", 'w'))
	#with open(nmFunction+".py", "w") as text_file:
	#	text_file.write(exec_str)
	

	
	funcList.append( funcToUIGen.createAndSave(id, window, nmFunction, str_buf) )
'''
def check_clipboard_every2s():
	#convertClipboard('1')
	#window.textEdit_in.setText(str_buf)
	#window.lineEdit_nm.setText(str_buf)
	threading.Timer(3.0, check_clipboard_every2s).start()
'''		

#=====================================================

PTP_mode_xyz_LINEAR=2		
PTP_mode_xyz=1
PTP_mode_J_LINEAR=5		
PTP_mode_J=4	
#!TODO toggle GUI

import traceback ##!!
def CopyToClipboard(s):
	try:
		win32clipboard.OpenClipboard()
		win32clipboard.EmptyClipboard()
		win32clipboard.SetClipboardText( s, win32clipboard.CF_TEXT )
		win32clipboard.CloseClipboard()
	except Exception:
		traceback.print_exc()
		#print("CloseClipboard")
		#win32clipboard.CloseClipboard()
		
def print_selected_PosNow_copy_movXYZ(pos):
	s="dType.SetPTPCmdEx_mon(api, "+id_nms_default[window.id_selected] +", "+str(PTP_mode_xyz_LINEAR)+",	%1s,	%1s,	%1s,	%1s, 1"%(pos[0],pos[1],pos[2],pos[3])+") #movXYZ\r\n"
	print("\r\n",s)
	CopyToClipboard(s)
	return s
def print_selected_PosNow_copy_movJ(pos, s1=""):
	s="dType.SetPTPCmdEx_mon(api, "+id_nms_default[window.id_selected] +", "+str(PTP_mode_J)+",	%1s,	%1s,	%1s,	%1s, 1"%(pos[4],pos[5],pos[6],pos[7])+") #movJ\r\n"
	print("\r\n",s)
	CopyToClipboard(s+s1)
	return s


#=====================================================

dobotStates=[None for i in range(9)]
class DobotState():
	pos=[0,0,0,0] #now, updates while exec "_mon" move function e.g.:  SetHOMECmdEx_mon
	pos_hist=[[22,33,44,55], [88,88,10,0]] #!!
	posCursor=[0,0,0,0] #target, updates on XY plot click or drom some functions that set target before exec move
	posCursorL=0;
	posHome=[0,0,0,0] # updates after run btnHome_h
	posPivot=[0,0,0,0,0]
	IODI=[]
	IOAI=[]
	bOn=False #Dobot online
	bRail=False
	dobotRailState=None
	_lock = threading.Lock()
	def __init__(self, nm, id_, c, bRail=False):
		self.color=c
		self.nm=nm
		self.id_=id_
		if(bDebug or not self.bOn):
			print ("init", nm, id_)
			self.pos=[id_*30,0,0,0]
			self.posCursor=[0,id_*30,0,0]
		else:
			self.pos=dType.GetPose(api, id_)
			self.posCursor=self.pos #  setPosCursorXYZR(self.pos)
		
		
		#print(dType.GetDeviceWithL(api, id_)) #?!TODO F^ always True at start
		#bRail=dType.GetDeviceWithL(api, id_)[0]
		self.bRail=bRail
		if(bRail):
			bRail_now=dType.GetDeviceWithL(api, id_)[0]
			if(bRail_now):
				print("dobot id: ",id_, " already connected Rail")
			else:
				dType.SetDeviceWithL(api, id_,  True)
				time.sleep(0.1)  #!del
				print("connecting rail...", id_nms_default[id_], dType.GetDeviceWithL(api, id_))
			global dobotRailState
			dobotRailState=DobotRailState(id_,  self)
			self.dobotRailState=dobotRailState

	def getPos(self, bRedraw=True):
		self._lock.acquire()
		self.pos=dType.GetPose(api, self.id_)
		self._lock.release()
		if(bRedraw):
			widgetDraw1.update()
	
	def setPosNow(self, n):
		self._lock.acquire()
		#self.pos[0:4]=[n[0],n[1],n[2],n[3],n[4]]
		self.pos=n
		self._lock.release()
		widgetDraw1.update()

	def setPosCursorXYZR(self, xyzr_arr):
		self._lock.acquire()
		self.posCursor=xyzr_arr
		self._lock.release()
		widgetDraw1.update()
	def setPosCursorXY(self, x,y):
		self._lock.acquire()
		self.posCursor[0]=x
		self.posCursor[1]=y
		self._lock.release()
		widgetDraw1.update()
	def setPosCursorZ(self, z):
		self._lock.acquire()
		self.posCursor[2]=z
		self._lock.release()
		widgetDraw1.update()
	def incrPosCursorZ(self, dz):
		self._lock.acquire()
		self.posCursor[2]+=dz
		self._lock.release()
		widgetDraw1.update()
	def incrPosCursorR(self, dr):
		self._lock.acquire()
		self.posCursor[3]+=dr
		self._lock.release()
		widgetDraw1.update()
	def incrPosCursorLRail(self, L): #!!TODO DobotRailState l posCursorL
		self._lock.acquire()
		self.posCursorL+=L
		if( self.posCursorL <0 ):
			self.posCursorL=0
		elif( self.posCursorL >999 ):
			self.posCursorL=999
		self._lock.release()
		widgetDraw1.update()
	
	def home_mon(self, btn=None):
		btnHome_f(self.id_, btn)

	#-------------------------------
	def mov(self, pos):	#relative to pivot r-axis
		if(pos[3] is not None):
			 pos[3]+=self.posPivot[3]
		dType.SetPTPCmdEx_mon(api, self.id_, 2, pos[0],  pos[1],  pos[2], pos[3], 1)	
	def mov_relative(self, pos):
		#print('mov_relative to ', pos)
		dType.SetPTPCmdEx_mon(api, self.id_, 7, pos[0],  pos[1],  pos[2], pos[3], 1)
		
	def movJ_relative(self, pos):
		#print('movJ_relative to ', pos)
		dType.SetPTPCmdEx_mon(api, self.id_, 6, pos[0],  pos[1],  pos[2], pos[3], 1)
	
	def movJ_abs(self, pos):
		dType.SetPTPCmdEx_mon(api, self.id_, 4, pos[0], pos[1], pos[2], pos[3], 1)
		#move J linear  PTPmode=5 is also not possible from 0
		
	#-------------------------------
	
	#def movJ(self, j1,j2,j3,j4):	#relative to pivot r-axis
	#	self.movJ_abs(self, [j1,  j2,  j3, j4+self.posPivot[3]]) 
		

	def movJ(self, pos):			#relative to pivot r-axis
		if(pos[3] is not None):
			 pos[3]+=self.posPivot[3]
		self.movJ_abs([pos[0], pos[1], pos[2], pos[3]])


	'''
	#now this is in DType for all
	def movJ_def_p(self, pos): #set None to stay in current position movJ_def_p([None,1,2,3]) mean x remain, but y=1 z=2 r=3 		#relative to pivot
		self.movJ_def(self, pos[0], pos[1], pos[2], pos[3])
	
	def posJ_fill_None_w_current(self, j1,j2,j3,j4):		#relative to pivot
		pos_now=dType.GetPose(api, self.id_)
		if(j1 is None):
			j1=pos_now[4]
		if(j2 is None):
			j2=pos_now[5]
		if(j3 is None):
			j3=pos_now[6]
		if(j4 is None):
			j4=pos_now[7]
		else:
			j4+=self.posPivot[3] #relative to pivot r-axis
		return [j1,j2,j3,j4]
	def movJ_def(self, j1,j2,j3,j4): #set None to stay in current position 		#relative to pivot
		posJ=self.posJ_fill_None_w_current(j1,j2,j3,j4)
		self.movJ_abs(posJ)
	'''
	def cursor_to_pos_selected(self): # TODO from scripts
		id_=window.id_selected
		current_pose = dType.GetPose(api, id_)
		dobotStates[id_].setPosCursorXYZR(current_pose)
		

class DobotRailState(): #!!TODO
	l=0
	id_=0
	_lock = threading.Lock()
	dobotSt=None
	def __init__(self,id_, dobotSt):
		self.dobotSt=dobotSt
		print('rail id_:', id_, id_nms_default[id_])
		if(not bDebug  and self.dobotSt.bOn):
			print(' rail L:', dType.GetPoseL(api,id_))
		self.id_=id_
		#self.mov(500) #test
		#print('rail L:', dType.GetPoseL(api,id_))
		#self.mov(600) #test
		#print('rail L:', dType.GetPoseL(api,id_))

	def getL(self, bRedraw=True):
		#self._lock.acquire() #!? fix freeze if lock (only if dobot connected)
		if(self.dobotSt.bOn): #!TODO move check to dType
			self.l=dType.GetPoseL(api, self.id_)[0]
		#self._lock.release()
		if(bRedraw):
			widgetDraw1.update()
		return self.l
	def mov_ex(self, l): #wait untill end
		#TODO
		self.l=l
	def mov_relative(self, l):	#TODO  now PosCursorL can't be negative in incrPosCursorLRail
		#TODO
		id_=self.id_
		current_pose = dType.GetPose(api, id_)
		dType.SetPTPWithLCmdEx(api, id_, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], self.getL(False)+l, 1)

	def mov(self, l): #non-blocking so can use from UI without new thread 
		id_=self.id_
		current_pose = dType.GetPose(api, id_)
		#dType.SetPTPLParamsEx(api, id_,50,30,1)
		dType.SetPTPWithLCmdEx(api, id_, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], l, 1)
	def mov_to_cursor(self, l): #non-blocking so can use from UI without new thread  #TODO mov_to_cursor all together xyzrL
		id_=self.id_
		current_pose = dType.GetPose(api, id_)
		#dType.SetPTPLParamsEx(api, id_,50,30,1)
		dType.SetPTPWithLCmdEx(api, id_, 1, current_pose[0], current_pose[1], current_pose[2], current_pose[3], self.dobotSt.posCursorL, 1)
		

	#def setCursor(l):
	#	pass
dobotRailState=None  #TODO multiple. But currently we have 1
	
	
#=====================================================
from PySide2.QtCore import Qt

class WidgetDraw1(QtWidgets.QWidget):
	cx=0 #center of widget
	cy=0
	def __init__(self):
		super(WidgetDraw1, self).__init__()
		
		self.initUI()
		
	def initUI(self):	  
		#self.setGeometry(300, 300, 280, 170)
		#self.setWindowTitle('dobot pos')
		self.show()

	def paintEvent(self, e): # is called every time you call update() or repaint(), for example it is called every time it is resized, the window is moved, etc.
		qp = QtGui.QPainter()
		qp.begin(self)
		qp.setRenderHint(QtGui.QPainter.Antialiasing, True)
		
		xywh=self.rect() 	#widget			#cent=self.geometry().center() #window
		cent=xywh.center() 
		#self.cent=cent
		self.xywh=xywh
		self.cx=cent.x()
		self.cy=cent.y()
		qp.drawLine(QPointF(0, self.cy), QPointF(xywh.width(), self.cy)) #w #center cross lines
		qp.drawLine(QPointF(self.cx, 0), QPointF(self.cx, xywh.height())) #h
		#print(self.cx, self.cy, xywh.width(), xywh.height())
		self.drawPoints(qp)
		
		qp.end()
	
	def drawPoints(self, qp):
		
		
		for dobotSt in dobotStates:
			if(dobotSt == None):
				#print("!") #?? why empty exist
				continue
				
			pos_hist_n=0
			for pos in dobotSt.pos_hist:
				qp.setPen(QPen(QtCore.Qt.white, 1))
				self.draw1pos_hist(qp, pos, pos_hist_n, dobotSt) #now history
				pos_hist_n+=1
				
			pos=dobotSt.pos
			posCursor=dobotSt.posCursor
			#print(i)
			#print(pos)
			
			if(len(pos)>2):
				#qp.setBrush(Qt.black)
				qp.setBrush(dobotSt.color)
				#qp.setBrush(Qt.transparent)
				qp.setPen(QPen(QtCore.Qt.red, 2))
				self.draw1pos(qp, pos[0], pos[1], pos[2], pos[3], dobotSt) #now
			if(len(posCursor)>2):
				qp.setPen(QPen(dobotSt.color, 2))
				qp.setBrush(dobotSt.color)
				self.draw1pos(qp, posCursor[0], posCursor[1], posCursor[2], posCursor[3], dobotSt, dobotSt.id_ == window.id_selected) #target
			if(dobotSt.bRail):
				qp.setPen(QPen(dobotSt.color, 2))
				xend=self.xywh.width()-50
				y=self.cy+111
				qp.drawLine(QPointF(xend-dobotSt.posCursorL/2, y), QPointF(xend, y))  #!TODO map L to w
				#!!!qp.drawLine(QPointF(xend-dobotRailState.getL(False), y-8), QPointF(xend, y-8))
				#print(dobotRailState.l)
			
	def draw1pos_hist(self, qp, pos, pos_hist_n, dobotSt): #TODO draw as always but dimmer. Add on move, del on return btn
		x=pos[0]
		y=pos[1]
		
		x= scale_f(x, xy_scale) +self.cx
		y=-scale_f(y, xy_scale) +self.cy
		
		qp.drawEllipse(QPoint(x,y),6,6)
		qp.setPen(QPen(QtCore.Qt.black, 1))
		font = QtGui.QFont("Segoe", 7)
		qp.setFont(font)
		qp.drawText(x-2, y+4, str(pos_hist_n))
		
	def draw1pos(self, qp, x, y, z, r, dobotSt, bMarkSelection=False):
		#xyz_str=str(round(x,1))+" "+str(round(y,1))+" "+str(round(z,1))+" "+str(round(r,1)) #before scale
		xyz_str='{:.0f} {:.0f} {:.0f} {:.1f}'.format(x,y,z,r) #before scale #https://mkaz.blog/code/python-string-format-cookbook/
		
		x= scale_f(x, xy_scale) +self.cx
		y=-scale_f(y, xy_scale) +self.cy
		
		z_start_out_of_circle=-25
		if(z<0):
			z_start_out_of_circle=-z_start_out_of_circle
		yz_start=y+z_start_out_of_circle
		qp.drawLine(QPointF(x, yz_start), QPointF(x, yz_start-scale_f(z,0.95))) #z
		
		
		r=radians(r)
		qp.drawLine(QPointF(x, y), QPointF(x+sin(r)*20, y+cos(r)*20)) #r
		
		#qp.setPen(QPen(Qt.red, 2))
		qp.drawEllipse(QPoint(x,y),10,10) # draw https://doc.qt.io/qtforpython/PySide2/QtGui/QPainter.html#PySide2.QtGui.PySide2.QtGui.QPainter.drawEllipse
		if(bMarkSelection):
			qp.setBrush(Qt.transparent)
			qp.drawEllipse(QPoint(x,y),16,16)

		#xyz
		font = QtGui.QFont("Segoe", 15)
		font.setFixedPitch(True)
		qp.setFont(font)
		qp.drawText(x+14, y-7, xyz_str)
		
		#nm
		qp.setPen(QPen(QtCore.Qt.black, 1))
		font = QtGui.QFont("Segoe", 8)
		qp.setFont(font)
		qp.drawText(x-2, y+4, dobotSt.nm[-1])
		
		
		
		
		# p.setPen(QPen(Qt.white, 3))
		# p.drawLine(QPointF(410.738, 364.399), QPointF(-63151.2, -63197.6))
		#qp.setPen(QPen(Qt.cyan, 2))
		
		

		# painter.setBrush(QtCore.Qt.blue)  # Set the circle color
		# center = QtCore.QPoint(90, 90)
		# painter.drawEllipse(center, 40, 40)
		# font = painter.font()
		# font.setPointSize(30)
		# pen = painter.pen()
		# pen.setColor(QtCore.Qt.white)  # Set the text color
		# painter.setPen(pen)
		# painter.setFont(font)
		# painter.drawText(80, 100, str(self.unreadCount))

		#size = self.size()
		# for i in range(1000):
			# x = random.randint(1, size.width()-1)
			# y = random.randint(1, size.height()-1)
			# qp.drawPoint(x, y) 

	
	def mousePressEvent(self, e):
		points = e.pos()
		if(bDebug):
			print("click at: ",points)
		
		if(dobotStates[window.id_selected] is not None):
			#print(scale_f(points.x()-self.cx, 1/xy_scale))
			#print(scale_f(points.y()-self.cy, 1/xy_scale))
			dobotStates[window.id_selected].setPosCursorXY(scale_f(points.x()-self.cx, 1/xy_scale) ,  -scale_f(points.y()-self.cy, 1/xy_scale))
		
		#self.update()
	def wheelEvent(self, event):
		if(dobotStates[window.id_selected] is not None):
			d_div=60
			if( Key.alt_l in class1.keys):
				d_div=6
			if( Key.alt_r in class1.keys):
				d_div=240
			d=event.delta()/d_div
			
			if Key.ctrl_l in class1.keys :
				dobotStates[window.id_selected].incrPosCursorR(d)
			elif Key.shift in class1.keys :

				#dobotStates[window.id_selected].incrPosCursorLRail(d)  #rail for selected dobot
				dobotRailState.dobotSt.incrPosCursorLRail(d) #if only single rail available
			else:
				dobotStates[window.id_selected].incrPosCursorZ(d)
		event.accept()
		#self.update()

def scale_f(x, scale):
	xsign= -1 if x<0 else 1 #save sing
	x=pow(abs(x), scale) #scale
	return  x*xsign
	
	
	
#=====================================================
import shutil
if __name__ == "__main__":
	global exepath
	exepath = os.path.dirname(sys.argv[0])+"\\"	 #path from lunch:  os.getcwd()+"\\"

	app = QApplication(sys.argv)

	
	#dobot dll install			#nw permission
	# dobotdllpathmust=os.path.join(os.path.dirname(sys.executable),"DobotDll.dll")
	# dobotdllpath=exepath+"DobotDll.dll"
	# if not os.path.exists(dobotdllpathmust):
		# shutil.copy(dobotdllpath,os.path.dirname(sys.executable)) 
	
	ui_file = QFile(exepath+"main.ui")
	ui_file.open(QFile.ReadOnly)
	loader = QUiLoader()
	global window
	window = loader.load(ui_file)
	ui_file.close()
	
	dType.window=window #for monitor xyz
	window.dType=dType
	window.id_selected=0 ###!! move to dType
	window.id_nms_default=id_nms_default
	window.dobotStates=dobotStates
	dType.dobotStates=dobotStates

	window.checkBox_ConnectAll.stateChanged.connect(checkBox_ConnectAll_click)
	connectDobots()
	

	btn_fill_bg=window.btn_fill10.styleSheet()
	window.btn_fill10.clicked.connect(btn_handler_btn_fill10)
	window.btn_fill50.clicked.connect(btn_handler_btn_fill50)
	window.btn_fill100.clicked.connect(btn_handler_btn_fill100)
	window.btn_fill110.clicked.connect(btn_handler_btn_fill110)
	
	window.btn_fill10.setStyleSheet(style_fill_btn)
	window.btn_fill50.setStyleSheet(style_fill_btn)
	window.btn_fill100.setStyleSheet(style_fill_btn)
	window.btn_fill110.setStyleSheet(style_fill_btn)


	window.btnHome_M1.clicked.connect(partial(btnHome_h,id_m1,window.btnHome_M1))
	window.btnHome_MagL.clicked.connect(partial(btnHome_h,id_magL,window.btnHome_MagL))
	window.btnHome_MagR.clicked.connect(partial(btnHome_h,id_magR,window.btnHome_MagR))
	
	window.btnStop_M1.clicked.connect(partial(btnStop_f,id_m1))
	window.btnStop_MagL.clicked.connect(partial(btnStop_f,id_magL))
	window.btnStop_MagR.clicked.connect(partial(btnStop_f,id_magR))
	
	window.btn_alarm_check_clear_m1.clicked.connect  (partial(btn_alarm_check_clear_f,id_m1,   window.btn_alarm_check_clear_m1))
	window.btn_alarm_check_clear_magL.clicked.connect(partial(btn_alarm_check_clear_f,id_magL, window.btn_alarm_check_clear_magL))
	window.btn_alarm_check_clear_magR.clicked.connect(partial(btn_alarm_check_clear_f,id_magR, window.btn_alarm_check_clear_magR))
	
	window.btn_convertClipboard_m1.clicked.connect(partial(convertClipboard,'m1')) #! or id_m1 if failed to exec "id='id_m1'"
	window.btn_convertClipboard_magL.clicked.connect(partial(convertClipboard,'magL'))
	window.btn_convertClipboard_magR.clicked.connect(partial(convertClipboard,'magR'))
	

	dirs = [f for f in os.scandir(exepath+'script') if os.path.isdir(f)]
	
	if(bMainBtns):
		for d in dirs:
			gen_btn_order_fromDir(d)
		

	global widgetDraw1
	widgetDraw1 = WidgetDraw1()
	window.widgetDraw1=widgetDraw1
	#global btn_order_row2
	window.QGridLayout_order.addWidget(widgetDraw1, btn_order_row2, 1, 1, 1)
	btn_order_row2+=1

	
	window.btn_M1_gripperOpen.clicked.connect(gripperOpen)
	window.btn_M1_gripperClose.clicked.connect(gripperClose)
	window.btn_M1_gripperOff.clicked.connect(gripperOff)

	# task
	window.t0_magR_rail_Home.clicked.connect(t0_magR_rail_Home)
	window.t01_m1_find_pivot.clicked.connect(t01_m1_find_pivot)
	window.t1_m1_pos_at_packet.clicked.connect(t1_m1_pos_at_packet_h)
	window.t2_m1_check_packet.clicked.connect(t2_m1_check_packet_h)
	window.t3_m1_get_packet.clicked.connect(t3_m1_get_packet_h)
	window.t4_m1_packet_to_mag_site.clicked.connect(t4_m1_packet_to_mag_site_h)
	
	window.t5_magL_wait_m1.clicked.connect(t5_magL_wait_m1_h)
	window.t6_magL_give_and_back.clicked.connect(t6_magL_give_and_back_h)
	

	#debug IO
	window.btn_getAll_In_draw.clicked.connect(getAll_In_draw)
	
	#window.btn_rail_up_20.clicked.connect(btn_rail_up_20_h) #!! move to scripts
	#window.btn_rail_down.clicked.connect(btn_rail_down_h)


	window.checkBox_bex2.clicked.connect(partial(SetIODOEx_h,window.checkBox_bex2, id_m1, 2))
	window.checkBox_bex3.clicked.connect(partial(SetIODOEx_h,window.checkBox_bex3, id_m1, 3))
	window.checkBox_bex4.clicked.connect(partial(SetIODOEx_h,window.checkBox_bex4, id_m1, 4))
	window.checkBox_bex5.clicked.connect(partial(SetIODOEx_h,window.checkBox_bex5, id_m1, 5))
	window.checkBox_bex6.clicked.connect(partial(SetIODOEx_h,window.checkBox_bex6, id_m1, 6))
	
	window.show()
	class1.window=window
	
	threading.Thread(target=keyhandler, args=(), daemon=True).start() #?is need daemon


	#robot tasks queues:
	thread_m1 = threading.Thread(target=thread_m1_f) #,args=(result[3],)
	thread_m1.setDaemon(True)
	thread_m1.start()	
	
	thread_magL = threading.Thread(target=thread_magL_f)
	thread_magL.setDaemon(True)
	thread_magL.start()
		
	thread_magR = threading.Thread(target=thread_magR_f)
	thread_magR.setDaemon(True)
	thread_magR.start()
	
	funcToUIGen.loadStringsAndGenUI()

	# for children in window.findChildren(QPushButton):
		# shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=3, yOffset=3)
		# window.setGraphicsEffect(shadow)

	if(not bIDLE):
		dType.DobotExec(api)
		#!!
		#check_clipboard_every2s()
		if len(sys.argv) > 0: # run from .bat .sh
			sys.exit(app.exec_()) # otherwise only work when running fron IDLE for debug
