from eudtrg import LICENSE #@UnusedImport
from eudtrg.base import * #@UnusedWildImport

class EUDVTable(Trigger):
    def __init__(self, varn):
        assert varn <= 32, 'VTable with more than 32 variables are not supported'
        
        PushTriggerScope()
        variables = [Forward() for _ in range(varn)]

        super().__init__(
            actions =
                [variables[i] << Disabled(SetDeaths(0, SetTo, 0, 0)) for i in range(varn)] +
                [SetDeaths(EPD(variables[i] + 28), SetTo, 2, 0) for i in range(varn)]
        )

        self._var = [EUDVariable(var, self) for var in variables]
        PopTriggerScope()

    def GetVariables(self):
        return List2Assignable(self._var)


class EUDVariable:
    def __init__(self, vartrigger, originvt):
        self._varact = vartrigger
        self._originvt = originvt


    def GetMemoryAddr(self):
        return self._varact + 20

    def GetVTable(self):
        return self._originvt


    def AtLeast(self, number):
        return Memory(self._varact + 20, AtLeast, number)

    def AtMost(self, number):
        return Memory(self._varact + 20, AtMost, number)

    def Exactly(self, number):
        return Memory(self._varact + 20, Exactly, number)


    def SetNumber(self, number):
        return SetMemory(self._varact + 20, SetTo, number)

    def AddNumber(self, number):
        return SetMemory(self._varact + 20, Add, number)

    def SubtractNumber(self, number):
        return SetMemory(self._varact + 20, Subtract, number)



    def QueueAssignTo(self, dest):
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x072D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
        ]


    def QueueAddTo(self, dest):
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x082D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
        ]

    def QueueSubtractTo(self, dest):
        if isinstance(dest, EUDVariable) or isinstance(dest, EUDLightVariable):
            dest = EPD(dest.GetMemoryAddr())

        return [
            SetDeaths(EPD(self._varact + 16), SetTo, dest, 0),
            SetDeaths(EPD(self._varact + 24), SetTo, 0x092D0000, 0),
            SetDeaths(EPD(self._varact + 28), SetTo, 0, 0)
        ]


class EUDLightVariable:
    def __init__(self):
        self._memory = Db(b'\0\0\0\0')

    def GetMemoryAddr(self):
        return self._memory

    def AtLeast(self, number):
        return Memory(self._memory, AtLeast, number)

    def AtMost(self, number):
        return Memory(self._memory, AtMost, number)

    def Exactly(self, number):
        return Memory(self._memory, Exactly, number)


    def SetNumber(self, number):
        return SetMemory(self._memory, SetTo, number)

    def AddNumber(self, number):
        return SetMemory(self._memory, Add, number)

    def SubtractNumber(self, number):
        return SetMemory(self._memory, Subtract, number)



def VTProc(vt, actions):
    nexttrg = Forward()

    Trigger(
        nextptr = vt,
        actions = actions + [SetNextPtr(vt, nexttrg)]
    )

    nexttrg << NextTrigger()





