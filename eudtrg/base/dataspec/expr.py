"""
Expression wrapper library. Expr class represents expression containing Addr.
Value of Expr class can be calculated only if all Addresses it's refering to
have been calculated. Used internally in eudtrg.
"""

from ..payload.rlocint import RelocatableInt

# Binary expression cache expire mechanism
_cachetoken = type('_ct', (), {})

def ExpireCacheToken():
	global _cachetoken
	_cachetoken = type('_ct', (), {})

def GetCacheToken():
	return _cachetoken


class Expr:
	def __init__(self):
		self._cachetoken = None

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

	
	def GetDependencyList(self):
		raise NotImplementedError("Subclass %s should implement this" % str(type(self)))

	def Evaluate(self):
		if self._cachetoken != _cachetoken:
			self._cache = self.EvalImpl()
			self._cachetoken = _cachetoken
		return self._cache
		
	def EvalImpl(self):
		raise NotImplementedError("Subclass %s should implement this" % str(type(self)))


# Expression class for binary operators
class BinopExpr(Expr):
	def __init__(self, exprA, exprB):
		super(BinopExpr, self).__init__()
		assert IsValidExpr(exprA), 'Lhs is not valid expression'
		assert IsValidExpr(exprB), 'Rhs is not Valid expression'
		
		self.exprA = exprA
		self.exprB = exprB

	def GetDependencyList(self):
		return [self.exprA, self.exprB]


class _AddExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_AddExpr, self).__init__(exprA, exprB)
		self._cache = None
		self._cachetoken = None
		
	def EvalImpl(self):
		return Evaluate(self.exprA) + Evaluate(self.exprB)


class _SubExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_SubExpr, self).__init__(exprA, exprB)
		self._cache = None
		self._cachetoken = None
		
	def EvalImpl(self):
		return Evaluate(self.exprA) - Evaluate(self.exprB)
	
	
class _MulExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_MulExpr, self).__init__(exprA, exprB)
		self._cache = None
		self._cachetoken = None
		
	def EvalImpl(self):
		return Evaluate(self.exprA) * Evaluate(self.exprB)
	

class _DivExpr(BinopExpr):
	def __init__(self, exprA, exprB):
		super(_DivExpr, self).__init__(exprA, exprB)
		
	def EvalImpl(self):
		return Evaluate(self.exprA) // Evaluate(self.exprB)
	


# Checks if expression is valid
def IsValidExpr(x):
	if type(x) is int or isinstance(x, RelocatableInt):
		return True
	else:
		return isinstance(x, Expr)






# Dependency walker
def GetDependencyList(item):
	try:
		return item.GetDependencyList()
	except AttributeError:
		return []



# Expression evaluator
def Evaluate(x):
	try:
		return x.Evaluate()
	except AttributeError:
		if type(x) is int:
			return RelocatableInt(x, 0)
	
		elif isinstance(x, RelocatableInt):
			return x

		else:
			raise RuntimeError('Function Evaluate called on unknown type')
