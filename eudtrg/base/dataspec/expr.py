from eudtrg import LICENSE  # @UnusedImport

from .rlocint import RelocatableInt

# Expression caching
_cachetoken = 0


def ExpireCacheToken():
    ''' Internal function. Don't use '''
    global _cachetoken
    _cachetoken += 1


def GetCacheToken():
    return _cachetoken


class Expr:

    '''
    Expression class. Handle expressions with unknown variables. Example::

        a = Forward() # some unknown variable
        b = Trigger() # some unknown variable
            # b's value is determined with a call of SaveMap()

        c = a + 5 - b # a + 5 - b is an expression with unknown variable.

        # since a, b is undetermined yet, c needs to store expression tree of
        # 'a + 5 - b', such as in form of (- (+ a 5) b). Expr class can be used
        # to store such expressions.

    Expr class supports basic arithmetic operators: addition, subtraction,
    muliplication, and division. Derived class should implement following two
    methods.

    - GetDependencyList : List of other expression required for evaluation of
      the expression. Circular dependency are supported.

    - EvalImpl : Calculate value of the expression. Evaluate() caches result of
      EvalImpl, so you should override EvalImpl method instead of Evaluate.

    '''

    def __init__(self):
        self._cachetoken = None

    # operations with default actions
    def __add__(self, other):
        return _AddExpr(self, other)

    def __sub__(self, other):
        return _SubExpr(self, other)

    def __mul__(self, other):
        return _MulExpr(self, other)

    def __floordiv__(self, other):
        return _DivExpr(self, other)

    def __radd__(self, other):
        return _AddExpr(other, self)

    def __rsub__(self, other):
        return _SubExpr(other, self)

    def __rmul__(self, other):
        return _MulExpr(other, self)

    def __rfloordiv__(self, other):
        return _DivExpr(other, self)

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __imul__(self, other):
        self = self * other
        return self

    def __ifloordiv__(self, other):
        self = self // other
        return self

    def GetDependencyList(self):
        '''
        :returns: List of Expr instances self depends on.
        :raises NotImplementedError: Derived class have not overridden this
            method.

        '''
        raise NotImplementedError(
            "Subclass %s should implement this" % str(type(self)))

    def Evaluate(self):
        '''
        :returns: Cached value of EvalImpl.

        Remarks
        -------
        Evaluate function caches and returns the value of EvalImpl. cache token
        expires or no values were cached before, Evaluate recaches its value by
        calling EvalImpl. Cache expires with a call of SaveMap.

        '''

        # Cache has expired, or no cache has been stored yet
        if self._cachetoken != _cachetoken:
            # Cache EvalImpl.
            self._cache = self.EvalImpl()
            self._cachetoken = _cachetoken

        return self._cache

    def EvalImpl(self):
        '''
        :returns: What the object should be evaluated to. For example,
        EUDObject returns the data's address in Starcraft Memory by default.
        Type of returned object should be one of int,
        :class:`eudtrg.RelocatableInt`, or one having `Evaluate` method.

        '''
        raise NotImplementedError(
            "Subclass %s should implement this" % str(type(self)))


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
        for i in range(10000):  # 10000 is some very large number.
            return x.Evaluate()  # Exits when evaluate fails

        raise RuntimeError(
            'Infinite evaluation loop detected with object %s' % str(x))

    except AttributeError:
        if type(x) is int:
            return RelocatableInt(x, 0)

        elif isinstance(x, RelocatableInt):
            return x

        else:
            raise RuntimeError('Function Evaluate called on unknown type')
