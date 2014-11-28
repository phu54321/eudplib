from .. import core as c
from ..core.utils.blockstru import (
    BlockStruManager,
    SetCurrentBlockStruManager
)
from .eudv import EUDVariable, EUDCreateVariables
from .eudsqc import SeqCompute

from functools import wraps
import inspect


def EUDFunc(fdecl_func):
    # Get argument number of fdecl_func
    argspec = inspect.getargspec(fdecl_func)
    assert argspec[1] is None, (
        'No variadic arguments (*args) allowed for EUDFunc.')
    assert argspec[2] is None, (
        'No variadic keyword arguments (*kwargs) allowed for EUDFunc.')

    argn = len(argspec[0])

    # Create function body
    f_bsm = BlockStruManager()
    prev_bsm = SetCurrentBlockStruManager(f_bsm)

    if 1:
        c.PushTriggerScope()

        f_args = c.Assignable2List(EUDCreateVariables(argn))
        fstart = c.NextTrigger()
        f_rets = c.Assignable2List(fdecl_func(*f_args))
        fend = c.Trigger()

        c.PopTriggerScope()

    SetCurrentBlockStruManager(prev_bsm)
    assert f_bsm.empty(), 'Block start/end mismatch inside function'

    # Assert that all return values are EUDVariable.
    for i, ret in enumerate(f_rets):
        assert isinstance(ret, EUDVariable), (
            '#%d of returned value is not instance of EUDVariable' % i)

    # Function to return
    @wraps(fdecl_func)
    def retfunc(*args):
        assert len(args) is argn, 'Argument number mismatch'

        # Assign arguments into argument space
        computeset = [(farg, c.SetTo, arg) for farg, arg in zip(f_args, args)]
        SeqCompute(computeset)

        # Call body
        fcallend = c.Forward()

        c.Trigger(
            nextptr=fstart,
            actions=[c.SetNextPtr(fend, fcallend)]
        )

        fcallend << c.NextTrigger()

        retn = len(f_rets)
        tmp_rets = [EUDVariable() for _ in range(retn)]
        SeqCompute([(tr, c.SetTo, r) for tr, r in zip(tmp_rets, f_rets)])
        return c.List2Assignable(tmp_rets)

    # return
    return retfunc


def SetVariables(srclist, dstlist, mdtlist=None):
    srclist = c.FlattenList(srclist)
    dstlist = c.FlattenList(dstlist)
    assert len(srclist) == len(dstlist), 'Input/output size mismatch'

    if mdtlist is None:
        mdtlist = [c.SetTo] * len(srclist)

    sqa = [(src, dst, mdt) for src, dst, mdt in zip(srclist, dstlist, mdtlist)]
    SeqCompute(sqa)
