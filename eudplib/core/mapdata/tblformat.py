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

'''
String table manager. Internally used in eudplib.
'''

from eudplib import utils as ut


class TBL:
    def __init__(self, content=None):
        #
        # datatb : table of strings                       : string data table
        # dataindextb : string id -> data id              : string offset table
        # stringmap : string -> representative string id
        #

        self._datatb = []
        self._stringmap = {}
        self._dataindextb = []  # String starts from #1
        self._capacity = 2  # Size of STR section

        if content is not None:
            self.LoadTBL(content)

    def LoadTBL(self, content):
        self._datatb.clear()
        self._stringmap.clear()
        self._capacity = 2

        stringcount = ut.b2i2(content, 0)
        for i in range(stringcount):
            i += 1
            stringoffset = ut.b2i2(content, i * 2)
            send = stringoffset
            while content[send] != 0:
                send += 1

            string = content[stringoffset:send]
            self.AddString(string)

    def AddString(self, string):
        string = ut.u2b(string)  # Starcraft uses multibyte encoding.
        if not isinstance(string, bytes):
            raise ut.EPError('Invalid type for string')

        stringindex = len(self._dataindextb)

        # If duplicate text exist -> just proxy it
        try:
            repr_stringid = self._stringmap[string]
            dataindex = self._dataindextb[repr_stringid]
            self._dataindextb.append(dataindex)
            self._capacity += 2  # just string offset

        # Else -> Create new entry
        except KeyError:
            dataindex = len(self._datatb)
            self._stringmap[string] = stringindex
            self._datatb.append(string)
            self._dataindextb.append(dataindex)
            # string + b'\0' + string offset
            self._capacity += len(string) + 1 + 2

        ut.ep_assert(self._capacity < 65536, 'String table overflow')

        return stringindex

    def GetString(self, index):
        if index == 0:
            return None
        else:
            try:
                dataindex = self._dataindextb[index - 1]
                return self._datatb[dataindex]
            except IndexError:
                return None

    def GetStringIndex(self, string):
        string = ut.u2b(string)
        if not isinstance(string, bytes):
            raise ut.EPError('Invalid type for string')

        try:
            return self._stringmap[string] + 1

        except KeyError:
            return self.AddString(string) + 1

    def SaveTBL(self):
        outbytes = []

        # calculate offset of each string
        stroffset = []
        outindex = 2 * len(self._dataindextb) + 2
        for s in self._datatb:
            stroffset.append(outindex)
            outindex += len(s) + 1

        # String count
        outbytes.append(ut.i2b2(len(self._dataindextb)))

        # String offsets
        for dataidx in self._dataindextb:
            outbytes.append(ut.i2b2(stroffset[dataidx]))

        # String data
        for s in self._datatb:
            outbytes.append(s)
            outbytes.append(b'\0')

        return b''.join(outbytes)
