
"dispenser_gift_py" - current in work

"dispenser_food_py" - is outdated

![python GUI](GUI_v0.41.png)

### About
Now this controls 1pcs Dobot M1 and 2pcs of Magician.
To create=save new buttons you can copy script from Dobot studio and click "convert from clipboard" or manually create files AND/OR folders in "script" folder
Press F1 for key map


### TODO
8khe37
* copy w L

* 🐛 fix stop cause cant resume

* fix clipboard deny error

* sw xyz/J
* convert xyz/J 2F^

* toggle auto upd pos from cursor
* upd coord, copy on click it

save rail at off

- [x] ask about function to check whether the next movement is good or will lead to error
https://forum.dobot.cc/t/check-possible-m1-movement-range-without-errors/3256
```
check possible M1 movement range without errors
Can you give me formulas or api function to check if next xyz is possible to reach or it will lead to error. Also I need function to full-automatic movement from possible point A to possible point B , without care of arm-orientation and other things.


How I imagine it:

xyz_now=GetPose(api, dobotId)

print( isMovementPossible(api, dobotId, xyz_now, xyz_next) )

print( isMovementPossible(api, dobotId, xyz_now, xyz_next, PTP_mode) )

print( get_distance_to_move_Rail_from_which_NextPosPossible(api, dobotId, xyz_now, xyz_next, PTP_mode) ) 
```
 
### install python libraries for Windows:

pip install PySide2

pip install pyserial

pip install pynput

pip install colorama

pip install pywin32 REM win32clipboard 


### UI  guide:
- ctrl+wheel change r-axis
- shift+wheel change rail L
- left|rigrt alt+above - faster|slower
- c cursor to current pos
### Tips:
* SetArmOrientation is need to move with XYZ, but not with Joints
* 🐛 M1 still has buggy HOME  function at 2020. Do not HOME or you lost angle of r-axis. Use "INITIAL Position". Also replace battery if it deplated. You can use 18650+3.3v LDO
* Rail calibrates to 0 after each reboot with HOME button, to avoid M1 HOME bug, connect rail to Magician (but not to M1). Install rail's end-switch not far from position you need. Для многих сценариев не нужно двигать роботов по всей рельсе. Поэтому для ускорения процесса и экономии ресурса стоит придумать, как поставить концевой датчик рельсы ближе к центру, чтоб робот при калибровке не ездил в дальний конец
* before turn off Dobot with rail, set rail to desired initial position (will be 0 at next boot), so not need to start work with HOME next time to find rail 0.
* most functions in DobotDllType.py uses return with array wraping 'return [value]' , so use result as result[0] or dType.GetValue(api, id_)[0]

