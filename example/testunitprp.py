from eudtrglib import *

LoadMap('outputmap/basemap/basemap.scx')

a = Trigger(
    nextptr = triggerend,
    actions = [
        SetDeaths(Player1, SetTo, 12345678, 0),
        CreateUnitWithProperties(1, 'Zerg Lurker', 'Anywhere', Player1, UnitProperty(burrowed = True))
    ]
)

SaveMap('outputmap/burrowtest.scx', a)
