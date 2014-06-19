from eudtrg import *

LoadMap('basemap.scx')

b = Forward()

a = Trigger(
    nextptr = b,
    actions = [
        SetDeaths(Player1, Add, 1, 'Terran Marine')
    ]
)

b << Trigger(
    nextptr = b,
    actions = [
        SetDeaths(Player2, Add, 1, 'Terran Marine')
    ]
)

SaveMap('output.scx', a)
