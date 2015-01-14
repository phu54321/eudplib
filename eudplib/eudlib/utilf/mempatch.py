from ... import core as c
from ... import ctrlstru as cs
from ..eudarray import EUDArray
from ..memiof import f_dwread_epd, f_dwwrite_epd, f_repmovsd_epd

_patchstack = EUDArray(3 * 8192)
_ps_top = c.EUDVariable()

def f_mempatch_epd(wstartepd, rstartepd, dwn):
    global _patchstack, _ps_top

    db = c.Db(4 * dwn)
    f_repmovsd_epd(c.EPD(db), wstartepd, dwn)
    f_repmovsd_epd(wstartepd, rstartepd, dwn)

    _patchstack[_ps_top] = wstartepd
    _ps_top += 1
    _patchstack[_ps_top] = c.EPD(db)
    _ps_top += 1
    _patchstack[_ps_top] = dwn
    _ps_top += 1


@c.EUDFunc
def f_dwpatch_epd(addrepd, value):
    global _patchstack, _ps_top

    db = c.Db(4)
    f_dwwrite_epd(c.EPD(db), f_dwread_epd(addrepd))
    f_dwwrite_epd(addrepd, value)

    _patchstack[_ps_top] = addrepd
    _ps_top += 1
    _patchstack[_ps_top] = c.EPD(db)
    _ps_top += 1
    _patchstack[_ps_top] = 1
    _ps_top += 1


@c.EUDFunc
def f_unpatchall():
    global _ps_top
    if cs.EUDWhile(_ps_top >= 1):
        wstartepd = _patchstack[_ps_top]
        _ps_top -= 1
        dbepd = _patchstack[_ps_top]
        _ps_top -= 1
        dwn = _patchstack[_ps_top]
        _ps_top -= 1
        f_repmovsd_epd(wstartepd, dbepd, dwn)
    cs.EUDEndWhile()
