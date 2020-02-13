''' layouts:
	#window.verticalLayout_debug.addWidget(newBtn)
	
	#parentElem=window.QGridLayout_order

	if id=="id_m1":
		parentElem=window.verticalLayout_m1
	elif  id=="id_magL":
		parentElem=window.verticalLayout_magL
	else:
		parentElem=window.verticalLayout_magR
'''
class class1: #hold for global access from threads
   key=None
   window=None
   bShow_verticalLayoutWidget_debug=True
   bShow_verticalLayoutWidget_help=False
   bShow_verticalLayout_manualControl_=False
   bFullScreen=False
   def toggle_FullScreen():
      class1.bFullScreen=not class1.bFullScreen
      if class1.bFullScreen:
         class1.window.showFullScreen()
      else:
         class1.window.showNormal()
   def toggle_helpView():
      class1.bShow_verticalLayoutWidget_help=not class1.bShow_verticalLayoutWidget_help
      if class1.bShow_verticalLayoutWidget_help:
         class1.window.verticalLayout_help_.show()
      else:
         class1.window.verticalLayout_help_.hide()
   def toggle_debugView():
      class1.bShow_verticalLayoutWidget_debug=not class1.bShow_verticalLayoutWidget_debug
      if class1.bShow_verticalLayoutWidget_debug:
         class1.window.verticalLayout_debug_2.show()
      else:
         class1.window.verticalLayout_debug_2.hide()
   def toggle_manualControl():
      class1.bShow_verticalLayout_manualControl_=not class1.bShow_verticalLayout_manualControl_
      if class1.bShow_verticalLayout_manualControl_:
         class1.window.verticalLayout_manualControl_.show()
      else:
         class1.window.verticalLayout_manualControl_.hide()



def closeThisElem(elem):
	elem.hide()
def handleOpenDialog(self):#!TODO
	#self.button1 = QPushButton("Click me")
	#self.button1.clicked.connect(partial(closeThisElem,self.button1))
	#self.addWidget(self.button1)
	#self.button1.show()
		#QMessageBox.warning(self,"<b><font size = '16' color = 'green'>The ","123",QMessageBox.Yes, QMessageBox.No)
	window=class1.window
	if '_dialog' not in locals():
		window._dialog = QDialog(self)
		window._dialog.resize(400, 200)
		window.labelD = QtWidgets.QLabel(window._dialog)
		#window.labelD.setGeometry(QtCore.QRect(80, 60, 47, 13))
		window.labelD.setObjectName("label")
		window.labelD.setText("g5hy45h")
		window.labelD.show()
		window._dialog.show() #cant close, only esc
		#time.sleep(3)
		#window._dialog.close()
	else:
		window._dialog.hide()
	#self._dialog.raise_()
	#self._dialog.activateWindow()
		#self._dialog.exec() #freeze

from pynput.keyboard import Key, Listener, KeyCode, Controller
keyboard = Controller()



def on_press(key):  #https://pythonhosted.org/pynput/keyboard.html#monitoring-the-keyboard
	pass
	#print('{0} pressed'.format(key))


def on_release(key):
	class1.key=key
	if(key is None):
		return False
		
	if key == KeyCode.from_char('p'):
		pass
	#print('{0} release'.format(key))

	if(key.char.isdigit()):
		id_selected=int(key.char) 
		#print(id_selected)
		class1.window.id_selected=id_selected #global nw here so sore in window
		class1.window.widgetDraw1.update()
	
	if key == Key.f1:
		#handleOpenDialog(class1.window)
		class1.toggle_helpView()
		
	elif key == Key.f12:
		class1.toggle_FullScreen()
	
	elif key == Key.f4:
		class1.toggle_debugView()
	
	elif key == Key.f5:
		class1.toggle_manualControl()
		
	elif key == Key.esc:
		# Stop listener
		return False


def keyhandler():
	with Listener(on_press=on_press,on_release=on_release) as listener:
		listener.join()