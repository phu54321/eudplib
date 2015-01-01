from ... import stdobj as so
from ... import core as c
from ... import ctrlstru as cs
from ..memiof import f_dwread_epd, f_dwwrite_epd

patcharr = so.EUDArray(16384)  # 64kb of buffer
patchsize = c.EUDVariable()

@c.EUDFunc
def f_dwpatch(addrepd, value):
    global patchsize
    origvalue = f_dwread_epd(addrepd)
    f_dwwrite_epd(addrepd, value)
    patcharr.set(patchsize, addrepd)
    patchsize += 1
    patcharr.set(patchsize, origvalue)
    patchsize += 1

@c.EUDFunc
def f_unpatchall():
    global patchsize
    if cs.EUDWhile(patchsize >= 2):
        patchsize -= 1
        origvalue = patcharr.get(patchsize)
        patchsize -= 1
        addrepd = patcharr.get(patchsize)
        f_dwwrite_epd(addrepd, origvalue)
    cs.EUDEndWhile()
