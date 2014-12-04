#!/usr/bin/python
#-*- coding: utf-8 -*-

from ... import core as c
from ... import ctrlstru as cs
from ... import varfunc as vf
from .. import math


def f_epd(addr):
    return math.f_div(addr + (0x100000000 - 0x58A364), 4)[0]


@vf.EUDFunc
def f_dwepdread_epd(targetplayer):
    retdw, retepd = vf.EUDVariable(), vf.EUDVariable()
    cmpc, a1, a2, a3 = c.Forward(), c.Forward(), c.Forward(), c.Forward()

    vf.SeqCompute([
        (c.EPD(cmpc + 4), c.SetTo, targetplayer),
        (c.EPD(a1 + 16), c.SetTo, targetplayer),
        (retdw, c.SetTo, 0),
        (retepd, c.SetTo, c.EPD(0))
    ])

    cmpt = c.Trigger(
        conditions=[
            cmpc << c.Memory(0, c.AtLeast, 2**31)
        ],
        actions=[
            a1 << c.SetMemory(0, c.Subtract, 2**31),
            a2 << retdw.AddNumber(2**31),
            a3 << retepd.AddNumber(2**29)
        ]
    )

    chain = [c.Forward() for _ in range(32)]
    for i in range(30, 1, -1):
        chain[i+1] << c.Trigger(
            nextptr=cmpt,
            actions=[
                c.SetNextPtr(cmpt, chain[i]),
                c.SetMemory(a1 + 20, c.SetTo, 2**i),
                c.SetMemory(a2 + 20, c.SetTo, 2**i),
                c.SetMemory(a3 + 20, c.SetTo, 2**(i-2))
            ]
        )

    for i in range(1, -1, -1):
        chain[i+1] << c.Trigger(
            nextptr=cmpt,
            actions=[
                c.SetNextPtr(cmpt, chain[i]),
                c.SetMemory(a1 + 20, c.SetTo, 2**i),
                c.SetMemory(a2 + 20, c.SetTo, 2**i),
                c.SetMemory(a3 + 20, c.SetTo, 0)
            ]
        )

    chain[0] << c.Trigger(
        actions=[
            c.SetNextPtr(cmpt, chain[31]),
            c.SetMemory(a1 + 20, c.SetTo, 2**31),
            c.SetMemory(a2 + 20, c.SetTo, 2**31),
            c.SetMemory(a3 + 20, c.SetTo, 2**29)
        ]
    )

    f_dwwrite_epd(targetplayer, retdw)

    return retdw, retepd


def f_dwread_epd(targetplayer):
    return f_dwread_epd_nw(targetplayer)
    # return f_dwepdread_epd(targetplayer)[0]

def f_epdread_epd(targetplayer):
    return f_epd(f_dwread_epd_nw(targetplayer))
    # return f_dwepdread_epd(targetplayer)[1]


# -------


@vf.EUDFunc
def f_dwread_epd_nw(targetplayer):
    ret = vf.EUDVariable()

    # Common comparison trigger
    c.PushTriggerScope()
    cmpc = c.Forward()
    cmp_player = cmpc + 4
    cmp_number = cmpc + 8
    cmpact = c.Forward()

    cmptrigger = c.Forward()
    cmptrigger << c.Trigger(
        conditions=[
            cmpc << c.Memory(0, c.AtMost, 0)
        ],
        actions=[
            cmpact << c.SetMemory(cmptrigger + 4, c.SetTo, 0)
        ]
    )
    cmpact_ontrueaddr = cmpact + 20
    c.PopTriggerScope()

    # static_for
    chain1 = [c.Forward() for _ in range(32)]
    chain2 = [c.Forward() for _ in range(32)]

    # Main logic start
    vf.SeqCompute([
        (c.EPD(cmp_player), c.SetTo, targetplayer),
        (c.EPD(cmp_number), c.SetTo, 0xFFFFFFFF),
        (ret,               c.SetTo, 0xFFFFFFFF)
    ])

    readend = c.Forward()

    for i in range(31, -1, -1):
        nextchain = chain1[i - 1] if i > 0 else readend

        chain1[i] << c.Trigger(
            nextptr=cmptrigger,
            actions=[
                c.SetMemory(cmp_number, c.Subtract, 2 ** i),
                ret.SubtractNumber(2 ** i),
                c.SetNextPtr(cmptrigger, chain2[i]),
                c.SetMemory(cmpact_ontrueaddr, c.SetTo, nextchain)
            ]
        )

        chain2[i] << c.Trigger(
            actions=[
                c.SetMemory(cmp_number, c.Add, 2 ** i),
                ret.AddNumber(2 ** i)
            ]
        )

    readend << c.NextTrigger()

    return ret


# -------


def f_dwwrite_epd(targetplayer, value):
    if isinstance(value, vf.EUDVariable):
        act = c.Forward()
        vf.SeqCompute([
            (c.EPD(act + 16), c.SetTo, targetplayer),
            (c.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.SetTo, 0))

    else:
        act = c.Forward()
        vf.SeqCompute([(c.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.SetTo, value))


def f_dwadd_epd(targetplayer, value):
    if isinstance(value, vf.EUDVariable):
        act = c.Forward()
        vf.SeqCompute([
            (c.EPD(act + 16), c.SetTo, targetplayer),
            (c.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.Add, 0))

    else:
        act = c.Forward()
        vf.SeqCompute([(c.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.Add, value))


def f_dwsubtract_epd(targetplayer, value):
    if isinstance(value, vf.EUDVariable):
        act = c.Forward()
        vf.SeqCompute([
            (c.EPD(act + 16), c.SetTo, targetplayer),
            (c.EPD(act + 20), c.SetTo, value)
        ])
        cs.DoActions(act << c.SetMemory(0, c.Subtract, 0))

    else:
        act = c.Forward()
        vf.SeqCompute([(c.EPD(act + 16), c.SetTo, targetplayer)])
        cs.DoActions(act << c.SetMemory(0, c.Subtract, value))


@vf.EUDFunc
def f_dwbreak(number):
    word = vf.EUDCreateVariables(2)
    byte = vf.EUDCreateVariables(4)

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

        c.Trigger(
            conditions=number.AtLeast(2 ** i),
            actions=[
                byte[byteidx].AddNumber(2 ** byteexp),
                word[wordidx].AddNumber(2 ** wordexp),
                number.SubtractNumber(2 ** i)
            ]
        )

    return word[0], word[1], byte[0], byte[1], byte[2], byte[3]
