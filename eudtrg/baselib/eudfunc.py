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

	