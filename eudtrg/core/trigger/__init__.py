#!/usr/bin/python
# -*- coding: utf-8 -*-

from .trigger import Trigger, GetTriggerCount
from .triggerscope import PushTriggerScope, PopTriggerScope, NextTrigger
from .condition import Condition
from .action import Action
from .stockcond import (
    NoCondition, CountdownTimer, Command, Bring, Accumulate, Kills,
    CommandMost, CommandMostAt, MostKills, HighestScore, MostResources,
    Switch, ElapsedTime, Briefing, Opponents, Deaths, CommandLeast,
    CommandLeastAt, LeastKills, LowestScore, LeastResources, Score,
    Always, Never, Memory,
)

from .stockact import (
    NoAction, Victory, Defeat, PreserveTrigger, Wait, PauseGame,
    UnpauseGame, Transmission, PlayWAV, DisplayText, CenterView,
    CreateUnitWithProperties, SetMissionObjectives, SetSwitch,
    SetCountdownTimer, RunAIScript, RunAIScriptAt, LeaderBoardControl,
    LeaderBoardControlAt, LeaderBoardResources, LeaderBoardKills,
    LeaderBoardScore, KillUnit, KillUnitAt, RemoveUnit, RemoveUnitAt,
    SetResources, SetScore, MinimapPing, TalkingPortrait, MuteUnitSpeech,
    UnMuteUnitSpeech, LeaderBoardComputerPlayers, LeaderBoardGoalControl,
    LeaderBoardGoalControlAt, LeaderBoardGoalResources,
    LeaderBoardGoalKills, LeaderBoardGoalScore, MoveLocation, MoveUnit,
    LeaderBoardGreed, SetNextScenario, SetDoodadState, SetInvincibility,
    CreateUnit, SetDeaths, Order, Comment, GiveUnits, ModifyUnitHitPoints,
    ModifyUnitEnergy, ModifyUnitShields, ModifyUnitResourceAmount,
    ModifyUnitHangarCount, PauseTimer, UnpauseTimer, Draw,
    SetAllianceStatus, SetMemory, SetNextPtr,
)

from .constenc import (
    All, Enemy, Ally, AlliedVictory, AtLeast, AtMost, Exactly, SetTo, Add,
    Subtract, Move, Patrol, Attack, P1, P2, P3, P4, P5, P6, P7, P8, P9,
    P10, P11, P12, Player1, Player2, Player3, Player4, Player5, Player6,
    Player7, Player8, Player9, Player10, Player11, Player12,
    CurrentPlayer, Foes, Allies, NeutralPlayers, AllPlayers, Force1,
    Force2, Force3, Force4, NonAlliedVictoryPlayers, Enable, Disable,
    Toggle, Ore, Gas, OreAndGas, Total, Units, Buildings,
    UnitsAndBuildings, Kills, Razings, KillsAndRazings, Custom, Set,
    Clear, Random, Cleared,

# encoders
    EncodeAllyStatus,
    EncodeComparison,
    EncodeCount,
    EncodeModifier,
    EncodeOrder,
    EncodePlayer,
    EncodeProperty,
    EncodePropState,
    EncodeResource,
    EncodeScore,
    EncodeSwitchAction,
    EncodeSwitchState,
)

from .strenc import (
    EncodeAIScript,
    EncodeLocation,
    EncodeString,
    EncodeSwitch,
    EncodeUnit,
)
