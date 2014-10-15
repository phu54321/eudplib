'''
Copyright (c) 2014 trgk

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.
   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.
   3. This notice may not be removed or altered from any source
   distribution.
'''
from .trgstrconst import AIScriptDict
from .utils import binio

# Long list of known constants


class _Unique:
    pass

All = _Unique()
Enemy = _Unique()
Ally = _Unique()
AlliedVictory = _Unique()
AtLeast = _Unique()
AtMost = _Unique()
Exactly = _Unique()
SetTo = _Unique()
Add = _Unique()
Subtract = _Unique()
Move = _Unique()
Patrol = _Unique()
Attack = _Unique()
P1 = _Unique()
P2 = _Unique()
P3 = _Unique()
P4 = _Unique()
P5 = _Unique()
P6 = _Unique()
P7 = _Unique()
P8 = _Unique()
P9 = _Unique()
P10 = _Unique()
P11 = _Unique()
P12 = _Unique()
Player1 = _Unique()
Player2 = _Unique()
Player3 = _Unique()
Player4 = _Unique()
Player5 = _Unique()
Player6 = _Unique()
Player7 = _Unique()
Player8 = _Unique()
Player9 = _Unique()
Player10 = _Unique()
Player11 = _Unique()
Player12 = _Unique()
CurrentPlayer = _Unique()
Foes = _Unique()
Allies = _Unique()
NeutralPlayers = _Unique()
AllPlayers = _Unique()
Force1 = _Unique()
Force2 = _Unique()
Force3 = _Unique()
Force4 = _Unique()
NonAlliedVictoryPlayers = _Unique()
Enable = _Unique()
Disable = _Unique()
Toggle = _Unique()
Ore = _Unique()
Gas = _Unique()
OreAndGas = _Unique()
Total = _Unique()
Units = _Unique()
Buildings = _Unique()
UnitsAndBuildings = _Unique()
Kills = _Unique()
Razings = _Unique()
KillsAndRazings = _Unique()
Custom = _Unique()
Set = _Unique()
Clear = _Unique()
Random = _Unique()
Cleared = _Unique()

AllyStatusDict = {
    Enemy: 0,
    Ally: 1,
    AlliedVictory: 2,
}

ComparisonDict = {
    AtLeast: 0,
    AtMost: 1,
    Exactly: 10,
}

ModifierDict = {
    SetTo: 7,
    Add: 8,
    Subtract: 9,
}

OrderDict = {
    Move: 0,
    Patrol: 1,
    Attack: 2,
}

PlayerDict = {
    P1: 0,
    P2: 1,
    P3: 2,
    P4: 3,
    P5: 4,
    P6: 5,
    P7: 6,
    P8: 7,
    P9: 8,
    P10: 9,
    P11: 10,
    P12: 11,
    Player1: 0,
    Player2: 1,
    Player3: 2,
    Player4: 3,
    Player5: 4,
    Player6: 5,
    Player7: 6,
    Player8: 7,
    Player9: 8,
    Player10: 9,
    Player11: 10,
    Player12: 11,
    CurrentPlayer: 13,
    Foes: 14,
    Allies: 15,
    NeutralPlayers: 16,
    AllPlayers: 17,
    Force1: 18,
    Force2: 19,
    Force3: 20,
    Force4: 21,
    NonAlliedVictoryPlayers: 26,
}

PropStateDict = {
    Enable: 4,
    Disable: 5,
    Toggle: 6,
}

ResourceDict = {
    Ore: 0,
    Gas: 1,
    OreAndGas: 2,
}

ScoreDict = {
    Total: 0,
    Units: 1,
    Buildings: 2,
    UnitsAndBuildings: 3,
    Kills: 4,
    Razings: 5,
    KillsAndRazings: 6,
    Custom: 7,
}

SwitchActionDict = {
    Set: 4,
    Clear: 5,
    Toggle: 6,
    Random: 11,
}

SwitchStateDict = {
    Set: 2,
    Cleared: 3,
}


def ParseConst(d, s):
    return d.get(s, s)


def ParseAllyStatus(s):
    '''
    Convert [Enemy, Ally, AlliedVictory] to number [0, 1, 2].
    '''
    return ParseConst(AllyStatusDict, s)


def ParseComparison(s):
    '''
    Convert [AtLeast, AtMost, Exactly] to number [0, 1, 10].
    '''
    return ParseConst(ComparisonDict, s)


def ParseModifier(s):
    '''
    Convert [SetTo, Add, Subtract] to number [7, 8, 9].
    '''
    return ParseConst(ModifierDict, s)


def ParseOrder(s):
    '''
    Convert [Move, Patrol, Attack] to number [0, 1, 2].
    '''
    return ParseConst(OrderDict, s)


def ParsePlayer(s):
    '''
    Convert player identifier to corresponding number.

    ======================= ========
        Identifier           Number
    ======================= ========
    P1                         0
    P2                         1
    P3                         2
    P4                         3
    P5                         4
    P6                         5
    P7                         6
    P8                         7
    P9                         8
    P10                        9
    P11                        10
    P12                        11
    Player1                    0
    Player2                    1
    Player3                    2
    Player4                    3
    Player5                    4
    Player6                    5
    Player7                    6
    Player8                    7
    Player9                    8
    Player10                   9
    Player11                   10
    Player12                   11
    CurrentPlayer              13
    Foes                       14
    Allies                     15
    NeutralPlayers             16
    AllPlayers                 17
    Force1                     18
    Force2                     19
    Force3                     20
    Force4                     21
    NonAlliedVictoryPlayers    26
    ======================= ========

    '''
    return ParseConst(PlayerDict, s)


def ParsePropState(s):
    '''
    Convert [Enable, Disable, Toogle] to number [4, 5, 6]
    '''
    return ParseConst(PropStateDict, s)


def ParseResource(s):
    '''
    Convert [Ore, Gas, OreAndGas] to [0, 1, 2]
    '''
    return ParseConst(ResourceDict, s)


def ParseScore(s):
    '''
    Convert score type identifier to number.

    ================= ========
        Score type     Number
    ================= ========
    Total                0
    Units                1
    Buildings            2
    UnitsAndBuildings    3
    Kills                4
    Razings              5
    KillsAndRazings      6
    Custom               7
    ================= ========

    '''
    return ParseConst(ScoreDict, s)


def ParseSwitchAction(s):
    '''
    Convert [Set, Clear, Toogle, Random] to [4, 5, 6, 11].
    '''
    return ParseConst(SwitchActionDict, s)


def ParseSwitchState(s):
    '''
    Convert [Set, Cleared] to [2, 3].
    '''
    return ParseConst(SwitchStateDict, s)


def ParseAIScript(s):
    '''
    Convert known AI Script to script ID. See :func:`eudtrg.RunAIScript` and
    :func:`eudtrg.RunAIScriptAt` for list of AI scripts.
    '''
    return binio.b2i4(ParseConst(AIScriptDict, s), 0)


def ParseCount(s):
    '''
    Convert [All, (other numbers)] to number [0, (as-is)].
    '''
    if s is All:
        return 0
    else:
        return s
