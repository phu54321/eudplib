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

from ..core.mapdata import mapdata, mpqapi

from .injector.applyInjector import applyInjector
from .inlinecode.ilcprocesstrig import PreprocessInlineCode
from .injector.doevents import _MainStarter
from .mpqadd import UpdateMPQ


def SaveMap(fname, rootf):
    """Save output map with root function.

    :param fname: Path for output map.
    :param rootf: Main entry function.
    """

    print('Saving to %s...' % fname)
    chkt = mapdata.GetChkTokenized()

    # Add payload
    root = _MainStarter(rootf)
    PreprocessInlineCode(chkt)
    mapdata.UpdateMapData()
    applyInjector(chkt, root)

    chkt.optimize()
    rawchk = chkt.savechk()
    print('Output scenario.chk : %.3fMB' % (len(rawchk) / 1000000))

    # Process by modifying existing mpqfile
    open(fname, 'wb').write(mapdata.GetRawFile())

    mw = mpqapi.MpqWrite()
    mw.Open(fname)
    mw.PutFile('staredit\\scenario.chk', rawchk, replace=True)
    UpdateMPQ(mw)
    # mw.DeleteFile('(listfile)')
    mw.Compact()
    mw.Close()
