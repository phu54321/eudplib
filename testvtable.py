from eudtrg import *

addvt = vtable.EUDVTable(3)
a, b, ret = addvt.GetVariables()

add1 = Trigger()

add0 = Trigger(
	nextptr = addvt,
	actions = [
		ret.SetNumber(0),
		a.QueueAddTo(ret),
		b.QueueAddTo(ret),
		SetNextPtr(addvt, add1)
	]
)


main2 = Forward()

main = Trigger(
	nextptr = add0,
	actions = [
		a.SetNumber(123),
		b.SetNumber(456),
		SetNextPtr(add1, main2)
	]
)

main2 << Trigger(
	actions = [
		ret.QueueAssignTo(EPD(0x58A364)),
	]
)


Inject('outputmap/basemap.scx', 'outputmap/vtable.scx', main)