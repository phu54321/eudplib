'''
Templates for TRIG section triggers. Uesd internally in eudtrglib.
'''

from eudtrglib import LICENSE #@UnusedImport

from struct import pack
from ..utils import binio


# for Deaths
AtLeast  = 0
AtMost   = 1
Exactly  = 10

# for Set Death
SetTo    = 7
Add      = 8
Subtract = 9

# player enum
Player1        = 0
Player2        = 1
Player3        = 2
Player4        = 3
Player5        = 4
Player6        = 5
Player7        = 6
Player8        = 7
Player9        = 8
Player10       = 9
Player11       = 10
Player12       = 11
CurrentPlayer  = 13
Foes           = 14
Allies         = 15
NeutralPlayers = 16
AllPlayers     = 17
Force1         = 18
Force2         = 19
Force3         = 20
Force4         = 21
Unused1        = 22
Unused2        = 23
Unused3        = 24
Unused4        = 25
NonAlliedVP    = 26

# for Switch
Set            = 2
Cleared        = 3

# for Set Switch
SwitchSet      = 4
SwitchClear    = 5
SwitchToogle   = 6
SwitchRandom   = 11

# constructor
_bc_dict = {
    1:binio.i2b1,
    2:binio.i2b2,
    4:binio.i2b4,
    None: (lambda x: x)
}

def _bconstruct(vspair):
    btb = []
    for value, size in vspair:
        btb.append(_bc_dict[size](value))
    return b''.join(btb)

def CreateTRIGCondition(locid, player, amount, unitid, comparison, condtype, restype, flag):
    if player<0: player += 0x100000000 #EPD
    return pack('<IIIHBBBBBB', locid, player, amount, unitid, comparison, condtype, restype, flag, 0, 0)

def CreateTRIGAction(locid1, strid, wavid, time, player1, player2, unitid, acttype, amount, flags):
    if player1<0: player1 += 0x100000000 #EPD
    if player2<0: player2 += 0x100000000 #EPD
    return pack('<IIIIIIHBBBBBB', locid1, strid, wavid, time, player1, player2, unitid, acttype, amount, flags, 0, 0, 0)
    
    
def CreateTRIGTrigger(players, conditions, actions, preservetrigger = False):
    assert type(players) is list and type(conditions) is list and type(actions) is list
    assert len(conditions) <= 16
    assert len(actions) <= 64

    peff = bytearray(28)
    for p in players:
        peff[p] = 1

    b = _bconstruct(
        [(cond, None) for cond in conditions] +
        [(bytes(20*(16-len(conditions))), None)] +
        [(act, None) for act in actions] +
        [(bytes(32*(64-len(actions))), None)] +
        [(b'\x04\0\0\0' if preservetrigger else b'\0\0\0\0', None)] +
        [(bytes(peff), None)]
    )
    assert len(b) == 2400
    return b


# file writer
def WriteTRIGTrg(fp, triggers):
    if type(fp) is str:
        fp = open(fp, 'wb')

    fp.write(b'\x71\x77\x98\x36\x18\x00\x00\x00')
    for t in triggers:
        fp.write(bytes(t))


# conditions
def CreateTRIGDeaths(player, comparison, number, unit):
    return CreateTRIGCondition(0x00000000, player, number, unit, comparison, 0x0F, 0x00, 0x10)

def CreateTRIGMemory(offset, comparison, number):
    assert offset % 4 == 0 # only this kind of comparison is possible
    player = Memory2Player(offset)

    if 0 <= player < 12 * 228: # eud possible
        unit = player // 12
        player = player % 12
        return CreateTRIGDeaths(player, comparison, number, unit)

    else: # use epd
        return CreateTRIGDeaths(player, comparison, number, 0)

def CreateTRIGSwitch(Switch, State):
    return CreateTRIGCondition(0, 0, 0, 0, State, 11, Switch, 0)


# actions
def CreateTRIGSetDeaths(player, settype, number, unit):
    return CreateTRIGAction(0x00000000, 0x00000000, 0x00000000, 0x00000000, player, number, unit, 0x2D, settype, 0x14)

def CreateTRIGSetMemory(offset, settype, number):
    assert offset % 4 == 0
    player = Memory2Player(offset)

    if 0 <= player < 12 * 228: # eud possible
        unit = player // 12
        player = player % 12
        return CreateTRIGSetDeaths(player, settype, number, unit)

    else: # use epd
        return CreateTRIGSetDeaths(player, settype, number, 0)

def CreateTRIGSetSwitch(Switch, SwitchState):
    return CreateTRIGAction(0, 0, 0, 0, 0, Switch, 0, 13, SwitchState, 4)

def CreateTRIGPreserveTrigger():
    return CreateTRIGAction(0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x0000, 3, 0x00, 4)


def CreateTRIGDisplayTextMessage(Text):
    return CreateTRIGAction(0, Text, 0, 0, 0, 0, 0, 9, 0, 4)

def CreateTRIGDraw():
    return CreateTRIGAction(0, 0, 0, 0, 0, 0, 0, 56, 0, 4)


# helper f
def CreateTRIGPlayerUnit2Memory(player, unit):
    return 0x0058A364 + (player + unit * 12) * 4

def Memory2Player(offset):
    assert offset % 4 == 0
    return (offset - 0x0058A364) // 4

