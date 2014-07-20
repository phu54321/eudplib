from .. import LICENSE

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVTable, EUDVariable
from .varassign import SetVariables, SeqCompute

import inspect



def EUDFunc(fdecl_func):
    '''
    Generates EUD Function. Usually used as decorators. EUD Function cannot
    be recursive. ::

        @EUDFunc
        def f_add(a, b):
            ret = EUDCreateVariables(1)
            SeqCompute([
                (ret, SetTo, 0),
                (ret, Add, a),
                (ret, Add, b)
            ])

            return ret

    EUD function gets several EUDVariables as arguments, but user can use both
    :class:`EUDVariable` and :class:`Expr` for calling function. ::

        a,b = EUDCreateVariable(2)
        c = Trigger()
        d = c_int

        f_mul(a,b) # ok
        f_mul(10, b) # ok. 10 can be implicitly converted to Expr.
        f_mul(10, 20) # ok.
        f_mul(a, c) # ok. Trigger is type of expression. In this case, address
            # of trigger will be passed to f_mul.
        f_mul(a, d) # Error. c_int is neither EUDVariable nor Expr.

    EUD Function may return several return values. Return values are 
    overwritten after every function call, so users should store it with
    :func:`SetVariables` or :func:`SeqCompute` if they need it. ::

        SeqCompute(local_variable, f_function()) # store return value

        f_function() # local_variable still presists its value.

    If returned values won't be used after another function call, users don't 
    have to store it. ::

        var = f_function()

        f_function() # var is overwritten now.


    :param fdecl_func: Function to be converted into EUD function.
        fdecl_func recieves several EUDVariable and should return single/list
        of EUDVariable. 
    '''
    # Get argument number of fdecl_func
    argspec = inspect.getargspec(fdecl_func)
    assert argspec[1] is None, 'No variadic arguments (*args) allowed for eud function'
    assert argspec[2] is None, 'No variadic keyword arguments (*kwargs) allowed for eud function'
    argn = len(argspec[0])


    # Create function body

    PushTriggerScope()
    
    f_args = Assignable2List(EUDVTable(argn).GetVariables())
    fstart = NextTrigger()
    f_rets = Assignable2List(fdecl_func(*f_args))
    fend = Trigger()

    PopTriggerScope()

    # Assert that all return values are EUDVariable.
    for i, ret in enumerate(f_rets):
        assert isinstance(ret, EUDVariable), 'Returned value #%d of original function is not EUDVariable' % i


    # Function to return
    def retfunc(*args):
        # Assign arguments into argument space
        computeset = [(farg, SetTo, arg) for farg, arg in zip(f_args, args)]
        SeqCompute(computeset)

        # Call body
        fcallend = Forward()

        Trigger(
            nextptr = fstart,
            actions = [ SetNextPtr(fend, fcallend) ]
        )

        fcallend << NextTrigger()

        return List2Assignable(f_rets)

    # return
    return retfunc
