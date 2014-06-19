from eudtrg import *

LoadMap('outputmap/basemap.scx')

main = NextTrigger()
retval = f_mul.call(1233, 567)
retvt = retval.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retvt, triggerend)
	]
)

SaveMap('outputmap/arithmetic.scx', main)
