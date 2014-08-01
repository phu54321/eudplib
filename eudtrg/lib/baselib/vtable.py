from eudtrg import LICENSE  # @UnusedImport
from eudtrg.base import *  # @UnusedWildImport


class EUDVTable(Trigger):

    '''
    Full Variable table. EUDVTable stores :class:`EUDVariable` objects.
    EUDVTable serves as a key component of trigger programming.

        vt = EUDVTable(3)
        a, b, c = vt.GetVariables()
        # use a, b, c for further calculations.

    EUDVTable is as itself a :class:`Trigger`, so it can be executed. When
    EUDVTable is executed, queued calculations are processed. You can queue
    calculations with :meth:`EUDVariable.QueueAssignTo` and its family.

    '''

    def __init__(self, varn):
        '''
        EUDVTable constructor.
        :param varn: Number of arguments EUDVTable should have. 0 < varn <= 32
        :raises AssertionError: varn <= 0 or varn > 32.
        '''
        assert varn > 0, 'EUDVTable should have at least 1 variables.'
        assert varn <= 32, (
            'EUDVTable with more than 32 variables are not supported')

        PushTriggerScope()
        variables = [Forward() for _ in range(varn)]

        super().__init__(
            actions=
                [variables[i] << Disabled(SetDeaths(0, SetTo, 0, 0)) for i in range(varn)] +
                [SetDeaths(EPD(variables[i] + 28), SetTo, 2, 0)
                 for i in range(varn)]
        )

        self._var = [EUDVariable(var, self) for var in variables]
        PopTriggerScope()

    def GetVariables(self):
        '''
        :returns: List of variables inside EUDVTable. If there is only one
            variable, return it.
        '''
        return List2Assignable(self._var)


class EUDVariable:

    '''
    Full variable.
    '''

    def __init__(self, vartrigger, originvt):
        self._varact = vartrigger
        self._originvt = originvt

    def GetMemoryAddr(self):
        '''
        :returns: Memory address where values are stored.
        '''
        return self._varact + 20

    def GetVTable(self):
        '''
        :returns: Parent EUDVTable.
        '''
        return self._originvt

    def AtLeast(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at least
            given number.
        '''
        return Memory(self.GetMemoryAddr(), AtLeast, number)

    def AtMost(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at most
            given number.
        '''
        return Memory(self.GetMemoryAddr(), AtMost, number)

    def Exactly(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at exactly
            given number.
        '''
        return Memory(self.GetMemoryAddr(), Exactly, number)

    def SetNumber(self, number):
        '''
        :param number: Number to assign.
        :returns: :class:`Action` for assigning given number to variable.
        '''
        return SetMemory(self.GetMemoryAddr(), SetTo, number)

    def AddNumber(self, number):
        '''
        :param number: Number to add.
        :returns: :class:`Action` for adding given number to variable.
        '''
        return SetMemory(self.GetMemoryAddr(), Add, number)

    def SubtractNumber(self, number):
        '''
        :param number: Number to subtract.
        :returns: :class:`Action` for subtracting given number to variable.

        .. warning::
            Subtraction won't underflow. Subtracting values with bigger one
            will yield 0.
        '''
        return SetMemory(self.GetMemoryAddr(), Subtract, number)

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
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x072D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
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
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x082D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
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
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x092D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
        ]


class EUDLightVariable:

    '''
    Light variable. EUDLightVariable occupies only 4 bytes.
    '''

    def __init__(self):
        self._memory = Db(b'\0\0\0\0')

    def GetMemoryAddr(self):
        '''
        :returns: Memory address where values are stored.
        '''
        return self._memory

    def AtLeast(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at least
            given number.
        '''
        return Memory(self.GetMemoryAddr(), AtLeast, number)

    def AtMost(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at most
            given number.
        '''
        return Memory(self.GetMemoryAddr(), AtMost, number)

    def Exactly(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at exactly
            given number.
        '''
        return Memory(self.GetMemoryAddr(), Exactly, number)

    def SetNumber(self, number):
        '''
        :param number: Number to assign.
        :returns: :class:`Action` for assigning given number to variable.
        '''
        return SetMemory(self.GetMemoryAddr(), SetTo, number)

    def AddNumber(self, number):
        '''
        :param number: Number to add.
        :returns: :class:`Action` for adding given number to variable.
        '''
        return SetMemory(self.GetMemoryAddr(), Add, number)

    def SubtractNumber(self, number):
        '''
        :param number: Number to subtract.
        :returns: :class:`Action` for subtracting given number to variable.

        .. warning::
            Subtraction won't underflow. Subtracting values with bigger one
            will yield 0.
        '''
        return SetMemory(self.GetMemoryAddr(), Subtract, number)


def VTProc(vt, actions):
    '''
    Shortcut for :class:`EUDVTable` calculation. VTProc automatically inserts
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

        VTProc(v, [
            a.QueueSetTo(EPD(0x58A364))
        ])

    :param actions: Actions to execute
    '''

    nexttrg = Forward()

    Trigger(
        nextptr=vt,
        actions=actions + [SetNextPtr(vt, nexttrg)]
    )

    nexttrg << NextTrigger()
