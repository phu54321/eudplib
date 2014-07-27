from eudtrglib import *


LoadMap('outputmap/basemap/basemap.scx')

main = NextTrigger()
retval = f_div(12345678, 567)[0]
retvt = retval.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retvt, triggerend)
	]
)

SaveMap('outputmap/arithmetic.scx', main)
