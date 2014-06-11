"""
Declares base struct Addressable and Addr. Addressable objects means object
loadable into Starcraft memory. Addr object acts as a pointer to Addressable
object.
"""

from ..payload import rlocint
from . import expr

"""
Base class for loadable object. Addressable object has two types.
  - Independent object : Object acts independently. Trigger is independent.
  - Dependent object   : Object is dependent to other parent object.
	 Condition and Action is dependent, and their addresses are calculated
	 by their parent Trigger's address.

Every class inherited from Addressable class should implement
  - GetDependencyList
  - IsIndependent
  - GetDataSize
  - WritePayloadChunk
"""

class Addressable:
	def __init__(self):
		super(Addressable, self).__init__()
		self._address = None
		
	"""
	Called when dependency graph builder assignes independent object an address.
	If object have other objects depending on it, then object can override this
	method to assign addresses to its custom child.
	"""
	def SetAddress(self, address):
		if address is None:
			self._address = None
			return
		
		assert self._address is None
		assert type(address) is int
		self._address = address
		
	"""
	Shouldn't be overridden.
	"""
	def GetAddress(self):
		assert self._address is not None, 'This error should not happen. Report this as a bug.'
		return rlocint.RelocatableInt(self._address, 4)



	# Needed for building dependency graph & allocating addresses
	"""
	Checks if the object is independent.
	 - Returns True if object is independent.
	 - Returns False if object is dependent.
	"""
	def IsIndependent(self):
		raise NotImplementedError('Pure virtual function')
	
	
	"""
	Return any object this object depends on. A depends on B if A needs
	information of B to be constructed. Cyclic dependency is allowd.
	
	For example, consider the following code:
	 trg1 = Addr(); trg2 = Addr()
	 trg1 << Trigger( nextptr = trg2 )
	 trg2 << Trigger( nextptr = trg1 )
	
	Then trg1 requires trg2, so trg1 depends on trg2.
	Vice versa, trg2 depends on trg1. So trg1 and trg2 depends on each other.
	"""
	def GetDependencyList(self):
		raise NotImplementedError('Pure virtual function')
	
	"""
	Returns raw size of object. Size of Condition and Action is each 20, 32.
	"""
	def GetDataSize(self):
		raise NotImplementedError('Pure virtual function')
	
	
	"""
	Function to write actual binary data to buffer. Length of total emitted
	bytes should match the value returned by GetDataSize. With emitbuffer,
	you can use the following methods.
	 - buf.EmitByte(b)  : Emit 1byte value. Value must be constant
	 - buf.EmitWord(w)  : Emit 2byte value. Value must be constant
	 - buf.EmitDword(d) : Emit 4byte value. Value may be constant or offsetted.
		If value is offsetted, then the dword should be aligned to 4byte.
	 - buf.EmitBytes(s) : Emit binary string to output. s should be convertible
		to bytes type.
	"""
	def WritePayloadChunk(self, emitbuffer):
		raise NotImplementedError('Pure virtual function')



"""
Addr object points to Addressable objects. Addr object can be freely mixed with
arithmetic operators(+, -, *, //). Addresses of Addressable object is assigned
runtime, so expression including Addr object to Addressable object also will be
evaluated runtime.
"""
class Addr(expr.Expr):
	
	
	"""
	Constructor.
	  A = Addr(object) : initalize with construct
	  A = Addr() : Initalize later with A << object
	"""
	def __init__(self, item = None):
		super(Addr, self).__init__()
		self.target = None

		if item:
			self << item # initalize with given object
			

	"""
	Initalizer. addr << Object. Addr() object can only be initalized once.
	"""
	def __lshift__(self, item):
		assert self.target is None, 'Double assignment to Addr()'
		assert isinstance(item, Addressable), 'Must assign Addressable object to Addr()'

		self.target = item
		
		return item
	
	

	def Evaluate(self): # Internally used.
		assert self.target is not None, 'Addr() not initalized'
		return self.target.GetAddress()
	
	
	
	def __getattr__(self, entry): # Attribute transfer
		return getattr(self.target, entry)

