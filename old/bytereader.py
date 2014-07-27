from eudtrglib import LICENSE #@UnusedImport

from eudtrglib.base import * #@UnusedWildImport

from .readdword import f_dwread
from .dwordbreak import f_dwbreak
from .arithmetic.muldiv import f_div

_epd, _suboffset, _ret = EUDCreateVariables(3)

class EUDByteReader:
    def __init__(self):
        self._dw = None
        self._w = [None]*2
        self._b = [None]*4
        self._suboffset = None
        self._offset = None

        self._dw, self._w[0], self._w[1], self._b[0], self._b[1],\
            self._b[2], self._b[3], self._suboffset, self_offset  = EUDCreateVariables(9)

    def seekepd(self, epdoffset):
        SeqCompute([
            (self._offset, SetTo, epdoffset),
            (self._suboffset, SetTo, 0)
        ])

        SetVariables(self._dw, f_dwread.call(epdoffset))
        SefVariables([self._w[i] for i in [0, 1]] + [self._b[i] for i in [0, 1, 2, 3]],
            f_dwbreak.call(self._dw)
        )

    def seekoffset(self, offset):
        if isinstance(offset, int):
            offset -= 0x58A364
            epd, suboffset = offset // 4, offset % 4

        else:
            # offset may refer to other variables. To prevent side effects,
            #  never subtract anything from offset variable.
            SetVariables([_epd, _suboffset], f_div.call(offset, 4))
            SeqCompute([ (_epd, Add, 0x100000000 - 0x58A364) ])
        

        self.seekepd(epd)


        if suboffset == 0:
            pass

        else:
            SeqCompute([
                (self._suboffset, SetTo, suboffset)
            ])


    def readbyte(self):
        case0, case1, case2, case3 = Forward(), Forward(), Forward(), Forward()

        case0 << NextTrigger()
        EUDJumpIfNot(self._suboffset.Exactly(0), case1)
        SeqCompute([
            (_ret, SetTo, self._b[0])
        ])
        EUDJump(swend)
        

    def readword(self):
        pass

    def readdword(self):
        pass