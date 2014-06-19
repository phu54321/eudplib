from eudtrg import *

UbconvUseCharset('cp949')

LoadMap('outputmap/basemap.scx')

sd1 = Trigger(
    actions = [
        SetDeaths(CurrentPlayer, SetTo, 1234, 0)
    ]
)

sd2 = Trigger(
    nextptr = triggerend,
    actions = [
        DisplayText('안녕하세요. Hello World!', 4),
        SetDeaths(CurrentPlayer, SetTo, 1234, 0)
    ]
)

psw = InitPlayerSwitch([sd1 for _ in range(8)])

SaveMap('outputmap/currentplayertest.scx', psw)
