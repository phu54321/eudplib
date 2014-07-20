from eudtrg import LICENSE #@UnusedImport

from .expr import Expr, Evaluate, GetCacheToken

class Forward(Expr):
    '''
    Forward declaration for expressions.

    Example) ::

        a = Trigger( nextptr = b ) # Error : b is not defined
        b = Trigger( nextptr = a ) 

    -> ::

        b = Forward() # Forward declaration
        a = Trigger( nextptr = b )
        b << Trigger( nextptr = a ) # put in value later.

    '''

    def __init__(self):
        super().__init__()
        self.target = None
        self._ct = None

    def __lshift__(self, item):
        '''
        Assign expression to self. The object will evaluate to assigned
        expressions afterwards.

        :raises AssertionError:
            - Forward has already been assigned.
            - Non-expression types are being assigned into.
        '''
        assert isinstance(item, Expr), 'Non-expr types cannot be assigned to Forward object.'
        assert self.target == None, 'Duplicate assignment'
        self.target = item
        return item

    def GetDependencyList(self):
        return [self.target]

    def EvalImpl(self):
        '''
        :raises AssertionError: Forward hasn't been assigned to any values by
            :meth:`__lshift__`.
        '''
        assert self.target is not None, 'Forward has not been properly initalized'
        return Evaluate(self.target)

