# to in-place, without start new line, use print("...", end="")

from __future__ import print_function
#import fixpath
from colorama import init as initcolorama, Fore, Back, Style
initcolorama()


def printColorizeStr(s,b, str_b=["",""]):
	if(b):
		return Fore.GREEN+s+str_b[1]+Fore.RESET
	else:
		return Fore.RED+s+str_b[0]+Fore.RESET
def printColorizeStr(s,b, str_b, color_b=[Fore.RED,Fore.GREEN]):
	if(b):
		return color_b[1]+s+str_b[1]+Fore.RESET
	else:
		return color_b[0]+s+str_b[0]+Fore.RESET
