from ..base import *
from .vtable import EUDVTable, EUDVariable


class EUDFunc:
	def __init__(self, starttrig, endtrig, vt, argn, retn):
		assert 0 <= retn < 16 and 0 <= argn < 16
		assert isinstance(vt, EUDVTable)

		self._fstarttrig = starttrig
		self._fendtrig = endtrig
		self._vt = vt
		self._retn = retn
		self._argn = argn
		
	def GetVTable(self):
		return self._vt
	
	def call(self, *args):
		assert len(args) == self._argn
		
		callend = Forward()
		
		# Bind arguments to vt
		callactions = [SetNextPtr(self._fendtrig, callend)]
		
		vt = self._vt
		vtvars = vt.GetVariables()
		vtset = set()
		
		# Collect variable binding actions & vtables needing to be traversed
		for i, arg in enumerate(args):
			if type(arg) is EUDVariable: # need QueueAssignTo action
				callactions.extend(arg.QueueAssignTo(vtvars[i]))
				vtset.add(arg.GetVTable()) # This vt needs to be traversed for argument to be really binded.
				
			else:
				callactions.append(vtvars[i].SetNumber(arg)) # Just set constant
	

		# Add vt traversal actions, if needed
		vtlist = list(vtset)
		if vtlist: # if there is vts to be traversed
			for i in range(len(vtlist) - 1):
				callactions.append(SetNextPtr(vtlist[i], vtlist[i + 1]))
	
			callactions.append(SetNextPtr(vtlist[len(vtlist) - 1], self._fstarttrig))
			bindernext = vtlist[0]
	
		else:
			bindernext = self._fstarttrig
	
		
		assert len(callactions) <= 64, '[Not implemented yet] Too much action required for function call. Report this, then I wil maybe fix.'
		# Create argument binder
		Trigger(
			nextptr = bindernext,
			actions = callactions
		)
		
		callend << NextTrigger()

		# Done.
		ret = tuple(vtvars[self._argn : self._argn + self._retn])
		if len(ret) == 1:
			ret = ret[0]
		return ret

	