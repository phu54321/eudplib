from .memiof import (
    f_epdread_epd,

    f_dwread_epd,
    f_wread_epd,
    f_bread_epd,

    f_dwwrite_epd,
    f_wwrite_epd,
    f_bwrite_epd,
)
from ..utils import EPError, ep_assert

import functools


rwdict = {
    2: (f_wread_epd, f_wwrite_epd),
    1: (f_bread_epd, f_bwrite_epd),
}


@functools.lru_cache(None)
def EPDOffsetMap(ct):
    addrTable = {}
    for name, offset, size in ct:
        if size not in [4, 2, 1]:
            raise EPError('EPDOffsetMap member size should be one of 4, 2, 1')
        if offset % size != 0:
            raise EPError('EPDOffsetMap member should be aligned')
        addrTable[name] = offset, size

    class _:
        def __init__(self, epd):
            self._epd = epd

        def __getattr__(self, name):
            offset, size = addrTable[name]
            offsetEPD = offset // 4
            subp = offset % 4
            if size == 4:
                return f_dwread_epd(self._epd + offsetEPD)
            else:
                return rwdict[size][0](self._epd + offsetEPD, subp)

        def getepd(self, name):
            offset, size = addrTable[name]
            ep_assert(size == 4, 'only dword can be read as epd')
            return f_epdread_epd(self._epd + offset // 4)

        def __setattr__(self, name, value):
            if name == '_epd':
                super().__setattr__(name, value)
                return

            offset, size = addrTable[name]
            offsetEPD = offset // 4
            subp = offset % 4
            if size == 4:
                return f_dwwrite_epd(self._epd + offsetEPD, value)
            else:
                return rwdict[size][1](self._epd + offsetEPD, subp, value)

    return _
