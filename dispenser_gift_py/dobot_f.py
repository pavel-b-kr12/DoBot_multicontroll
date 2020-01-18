
bex2=0
def ex2():
	print(2)
	btn=window.checkBox_bex2
	tskStart_mark(btn)
 
	global bex2
	bex2= not bex2
	window.checkBox_bex2.setChecked(bex2)
	
	rID=id_m1
	dType.SetIODOEx(api, rID, 2, bex2, 1)

	tskEnd_mark(btn)


bex3=0
def ex3():
	btn=window.checkBox_bex3
	tskStart_mark(btn)

	global bex3
	bex3= not bex3
	window.checkBox_bex3.setChecked(bex3)
	
	rID=id_m1
	dType.SetIODOEx(api, rID, 2, bex3, 1)

	tskEnd_mark(btn)


bex4=0
def ex4():
	btn=window.checkBox_bex4
	tskStart_mark(btn)

	global bex4
	bex4= not bex4
	window.checkBox_bex4.setChecked(bex4)
	
	rID=id_m1
	dType.SetIODOEx(api, rID, 2, bex4, 1)

	tskEnd_mark(btn)
	

bex5=0
def ex5():
	btn=window.checkBox_bex5
	tskStart_mark(btn)

	global bex5
	bex5= not bex5
	window.checkBox_bex5.setChecked(bex5)
	
	rID=id_m1
	dType.SetIODOEx(api, rID, 2, bex5, 1)

	tskEnd_mark(btn)


bex6=0
def ex6():
	btn=window.checkBox_bex6
	tskStart_mark(btn)

	global bex6
	bex6= not bex6
	window.checkBox_bex6.setChecked(bex6)
	
	rID=id_m1
	dType.SetIODOEx(api, rID, 2, bex6, 1)

	tskEnd_mark(btn)