 #!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


from eudtrg import base as b
from . import vtable as vt

from functools import wraps
import inspect


def EUDFunc(fdecl_func):
    '''
    Generates EUD Function. Usually used as decorators. EUD Function shouldn't
    be applied to recursive functions. ::

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
    assert argspec[1] is None, (
        'No variadic arguments (*args) allowed for eud function')
    assert argspec[2] is None, (
        'No variadic keyword arguments (*kwargs) allowed for eud function')

    argn = len(argspec[0])

    # Create function body
    b.PushTriggerScope()

    f_args = b.Assignable2List(vt.EUDCreateVariables(argn))
    fstart = b.NextTrigger()
    f_rets = b.Assignable2List(fdecl_func(*f_args))
    fend = b.Trigger()

    b.PopTriggerScope()

    # Assert that all return values are EUDVariable.
    for i, ret in enumerate(f_rets):
        assert isinstance(ret, vt.EUDVariable), (
            'Returned value #%d of original function is not EUDVariable' % i)

    # Function to return
    @wraps(fdecl_func)
    def retfunc(*args):
        # Assign arguments into argument space
        computeset = [(farg, b.SetTo, arg) for farg, arg in zip(f_args, args)]
        vt.SeqCompute(computeset)

        # Call body
        fcallend = b.Forward()

        b.Trigger(
            nextptr=fstart,
            actions=[b.SetNextPtr(fend, fcallend)]
        )

        fcallend << b.NextTrigger()

        retn = len(f_rets)
        tmp_rets = [vt.CreateTempVariable() for _ in range(retn)]
        vt.SetVariables(tmp_rets, f_rets)
        return b.List2Assignable(tmp_rets)

    # return
    return retfunc
