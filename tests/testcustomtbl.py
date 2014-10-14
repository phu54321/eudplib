import sys
import os
sys.path.insert(0, os.path.abspath('..\\'))

from eudtrg import *


LoadMap('outputmap/basemap/basemap.scx')


tbl = EUDTbl()  # New string table

f_initeudtbl()  # Backup original STR section address


tbl.SetAsDefault()  # Use 'tbl' string table for DisplayText
DoActions(DisplayText(tbl.StringIndex("Hello World!")))
 # tbl.StringIndex("Hello World!") returns string id of 'Hello World!' in tbl
 # Since tbl is now set as default string table, DisplayText(~) displays
 # 'Hello World!'
f_reseteudtbl()  # Reset STR section pointer


EUDJump(triggerend)  # Goto end


# Current player thing
SaveMap('outputmap/eudtbl.scx')
