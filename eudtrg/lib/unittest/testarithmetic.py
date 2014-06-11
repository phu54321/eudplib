from eudtrg.base import * #@UnusedWildImport
from eudtrg.lib import arithmetic


main = Addr(Trigger())
retval = arithmetic.f_mul.call(12345, 67890)
retvt = Addr(retval.GetVTable())

main2 = Addr(Trigger(
	nextptr = Addr(retval.GetVTable()),
	actions = [
		retval.QueueAssignTo(EPD(0x51A364)),
		SetNextPtr(retvt, triggerend)
	]
))

Inject('basemap.scx', 'arithmetic.scx', main)