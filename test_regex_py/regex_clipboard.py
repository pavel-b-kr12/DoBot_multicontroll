#@@ http://www.informit.com/articles/article.aspx?p=30708&seqNum=3
#@@ https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
#@@ http://www.losart3d.com/?p=809


import win32clipboard


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




def convertClipboard():
	win32clipboard.OpenClipboard()
	global str_buf
	str_buf = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard()
	
	global str_out
	#dType.SetHOMECmdEx(api, 1)
	str_out = re.sub(r"dType.SetHOMECmdEx\(api, 1\)", r"dType.SetHOMECmdEx(api, %s, 1)" % 1, str_buf)
	#print(re.sub(r"a(.*?\r\n)", r"\1 xxx %s" % 1, str_buf))
	#print(re.sub(r"dType.SetHOMECmdEx\(api, 1\)", r"dType.SetHOMECmdEx(api, 0, 1) %s" % 1, str_buf))
	print(str_out)
	# win32clipboard.OpenClipboard()
	# win32clipboard.EmptyClipboard()
	# win32clipboard.SetClipboardText(exec_str)
	# win32clipboard.CloseClipboard()
	#if str_out:
	#	window.textEdit_in.setText(str_buf)
	#	window.textEdit_out.setText(str_out)

def check_clipboard():
	convertClipboard()
	threading.Timer(3.0, check_clipboard).start()
		
if __name__ == "__main__":
	global exepath
	exepath = os.path.dirname(sys.argv[0])+"\\"	 #path from lunch:  os.getcwd()+"\\"

	app = QApplication(sys.argv)
	
	ui_file = QFile(exepath+"regex.ui")
	ui_file.open(QFile.ReadOnly)
	loader = QUiLoader()
	global window
	window = loader.load(ui_file)
	ui_file.close()
	window.show()
	

		
	window.textEdit_in.setEnabled(False)
	window.textEdit_out.setEnabled(False)
	window.lineEdit_regex.setEnabled(False)
	window.lineEdit_regexre.setEnabled(False)
	window.btn_convert.clicked.connect(convertClipboard)
	
	#btn_copy

	#check_clipboard()
	threading.Thread(target=check_clipboard, args=(), daemon=True).start() #?is need daemon

	sys.exit(app.exec_()) #IDLE debug|run
	
	
	
