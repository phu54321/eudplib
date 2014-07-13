from eudtrg import *

LoadMap('outputmap/basemap.scx')

ep = Trigger()
DoActions(SetNextPtr(ep, triggerend))


# Test #1 : Display Text (tests InitPlayerSwitch)
# Display text action
DoActions(DisplayText('Test #1 success')) # If this message appears, then test was successful.


# Test #2 : basic loop
loop0_start = Trigger(
    actions = [
        CreateUnit(1, 'Terran Marine', 'Anywhere', Player1),
        SetDeaths(Player1, Add, 1, 'Terran Marine') 
    ]
)

EUDJumpIf( Deaths(Player1, AtMost, 319, 'Terran Marine') , loop0_start )

DoActions( LeaderBoardControl( 'Terran Marine', 'Should be 320' ) )

Trigger(
    conditions = [
        Command(Player1, Exactly, 320, 'Terran Marine')
    ],
    actions = [
        DisplayText('Test #2 success')
    ]
)




psw = InitPlayerSwitch([ep, None, None, None, None, None, None, None])
SaveMap('outputmap/eudtrgout.scx', psw)
