from ...ctrlstru import (
    EUDInfLoop,
    EUDEndInfLoop,
    EUDIf,
    EUDElse,
    EUDEndIf,
    EUDBreakIf,
    EUDBreak,
    EUDSwitch,
    EUDSwitchCase,
    EUDEndSwitch,
)
from .rwcommon import br1, bw1
from .cp949_table import cp949_table

"""
KSC5601 -> Unicode 2.0 mapping table, compressed for the 94*94 codeset.
Generated based on  KSC5601.txt at
  ftp://ftp.unicode.org/Public/MAPPINGS/EASTASIA/KSC

Unlike kuten-table, needed offset is 33 (0x21) instead of
32 for 7-bit portion of each byte.  i.e., a Unicode
codepoint for KSC's codepoint (n, m) would be found at
index (n-33)*94+m-33.
"""


def f_cp949_to_utf8_cpy(dst, src):
    br1.seekoffset(src)
    bw1.seekoffset(dst)

    if EUDInfLoop()():
        b1 = br1.readbyte()
        EUDBreakIf(b1 == 0)
        if EUDIf()(b1 < 128):
            bw1.writebyte(b1)
        if EUDElse()():
            b2 = br1.readbyte()
            EUDBreakIf(b2 == 0)

            # Apply conversion table
            cvtb = {}
            for (ch1, ch2), tab in cp949_table:
                try:
                    cvtb[ch1].append((ch2, tab))
                except KeyError:
                    cvtb[ch1] = [(ch2, tab)]

            EUDSwitch(b1)
            for ch1, tb in cvtb.items():
                EUDSwitchCase()(ch1)
                EUDSwitch(b2)
                for ch2, code in tb:
                    EUDSwitchCase()(ch2)
                    if 0x0080 <= code <= 0x07FF:
                        # Encode as 2-byte
                        bw1.writebyte(0b11000000 | (code >> 6) & 0b11111)
                        bw1.writebyte(0b10000000 | (code >> 0) & 0b111111)
                    elif 0x0800 <= code <= 0xFFFF:
                        # Encode as 3-byte
                        bw1.writebyte(0b11100000 | (code >> 12) & 0b1111)
                        bw1.writebyte(0b10000000 | (code >> 6) & 0b111111)
                        bw1.writebyte(0b10000000 | (code >> 0) & 0b111111)
                    EUDBreak()
                EUDEndSwitch()
                EUDBreak()
            EUDEndSwitch()
        EUDEndIf()
    EUDEndInfLoop()
    bw1.writebyte(0)
    bw1.flushdword()
