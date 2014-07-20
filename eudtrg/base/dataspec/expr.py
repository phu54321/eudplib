'''
Expression library wrapper. Used for calculating expression with addreses.
Internally used in eudtrg.
'''

from eudtrg import LICENSE #@UnusedImport
from ..payload.rlocint import RelocatableInt

# Expression caching
_cachetoken = 0

def ExpireCacheToken():
    global _cachetoken
    _cachetoken += 1

def GetCacheToken():
    return _cachetoken



class Expr:
    '''
    Expression class. Object of this type can be evaluated into
    :class:`RelocatableInt`. Derived classes should override:
    
    - :meth:`GetDependencyList`
    - :meth:`EvalImpl`
    '''
    
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
        '''
        :returns: Expressions this expression depends on
        :raises NotImplementedError: Derived class didn't override this method.
        '''
        raise NotImplementedError("Subclass %s should implement this" % str(type(self)))

    def Evaluate(self):
        '''
        This function caches :meth:`EvalImpl` and returns its value. Cache
        expires as :func:`SaveMap` ends, so cached values shouldn't affect
        each others.
        :returns: Cached value of :meth:`EvalImpl`.
        '''
        if self._cachetoken != _cachetoken: # Cache has expired, or no cache has been stored yet
            # Cache EvalImpl.
            self._cache = self.EvalImpl()
            self._cachetoken = _cachetoken

        return self._cache


    def EvalImpl(self):
        '''
        :returns: What the expression should be evaluated to.
        '''
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






# Helper functions
def IsValidExpr(x):
    if type(x) is int or isinstance(x, RelocatableInt):
        return True
    else:
        return isinstance(x, Expr)


def GetDependencyList(item):
    try:
        return item.GetDependencyList()
    except AttributeError:
        return []


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
