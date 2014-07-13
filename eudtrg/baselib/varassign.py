from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVariable, VTProc
from .ctrlstru import DoActions

"""
This function is rather complex one.


"""
def SetVariables(dstlist, srclist, mdtlist = None):
    dstlist = FlattenList(dstlist)
    srclist = FlattenList(srclist)
    if mdtlist is None:
        mdtlist = [SetTo] * len(dstlist)
    else:
        mdtlist = FlattenList(mdtlist)

    assert len(dstlist) == len(srclist) == len(mdtlist), 'Src/Dest/Mdt has different numbers of elements'

    SeqCompute(list(zip(dstlist, mdtlist, srclist)))


def SeqCompute(assignpairs):
    # Dictionary needed.
    queueactiondict = {
        SetTo    : EUDVariable.QueueAssignTo,
        Add      : EUDVariable.QueueAddTo,
        Subtract : EUDVariable.QueueSubtractTo
    }

    directactiondict = {
        SetTo    : EUDVariable.SetNumber,
        Add      : EUDVariable.AddNumber,
        Subtract : EUDVariable.SubtractNumber
    }

    for dst, mdt, src in assignpairs:
        assert mdt != Set, "Change 'Set' to 'SetTo'."
        if isinstance(src, EUDVariable):
            VTProc(src.GetVTable(), [
                queueactiondict[mdt].__get__(src, type(src))(dst)
            ])

        else:
            if isinstance(dst, EUDVariable):
                DoActions(directactiondict[mdt].__get__(dst, type(dst))(src))

            else:
                DoActions( SetDeaths(dst, mdt, src, 0) )

def DerefWrite(varname, value):
    if type(value) is int:
        act = Forward()
        SeqCompute([(EPD(act + 16), SetTo, varname)])
        DoActions(act << SetMemory(0, SetTo, value))

    else:
        act = Forward()
        SeqCompute([
            (EPD(act + 16), SetTo, varname),
            (EPD(act + 20), SetTo, value)
        ])
        DoActions(act << SetMemory(0, SetTo, 0))