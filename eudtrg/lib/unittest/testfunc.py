from eudtrg.base import * #@UnusedWildImport
from eudtrg.lib import vtable, eudfunc


# Create function f_add
PushTriggerScope()
addvt = Addr(vtable.EUDVTable(3))
a, b, ret = addvt.GetVariables()

add1 = Addr()

add0 = Addr(Trigger(
	nextptr = addvt,
	actions = [
		ret.SetNumber(0),
		a.QueueAddTo(ret),
		b.QueueAddTo(ret),
		SetNextPtr(addvt, add1)
	]
))

add1 << Trigger()
PopTriggerScope()

f_add = eudfunc.EUDFunc(add0, add1, addvt, 2, 1)




main = Addr(Trigger())
retval = f_add.call(123, 456)
main2 = Addr(Trigger(
	nextptr = Addr(retval.GetVTable()),
	actions = [
		retval.QueueAssignTo(EPD(0x51A364)),
		SetNextPtr(retval.GetVTable(), triggerend)
	]
))

Inject('basemap.scx', 'function.scx', main)