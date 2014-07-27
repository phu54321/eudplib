from eudtrglib import LICENSE #@UnusedImport

from .expr import Expr, Evaluate, GetCacheToken

class Forward(Expr):
    '''
    Forward declaration for expressions. Example::

        b = Forward() # Forward declaration
        a = Trigger( nextptr = b ) # b is defined here, so no error occurs.
        b << Trigger( nextptr = a ) # put in value later.

    Forward() class can be assigned a value only once.
    '''

    def __init__(self):
        super().__init__()
        self.target = None
        self._ct = None

    def __lshift__(self, item):
        return self.Assign(item)

    def Assign(self, item):
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
            :meth:`Assign`.
        '''
        assert self.target is not None, 'Forward has not been properly initalized'
        return Evaluate(self.target)

