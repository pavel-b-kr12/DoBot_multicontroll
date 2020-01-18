import sys,threading,time
import DobotDllType as dType

from test_ui import *


def order_wine():
	threads[0].start()
	threads[0].join()