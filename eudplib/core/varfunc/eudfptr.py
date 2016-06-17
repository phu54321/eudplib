from .eudfuncn import EUDFuncN
from ... import utils as ut
from .eudv import (
    _VProc,
    EUDVariable,
    SetVariables,
)
from .. import rawtrigger as rt
from ..allocator import Forward


#
# Common argument / returns storage
#

def getArgStorage(argn, _argstorage_dict={}):
    """ Get common arguments storage for argn """
    if argn not in _argstorage_dict:
        _argstorage_dict[argn] = [EUDVariable() for _ in range(argn)]
    return _argstorage_dict[argn]


def getRetStorage(retn, _retstorage_dict={}):
    """ Get common returns storage for retn """
    if retn not in _retstorage_dict:
        _retstorage_dict[retn] = [EUDVariable() for _ in range(retn)]
    return _retstorage_dict[retn]


def fillArguments(f):
    """ Copy values from common argument storage to f._args """
    if f._argn:
        argStorage = getArgStorage(f._argn)
        for farg, arg in zip(f._fargs, argStorage):
            _VProc(arg, arg.QueueAssignTo(farg))


def fillReturns(f):
    """ Copy values from f_rets to common returns storage """
    if f._retn:
        retStorage = getRetStorage(f._retn)
        for fret, ret in zip(f._frets, retStorage):
            _VProc(fret, fret.QueueAssignTo(ret))


def callFuncBody(fstart, fend):
    """ Call function's body triggers """
    fcallend = Forward()

    rt.RawTrigger(
        nextptr=fstart,
        actions=[rt.SetNextPtr(fend, fcallend)]
    )

    fcallend << rt.NextTrigger()


def createIndirectCaller(f, _caller_dict={}):
    """ Create function caller using common argument/return storage """

    # Cache function in _caller_dict. If uncached,
    if f not in _caller_dict:
        rt.PushTriggerScope()
        caller_start = rt.NextTrigger()
        fillArguments(f)
        callFuncBody(f._fstart, f._fend)
        fillReturns(f)
        caller_end = rt.RawTrigger()
        rt.PopTriggerScope()

        _caller_dict[f] = (caller_start, caller_end)

    return _caller_dict[f]


# ---------------------------------


class EUDFuncPtr:
    def __init__(self, argn, retn, f_init=None):
        """ Constructor with function prototype

        :param argn: Number of arguments function can accepy
        :param retn: Number of variables function will return.
        :param f_init: First function
        """

        self._argn = argn
        self._retn = retn

        if f_init:
            self.checkValidFunction(f_init)
            f_idcstart, f_idcend = createIndirectCaller(f_init)
            self._fstart = EUDVariable(f_idcstart)
            self._fendnext_epd = EUDVariable(ut.EPD(f_idcend + 4))

        else:
            self._fstart = EUDVariable()
            self._fendnext_epd = EUDVariable()

    def checkValidFunction(self, f):
        ut.ep_assert(isinstance(f, EUDFuncN))
        if not f._fstart:
            f._CreateFuncBody()

        f_argn = f._argn
        f_retn = f._retn
        ut.ep_assert(self._argn == f_argn, "Function with different prototype")
        ut.ep_assert(self._retn == f_retn, "Function with different prototype")

    def setFunc(self, f):
        """ Set function pointer's target to function

        :param f: Target function
        """
        self.checkValidFunction(f)

        # Build actions
        f_idcstart, f_idcend = createIndirectCaller(f)
        rt.RawTrigger(
            actions=[
                self._fstart.SetNumber(f_idcstart),
                self._fendnext_epd.SetNumber(ut.EPD(f_idcend + 4)),
            ]
        )

    def __lshift__(self, rhs):
        self.setFunc(rhs)

    def __call__(self, *args):
        """ Call target function with given arguments """
        if self._argn:
            argStorage = getArgStorage(self._argn)
            SetVariables(argStorage, args)

        # Call function
        t, a = Forward(), Forward()
        _VProc(self._fstart, [self._fstart.QueueAssignTo(ut.EPD(t + 4))])
        _VProc(self._fendnext_epd, [
            self._fendnext_epd.QueueAssignTo(ut.EPD(a + 16))
        ])

        fcallend = Forward()
        t << rt.RawTrigger(
            actions=[
                a << rt.SetNextPtr(0, fcallend)
            ]
        )
        fcallend << rt.NextTrigger()

        if self._retn:
            tmpRets = [EUDVariable() for _ in range(self._retn)]
            retStorage = getRetStorage(self._retn)
            SetVariables(tmpRets, retStorage)
            return ut.List2Assignable(tmpRets)
