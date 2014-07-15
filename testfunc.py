from eudtrg import *


# Create function f_add

LoadMap('outputmap/basemap/basemap.scx')

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
retval = f_add(123, 456)
main2 = Trigger(
	nextptr = retval.GetVTable(),
	actions = [
		SetDeaths(0, SetTo, 1234, 0),
		retval.QueueAssignTo(EPD(0x58A364)),
		SetNextPtr(retval.GetVTable(), triggerend)
	]
)

SaveMap('outputmap/function.scx', main)