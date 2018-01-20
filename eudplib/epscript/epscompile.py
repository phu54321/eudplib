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

from ctypes import (
    CDLL,
    c_int, c_char_p, c_void_p
)

from eudplib.utils import (
    u2b, find_data_file
)

import platform

libFile = {
    'windows': 'libepScriptLib.dll',  # Windows
    'darwin': 'libepScriptLib.dylib',  # Mac
}[platform.system().lower()]


libeps = CDLL(find_data_file(libFile, __file__))
libeps.compileString.argtypes = [c_char_p, c_char_p]
libeps.compileString.restype = c_void_p
libeps.freeCompiledResult.argtypes = [c_void_p]
libeps.setDebugMode.argtypes = [c_int]
libeps.getErrorCount.argtypes = []
libeps.getErrorCount.resType = c_int


def epsCompile(modname, bCode):
    modname = u2b(modname)
    output = libeps.compileString(modname, bCode)
    if not output or libeps.getErrorCount():
        return None
    outputStr = c_char_p(output).value
    libeps.freeCompiledResult(output)
    return outputStr


def EPS_SetDebug(b):
    libeps.setDebugMode(b)
