
"dispenser_gift_py" - current in work

"dispenser_food_py" - is outdated

![python GUI](GUI_v0.41.png)

### About
Now this controls 1pcs Dobot M1 and 2pcs of Magician.
To create=save new buttons you can copy script from Dobot studio and click "convert from clipboard" or manually create files AND/OR folders in "script" folder
Press F1 for key map



 
### install python libraries for Windows:
pip install PySide2
pip install pywin32
pip install pyserial
pip install pynput
pip install colorama
pip install pywin32 REM win32clipboard 

### Tips:
* 🐛 M1 still has buggy HOME  function at 2020. Do not HOME or you lost angle of r-axis. Use "INITIAL Position". Also replace battery if it deplated. You can use 18650+3.3v LDO
* Rail calibrates to 0 after each reboot with HOME button, to avoid M1 HOME bug, connect rail to Magician (but not to M1). Install rail's end-switch not far from position you need. Для многих сценариев не нужно двигать роботов по всей рельсе. Поэтому для ускорения процесса и экономии ресурса стоит придумать, как поставить концевой датчик рельсы ближе к центру, чтоб робот при калибровке не ездил в дальний конец
* before turn off Dobot with rail, set rail to desired initial position (will be 0 at next boot), so not need to start work with HOME next time to find rail 0.


