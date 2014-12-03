#!/usr/bin/python
#-*- coding: utf-8 -*-

import types

from .condition import Condition
from .constenc import (
    EncodeComparison,
    EncodePlayer,
    EncodeResource,
    EncodeScore,
    EncodeSwitchState,
    EncodeLocation,
    EncodeSwitch,
    EncodeUnit,
    Kills  # for __calls__ binding
)
from ..utils import EPD


def NoCondition():
    return Condition(0, 0, 0, 0, 0, 0, 0, 0)


def CountdownTimer(Comparison, Time):
    """Checks countdown timer.

    Example::

        CountdownTimer(AtLeast, 10)

    Memory Layout::

        0000 0000 0000 0000 TTTT TTTT 0000 CP01 0000

        T : Time, CP : Comparison.
    """
    Comparison = EncodeComparison(Comparison)
    return Condition(0, 0, Time, 0, Comparison, 1, 0, 0)


def Command(Player, Comparison, Number, Unit):
    """[Player] commands [Comparison] [Number] [Unit].

    Example::
        Command(Player1, AtLeast, 30, "Terran Marine")


    """
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    Unit = EncodeUnit(Unit)
    return Condition(0, Player, Number, Unit, Comparison, 2, 0, 0)


def Bring(Player, Comparison, Number, Unit, Location):
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    Unit = EncodeUnit(Unit)
    Location = EncodeLocation(Location)
    return Condition(Location, Player, Number, Unit, Comparison, 3, 0, 0)


def Accumulate(Player, Comparison, Number, ResourceType):
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    ResourceType = EncodeResource(ResourceType)
    return Condition(0, Player, Number, 0, Comparison, 4, ResourceType, 0)


# 'Kills' is already defined inside constenc, so we just add __call__ method
# to there instead of creating new function
def __Kills__internal(Player, Comparison, Number, Unit):
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    Unit = EncodeUnit(Unit)
    return Condition(0, Player, Number, Unit, Comparison, 5, 0, 0)

Kills._internalf = __Kills__internal


def CommandMost(Unit):
    Unit = EncodeUnit(Unit)
    return Condition(0, 0, 0, Unit, 0, 6, 0, 0)


def CommandMostAt(Unit, Location):
    Unit = EncodeUnit(Unit)
    Location = EncodeLocation(Location)
    return Condition(Location, 0, 0, Unit, 0, 7, 0, 0)


def MostKills(Unit):
    Unit = EncodeUnit(Unit)
    return Condition(0, 0, 0, Unit, 0, 8, 0, 0)


def HighestScore(ScoreType):
    ScoreType = EncodeScore(ScoreType)
    return Condition(0, 0, 0, 0, 0, 9, ScoreType, 0)


def MostResources(ResourceType):
    ResourceType = EncodeResource(ResourceType)
    return Condition(0, 0, 0, 0, 0, 10, ResourceType, 0)


def Switch(Switch, State):
    Switch = EncodeSwitch(Switch)
    State = EncodeSwitchState(State)
    return Condition(0, 0, 0, 0, State, 11, Switch, 0)


def ElapsedTime(Comparison, Time):
    Comparison = EncodeComparison(Comparison)
    return Condition(0, 0, Time, 0, Comparison, 12, 0, 0)


def Briefing():
    return Condition(0, 0, 0, 0, 0, 13, 0, 0)


def Opponents(Player, Comparison, Number):
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    return Condition(0, Player, Number, 0, Comparison, 14, 0, 0)


def Deaths(Player, Comparison, Number, Unit):
    Player = EncodePlayer(Player)
    Comparison = EncodeComparison(Comparison)
    Unit = EncodeUnit(Unit)
    return Condition(0, Player, Number, Unit, Comparison, 15, 0, 0)


def CommandLeast(Unit):
    Unit = EncodeUnit(Unit)
    return Condition(0, 0, 0, Unit, 0, 16, 0, 0)


def CommandLeastAt(Unit, Location):
    Unit = EncodeUnit(Unit)
    Location = EncodeLocation(Location)
    return Condition(Location, 0, 0, Unit, 0, 17, 0, 0)


def LeastKills(Unit):
    Unit = EncodeUnit(Unit)
    return Condition(0, 0, 0, Unit, 0, 18, 0, 0)


def LowestScore(ScoreType):
    ScoreType = EncodeScore(ScoreType)
    return Condition(0, 0, 0, 0, 0, 19, ScoreType, 0)


def LeastResources(ResourceType):
    ResourceType = EncodeResource(ResourceType)
    return Condition(0, 0, 0, 0, 0, 20, ResourceType, 0)


def Score(Player, ScoreType, Comparison, Number):
    Player = EncodePlayer(Player)
    ScoreType = EncodeScore(ScoreType)
    Comparison = EncodeComparison(Comparison)
    return Condition(0, Player, Number, 0, Comparison, 21, ScoreType, 0)


def Always():
    return Condition(0, 0, 0, 0, 0, 22, 0, 0)


def Never():
    return Condition(0, 0, 0, 0, 0, 23, 0, 0)


def Memory(dest, cmptype, value):
    return Deaths(EPD(dest), cmptype, value, 0)
