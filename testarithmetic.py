from eudtrg import *

main = NextTrigger()
retval, remainder = muldiv.f_div.call(123456789, 2867)
retvt = retval.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		retval.QueueAssignTo(EPD(0x58A364)),
		remainder.QueueAssignTo(EPD(0x58A368)),
		SetNextPtr(retvt, triggerend)
	]
)

Inject('outputmap/basemap.scx', 'outputmap/arithmetic.scx', main)
