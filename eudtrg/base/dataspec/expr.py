"""
Expression wrapper library. Expr class represents expression containing Addr.
Value of Expr class can be calculated only if all Addresses it's refering to
have been calculated. Expr class is used in eudtrg internally. You shouldn't
use this class on normal situation.
"""

from ..payload.rlocint import RelocatableInt

class Expr:
	def __init__(self):
		pass

	# operations with default actions
	def __add__       (self, other): return _AddExpr(self, other)
	def __sub__       (self, other): return _SubExpr(self, other)
	def __mul__       (self, other): return _MulExpr(self, other)
	def __floordiv__  (self, other): return _DivExpr(self, other)

	def __radd__      (self, other): return _AddExpr(other, self)
	def __rsub__      (self, other): return _SubExpr(other, self)
	def __rmul__      (self, other): return _MulExpr(other, self)
	def __rfloordiv__ (self, other): return _DivExpr(other, self)

	def __iadd__      (self, other): self = self + other; return self
	def __isub__      (self, other): self = self - other; return self
	def __imul__      (self, other): self = self * other; return self
	def __ifloordiv__ (self, other): self = self // other; return self

	
	# user have to define below
	def GetDependencyList(self):
		raise NotImplementedError("Subclass should implement this")

	def Evaluate(self):
		raise NotImplementedError("Subclass should implement this")


class BinopExpr(Expr):
	def __init__(self, exprA, exprB):
		super(BinopExpr, self).__init__()
		self.exprA = exprA
		self.exprB = exprB


class _AddExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_AddExpr, self).__init__(exprA, exprB)
		self._cache = None
		
	def Evaluate(self):
		if self._cache is None:
			self._cache = Evaluate(self.exprA) + Evaluate(self.exprB);
		return self._cache


class _SubExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_SubExpr, self).__init__(exprA, exprB)
		self._cache = None
		
	def Evaluate(self):
		if self._cache is None:
			self._cache = Evaluate(self.exprA) - Evaluate(self.exprB);
		return self._cache
	
	
class _MulExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_MulExpr, self).__init__(exprA, exprB)
		self._cache = None
		
	def Evaluate(self):
		if self._cache is None:
			self._cache = Evaluate(self.exprA) * Evaluate(self.exprB);
		return self._cache
	

class _DivExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_DivExpr, self).__init__(exprA, exprB)
		self._cache = None
		
	def Evaluate(self):
		if self._cache is None:
			self._cache = Evaluate(self.exprA) // Evaluate(self.exprB);
		return self._cache
	

def IsValidExpr(x):
	if type(x) is int or isinstance(x, RelocatableInt):
		return True
	else:
		if hasattr(x, 'Evaluate'):
			return True
		else:
			return False
	
def Evaluate(x):
	if type(x) is int:
		return RelocatableInt(x, 0)

	elif isinstance(x, RelocatableInt):
		return x

	else:
		try:
			return x.Evaluate()
		except:
			raise RuntimeError('Function Evaluate called on unknown type')

if __name__ == '__main__':
	a = _MulExpr(RelocatableInt(1, 3), 2)
	b = Evaluate(a)
	print(a, b)

	c = RelocatableInt(4, 6)
	d = RelocatableInt(2, 0)
	e = c // d
	print(e)

	assert b == RelocatableInt(2, 6)
	assert e == RelocatableInt(2, 3)