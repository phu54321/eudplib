from eudtrg import *

LoadMap('outputmap/basemap/basemap.scx')


fstart = NextTrigger()
f_strcpy(0x58A364, Db(b'How are you today?\0'))
f_strcpy(0x58A365, Db(b'Hello World!\0'))
# Check offset 0x58A364

SaveMap('outputmap/strcpy.scx', fstart)
