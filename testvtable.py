from eudtrg import *

LoadMap('outputmap/basemap.scx');
addvt = vtable.EUDVTable(3)
a, b, ret = addvt.GetVariables()

add1 = Trigger()

add0 = Trigger(
	nextptr = addvt,
	actions = [
		SetDeaths(1, SetTo, 1234, 0),
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
		SetDeaths(2, SetTo, 1234, 0),
		a.SetNumber(123),
		b.SetNumber(456),
		SetNextPtr(add1, main2)
	]
)

main2 << Trigger(
	nextptr = triggerend,
	actions = [
		SetDeaths(3, SetTo, 1234, 0),
		ret.QueueAssignTo(EPD(0x58A364)),
	]
)

SaveMap('outputmap/vtable.scx', main)