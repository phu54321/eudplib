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

from . import dwmemio as dwm
from . import byterw as brw

# Helper functions

_bw = brw.EUDByteWriter()
_br = brw.EUDByteReader()


def f_dwwrite(ptr, dw):
    chars = dwm.f_dwbreak(dw)[2:]
    _bw.seekoffset(ptr)
    _bw.writebyte(chars[0])
    _bw.writebyte(chars[1])
    _bw.writebyte(chars[2])
    _bw.writebyte(chars[3])
    _bw.flushdword()


def f_wwrite(ptr, w):
    chars = dwm.f_dwbreak(w)[2:]
    _bw.seekoffset(ptr)
    _bw.writebyte(chars[0])
    _bw.writebyte(chars[1])
    _bw.flushdword()


def f_bwrite(ptr, b):
    _bw.seekoffset(ptr)
    _bw.writebyte(b)
    _bw.flushdword()


# -----------------------------


def f_dwread(ptr):
    _br.seekoffset(ptr)
    chars0 = _br.readbyte()
    chars1 = _br.readbyte()
    chars2 = _br.readbyte()
    chars3 = _br.readbyte()
    return (
        chars0 +
        chars1 * 0x100 +
        chars2 * 0x10000 +
        chars3 * 0x1000000
    )


def f_wread(ptr):
    _br.seekoffset(ptr)
    chars0 = _br.readbyte()
    chars1 = _br.readbyte()
    return (
        chars0 +
        chars1 * 0x100
    )


def f_bread(ptr):
    _br.seekoffset(ptr)
    return _br.readbyte()
