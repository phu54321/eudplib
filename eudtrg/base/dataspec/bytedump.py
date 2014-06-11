from .addressable import Addressable

"""
eudtrg equivilant to 'db' command in eudasm. You can load any sequence of bytes
into Starcraft memory using Db class. Db class is one of the most basic class 
implementing Addressable class, so this may be your starting point for creating
your own Addressable class.
"""
class Db(Addressable):
	"""
	Initalize db class with binary contents. Constructor accepts anything
	convertible to bytes type.
	"""
	def __init__(self, content):
		super(Db, self).__init__()
		
		# convert & store
		content = bytes(content)
		self._content = content

	def GetDataSize(self):
		return len(self._content)
	
	def IsIndependent(self):
		return True

	def GetDependencyList(self):
		return []
	
	def WritePayloadChunk(self, buf):
		buf.EmitBytes(self._content)


