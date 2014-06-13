"""
This file defines class Trigger, Condition, Actions. Trigger class represents
triggers with next pointer. Each class is addressable. This file also defines
PushTriggerScope and PopTriggerScope function for trigger scoping.
"""

from .eudobj import EUDObject
from .expr import Expr, IsValidExpr, Evaluate
from ..payload.rlocint import RelocatableInt

# Utility for Trigger
def _FlattenList(l):
	ret = []
	for item in l:
		try:
			ret.extend(_FlattenList(item))
		except: # item cannot be flattened. Maybe already flattened?
			ret.append(item)
			
	return ret

# Trigger scoping thing
_last_trigger = [None]
def PushTriggerScope():
	_last_trigger.append(None)

def PopTriggerScope():
	_last_trigger.pop()



# Used while evaluating Trigger
_next_triggers = []
class NextTrigger(Expr):
	def __init__(self):
		_next_triggers.append(self)
		
	def SetTrigger(self, trg):
		self._trg = trg
		
	def GetDependencyList(self):
		return [self._trg]
	
	def Evaluate(self):
		return Evaluate(self._trg)


class Trigger(EUDObject):
	def __init__(self, nextptr = None, conditions = [], actions = []):
		global _last_trigger
		global _next_triggers
		
		super().__init__()

		conditions = _FlattenList(conditions)
		actions = _FlattenList(actions)
		
		# basic assertion
		assert len(conditions) <= 16
		assert len(actions) <= 64
		
		for cond in conditions:
			assert type(cond) is Condition
			
		for act in actions:
			assert type(act) is Action


		# Set fields
		if nextptr:
			assert IsValidExpr(nextptr), "nextptr is not an addressable object or expression."
		self._nextptr = nextptr
		self._conditions = conditions
		self._actions = actions
		self._nexttrg = 0xFFFFFFFF


		# Set parents of conditions and actions.
		for i, cond in enumerate(conditions):
			cond.SetParentTrigger(self, i)

		for i, act in enumerate(actions):
			act.SetParentTrigger(self, i)


		
		# link previous trigger with this, if previous trigger had not specified nextptr.
		last_trigger = _last_trigger.pop()
		if last_trigger:
			if last_trigger._nextptr is None:
				last_trigger._nextptr = self
			last_trigger._nexttrg = self
		last_trigger = self
		_last_trigger.append(last_trigger)
		
		# link NextTriggers
		for nt in _next_triggers:
			nt.SetTrigger(self)
			
		_next_triggers = []
		
		
	def MUTATE_SetNextPtr(self, nexttrg):
		assert nexttrg
		self._nextptr = nexttrg
		
	# some helper func
	def NextPtr(self):
		return self + 4
	
	def Condition(self, index):
		return self._conditions[index]
	
	def Action(self, index):
		return self._actions[index]
	
	
	# function needed for payloadmanager
	def GetDataSize(self):
		return 2408

	def GetDependencyList(self):
		deplist = [self._nextptr]

		for cond in self._conditions:
			deplist.extend(cond.GetDependencyList())

		for act in self._actions:
			deplist.extend(act.GetDependencyList())

		return deplist

	
	def WritePayload(self, buf):
		_next_trigger = self._nexttrg
		
		buf.EmitDword(0)
		if self._nextptr is None:
			buf.EmitDword(0xFFFFFFFF) # by default behavior.
		else:
			buf.EmitDword(self._nextptr)

		for cond in self._conditions:
			cond.WritePayload(buf)

		buf.EmitBytes(bytes(20 * (16 - len(self._conditions))))

		for act in self._actions:
			act.WritePayload(buf)

		buf.EmitBytes(bytes(32 * (64 - len(self._actions))))
		
		# 04 00 00 00 means 'preserve trigger'.
		buf.EmitBytes(b'\x04\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0')





"""
Condition class. Immutable. Stock conditions are defined at stocktrg.
"""
class Condition(Expr):
	def __init__(self, locid, player, amount, unitid, comparison, condtype, restype, flags):
		assert IsValidExpr(locid)
		assert IsValidExpr(player)
		assert IsValidExpr(amount)
		assert IsValidExpr(unitid)
		assert IsValidExpr(comparison)
		assert IsValidExpr(condtype)
		assert IsValidExpr(restype)
		assert IsValidExpr(flags)
		
		super(Condition, self).__init__()
		self._locid = locid
		self._player = player
		self._amount = amount
		self._unitid = unitid
		self._comparison = comparison
		self._condtype = condtype
		self._restype = restype
		self._flags = flags
		
		self._parenttrg = None
		self._condindex = None

	def SetParentTrigger(self, trg, index):
		assert self._parenttrg is None, 'Condition cannot be shared by two triggers. Deep copy each conditions'
		assert trg is not None, 'Trigger should not be null.'
		assert 0 <= index < 16, 'WTF'

		self._parenttrg = trg
		self._condindex = index

	def Disable(self):
		self._flags |= 2



	# Expr
	def Evaluate(self):
		return Evaluate(self._parenttrg) + RelocatableInt(8 + 20 * self._condindex, 0)

	# Used by Trigger::GetDependencyList
	def GetDependencyList(self):
		return [
			self._locid,
			self._player,
			self._amount,
			self._unitid,
			self._comparison,
			self._condtype,
			self._restype,
			self._flags,
		]

	# Used by Trigger::WritePayload
	def WritePayload(self, buf):
		buf.EmitDword (self._locid)
		buf.EmitDword (self._player)
		buf.EmitDword (self._amount)
		buf.EmitWord  (self._unitid)
		buf.EmitByte  (self._comparison)
		buf.EmitByte  (self._condtype)
		buf.EmitByte  (self._restype)
		buf.EmitByte  (self._flags)
		buf.EmitBytes (b'\0\0')
		
		
"""
Action class. Immutable. Stock actions are defined at stocktrg.
"""
class Action(Expr):
	def __init__(self, locid1, strid, wavid, time, player1, player2, unitid, acttype, amount, flags):
		super(Action, self).__init__()
		
		assert IsValidExpr(locid1)
		assert IsValidExpr(strid)
		assert IsValidExpr(wavid)
		assert IsValidExpr(time)
		assert IsValidExpr(player1)
		assert IsValidExpr(player2)
		assert IsValidExpr(unitid)
		assert IsValidExpr(acttype)
		assert IsValidExpr(amount)
		assert IsValidExpr(flags)
		
		self._locid1 = locid1
		self._strid = strid
		self._wavid = wavid
		self._time = time
		self._player1 = player1
		self._player2 = player2
		self._unitid = unitid
		self._acttype = acttype
		self._amount = amount
		self._flags = flags
	
		self._parenttrg = None
		self._actindex = None

	def SetParentTrigger(self, trg, index):
		assert self._parenttrg is None, 'Condition cannot be shared by two triggers. Deep copy each conditions'
		assert trg is not None, 'Trigger should not be null.'
		assert 0 <= index < 64, 'WTF'

		self._parenttrg = trg
		self._actindex = index

	def Disable(self):
		self._flags |= 2



	# Expr
	def Evaluate(self):
		return Evaluate(self._parenttrg) + RelocatableInt(8 + 320 + 32 * self._actindex, 0)
		
	# Used in Trigger::GetDependencyList
	def GetDependencyList(self):
		return [
			self._locid1,
			self._strid,
			self._wavid,
			self._time,
			self._player1,
			self._player2,
			self._unitid,
			self._acttype,
			self._amount,
			self._flags,
		]


	# Used in Trigger::WritePayload
	def WritePayload(self, buf):
		buf.EmitDword (self._locid1)
		buf.EmitDword (self._strid)
		buf.EmitDword (self._wavid)
		buf.EmitDword (self._time)
		buf.EmitDword (self._player1)
		buf.EmitDword (self._player2)
		buf.EmitWord  (self._unitid)
		buf.EmitByte  (self._acttype)
		buf.EmitByte  (self._amount)
		buf.EmitByte  (self._flags)
		buf.EmitBytes (b'\0\0\0')
		

	
def Disabled(item):
	item.Disable()
	return item