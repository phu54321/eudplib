#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2019 Armoha

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
"""

import itertools
from ... import core as c, ctrlstru as cs, utils as ut
from ..memiof import f_getcurpl, f_setcurpl
from .eudprint import ptr2s, epd2s
from .cpprint import prevcp, f_cpstr_print, cw
from .rwcommon import br1
from .strfunc import f_strlen_epd


"""
texteffect.py 0.3.4 by Artanis

## [0.3.4] - 2019-01-18
### Fixed
- f_fadein, f_fadeout used (arg,) as timer when len(args) == 1.
- Now use MemoryX and SetDeathsX from eudx.py or euddraft 0.8.3.0+.
- f_fadein, f_fadeout issued error with color code(s) and no content.

## [0.3.2] - 2018-12-12
### Changed
- Now use customText 0.4.0
### Added
- cp949 option for stat_txt.tbl modification
- s2u option for concatenate unit name

## [0.3.1] - 2018-12-03
### Fixed
- Fix keep running f_fadeout(line=12) crash SC

## [0.3.0] - 2018-12-03
### A complete code rewrite for customText4 0.3.2
### Changed
- Change named argument's name of f_fadein, f_fadeout as followings
    interval -> wait
    autoreset -> reset
- Text identifier and timer are now identical
    - Can remove text on screen by f_remove(timer).
    - Effects sharing timer uses same identifier.

### Added
- f_cpchar_print and series of CurrentPlayer print functions are added.
- Add f_settimer(timer, Modifier, Value)

### Removed
- ct.f_get is unsupported for now.

0.2.1 - reduce trigger amount. increase identifiers from 253 to 113379904.
0.2.0 - corrected issue: fixed-line display doesn't remove previous text.
        return 0 when effect is over, return 1 when effect is ongoing.
0.1.0 - inital release.
"""

color_codes = list(range(1, 32))
color_codes.remove(0x12)  # right align
color_codes.remove(0x13)  # center align

color_code = b"\x02"
color_v = c.EUDVariable()


@c.EUDFunc
def f_cpchar_addstr(src):
    if cs.EUDInfLoop()():
        b1 = br1.readbyte()
        cs.EUDBreakIf(b1 == 0)
        cw.writebyte(color_v)
        cw.writebyte(b1)
        if cs.EUDIf()(b1 <= 0x7F):
            cw.flushdword()
        if cs.EUDElse()():
            b2 = br1.readbyte()
            cw.writebyte(b2)
            if cs.EUDIf()(b1 <= 0xDF):  # Encode as 2-byte
                cw.flushdword()
            if cs.EUDElse()():  # 3-byte
                cw.writebyte(br1.readbyte())
            cs.EUDEndIf()
        cs.EUDEndIf()
    cs.EUDEndInfLoop()


@c.EUDFunc
def f_cpchar_adddw(number):
    skipper = [c.Forward() for _ in range(9)]
    ch = [0] * 10

    for i in range(10):  # Get digits
        number, ch[i] = c.f_div(number, 10)
        if i != 9:
            cs.EUDJumpIf(number == 0, skipper[i])

    for i in range(9, -1, -1):  # print digits
        if i != 9:
            skipper[i] << c.NextTrigger()
        cs.DoActions(
            [
                c.SetDeaths(
                    c.CurrentPlayer, c.SetTo, color_v + ch[i] * 256 + (0x0D0D3000), 0
                ),
                c.AddCurrentPlayer(1),
            ]
        )


def f_cpchar_print(*args):
    global color_code
    args = ut.FlattenList(args)

    for arg in args:
        encode_func = ut.u2utf8
        if isinstance(arg, bytes):
            try:
                arg = arg.decode("cp949")
                encode_func = ut.u2b
            except (UnicodeDecodeError):
                arg = arg.decode("UTF-8")
        if isinstance(arg, str):
            bytestring = b""
            for char in arg:
                char = encode_func(char)
                if ut.b2i1(char) in color_codes:
                    color_code = char
                    continue
                while len(char) < 3:
                    char = char + b"\r"
                bytestring = bytestring + color_code + char
            cs.DoActions(color_v.SetNumber(ut.b2i1(color_code)))
            if not bytestring:
                bytestring = color_code + b"\r\r\r"
            f_cpstr_print(bytestring)
        elif ut.isUnproxyInstance(arg, ptr2s):
            br1.seekoffset(arg._value)
            f_cpchar_addstr(arg._value)
        elif ut.isUnproxyInstance(arg, epd2s):
            br1.seekepd(arg._value)
            f_cpchar_addstr(arg._value)
        elif ut.isUnproxyInstance(arg, c.EUDVariable) or c.IsConstExpr(arg):
            f_cpchar_adddw(arg)
        else:
            f_cpstr_print(arg)
    cs.DoActions(c.SetDeaths(c.CurrentPlayer, c.SetTo, 0, 0))
