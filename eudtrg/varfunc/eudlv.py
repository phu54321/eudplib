from .. import core as c
from .vbase import VariableBase


class EUDLightVariable(VariableBase):

    def __init__(self, initvalue=0):
        self._memaddr = c.Db(c.i2b4(initvalue))

    def GetVariableMemoryAddr(self):
        return self._memaddr
