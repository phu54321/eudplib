"""
Payload packager. Used internally in eudtrg
"""


from . import depgraph
from ..dataspec import expr
from ..utils import binio

class Payload:
	def __init__(self, data, prttable = [], orttable = []):
		self.data = data
		self.prttable = prttable
		self.orttable = orttable


# Payload packager

def CreatePayload(root):
	needed_objects = depgraph.GetAllDependencies(root)

	objsizetable = []
	current_cursor = 0
	

	# Since writing binary data requires that all of the objects have predetermined addresses,
	# we first calculate addresses of all objects
	for obj in needed_objects:
		obj.SetAddress(current_cursor)
		
		size = obj.GetDataSize()
		objsizetable.append(size)
		size = size + (-size & 0x3) # align by 4 byte
		current_cursor += size

	# Write data
	buf = _PayloadBuffer()
	for i, obj in enumerate(needed_objects):
		buf.StartEmit()
		obj.WritePayloadChunk(buf)
		emitted_size = buf.EndEmit()
		assert emitted_size == objsizetable[i], \
			"Expected %d bytes, got %d bytes, Object type %s" % (objsizetable[i], emitted_size, str(type(obj)))

	# done.
	return buf.CreatePayload()



# Payload buffer class related
# buffer class creates payload


class _PayloadBuffer:
	def __init__(self):
		self._datas = []
		self._datalen = 0
		self._prttable = []
		self._orttable = []
		
	def StartEmit(self):
		self._datastart = self._datalen
		
	def EndEmit(self):
		emitted_size = self._datalen - self._datastart
		padding_byten = (-emitted_size & 0x3)
		self.EmitBytes(bytes(padding_byten))
		return emitted_size

	def EmitByte(self, number):
		number = expr.Evaluate(number)
		assert number.offset_applied == 0
		number.number &= 0xFF
		
		self._datas.append( binio.i2b1(number.number) )
		self._datalen += 1

	def EmitWord(self, number):
		number = expr.Evaluate(number)
		assert number.offset_applied == 0
		number.number &= 0xFFFF
		
		self._datas.append( binio.i2b2(number.number) )
		self._datalen += 2

	def EmitDword(self, number):
		number = expr.Evaluate(number)
		number.number &= 0xFFFFFFFF

		if number.offset_applied != 0:
			assert self._datalen % 4 == 0
			if number.offset_applied == 1:
				self._prttable.append(self._datalen)

			elif number.offset_applied == 4:
				self._orttable.append(self._datalen)

			else:
				raise RuntimeError('DWORD is not either PRT nor ORT!')

		self._datas.append( binio.i2b4(number.number) )
		self._datalen += 4

	def EmitBytes(self, b):
		b = bytes(b)
		self._datas.append( b )
		self._datalen += len(b)

	def CreatePayload(self):
		return Payload(b''.join(self._datas), self._prttable, self._orttable)
	
