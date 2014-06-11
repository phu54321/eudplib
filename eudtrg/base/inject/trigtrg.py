"""
Templates for TRIG section triggers. Internally used in eudtrg.
"""

from ctypes import * #@UnusedWildImport

class TrigCond(LittleEndianStructure):
	_fields_ = [
		('locid', c_uint),
		('player', c_uint),
		('amount', c_uint),
		('unitid', c_ushort),
		('comparison', c_ubyte),
		('condtype', c_ubyte),
		('restype', c_ubyte),
		('flag', c_ubyte),
		('internal', c_ubyte * 2)
	]


class TrigAct(LittleEndianStructure):
	_fields_ = [
		('locid1', c_uint),
		('strid', c_uint),
		('wavid', c_uint),
		('time', c_uint),
		('player1', c_uint),
		('player2', c_uint),
		('unitid', c_ushort),
		('acttype', c_ubyte),
		('amount', c_ubyte),
		('flags', c_ubyte),
		('internal', c_ubyte * 3)
	]


class TrigBox(LittleEndianStructure):
	_fields_ = [
		('conditions', TrigCond * 16),
		('actions', TrigAct * 64),
		('internal', c_uint),
		('effplayer', c_ubyte * 28)
	]


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

# constructor
def CreateTRIGCondition(locid, player, amount, unitid, comparison, condtype, restype, flag):
	cond = TrigCond()
	cond.locid = locid
	cond.player = player
	cond.amount = amount
	cond.unitid = unitid
	cond.comparison = comparison
	cond.condtype = condtype
	cond.restype = restype
	cond.flag = flag
	return cond

def CreateTRIGAction(locid1, strid, wavid, time, player1, player2, unitid, acttype, amount, flags):
	act = TrigAct()
	act.locid1 = locid1
	act.strid = strid
	act.wavid = wavid
	act.time = time
	act.player1 = player1
	act.player2 = player2
	act.unitid = unitid
	act.acttype = acttype
	act.amount = amount
	act.flags = flags
	return act

def CreateTRIGTrigger(players, conditions, actions, preservetrigger = False):
	assert type(players) is list and type(conditions) is list and type(actions) is list
	assert len(conditions) <= 16
	assert len(actions) <= 64

	trg = TrigBox()
	for i in range(16):
		memset(addressof(trg.conditions[i]), 0x00, sizeof(TrigCond))

	for i in range(64):
		memset(addressof(trg.actions[i]), 0x00, sizeof(TrigAct))

	for p in players:
		trg.effplayer[p] = 1

	for i in range(len(conditions)):
		trg.conditions[i] = conditions[i]
	if len(conditions) != 16:
		trg.conditions[len(conditions)].condtype = 0

	for i in range(len(actions)):
		trg.actions[i] = actions[i]
	if len(actions) != 64:
		trg.actions[len(actions)].acttype = 0

		

	if preservetrigger:
		trg.internal = 4

	return trg


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

# helper f
def CreateTRIGPlayerUnit2Memory(player, unit):
	return 0x0058A364 + (player + unit * 12) * 4

def Memory2Player(offset):
	assert offset % 4 == 0
	return (offset - 0x0058A364) // 4

