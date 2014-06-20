from eudtrg import *

LoadMap('outputmap/basemap.scx')

main = NextTrigger()

word0, word1, byte0, byte1, byte2, byte3 = f_dwbreak.call(0x12345678)
retvt = word0.GetVTable()

main2 = Trigger(
	nextptr = retvt,
	actions = [
		word0.QueueAssignTo(EPD(0x58A364 + 4 * 0)),
		word1.QueueAssignTo(EPD(0x58A364 + 4 * 1)),
		byte0.QueueAssignTo(EPD(0x58A364 + 4 * 2)),
		byte1.QueueAssignTo(EPD(0x58A364 + 4 * 3)),
		byte2.QueueAssignTo(EPD(0x58A364 + 4 * 4)),
		byte3.QueueAssignTo(EPD(0x58A364 + 4 * 5)),
		SetNextPtr(retvt, triggerend)
	]
)

SaveMap('outputmap/dwbreak.scx', main)
