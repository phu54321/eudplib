from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVariable, EUDLightVariable, VTProc
from .ctrlstru import DoActions


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

    directactiondict_fv = {
        SetTo    : EUDVariable.SetNumber,
        Add      : EUDVariable.AddNumber,
        Subtract : EUDVariable.SubtractNumber
    }

    directactiondict_lv = {
        SetTo    : EUDLightVariable.SetNumber,
        Add      : EUDLightVariable.AddNumber,
        Subtract : EUDLightVariable.SubtractNumber
    }

    # action buffer
    actionbuffer = []

    def FlushActionBuffer():
        nonlocal actionbuffer

        if actionbuffer:
            DoActions(actionbuffer)
        actionbuffer = []


    for dst, mdt, src in assignpairs:
        assert mdt != Set, "Change 'Set' in arguments for SeqCompute to 'SetTo'."
        assert not isinstance(src, EUDLightVariable), 'Light variable cannot be assigned to other variables directly'
        if isinstance(src, EUDVariable):
            FlushActionBuffer()
            VTProc(src.GetVTable(), [
                queueactiondict[mdt].__get__(src, type(src))(dst)
            ])

        else:
            if isinstance(dst, EUDVariable) or isinstance(dst, EUDLightVariable):
                dstaddr = EPD(dst.GetMemoryAddr())

            else:
                dstaddr = dst
            
            actionbuffer.append(SetDeaths(dstaddr, mdt, src, 0))
            if len(actionbuffer) == 64:
                FlushActionBuffer()

    FlushActionBuffer()
