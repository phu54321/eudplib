'''
Core of eudtrg. Everything in eudtrg are implemented using eudtrg.base
Core defines

- EUD Object (EUDObject class)
- Trigger (Trigger, Condition, Action class)
- Raw bytes object (Db)
- Calculation of expression containing addresses. (Expr class)
- Map reading/writing (LoadMap, SaveMap)

'''

from .dataspec.eudobj import EUDObject  # noqa
from .dataspec.forward import Forward
from .dataspec.trigger import (
    PushTriggerScope,
    PopTriggerScope,
    Trigger,
    Condition,
    Action,
    NextTrigger,
    Disabled,
    triggerend
)
from .dataspec.expr import Expr
from .dataspec.bytedump import Db
from .dataspec.struoffset import CreateOffsetMapping

from .mapdata.unitprp import UnitProperty

# Stock triggers
from .stocktrg import (
    NoCondition, CountdownTimer, Command, Bring, Accumulate, Kills,
    CommandMost, CommandMostAt, MostKills, HighestScore, MostResources,
    Switch, ElapsedTime, Briefing, Opponents, Deaths, CommandLeast,
    CommandLeastAt, LeastKills, LowestScore, LeastResources, Score, Always,
    Never, NoAction, Victory, Defeat, PreserveTrigger, Wait, PauseGame,
    UnpauseGame, Transmission, PlayWAV, DisplayText, CenterView,
    CreateUnitWithProperties, SetMissionObjectives, SetSwitch,
    SetCountdownTimer, RunAIScript, RunAIScriptAt, LeaderBoardControl,
    LeaderBoardControlAt, LeaderBoardResources, LeaderBoardKills,
    LeaderBoardScore, KillUnit, KillUnitAt, RemoveUnit, RemoveUnitAt,
    SetResources, SetScore, MinimapPing, TalkingPortrait, MuteUnitSpeech,
    UnMuteUnitSpeech, LeaderBoardComputerPlayers, LeaderBoardGoalControl,
    LeaderBoardGoalControlAt, LeaderBoardGoalResources, LeaderBoardGoalKills,
    LeaderBoardGoalScore, MoveLocation, MoveUnit, LeaderBoardGreed,
    SetNextScenario, SetDoodadState, SetInvincibility, CreateUnit, SetDeaths,
    Order, Comment, GiveUnits, ModifyUnitHitPoints, ModifyUnitEnergy,
    ModifyUnitShields, ModifyUnitResourceAmount, ModifyUnitHangarCount,
    PauseTimer, UnpauseTimer, Draw, SetAllianceStatus, Memory, SetMemory,
    SetNextPtr
)

# Constant parser
from .trgconst import (
    # Constant parsers
    ParseConst, ParseAllyStatus, ParseComparison, ParseModifier, ParseOrder,
    ParsePlayer, ParsePropState, ParseResource, ParseScore, ParseSwitchAction,
    ParseSwitchState, ParseAIScript, ParseCount,

    # Constants
    All, Enemy, Ally, AlliedVictory, AtLeast, AtMost, Exactly, SetTo, Add,
    Subtract, Move, Patrol, Attack, P1, P2, P3, P4, P5, P6, P7, P8, P9, P10,
    P11, P12, Player1, Player2, Player3, Player4, Player5, Player6, Player7,
    Player8, Player9, Player10, Player11, Player12, CurrentPlayer, Foes,
    Allies, NeutralPlayers, AllPlayers, Force1, Force2, Force3, Force4,
    NonAlliedVictoryPlayers, Enable, Disable, Toggle, Ore, Gas, OreAndGas,
    Total, Units, Buildings, UnitsAndBuildings, Kills, Razings,
    KillsAndRazings, Custom, Set, Clear, Random, Cleared
)

# String parser
from .mapdata.nametable import (
    ParseUnit,
    ParseLocation,
    ParseString
)

# Property parser
from .mapdata.prptable import ParseProperty

# Map logic related
from .mapdata.maprw import LoadMap, SaveMap, GetCHKSection
from .mapdata.doevents import EUDDoEvents

# Utilities
from .utils.utils import (
    EPD, FlattenList, SCM2Text, List2Assignable, Assignable2List
)

from .utils import binio, ubconv
