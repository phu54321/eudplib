from helper import *


@TestInstance
def test_ptrigger():
    if EUDPlayerLoop()():
        PTrigger(
            players=[Player1],
            actions=[
                SetDeaths(CurrentPlayer, Add, 1, "Terran Marine"),
                PreserveTrigger()
            ]
        )

        PTrigger(
            players=[Player1, Player7],
            actions=[
                SetDeaths(CurrentPlayer, Add, 1, "Terran Marine"),
                PreserveTrigger()
            ]
        )

        PTrigger(
            players=[Force1],
            actions=[
                SetDeaths(CurrentPlayer, Add, 1, "Terran Marine"),
                PreserveTrigger()
            ]
        )
    EUDEndPlayerLoop()

    test_assert("test_ptrigger", [
        Deaths(P1, Exactly, 3, "Terran Marine"),
        Deaths(P7, Exactly, 1, "Terran Marine"),
        Deaths(P8, Exactly, 0, "Terran Marine"),
    ])

    DoActions(SetDeaths(AllPlayers, SetTo, 0, "Terran Marine"))
