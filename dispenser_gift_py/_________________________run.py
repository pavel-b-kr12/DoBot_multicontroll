#F4 to toggle prog panel

#int ClearAllAlarmsState(api, id_)

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import (QApplication,QDialog, QMessageBox, QPushButton)
from PySide2.QtCore import (QFile,QPoint,QObject)
from PySide2 import (QtGui,QtCore,QtWidgets)


import sys, threading,time, os
import re
from os.path import dirname, join, isdir, abspath, basename
from threading import Timer
from functools import partial
import queue
import inspect

#from dataclasses import dataclass

from ui import *
exec(open("./dobot_f.py").read()) #from dobot_f import *		# common scripts		#TODO2 set as https://stackoverflow.com/questions/436198/what-is-an-alternative-to-execfile-in-python-3
exec(open("./task_btn_f.py").read()) #from task_btn_f import *		# task scripts

import DobotDllType as dType
api = dType.load()

#===================================================================== Dobot start
def doTask(que, k):
	fitem = que.get()
	keyboard.press(k)
	keyboard.release(k)
	fitem()
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

id_m1=-2
id_magL=-2
id_magR=-2

maxDobotConnectCount = 10
errorString = ['Success','NotFound','Occupied']

def checkBox_ConnectAll_click(state):
	print("checkBox_ConnectAll_click: ",state)
	if state == 2:
		connectDobots()
	else: #0
		disconnectDobots()

def connectDobots():
	global id_m1
	global id_magL
	global id_magR
	print("connecting all Dobots")
	# print("Start search dobot, max:", maxDobotConnectCount)
	# for i in range(0, maxDobotConnectCount):
		# result = dType.ConnectDobot(api, "",115200)
	id_m1 = connectCOM("COM3")
	window.checkBox_M1.setChecked(id_m1!=-1)
	window.label_M1_id.setText(str(id_m1)) #f'{10}'
	if id_m1>-1:
		dType.SetQueuedCmdClear(api,id_m1)
		dType.SetQueuedCmdStartExec(api,id_m1)
	
	id_magL = connectCOM("COM5")
	window.checkBox_MagL.setChecked(id_magL!=-1)
	window.label_MagL_id.setText(str(id_magL))

	if id_magL>-1:
		dType.SetQueuedCmdClear(api,id_magL)
		dType.SetQueuedCmdStartExec(api,id_magL)
	
	id_magR = connectCOM("COM4")
	window.checkBox_MagR.setChecked(id_magR!=-1)
	window.label_MagR_id.setText(str(id_magR))
	if id_magR>-1:
		dType.SetQueuedCmdClear(api,id_magR)
		dType.SetQueuedCmdStartExec(api,id_magR)
	
		# state = dType.ConnectDobot(self.DobotAPI, "", 115200)

		# if state[0] != dType.DobotConnect.DobotConnect_NoError:
			# raise ValueError("Failed to connect dobot. ", CON_STR[state[0]])

		# dType.SetQueuedCmdClear(self.DobotAPI)
		# dType.SetHOMEParams(self.DobotAPI, self.home_x, self.home_y, self.home_z, 0, isQueued=1)
		
		
		#dType.SetHOMECmd(api, temp = 0, isQueued = 1)
		
	#initial id, for debug or create functions w.o robots
	if(id_m1==-1):
		id_m1=1
	if(id_magL==-1): ########!! check
		id_magL=2
	if(id_magR==-1):
		id_magR=3

	
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
	print("Connect : {}, err?: {}, id: {}".format(COMName, errorString[result[0]], result[3]))
	if result[0] == 0:
		return result[3]
	else:
		return -1

#===================================================================== GUI
bStopEnqueue=False

tskMarks=[]
def tskStart_mark(elem, id):
	print(id)
	tskMarks.append(elem)
	if id==id_m1:
		elem.setStyleSheet("background-color: #ffffaa")
	if id==id_magL:
		elem.setStyleSheet("background-color: #eeffaa")
	if id==id_magR:
		elem.setStyleSheet("background-color: #ffeeaa")
	#elem.update()
	#window.update()
	QApplication.processEvents()
	#window.update()
	#elem.hide()
def tskWait_mark(elem, id):
	elem.setStyleSheet("background-color: #aaaaff")
	
def tskEnd_mark(elem):
	elem.setStyleSheet("background-color: #aaff88")
	QApplication.processEvents()
def tskMarks_clear_all(bStopEnque):
	global bStopEnqueue
	bStopEnqueue=bStopEnque
	#print("tskMarks_clear_all", bStopEnqueue)
	for elem in tskMarks:
		elem.setStyleSheet("background-color: #cccccc") #!!default
	tskMarks.clear()

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


fill=100

def btn_fill_redraw():
	window.btn_fill10.setStyleSheet(style_fill_btn)
	window.btn_fill50.setStyleSheet(style_fill_btn)
	window.btn_fill100.setStyleSheet(style_fill_btn)
	window.btn_fill110.setStyleSheet(style_fill_btn)

def btn_fill_redraw_selected(btn):
	btn.setStyleSheet(style_fill_btn_selected)

def btn_handler_btn_fill10():
	fill=10
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill50():
	fill=50
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill50)
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill100():
	fill=100
	btn_fill_redraw()
	btn_fill_redraw_selected(window.btn_fill100)
	btn_fill_redraw_selected(window.btn_fill50)
	btn_fill_redraw_selected(window.btn_fill10)
def btn_handler_btn_fill110():
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
 font-size:28px;
 font-weight:bold;
 background-color: #dddddd
}
"""
style_order_btn_act="""
QPushButton
{
 font-size:28px;
 font-weight:bold;
 background-color: #ffaa88
}
"""
#aaff88

style_fill_btn="""
QPushButton
{
 font-size:28px;
 font-weight:bold;
 background-color: #dddddd
}
"""
style_fill_btn_selected="""
QPushButton
{
 font-size:28px;
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
#tst
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
	#window.btn_order_.setText(QtWidgets.QApplication.translate("mainWindow", "  Кава2       Coffe       Кофе    der Kaffee", None, -1))
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
	
	img_elem.setMask(pixmap.mask());
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
	id=None
	
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
		return cls(modul.id, window, module_name, None)
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

			id=fileNm_strArr[1]
			# id='id=id_'+fileNm_strArr[1]
			print("read file nm")
			print(fileNm_strArr)
			print("nmFunction:"+nmFunction)
			#print(stri)
			# exec(id) #! TST
			# print(id)
			#funcToUIGen_x=funcToUIGen()
			funcList.append( funcToUIGen.createFromFile(id, window, nmFunction, stri) )	
	
	@classmethod
	def createFromFile(cls, id, window, nmFunction, stri):
		cls.id = id
		cls.window = window
		cls.nmFunction = nmFunction
		#cls.btn = cls.createBtn(cls)
		cls.exec_str=stri
		cls.btn = funcToUIGen.createBtn(nmFunction, id, stri)
		cls.fn = funcToUIGen.createFunctionFromStr(nmFunction)
		return cls()
	
	@classmethod
	def createAndSave(cls, id, window, nmFunction, stri):
		cls.id = id
		cls.window = window
		cls.nmFunction = nmFunction
		cls.nmFile = nmFunction
		#cls.btn = cls.createBtn(cls)
		stri="id = '"+id+"'\r\nnmFunction = '"+cls.nmFile+"'\r\n"+stri
		cls.exec_str=stri	#"print('TODO exec_str')"
		print("save file "+cls.nmFile)
		print(stri)
		with open(exepath+"script\\"+cls.nmFile+".txt", "w") as text_file:
			text_file.write(stri)
		return cls()
		
	def __init__(self):
		print("init funcToUIGen")
		#self.btn = self.createBtn()
		#self.fn = self.createFunctionFromStr()
		
		
	
	def createFunctionFromStr(nmFunction):
		exec_strf="global "+nmFunction+"\r\ndef "+nmFunction+"():\r\n" + '\t'.join(('\n'+funcToUIGen.exec_str.lstrip()).splitlines(True))
		# exec_strf="def fn():\r\n" + '\t'.join(('\n'+self.exec_str.lstrip()).splitlines(True))
		print("create f: "+exec_strf)
		exec(exec_strf)
		if nmFunction == 'functionNameAt0': #!tst
			functionNameAt0()
			print("?functionNameAt0?")
		# self.fn=fn
		# fn()
		 
	def createBtn(nmFunction, id, stri):

		
		#window.xx = QtWidgets.QPushButton(window.verticalLayout_debug_2)
		btn = QtWidgets.QPushButton(window.verticalLayout_debug_2)
		
		btn.nmFunction = nmFunction
		btn.id = id
		btn.exec_str=stri
                
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setWeight(50)
		font.setItalic(False)
		font.setBold(False)
		btn.setFont(font)
		btn.setStyleSheet("font: 12pt ;")
		print("create btn: "+nmFunction)
		btn.setObjectName(nmFunction)
		btn.setText(nmFunction)
		if id=="m1":
			parentElem=window.verticalLayout_m1
		elif  id=="magL":
			parentElem=window.verticalLayout_magL
		else:
			parentElem=window.verticalLayout_magR
		
		parentElem.addWidget(btn)	#btn_order_, btn_order_row2, 1, 1, 1)
		
		#btn.clicked.connect(funcToUIGen.btnHandler) #this send false to Handler
		btn.clicked.connect(partial(funcToUIGen.btnHandler, btn))
		#print(__name__) ##==__main__
		return btn

	#thread to not freeze GUI
	def btnHandler(btn):
		print("run btnHandler: "+btn.nmFunction)
		th = threading.Thread(target=funcToUIGen.btnThr, args=[btn], daemon=True) #?is need daemon
		th.start()
		
	#wram worker function with UI signaling
	def btnThr(btn):
		print(btn.nmFunction)

		#btn=window.findChild(QtWidgets.QPushButton, self.nmFunction)

		rID=btn.id
		tskStart_mark(btn, rID)
		#if self.modul is None:
		exec(btn.exec_str)
		#else:
		#	self.modul.run()
		tskEnd_mark(btn)


funcList = []
import win32clipboard
def convertClipboard(id):
	print("convertClipboard id: "+id)
	N=window.spinBox_N.value()
	window.spinBox_N.setValue(N+1)
	nm=window.lineEdit_nm.text()

	nmFunction='n'+str(N)+"_"+id+"_"+nm
	#nmFile=str(N)+" "+id+" "+nm+str(N)
	#nmBtn="btn"+nmFunction #? is need

	global func_str
	# get clipboard data
	win32clipboard.OpenClipboard()
	func_str = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	'''	
	#print(   '\t'.join(func_str.splitlines(True)))
	#print(   '\t'.join(('\n'+func_str.lstrip()).splitlines(True)))
	#func_str='\t'.join(('\n'+func_str.lstrip()).splitlines(True))
	'''
	
	'''
	win32clipboard.OpenClipboard()
	win32clipboard.EmptyClipboard()
	win32clipboard.SetClipboardText(exec_str)
	win32clipboard.CloseClipboard()
	'''

	#func_str = re.sub(r"exec_str(.*?\r\n)", r"\1 xxx %s" % 1, func_str)
	#func_str = re.sub(r"(nc_str\)\r\n)", r"%s" % 1, func_str)
	
	func_str = re.sub(r"SetQueuedCmdClear\(api\,", r"SetQueuedCmdClear(api, %s" % id, str_buf)
	func_str = re.sub(r"SetHOMECmdEx\(api, 1\)", r"SetHOMECmdEx(api, %s, 1)" % id, str_buf)
	func_str = re.sub(r"SetQueuedCmdForceStopExec(api)\(api, 1\)", r"SetQueuedCmdForceStopExec(api, %s)" % id, str_buf)
	func_str = re.sub(r"GetPoseEx\(api\)", r"GetPoseEx(api, %s)" % id, str_buf)
	func_str = re.sub(r"GetPose\(api\)", r"GetPose(api, %s)" % id, str_buf)
	func_str = re.sub(r"SetPTPCmdEx\(api\,", r"SetPTPCmdEx(api, %s" % id, str_buf) #not exactly match
	func_str = re.sub(r"GetIODI\(api\,", r"GetIODI(api, %s" % id, str_buf) #not exactly match
	func_str = re.sub(r"SetHOMECmdEx\(api\,", r"SetHOMECmdEx(api, %s" % id, str_buf) #not exactly match
	

	
	global exec_str
	exec_str="global "+nmFunction+"\r\n"
	exec_str+="def "+nmFunction+"():"+func_str
	exec(exec_str)
	newBtn=funcToUIGen.createBtn(nmFunction, id, func_str)
	newBtn.clicked.connect(globals()[nmFunction])
	
	print(exec_str,  file=open(nmFunction+".py", 'w'))
	#with open(nmFunction+".py", "w") as text_file:
	#    text_file.write(exec_str)
	

	


	funcList.append( funcToUIGen.createAndSave(id, window, nmFunction, func_str) )
'''
def check_clipboard_every2s():
	#convertClipboard('1')
	#window.textEdit_in.setText(str_buf)
	#window.lineEdit_nm.setText(func_str)
	threading.Timer(3.0, check_clipboard_every2s).start()
'''		
	
def btnHome_f(id_,btn):
	tskMarks_clear_all(False)
	tskStart_mark(btn, id_)
	dType.SetHOMECmdEx(api, id_, 1)
	tskEnd_mark(btn)
	
	
def btnStop_f(id_, btn):
	tskMarks_clear_all(True)
	
	queue_clear(thread_m1_queue)
	queue_clear(thread_magL_queue)
	queue_clear(thread_magR_queue)
	
	dType.SetQueuedCmdForceStopExec(api, id_)
def queue_clear(q):
	with q.mutex:
		q.queue.clear()
	
	
def queue_put(q, f): #TODO2 mark enqueued
	#print("bStopEnqueue: ", bStopEnqueue)
	if(not bStopEnqueue):
		q.put(f)
	


	
#################
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


	window.btnHome_M1.clicked.connect(partial(btnHome_f,id_m1,window.btnHome_M1))
	window.btnHome_MagL.clicked.connect(partial(btnHome_f,id_magL,window.btnHome_MagL))
	window.btnHome_MagR.clicked.connect(partial(btnHome_f,id_magR,window.btnHome_MagR))
	
	window.btnStop_M1.clicked.connect(partial(btnStop_f,id_m1,window.btnStop_M1))
	window.btnStop_MagL.clicked.connect(partial(btnStop_f,id_magL,window.btnStop_MagL))
	window.btnStop_MagR.clicked.connect(partial(btnStop_f,id_magR,window.btnStop_MagR))
	
	window.btn_convertClipboard_m1.clicked.connect(partial(convertClipboard,'m1')) #! or id_m1 if failed to exec "id='id_m1'"
	window.btn_convertClipboard_magL.clicked.connect(partial(convertClipboard,'magL'))
	window.btn_convertClipboard_magR.clicked.connect(partial(convertClipboard,'magR'))
	

	dirs = [f for f in os.scandir(exepath+'script') if os.path.isdir(f)]
	for d in dirs:
		gen_btn_order_fromDir(d)




	
	window.btn_M1_gripperOpen.clicked.connect(gripperOpen)
	window.btn_M1_gripperClose.clicked.connect(gripperClose)
	window.btn_M1_gripperOff.clicked.connect(gripperOff)

	# task
	window.t1_m1_pos_at_packet.clicked.connect(t1_m1_pos_at_packet_h)
	window.t2_m1_check_packet.clicked.connect(t2_m1_check_packet_h)
	window.t3_m1_get_packet.clicked.connect(t3_m1_get_packet_h)
	window.t4_m1_packet_to_mag_site.clicked.connect(t4_m1_packet_to_mag_site_h)
	
	window.t5_magL_wait_m1.clicked.connect(t5_magL_wait_m1_h)
	window.t6_magL_give_and_back.clicked.connect(t6_magL_give_and_back_h)
	

	#debug IO
	window.btn_getAll_In_draw.clicked.connect(getAll_In_draw)


	window.checkBox_bex2.clicked.connect(ex2)
	window.checkBox_bex3.clicked.connect(ex3)
	window.checkBox_bex4.clicked.connect(ex4)
	window.checkBox_bex5.clicked.connect(ex5)
	window.checkBox_bex6.clicked.connect(ex6)
	
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


	dType.DobotExec(api)
	
	#check_clipboard_every2s()
	if len(sys.argv) > 0: # run from .bat .sh
		sys.exit(app.exec_()) # otherwise only work when running fron IDLE for debug


