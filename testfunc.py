from eudtrglib import *

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
VTProc(retval.GetVTable(), [
	SetDeaths(Player1, SetTo, 1234, 'Terran Marine'),
	retval.QueueAssignTo(EPD(0x58A364))
])

SaveMap('outputmap/function.scx', main)

