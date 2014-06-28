from eudtrg import *

LoadMap('saibi2 template.scx')

humantrg = Forward()

# global game initalization trigger
init = NextTrigger()
DoActions(SetMemory(0x6509A0, SetTo, 0)) # Turbo
InitPlayerSwitch([humantrg, humantrg, humantrg, humantrg, humantrg, humantrg, None, None])

# player trigger
humantrg << NextTrigger()
Trigger(
    actions = [
        RunAIScript('Turn ON Shared Vision for Player 7'),
        RunAIScript('Turn ON Shared Vision for Player 8'),
        DisplayText('\x13\x04Welcome to Saibi Labatory')
    ],
    preserved = False
)

EUDJump(triggerend)

SaveMap('Missile pack [saibi2].scx', init)
