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

from . import ctrlstru as cs
from .lightvar import EUDLightVariable


vdp = 2408


class _EUDVarBuffer(b.EUDObject):

    """Variable buffer

    40 bytes per variable.
    """

    def __init__(self):
        super().__init__()
        self._varn = 0

    def CreateVarTrigger(self):
        ret = self + (vdp * self._varn)
        self._varn += 1
        return ret

    def GetDependencyList(self):
        return []

    def GetDataSize(self):
        return 2408 + vdp * (self._varn - 1)

    def WritePayload(self, emitbuffer):
        output = bytearray(2408 + vdp * (self._varn - 1))

        for i in range(self._varn):
            output[vdp*i+2376:vdp*i+2380] = b'\x04\0\0\0'  # 'preserve trigger'

        emitbuffer.EmitBytes(output)

_evb = _EUDVarBuffer()


class EUDVariable:

    '''
    Full variable.
    '''

    def __init__(self):
        self._vartrigger = _evb.CreateVarTrigger()
        self._varact = self._vartrigger + (8 + 320)

    def GetVTable(self):
        return self._vartrigger

    def GetMemoryAddr(self):
        '''
        :returns: Memory address where values are stored.
        '''
        return self._varact + 20

    def AtLeast(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at least
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.AtLeast, number)

    def AtMost(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at most
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.AtMost, number)

    def Exactly(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at exactly
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.Exactly, number)

    def SetNumber(self, number):
        '''
        :param number: Number to assign.
        :returns: :class:`Action` for assigning given number to variable.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.SetTo, number)

    def AddNumber(self, number):
        '''
        :param number: Number to add.
        :returns: :class:`Action` for adding given number to variable.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.Add, number)

    def SubtractNumber(self, number):
        '''
        :param number: Number to subtract.
        :returns: :class:`Action` for subtracting given number to variable.

        .. warning::
            Subtraction won't underflow. Subtracting values with bigger one
            will yield 0.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.Subtract, number)

    def QueueAssignTo(self, dest):
        '''
        :param dest: Where to assign variable value to.

            - EUDVariable : Value of variable is assigned to dest variable.
            - :class:`EUDLightVariable` : Value of variable is assigned to dest
                variable.
            - :class:`Expr` : Value of variable is assigned to memory. dest is
                interpreted as EPD Player.

        :returns: List of :class:`Action` needed for queueing assignment.
        '''
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = b.EPD(dest.GetMemoryAddr())

        return [
            b.SetDeaths(b.EPD(self._varact + 16), b.SetTo, dest, 0),
            b.SetDeaths(b.EPD(self._varact + 24), b.SetTo, 0x072D0000, 0),
        ]

    def QueueAddTo(self, dest):
        '''
        :param dest: Where to add variable value to.

            - EUDVariable : Value of variable is added to dest variable.
            - :class:`EUDLightVariable` : Value of variable is added to dest
              variable.
            - :class:`Expr` : Value of variable is added to memory. dest is
              interpreted as EPD Player.

        :returns: List of :class:`Action` needed for queueing addition.
        '''
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = b.EPD(dest.GetMemoryAddr())

        return [
            b.SetDeaths(b.EPD(self._varact + 16), b.SetTo, dest, 0),
            b.SetDeaths(b.EPD(self._varact + 24), b.SetTo, 0x082D0000, 0),
        ]

    def QueueSubtractTo(self, dest):
        '''
        :param dest: Where to subtract variable value to.

            - EUDVariable : Value of variable is subtracted to dest variable.
            - :class:`EUDLightVariable` : Value of variable is subtracted to
              dest variable.
            - :class:`Expr` : Value of variable is subtracted to memory. dest
              is interpreted as EPD Player.

        :returns: List of :class:`Action` needed for queueing addition.

        .. warning::
            Subtraction won't underflow. Subtracting values with bigger one
            will yield 0.
        '''
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = b.EPD(dest.GetMemoryAddr())

        return [
            b.SetDeaths(b.EPD(self._varact + 16), b.SetTo, dest, 0),
            b.SetDeaths(b.EPD(self._varact + 24), b.SetTo, 0x092D0000, 0),
        ]

    '''
    Simple wrapper for arithmetic operators.
    '''

    def __add__(self, other):
        t = CreateTempVariable()
        SeqCompute([
            (t, b.SetTo, self),
            (t, b.Add, other)
        ])
        return t

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        t = CreateTempVariable()
        SeqCompute([
            (t, b.SetTo, self),
            (t, b.Subtract, other)
        ])
        return t

    def __rsub__(self, other):
        t = CreateTempVariable()
        SeqCompute((
            (t, b.SetTo, other),
            (t, b.Subtract, self)
        ))
        return t

    def __iadd__(self, other):
        SeqCompute((
            (self, b.Add, other),
        ))
        return self

    def __isub__(self, other):
        SeqCompute((
            (self, b.Subtract, other),
        ))
        return self

    def __lshift__(self, other):
        SeqCompute((
            (self, b.SetTo, other),
        ))
        return self

    ''' Comparison operators '''

    def __eq__(self, other):
        if isinstance(other, EUDVariable):
            return [(self - other).Exactly(0), (other - self).Exactly(0)]

        else:
            return self.Exactly(other)

    def __le__(self, other):
        if isinstance(other, EUDVariable):
            return (self - other).Exactly(0)
        else:
            return self.AtMost(other)

    def __ge__(self, other):
        if isinstance(other, EUDVariable):
            return (other - self).Exactly(0)
        else:
            return self.AtLeast(other)


def _VTProc(vt, actions):
    '''
    Shortcut for :class:`_EUDVTable` calculation. _VTProc automatically inserts
    nextptr manipulation triggers, so you wouldn't have to write them every
    time.

    Before::

        t = Forward()
        Trigger(
            nextptr = vt,
            actions = [
                a.QueueSetTo(EPD(0x58A364)),
                SetNextPtr(vt, t)
            ]
        )

        t = NextTrigger()

    After::

        _VTProc(v, [
            a.QueueSetTo(EPD(0x58A364))
        ])

    :param actions: Actions to execute
    '''

    nexttrg = b.Forward()

    b.Trigger(
        nextptr=vt,
        actions=actions + [b.SetNextPtr(vt, nexttrg)]
    )

    nexttrg << b.NextTrigger()


def CreateTempVariable():
    """ Create temporary variables for various uses. """
    return EUDCreateVariables(1)


# From vbuffer.py
_lastvtvars = None
_lastvt_filled = 32


def EUDCreateVariables(varn):
    '''
    Create (varn) :class:`EUDVariables`. Returned variables are not guarranted
    to be in the same variable table.

    :param varn: Number of EUDVariables to create.
    :returns: List of variables. If varn is 1, then a variable is returned.
    '''

    return b.List2Assignable([EUDVariable() for _ in range(varn)])


# from varassign.py


def SetVariables(dstlist, srclist, mdtlist=None):
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

    dstlist = b.FlattenList(dstlist)
    srclist = b.FlattenList(srclist)
    if mdtlist is None:
        mdtlist = [b.SetTo] * len(dstlist)
    else:
        mdtlist = b.FlattenList(mdtlist)

    assert len(dstlist) == len(srclist) == len(mdtlist), (
        'Src/Dest/Mdt has different numbers of elements')

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
          assigned. They must be read with f_dwread_epd, or be copied to.

    .. warning::
        Subtraction won't underflow. Subtracting values with bigger one will
        yield 0.
    '''

    # Dictionary needed.
    queueactiondict = {
        b.SetTo: EUDVariable.QueueAssignTo,
        b.Add: EUDVariable.QueueAddTo,
        b.Subtract: EUDVariable.QueueSubtractTo
    }

    # action buffer
    actionbuffer = []

    def FlushActionBuffer():
        nonlocal actionbuffer

        if actionbuffer:
            cs.DoActions(actionbuffer)
        actionbuffer = []

    for dst, mdt, src in assignpairs:
        assert mdt != b.Set, (
            "Change 'Set' in arguments for SeqCompute to 'SetTo'.")
        assert not isinstance(src, EUDLightVariable), (
            'Light variable cannot be assigned to other variables directly')

        if isinstance(src, EUDVariable):
            FlushActionBuffer()
            _VTProc(src.GetVTable(), [
                queueactiondict[mdt].__get__(src, type(src))(dst)
            ])

        else:
            if isinstance(dst, EUDVariable) or \
                    isinstance(dst, EUDLightVariable):
                dstaddr = b.EPD(dst.GetMemoryAddr())

            else:
                dstaddr = dst

            actionbuffer.append(b.SetDeaths(dstaddr, mdt, src, 0))
            if len(actionbuffer) == 64:
                FlushActionBuffer()

    FlushActionBuffer()
