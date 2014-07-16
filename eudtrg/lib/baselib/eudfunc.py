from .. import LICENSE

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVTable, EUDVariable
from .varassign import SetVariables, SeqCompute

import inspect



def EUDFunc(fdecl_func):
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
        assert isinstance(ret, EUDVariable), 'Return value #%d is not EUDVariable' % i


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
