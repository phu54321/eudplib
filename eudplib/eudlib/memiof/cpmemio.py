from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)


@c.EUDFunc
def _reader(cpo):
    ptr, epd = c.EUDVariable(), c.EUDVariable()
    ptr << 0
    epd << ut.EPD(0)
    for i in range(31, -1, -1):
        c.RawTrigger(
            conditions=[
                c.Deaths(c.CurrentPlayer, c.AtLeast, 2**i, 0)
            ],
            actions=[
                c.SetDeaths(c.CurrentPlayer, c.Subtract, 2**i, 0),
                ptr.AddNumber(2 ** i),
                epd.AddNumber(2 ** (i - 2)) if i >= 2 else []
            ]
        )
    cs.DoActions(c.SetDeaths(c.CurrentPlayer, c.SetTo, ptr, 0))

    return ptr, epd


def f_dwepdread_cp(cpo):
    if cpo != 0:
        cs.DoActions(c.SetMemory(0x6509B0, c.Add, cpo))
    ptr, epd = _reader(cpo)
    if cpo != 0:
        cs.DoActions(c.SetMemory(0x6509B0, c.Add, -cpo))
    return ptr, epd


def f_dwread_cp(cpo):
    return f_dwepdread_cp(cpo)[0]


def f_epdread_cp(cpo):
    return f_dwepdread_cp(cpo)[1]


def f_dwwrite_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.SetTo, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])


def f_dwadd_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.Add, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])


def f_dwsubtract_cp(cpo, value):
    cs.DoActions([
        c.SetMemory(0x6509B0, c.Add, cpo),
        c.SetDeaths(c.CurrentPlayer, c.subtract, value, 0),
        c.SetMemory(0x6509B0, c.Add, -cpo),
    ])
