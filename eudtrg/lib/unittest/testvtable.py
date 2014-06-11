from eudtrg.base import * #@UnusedWildImport
from eudtrg.lib import vtable

PushTriggerScope()
addvt = vtable.EUDVTable(3)
a, b, ret = addvt.GetVariables()

add1 = Addr(Trigger())

add0 = Addr(Trigger(
	nextptr = Addr(addvt),
	actions = [
		ret.SetNumber(0),
		a.QueueAddTo(ret),
		b.QueueAddTo(ret),
		SetNextPtr(addvt, add1)
	]
))

PopTriggerScope()


main2 = Addr()

main = Addr(Trigger(
	nextptr = add0,
	actions = [
		a.SetNumber(123),
		b.SetNumber(456),
		SetNextPtr(add1, main2)
	]
))

main2 << Trigger(
	nextptr = triggerend,
	actions = [
		ret.QueueAssignTo(EPD(0x51A364)),
	]
)

Inject('basemap.scx', 'vtable.scx', main)