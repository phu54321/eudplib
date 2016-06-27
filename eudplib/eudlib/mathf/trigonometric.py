#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Copyright (c) 2014 trgk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import math

from eudplib import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

from ..memiof import f_dwread_epd
from ..stringf import f_simpleprint

@c.EUDFunc
def f_lengthdir(length, angle):
    # sin, cos table
    clist = []
    slist = []

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    for i in range(91):
        cosv = math.floor(math.cos(math.pi / 180 * i) * 65536 + 0.5)
        sinv = math.floor(math.sin(math.pi / 180 * i) * 65536 + 0.5)
        clist.append(ut.i2b4(cosv))
        slist.append(ut.i2b4(sinv))

    cdb = c.Db(b''.join(clist))
    sdb = c.Db(b''.join(slist))

    # MAIN LOGIC

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    if cs.EUDIf()(angle >= 360):
        angle << c.f_div(angle, 360)[1]
    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    ldir_x, ldir_y = c.EUDVariable(), c.EUDVariable()  # cos, sin * 65536
    # sign of cos, sin
    csign, ssign = c.EUDLightVariable(), c.EUDLightVariable()
    tableangle = c.EUDVariable()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # get cos, sin from table
    if cs.EUDIf()(angle <= 89):
        tableangle << angle
        csign << 1
        ssign << 1

    if cs.EUDElseIf()(angle <= 179):
        tableangle << 180 - angle
        csign << -1
        ssign << 1

    if cs.EUDElseIf()(angle <= 269):
        tableangle << angle - 180
        csign << -1
        ssign << -1

    if cs.EUDElse()():
        tableangle << 360 - angle
        csign << 1
        ssign << -1

    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    tablecos = f_dwread_epd(ut.EPD(cdb) + tableangle)
    tablesin = f_dwread_epd(ut.EPD(sdb) + tableangle)

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # calculate lengthdir
    ldir_x << c.f_div(c.f_mul(tablecos, length), 65536)[0]
    ldir_y << c.f_div(c.f_mul(tablesin, length), 65536)[0]

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    # restore sign of cos, sin
    if cs.EUDIf()(csign == -1):
        ldir_x << 0xFFFFFFFF - ldir_x + 1
    cs.EUDEndIf()

    if cs.EUDIf()(ssign == -1):
        ldir_y << 0xFFFFFFFF - ldir_y + 1
    cs.EUDEndIf()

    cs.DoActions(c.SetDeaths(1, c.Add, 1, 0))
    return ldir_x, ldir_y


# Formula source : http://nghiaho.com/?p=997

@c.EUDFunc
def f_atan2(y, x):
    signflags = c.EUDVariable()
    signflags << 0

    # Check x sign
    if cs.EUDIf()(x >= 0x80000000):
        x << -x
        signflags += 1  # set xsign
    cs.EUDEndIf()

    # Check y sign
    if cs.EUDIf()(y >= 0x80000000):
        y << -y
        signflags += 2  # set ysign
    cs.EUDEndIf()

    # Check x/y order
    if cs.EUDIf()(y >= x):
        z = c.EUDVariable()
        # Swap x, y so that y <= x
        z << x
        x << y
        y << z
        signflags += 4  # set xyabscmp
    cs.EUDEndIf()

    # To prevent overflow, we limit values of y and x.
    # atan value is maximized when x = y, then atan_value = 45 * x**3
    # 45 * x**3 <= 0xFFFFFFFF : x <= 456.99....
    if cs.EUDIf()(x >= 400):
        # Normalize below 400
        divn = x // 400 + 1
        x //= divn
        y //= divn
    cs.EUDEndIf()

    # Calculate arctan value
    # arctan(z) ~= z * (45 - (z-1) * (14 + 4*z)), 0 <= z <= 1
    # arctan(y/x) ~= y/x * (45 - (y-x)/x * (14x + 4y)/x))
    # arctan(y/x) ~= y * (45*x*x - (y-x)(14x+4y)) / (x*x*x)
    t1 = x * x
    t2 = y * (45 * t1 - (y - x) * (14 * x + 4 * y))
    t3 = x * t1
    atan_value = t2 // t3

    # Translate angles by sign flags
    #
    #      |  0 |  1 | xsign          |  0 |  1 | xsign
    # -----+----+----+-----      -----+----+----+-----
    #   0  |  0+|180-|             0  | 90-| 90+|
    # -----+----+----+           -----+----+----+
    #   1  |360-|180+|             1  |270+|270-|
    # -----+----+----+           -----+----+----+
    # ysign|      xyabscmp=0     ysign|      xyabscmp=1

    cs.EUDSwitch(signflags)
    cs.EUDSwitchCase()(0)  # xsign, ysign, xyabscmp = 0, 0, 0
    c.EUDReturn(atan_value)
    cs.EUDSwitchCase()(1)  # xsign, ysign, xyabscmp = 1, 0, 0
    c.EUDReturn(180 - atan_value)
    cs.EUDSwitchCase()(2)  # xsign, ysign, xyabscmp = 0, 1, 0
    c.EUDReturn(360 - atan_value)
    cs.EUDSwitchCase()(3)  # xsign, ysign, xyabscmp = 1, 1, 0
    c.EUDReturn(180 + atan_value)
    cs.EUDSwitchCase()(4)  # xsign, ysign, xyabscmp = 0, 0, 1
    c.EUDReturn(90 - atan_value)
    cs.EUDSwitchCase()(5)  # xsign, ysign, xyabscmp = 1, 0, 1
    c.EUDReturn(90 + atan_value)
    cs.EUDSwitchCase()(6)  # xsign, ysign, xyabscmp = 0, 1, 1
    c.EUDReturn(270 + atan_value)
    cs.EUDSwitchCase()(7)  # xsign, ysign, xyabscmp = 1, 1, 1
    c.EUDReturn(270 - atan_value)
    cs.EUDEndSwitch()
