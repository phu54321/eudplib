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

from eudplib import (
    core as c,
    ctrlstru as cs,
    utils as ut,
)

from .rwcommon import br1, bw1
from .dbstr import DBString


@c.EUDFunc
def f_dbstr_addstr(dst, src):
    """Print string as string to dst. Same as strcpy except of return value.

    :param dst: Destination address (Not EPD player)
    :param src: Source address (Not EPD player)

    :returns: dst + strlen(src)
    """
    b = c.EUDVariable()

    br1.seekoffset(src)
    bw1.seekoffset(dst)

    if cs.EUDInfLoop()():
        c.SetVariables(b, br1.readbyte())
        bw1.writebyte(b)
        cs.EUDBreakIf(b == 0)
        dst += 1
    cs.EUDEndInfLoop()

    bw1.flushdword()

    return dst


@c.EUDFunc
def f_dbstr_adddw(dst, number):
    """Print number as string to dst.

    :param dst: Destination address (Not EPD player)
    :param number: DWORD to print

    :returns: dst + strlen(itoa(number))
    """
    bw1.seekoffset(dst)

    skipper = [c.Forward() for _ in range(9)]

    # Get digits
    number, ch0 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[0])
    number, ch1 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[1])
    number, ch2 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[2])
    number, ch3 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[3])
    number, ch4 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[4])
    number, ch5 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[5])
    number, ch6 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[6])
    number, ch7 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[7])
    number, ch8 = c.f_div(number, 10)
    cs.EUDJumpIf(number == 0, skipper[8])
    number, ch9 = c.f_div(number, 10)

    # print digits
    bw1.writebyte(ch9 + b'0'[0])
    dst += 1
    skipper[8] << c.NextTrigger()
    bw1.writebyte(ch8 + b'0'[0])
    dst += 1
    skipper[7] << c.NextTrigger()
    bw1.writebyte(ch7 + b'0'[0])
    dst += 1
    skipper[6] << c.NextTrigger()
    bw1.writebyte(ch6 + b'0'[0])
    dst += 1
    skipper[5] << c.NextTrigger()
    bw1.writebyte(ch5 + b'0'[0])
    dst += 1
    skipper[4] << c.NextTrigger()
    bw1.writebyte(ch4 + b'0'[0])
    dst += 1
    skipper[3] << c.NextTrigger()
    bw1.writebyte(ch3 + b'0'[0])
    dst += 1
    skipper[2] << c.NextTrigger()
    bw1.writebyte(ch2 + b'0'[0])
    dst += 1
    skipper[1] << c.NextTrigger()
    bw1.writebyte(ch1 + b'0'[0])
    dst += 1
    skipper[0] << c.NextTrigger()
    bw1.writebyte(ch0 + b'0'[0])
    dst += 1

    bw1.writebyte(0)  # EOS
    bw1.flushdword()

    return dst


def f_dbstr_print(dst, *args):
    """Print multiple string / number to dst.

    :param dst: Destination address (Not EPD player)
    :param args: Things to print

    """
    if isinstance(dst, DBString):
        dst = dst.GetStringMemoryAddr()

    args = ut.FlattenList(args)
    for arg in args:
        if isinstance(arg, bytes):
            dst = f_dbstr_addstr(dst, c.Db(arg) + b'\0')
        elif isinstance(arg, str):
            dst = f_dbstr_addstr(dst, c.Db(ut.u2b(arg) + b'\0'))
        elif isinstance(arg, DBString):
            dst = f_dbstr_addstr(dst, arg.GetStringMemoryAddr())
        elif isinstance(arg, int):
            # int and c.EUDVariable should act the same if possible.
            # EUDVariable has a value of 32bit unsigned integer.
            # So we adjust arg to be in the same range.
            dst = f_dbstr_addstr(dst, str(arg & 0xFFFFFFFF))
        elif isinstance(arg, c.EUDVariable):
            dst = f_dbstr_adddw(dst, arg)
        else:
            raise ut.EPError(
                'Object wit unknown parameter type %s given to f_eudprint.'
                % type(arg)
            )

    return dst


_printf_buffer = DBString(1024)


def f_simpleprint(*args):
    # Add spaces between arguments
    spaced_args = []
    for arg in args:
        spaced_args.extend([arg, ' '])
    args = spaced_args[:-1]

    f_dbstr_print(_printf_buffer, *args)
    cs.DoActions(_printf_buffer.GetDisplayAction())
