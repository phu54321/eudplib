"""
Declares base struct Addressable and Addr. Addressable objects means object
loadable into Starcraft memory. Addr object acts as a pointer to Addressable
object.
"""

from ..payload.rlocint import RelocatableInt
from .expr import Expr

class EUDObject(Expr):
	def __init__(self):
		super().__init__()
		self._address = None
		
	def SetAddress(self, address):
		assert self._address is None
		self._address = address
		
	def ResetAddress(self):
		assert self._address is not None
		self._address = None
		
	def EvalImpl(self):
		assert self._address is not None, 'Object of type %s not initalized' % type(self)
		return RelocatableInt(self._address, 4)
		
	def GetDependencyList(self):
		raise NotImplementedError("Subclass %s should implement this" % str(type(self)))
	
	def GetDataSize(self):
		raise NotImplementedError("Subclass %s should implement this" % str(type(self)))
	
	def WritePayload(self, emitbuffer):
		raise NotImplementedError("Subclass %s should implement this" % str(type(self)))


