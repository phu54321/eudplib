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

from .. import core as c


class VariableBase:
    def __init__(self):
        pass

    def GetVariableMemoryAddr(self):
        raise NotImplementedError('override')

    # -------

    def AtLeast(self, value):
        return c.Memory(self.GetVariableMemoryAddr(), c.AtLeast, value)

    def AtMost(self, value):
        return c.Memory(self.GetVariableMemoryAddr(), c.AtMost, value)

    def Exactly(self, value):
        return c.Memory(self.GetVariableMemoryAddr(), c.Exactly, value)

    # -------

    def SetNumber(self, value):
        return c.SetMemory(self.GetVariableMemoryAddr(), c.SetTo, value)

    def AddNumber(self, value):
        return c.SetMemory(self.GetVariableMemoryAddr(), c.Add, value)

    def SubtractNumber(self, value):
        return c.SetMemory(self.GetVariableMemoryAddr(), c.Subtract, value)

    # -------

    def Assign(self, value):
        c.Trigger(actions=c.SetMemory(self.GetVariableMemoryAddr(), c.SetTo, value))

    def __lshift__(self, value):
        self.Assign(value)

    def __iadd__(self, value):
        c.Trigger(actions=c.SetMemory(self.GetVariableMemoryAddr(), c.Add, value))

    def __isub__(self, value):
        c.Trigger(actions=c.SetMemory(self.GetVariableMemoryAddr(), c.Subtract, value))

    # -------

    def __eq__(self, other):
        return self.Exactly(other)

    def __le__(self, other):
        return self.AtMost(other)

    def __ge__(self, other):
        return self.AtLeast(other)
