from eudtrg import *

main = NextTrigger()
retval = f_exp.call(1233, 567)
retvt = retval.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retvt, triggerend)
	]
)

Inject('outputmap/basemap.scx', 'outputmap/arithmetic.scx', main)
