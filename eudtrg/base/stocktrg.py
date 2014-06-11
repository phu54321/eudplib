"""
Useful stock triggers.
"""

from .dataspec import trigger
from .utils.utils import EPD

# predefined constants
triggerend = 0xFFFFFFFF # bigger than 0x80000000

# for Deaths
AtLeast  = 0
AtMost   = 1
Exactly  = 10

# for Set Death
SetTo	= 7
Add	  = 8
Subtract = 9

# player enum
Player1		= 0
Player2		= 1
Player3		= 2
Player4		= 3
Player5		= 4
Player6		= 5
Player7		= 6
Player8		= 7
Player9		= 8
Player10	   = 9
Player11	   = 10
Player12	   = 11
CurrentPlayer  = 13
Foes		   = 14
Allies		 = 15
NeutralPlayers = 16
AllPlayers	 = 17
Force1		 = 18
Force2		 = 19
Force3		 = 20
Force4		 = 21
Unused1		= 22
Unused2		= 23
Unused3		= 24
Unused4		= 25
NonAlliedVP	= 26

# for Switch
Set			= 2
Cleared		= 3

# for Set Switch
SwitchSet	  = 4
SwitchClear	= 5
SwitchToogle   = 6
SwitchRandom   = 11


# predefined conditions
def NoCondition():
	return trigger.Condition(0, 0, 0, 0, 0, 0, 0, 0)

def CountdownTimer(Comparison, Time):
	return trigger.Condition(0, 0, Time, 0, Comparison, 1, 0, 0)

def Command(Player, Comparison, Number, Unit):
	return trigger.Condition(0, Player, Number, Unit, Comparison, 2, 0, 0)

def Bring(Player, Comparison, Number, Unit, Location):
	return trigger.Condition(Location, Player, Number, Unit, Comparison, 3, 0, 0)

def Accumulate(Player, Comparison, Number, ResourceType):
	return trigger.Condition(0, Player, Number, 0, Comparison, 4, ResourceType, 0)

def Kills(Player, Comparison, Number, Unit):
	return trigger.Condition(0, Player, Number, Unit, Comparison, 5, 0, 0)

def CommandMost(Unit):
	return trigger.Condition(0, 0, 0, Unit, 0, 6, 0, 0)

def CommandMostAt(Unit, Location):
	return trigger.Condition(Location, 0, 0, Unit, 0, 7, 0, 0)

def MostKills(Unit):
	return trigger.Condition(0, 0, 0, Unit, 0, 8, 0, 0)

def HighestScore(ScoreType):
	return trigger.Condition(0, 0, 0, 0, 0, 9, ScoreType, 0)

def MostResources(ResourceType):
	return trigger.Condition(0, 0, 0, 0, 0, 10, ResourceType, 0)

def Switch(Switch, State):
	return trigger.Condition(0, 0, 0, 0, State, 11, Switch, 0)

def ElapsedTime(Comparison, Time):
	return trigger.Condition(0, 0, Time, 0, Comparison, 12, 0, 0)

def Briefing():
	return trigger.Condition(0, 0, 0, 0, 0, 13, 0, 0)

def Opponents(Player, Comparison, Number):
	return trigger.Condition(0, Player, Number, 0, Comparison, 14, 0, 0)

def Deaths(Player, Comparison, Number, Unit):
	return trigger.Condition(0, Player, Number, Unit, Comparison, 15, 0, 0)

def CommandLeast(Unit):
	return trigger.Condition(0, 0, 0, Unit, 0, 16, 0, 0)

def CommandLeastAt(Unit, Location):
	return trigger.Condition(Location, 0, 0, Unit, 0, 17, 0, 0)

def LeastKills(Unit):
	return trigger.Condition(0, 0, 0, Unit, 0, 18, 0, 0)

def LowestScore(ScoreType):
	return trigger.Condition(0, 0, 0, 0, 0, 19, ScoreType, 0)

def LeastResources(ResourceType):
	return trigger.Condition(0, 0, 0, 0, 0, 20, ResourceType, 0)

def Score(Player, ScoreType, Comparison, Number):
	return trigger.Condition(0, Player, Number, 0, Comparison, 21, ScoreType, 0)

def Always():
	return trigger.Condition(0, 0, 0, 0, 0, 22, 0, 0)

def Never():
	return trigger.Condition(0, 0, 0, 0, 0, 23, 0, 0)


# predefined trigger.Action
def NoAction():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 0, 0, 4)

def Victory():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 1, 0, 4)

def Defeat():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 2, 0, 4)

def PreserveTrigger():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 3, 0, 4)

def Wait(Time):
	return trigger.Action(0, 0, 0, Time, 0, 0, 0, 4, 0, 4)

def PauseGame():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 5, 0, 4)

def UnpauseGame():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 6, 0, 4)

def Transmission(Unit, Where, WAVName, TimeModifier, Time, Text, AlwaysDisplay):
	return trigger.Action(Where, Text, WAVName, Time, 0, 0, Unit, 7, TimeModifier, AlwaysDisplay)

def PlayWAV(WAVName):
	return trigger.Action(0, 0, WAVName, 0, 0, 0, 0, 8, 0, 4)

def DisplayText(Text, AlwaysDisplay):
	return trigger.Action(0, Text, 0, 0, 0, 0, 0, 9, 0, AlwaysDisplay)

def CenterView(Where):
	return trigger.Action(Where, 0, 0, 0, 0, 0, 0, 10, 0, 4)

def CreateUnitWithProperties(Count, Unit, Where, Player, Properties):
	return trigger.Action(Where, 0, 0, 0, Player, Properties, Unit, 11, Count, 28)

def SetMissionObjectives(Text):
	return trigger.Action(0, Text, 0, 0, 0, 0, 0, 12, 0, 4)

def SetSwitch(Switch, State):
	return trigger.Action(0, 0, 0, 0, 0, Switch, 0, 13, State, 4)

def SetCountdownTimer(TimeModifier, Time):
	return trigger.Action(0, 0, 0, Time, 0, 0, 0, 14, TimeModifier, 4)

def RunAIScript(Script):
	return trigger.Action(0, 0, 0, 0, 0, Script, 0, 15, 0, 4)

def RunAIScriptAt(Script, Where):
	return trigger.Action(Where, 0, 0, 0, 0, Script, 0, 16, 0, 4)

def LeaderBoardControl(Unit, Label):
	return trigger.Action(0, Label, 0, 0, 0, 0, Unit, 17, 0, 20)

def LeaderBoardControlAt(Unit, Location, Label):
	return trigger.Action(Location, Label, 0, 0, 0, 0, Unit, 18, 0, 20)

def LeaderBoardResources(ResourceType, Label):
	return trigger.Action(0, Label, 0, 0, 0, 0, ResourceType, 19, 0, 4)

def LeaderBoardKills(Unit, Label):
	return trigger.Action(0, Label, 0, 0, 0, 0, Unit, 20, 0, 20)

def LeaderBoardScore(ScoreType, Label):
	return trigger.Action(0, Label, 0, 0, 0, 0, Score, 21, 0, 4)

def KillUnit(Unit, Player):
	return trigger.Action(0, 0, 0, 0, Player, 0, Unit, 22, 0, 20)

def KillUnitAt(Count, Unit, Where, ForPlayer):
	return trigger.Action(Where, 0, 0, 0, ForPlayer, 0, Unit, 23, Count, 20)

def RemoveUnit(Unit, Player):
	return trigger.Action(0, 0, 0, 0, Player, 0, Unit, 24, 0, 20)

def RemoveUnitAtLocation(Count, Unit, ForPlayer, Where):
	return trigger.Action(Where, 0, 0, 0, ForPlayer, 0, Unit, 25, Count, 20)

def SetResources(Player, Modifier, Amount, ResourceType):
	return trigger.Action(0, 0, 0, 0, Player, Amount, ResourceType, 26, Modifier, 4)

def SetScore(Player, Modifier, Amount, ScoreType):
	return trigger.Action(0, 0, 0, 0, Player, Amount, ScoreType, 27, Modifier, 4)

def MinimapPing(Where):
	return trigger.Action(Where, 0, 0, 0, 0, 0, 0, 28, 0, 4)

def TalkingPortrait(Unit, Time):
	return trigger.Action(0, 0, 0, Time, 0, 0, Unit, 29, 0, 20)

def MuteUnitSpeech():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 30, 0, 4)

def UnMuteUnitSpeech():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 31, 0, 4)

def LeaderBoardComputerPlayers(State):
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 32, State, 4)

def LeaderBoardGoalControl(Goal, Unit, Label):
	return trigger.Action(0, Label, 0, 0, 0, Goal, Unit, 33, 0, 20)

def LeaderBoardGoalControlAt(Goal, Unit, Location, Label):
	return trigger.Action(Location, Label, 0, 0, 0, Goal, Unit, 34, 0, 20)

def LeaderBoardGoalResources(Goal, ResourceType, Label):
	return trigger.Action(0, Label, 0, 0, 0, Goal, ResourceType, 35, 0, 4)

def LeaderBoardGoalKills(Goal, Unit, Label):
	return trigger.Action(0, Label, 0, 0, 0, Goal, Unit, 36, 0, 20)

def LeaderBoardGoalScore(Goal, ScoreType, Label):
	return trigger.Action(0, Label, 0, 0, 0, Goal, ScoreType, 37, 0, 4)

def MoveLocation(Location, OnUnit, Owner, DestLocation):
	return trigger.Action(DestLocation, 0, 0, 0, Owner, Location, OnUnit, 38, 0, 20)

def MoveUnit(Count, UnitType, Owner, StartLocation, DestLocation):
	return trigger.Action(StartLocation, 0, 0, 0, Owner, DestLocation, UnitType, 39, Count, 20)

def LeaderBoardGreed(Goal):
	return trigger.Action(0, 0, 0, 0, 0, Goal, 0, 40, 0, 4)

def SetNextScenario(ScenarioName):
	return trigger.Action(0, ScenarioName, 0, 0, 0, 0, 0, 41, 0, 4)

def SetDoodadState(State, Unit, Owner, Where):
	return trigger.Action(Where, 0, 0, 0, Owner, 0, Unit, 42, State, 20)

def SetInvincibility(State, Unit, Owner, Where):
	return trigger.Action(Where, 0, 0, 0, Owner, 0, Unit, 43, State, 20)

def CreateUnit(Number, Unit, Where, ForPlayer):
	return trigger.Action(Where, 0, 0, 0, ForPlayer, 0, Unit, 44, Number, 20)

def SetDeaths(Player, Modifier, Number, Unit):
	return trigger.Action(0, 0, 0, 0, Player, Number, Unit, 45, Modifier, 20)

def Order(Unit, Owner, StartLocation, Order, DestLocation):
	return trigger.Action(StartLocation, 0, 0, 0, Owner, DestLocation, Unit, 46, Order, 20)

def Comment(Text):
	return trigger.Action(0, Text, 0, 0, 0, 0, 0, 47, 0, 4)

def GiveUnits(Count, Unit, Owner, Where, NewOwner):
	return trigger.Action(Where, 0, 0, 0, Owner, NewOwner, Unit, 48, Count, 20)

def ModifyUnitHitPoints(Count, Unit, Owner, Where, Percent):
	return trigger.Action(Where, 0, 0, 0, Owner, Percent, Unit, 49, Count, 20)

def ModifyUnitEnergy(Count, Unit, Owner, Where, Percent):
	return trigger.Action(Where, 0, 0, 0, Owner, Percent, Unit, 50, Count, 20)

def ModifyUnitShields(Count, Unit, Owner, Where, Percent):
	return trigger.Action(Where, 0, 0, 0, Owner, Percent, Unit, 51, Count, 20)

def ModifyUnitResourceAmount(Count, Owner, Where, NewValue):
	return trigger.Action(Where, 0, 0, 0, Owner, 0, 0, 52, Count, 4)

def ModifyUnitHangarCount(Add, Count, Unit, Owner, Where):
	return trigger.Action(Where, 0, 0, 0, Owner, Add, Unit, 53, Count, 20)

def PauseTimer():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 54, 0, 4)

def UnpauseTimer():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 55, 0, 4)

def Draw():
	return trigger.Action(0, 0, 0, 0, 0, 0, 0, 56, 0, 4)

def SetAllianceStatus(Player, Status):
	return trigger.Action(0, 0, 0, 0, Player, 0, Status, 57, 0, 4)


# compound triggers
def Memory(dest, cmptype, value):
	return Deaths(EPD(dest), cmptype, value, 0)

def SetMemory(dest, modtype, value):
	return SetDeaths(EPD(dest), modtype, value, 0)

def SetNextPtr(trg, dest):
	return SetDeaths(trg.GetNextPtrAddr(), SetTo, dest, 0)