from ..base import *

class _EUDVTable(Trigger):
	def __init__(self, varn):
		PushTriggerScope()
		variables = [Forward() for _ in range(varn)]
		
		super().__init__(
			actions = 
				[variables[i] << Disabled(SetDeaths(0, SetTo, 0, 0)) for i in range(varn)] + 
				[SetDeaths(EPD(variables[i] + 28), SetTo, 2, 0) for i in range(varn)]
		)
		
		self._var = [EUDVariable(var, self) for var in variables]
		PopTriggerScope()
		
	def GetVariableList(self):
		return self._var
	
	
class EUDVariable:
	def __init__(self, vartrigger, originvt):
		self._varact = vartrigger
		self._originvt = originvt
		
		
	def GetActionAddr(self):
		return self._varact
		
	def GetVTable(self):
		return self._originvt
	
	
	def AtLeast(self, number):
		return Memory(self._varact + 20, AtLeast, number)
	
	def AtMost(self, number):
		return Memory(self._varact + 20, AtMost, number)
	
	def Exactly(self, number):
		return Memory(self._varact + 20, Exactly, number)
	
		
	def SetNumber(self, number):
		return SetMemory(self._varact + 20, SetTo, number)
	
	def AddNumber(self, number):
		return SetMemory(self._varact + 20, Add, number)
	
	def SubtractNumber(self, number):
		return SetMemory(self._varact + 20, Subtract, number)
	
	
	
	def QueueAssignTo(self, dest):
		if isinstance(dest, EUDVariable):
			dest = EPD(dest.GetActionAddr() + 20)
		
		return [
			SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
			SetDeaths(EPD(self._varact + 24), SetTo, 0x072D0000, 0),
			SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
		]
	
	
	def QueueAddTo(self, dest):
		if isinstance(dest, EUDVariable):
			dest = EPD(dest.GetActionAddr() + 20)
		
		return [
			SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
			SetDeaths(EPD(self._varact + 24), SetTo, 0x082D0000, 0),
			SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
		]
		
	def QueueSubtractTo(self, dest):
		if isinstance(dest, EUDVariable):
			dest = EPD(dest.GetActionAddr() + 20)
		
		return [
			SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
			SetDeaths(EPD(self._varact + 24), SetTo, 0x092D0000, 0),
			SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
		]



def CreateVariable(varn):
	vts = []
	variables = []

	while varn > 0:
		varn_for_vt = min(varn, 32)
		varn -= varn_for_vt
		vt = _EUDVTable(varn_for_vt)
		vtn.append(vt)
		variables.extend(list(_EUDVTable.GetVariableList()))

	if varn == 1:
		return variables[0]
	else:
		return variables
