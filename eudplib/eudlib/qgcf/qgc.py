from ... import core as c
from ... import ctrlstru as cs
from ..memiof import f_dwread_epd, f_memcpy

@c.EUDFunc
def QueueGameCommand(buf, size):
    prov_maxbuffer = f_dwread_epd(c.EPD(0x57F0D8))
    cmdqlen = f_dwread_epd(c.EPD(0x654AA0))
    if cs.EUDIfNot(cmdqlen + size + 1 >= prov_maxbuffer):
        f_memcpy(0x654880 + cmdqlen, buf, size)
        c.SetVariables(c.EPD(0x654AA0), cmdqlen + size)
    cs.EUDEndIf()


@c.EUDFunc
def QueueGameCommand_RightClick(x):
    RightClickCommand = c.Db(b'...\x14XXYY\0\0\xE4\0\x00')
    c.SetVariables(c.EPD(RightClickCommand + 4), x)
    QueueGameCommand(RightClickCommand + 3, 10)
