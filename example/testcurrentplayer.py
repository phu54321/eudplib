from eudtrglib import *

UbconvUseCharset('cp949')

LoadMap('outputmap/basemap/basemap.scx')

sd1 = Trigger(
    nextptr = triggerend,
    actions = [
        DisplayText('안녕하세요. Hello World!', 4),
        SetDeaths(CurrentPlayer, SetTo, 1234, 0),
        CreateUnit(1, 'Protoss Scout', 'Anywhere', CurrentPlayer)
    ]
)

psw = InitPlayerSwitch([sd1 for _ in range(8)])

SaveMap('outputmap/currentplayertest.scx', psw)
