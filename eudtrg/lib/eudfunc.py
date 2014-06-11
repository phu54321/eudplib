"""
Basic eud function library.


"""

from eudtrg.base import * #@UnusedWildImports
from eudtrg.lib.vtable import EUDVariable

class EUDFunc:
	def __init__(self, starttrig, endtrig, vt, argn, retn):
		assert 0 <= retn < 16 and 0 <= argn < 16

		self._fstarttrig = starttrig
		self._fendtrig = endtrig
		self._vt = vt
		self._retn = retn
		self._argn = argn

		
	def call(self, *args):
		assert len(args) == self._argn

		vtvars = self._vt.GetVariables()
		retn = self._retn
		argn = self._argn
		fstart = self._fstarttrig
		fend = self._fendtrig

		# Trigger to return after call
		callend = Addr()

		callactions = [
			SetNextPtr(fend, callend)
		]

		vtset = set()
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

			callactions.append(SetNextPtr(vtlist[len(vtlist) - 1], fstart))
			bindernext = vtlist[0]

		else:
			bindernext = fstart

		
		assert len(callactions) <= 64, '[Not yet implemented] Too much action required for function call. Report this, then I wil maybe fix.'
		# Create argument binder
		Trigger(
			nextptr = bindernext,
			actions = callactions
		)

		# Dummy trigger after call. Needed for a return point.
		callend << Trigger()

		# Done.
		ret = tuple(vtvars[argn : argn + retn])
		if len(ret) == 1:
			ret = ret[0]
		return ret