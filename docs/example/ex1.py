from eudtrg import *

LoadMap("basemap.scx")

ptrg = Trigger(
    nextptr = triggerend,
    actions = [
        DisplayText("Hello World!")
    ]
)


psw = InitPlayerSwitch([
    ptrg, ptrg, ptrg, ptrg, ptrg, ptrg,
    None, None
])


SaveMap("ex1.scx", psw)
