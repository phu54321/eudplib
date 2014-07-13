from eudtrg import *


# Create function f_add

LoadMap('outputmap/basemap.scx')

# type 1
'''
addvt = vtable.EUDVTable(3)
a, b, ret = addvt.GetVariables()

add1 = Forward()
add0 = Trigger(
	nextptr = addvt,
	actions = [
		ret.SetNumber(0),
		a.QueueAddTo(ret),
		b.QueueAddTo(ret),
		SetNextPtr(addvt, add1)
	]
)

add1 << Trigger()

f_add = eudfunc.EUDFunc(add0, add1, addvt, 2, 1)
'''



# type 2
@EUDFunc
def f_add(a, b):
	ret = EUDCreateVariables(1)
	SeqCompute([
		(ret, SetTo, 0),
		(ret, Add, a),
		(ret, Add, b)
	])

	return ret



main = NextTrigger()
[retval] = f_add(123, 456)
main2 = Trigger(
	nextptr = retval.GetVTable(),
	actions = [
		SetDeaths(0, SetTo, 1234, 0),
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retval.GetVTable(), triggerend)
	]
)

SaveMap('outputmap/function.scx', main)