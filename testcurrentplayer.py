from eudtrg import *

LoadMap('outputmap/basemap.scx')

sd1 = Trigger(
    actions = [
        SetDeaths(CurrentPlayer, SetTo, 1234, 0)
    ]
)

sd2 = Trigger(
    nextptr = triggerend,
    actions = [
        SetDeaths(CurrentPlayer, SetTo, 1234, 0)
    ]
)

psw = InitPlayerSwitch([sd1 for _ in range(8)])

SaveMap('outputmap/curpltest.scx', psw)
