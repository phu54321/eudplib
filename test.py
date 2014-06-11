from eudtrg import *

trigA = Addr()
trigB = Addr()
trigB_act1 = Addr()

trigA << Trigger(
	nextptr = trigB,
	conditions = [
		Deaths(0, Exactly, 320, 1)
	],
	
	actions = [
		SetDeaths(EPD(trigA + 4), SetTo, triggerend, 0),
	]
)

trigB << Trigger(
	nextptr = trigA,
	actions = [
		trigB_act1 << SetDeaths(EPD(0x0058D740), SetTo, 0x00000000, 0),
		SetDeaths(EPD(trigB_act1 + 16), Add, 1, 0),
		SetDeaths(EPD(trigB_act1 + 20), Add, 1, 0),
		SetDeaths(Player1, Add, 1, 1)
	]
)



Inject('basemap.scx', 'out.scx', trigA)