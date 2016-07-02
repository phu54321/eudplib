from ... import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

from .modcurpl import (
    f_setcurpl,
    f_getcurpl,
)


@c.EUDFunc
def f_dwepdread_epd(targetplayer):
    origcp = f_getcurpl()
    f_setcurpl(targetplayer)

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
    f_setcurpl(origcp)

    return ptr, epd


def f_dwread_epd(targetplayer):
    return f_dwepdread_epd(targetplayer)[0]


def f_epdread_epd(targetplayer):
    return f_dwepdread_epd(targetplayer)[1]


def f_dwwrite_epd(targetplayer, value):
    if isinstance(value, c.EUDVariable):
        act = c.Forward()
        c.SeqCompute([
            (ut.EPD(act + 16), c.SetTo, targetplayer),
            (ut.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.SetTo, 0))

    else:
        act = c.Forward()
        c.SeqCompute([(ut.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.SetTo, value))


def f_dwadd_epd(targetplayer, value):
    if isinstance(value, c.EUDVariable):
        act = c.Forward()
        c.SeqCompute([
            (ut.EPD(act + 16), c.SetTo, targetplayer),
            (ut.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.Add, 0))

    else:
        act = c.Forward()
        c.SeqCompute([(ut.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.Add, value))


def f_dwsubtract_epd(targetplayer, value):
    if isinstance(value, c.EUDVariable):
        act = c.Forward()
        c.SeqCompute([
            (ut.EPD(act + 16), c.SetTo, targetplayer),
            (ut.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.Subtract, 0))

    else:
        act = c.Forward()
        c.SeqCompute([(ut.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.Subtract, value))


@c.EUDFunc
def f_dwbreak(number):
    """Get hiword/loword/4byte of dword"""
    word = c.EUDCreateVariables(2)
    byte = c.EUDCreateVariables(4)

    # Clear byte[], word[]
    cs.DoActions([
        word[0].SetNumber(0),
        word[1].SetNumber(0),
        byte[0].SetNumber(0),
        byte[1].SetNumber(0),
        byte[2].SetNumber(0),
        byte[3].SetNumber(0)
    ])

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16
        byteexp = i % 8
        wordexp = i % 16

        c.RawTrigger(
            conditions=number.AtLeast(2 ** i),
            actions=[
                byte[byteidx].AddNumber(2 ** byteexp),
                word[wordidx].AddNumber(2 ** wordexp),
                number.SubtractNumber(2 ** i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]


@c.EUDFunc
def f_dwbreak2(number):
    """Get hiword/loword/4byte of dword"""
    word = c.EUDCreateVariables(2)
    byte = c.EUDCreateVariables(4)

    # Clear byte[], word[]
    cs.DoActions([
        word[0].SetNumber(0),
        word[1].SetNumber(0),
        byte[0].SetNumber(0),
        byte[1].SetNumber(0),
        byte[2].SetNumber(0),
        byte[3].SetNumber(0)
    ])

    for i in range(31, -1, -1):
        byteidx = i // 8
        wordidx = i // 16

        c.RawTrigger(
            conditions=number.AtLeast(2 ** i),
            actions=[
                byte[byteidx].AddNumber(2 ** i),
                word[wordidx].AddNumber(2 ** i),
                number.SubtractNumber(2 ** i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]
