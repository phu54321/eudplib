from eudtrg import LICENSE #@UnusedImport

from eudtrg.base import * #@UnusedWildImport
from .vtable import EUDVariable, EUDLightVariable, VTProc
from .ctrlstru import DoActions


def SetVariables(dstlist, srclist, mdtlist = None):
    '''
    Assigns values to variables/memory. This is just a syntax sugar for
    :func:`SeqCompute`. Useful for retrieving function return values after
    EUD Function call. ::

        SetVariables([unitx, unity], f_dwbreak(position)[0:2])

    :param dstlist: Nested list of EUDVariable/EUDLightVariable/Expr.

        - :class:`EUDVariable` : Value is stored at variable.
        - :class:`EUDLightVariable` : Value is stored at variable.
        - :class:`Expr` : Value is stored at memory. Expr is interpreted
            as EPD Player.

    :param srclist: Nested list of EUDVariable/Expr.

        - :class:`EUDVariable` : Value is pulled off from variable
        - :class:`Expr` : Value is evaluated.

    :param mdtlist: Nested list of SetTo/Add/Subtract. Default:
        [SetTo * (Number of varaibles)]

    :raises AssertionError: Raises when:

        - len(dstlist), len(srclist), len(mdtlist) is different
        - Type error of arguments.

    .. warning::
        Subtraction won't underflow. Subtracting values with bigger one will
        yield 0.
    '''


    dstlist = FlattenList(dstlist)
    srclist = FlattenList(srclist)
    if mdtlist is None:
        mdtlist = [SetTo] * len(dstlist)
    else:
        mdtlist = FlattenList(mdtlist)

    assert len(dstlist) == len(srclist) == len(mdtlist), 'Src/Dest/Mdt has different numbers of elements'

    SeqCompute(list(zip(dstlist, mdtlist, srclist)))


def SeqCompute(assignpairs):
    '''
    Do multiple assignment/addition/subtraction sequentially.

    :param assignpairs: List of (dst, src, modtype)

        - dst : Where to compute

            - :class:`EUDVariable` : Value is stored at variable
            - :class:`EUDLightVariable` : Value is stored at variable
            - :class:`Expr` : Value is stored at memory. Expr is interpreted as
                EPD player value.

        - src : What value to use with computation

            - :class:`EUDVariable` : Value is pulled of from variable.
            - :class:`Expr` : Value is evaluated

        - modtype : What type of computation to do.

            - SetTo : Assignment. dst = src
            - Add : Addition. dst += src
            - Subtract : Subtraction. dst -= src


    :raises AssertionError:
        Raises when:
        
        - EUDLightVariable is given as src : Light Variable cannot be direcly
          assigned. They must be read with f_dwread, or be copied to.

    .. warning::
        Subtraction won't underflow. Subtracting values with bigger one will
        yield 0.
    '''

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
