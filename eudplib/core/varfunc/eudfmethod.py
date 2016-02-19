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

import functools
import inspect

from . import eudf
from eudplib import utils as ut

__f_increment = 0


def EUDFuncMethod(method):
    global __f_increment

    # Get argument number of fdecl_func
    argspec = inspect.getargspec(method)
    ut.ep_assert(
        argspec[1] is None,
        'No variadic arguments (*args) allowed for EUDFunc.'
    )
    ut.ep_assert(
        argspec[2] is None,
        'No variadic keyword arguments (*kwargs) allowed for EUDFunc.'
    )

    argn = len(argspec[0]) - 1
    idf = __f_increment
    __f_increment += 1

    def call(self, *args):
        # Create eudfuncmethod list
        if not hasattr(self, '_efmlist'):
            self._efmlist = {}

        # Create wrapper for eudfunc
        if idf not in self._efmlist:
            def call2(*args):
                return method(self, *args)
            call2 = eudf.EUDFuncN(call2, argn)
            self._efmlist[idf] = call2

        # Call that wrapper with arguments
        return self._efmlist[idf](*args)

    functools.update_wrapper(call, method)
    return call
