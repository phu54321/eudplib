from eudtrglib import *


LoadMap('outputmap/basemap/basemap.scx')


tbl = EUDTbl() # New string table


start = NextTrigger()

f_initeudtbl() # Backup original STR section address



tbl.SetAsDefault() # Use 'tbl' string table for DisplayText
DoActions(DisplayText(tbl.StringIndex("Hello World!")))
 # tbl.StringIndex("Hello World!") returns string id of 'Hello World!' in tbl
 # Since tbl is now set as default string table, DisplayText(~) displays
 # 'Hello World!'
f_reseteudtbl() # Reset STR section pointer


EUDJump(triggerend) # Goto end


# Current player thing
psw = InitPlayerSwitch([start, None, None, None, None, None, None, None])
SaveMap('outputmap/eudtbl.scx', psw)

