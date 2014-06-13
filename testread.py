from eudtrg import *

main = NextTrigger()

retval = f_dwread.call(EPD(0x5993D4)) # Get address of STR section
retvt = retval.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retvt, triggerend)
	]
)

Inject('outputmap/basemap.scx', 'outputmap/readdword.scx', main)
