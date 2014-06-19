<<<<<<< HEAD
from ..base import *
from .vtable import EUDVariable
from .varassign import SetVariables

class EUDFunc:
	def __init__(self, starttrig, endtrig, argv, retv):
		argv = FlattenList(argv)
		retv = FlattenList(retv)
		assert 0 <= len(argv) < 16 and 0 <= len(retv) < 16

		self._fstarttrig = starttrig
		self._fendtrig = endtrig
		self._vt = vt
		self._argv = argv
		self._retv = retv
		

	def call(self, args):
		args = FlattenList(args)
		assert len(args) == len(self._argv)

		SetVariables(self._argv, args)

		callend = Forward()
		Trigger(
			nextptr = self._fstarttrig,
			actions = [SetNextPtr(self._fendtrig, callend)]
		)
		callend << NextTrigger()

		return self._retv

	
=======
from .. import LICENSE

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVTable, EUDVariable
from .varassign import SetVariables

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

        vtvars = self._vt.GetVariables()

        SetVariables(vtvars[0:self._argn], args)

        callend = Forward()
        Trigger(
            nextptr = self._fstarttrig,
            actions = [SetNextPtr(self._fendtrig, callend)]
        )
        callend << NextTrigger()

        ret = tuple(vtvars[self._argn : self._argn + self._retn])
        if len(ret) == 1:
            ret = ret[0]
        return ret


>>>>>>> development
