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

from ... import utils as ut
from ..allocator import IsConstExpr
from ..variable import EUDVariable
from .vararray import EUDVArray
from .structarr import _EUDStruct_Metaclass


class EUDStruct(ut.ExprProxy, metaclass=_EUDStruct_Metaclass):
    def __init__(self, initvar=None):
        basetype = type(self)
        fields = basetype._fields_
        fieldn = len(fields)

        # Fill fielddict
        fielddict = {}
        for index, nametype in enumerate(fields):
            if isinstance(nametype, str):
                fielddict[nametype] = (index, None)
            else:
                fielddict[nametype[0]] = (index, nametype[1])
        self._fielddict = fielddict

        # With initialization
        if initvar is None:
            initvals = []
            for nametype in fields:
                if isinstance(nametype, str):
                    initvals.append(0)
                else:
                    _, attrtype = nametype
                    initvals.append(attrtype())

            super().__init__(EUDVArray(fieldn)(initvals))

        else:
            super().__init__(EUDVArray(fieldn)(initvar))

        self._initialized = True

    # Initializer

    def clone(self):
        """ Create struct clone """
        basetype = type(self)
        inst = basetype()
        self.deepcopy(inst)
        return inst

    def setall(self, values):
        self.fill(values, assert_expected_values_len=len(self._fielddict))

    def deepcopy(self, inst):
        """ Copy struct to other instance """
        basetype = type(self)
        fields = basetype._fields_
        for i, nametype in enumerate(fields):
            if isinstance(nametype, str):
                inst.set(i, self.get(i))
            else:
                _, attrtype = nametype
                attrtype(self.get(i)).deepcopy(attrtype(inst.get(i)))

    # Field setter & getter

    def getfield(self, name):
        attrid, attrtype = self._fielddict[name]
        attr = self.get(attrid)
        if attrtype:
            return attrtype(attr)
        else:
            return attr

    def setfield(self, name, value):
        attrid, _ = self._fielddict[name]
        self.set(attrid, value)

    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return self.getfield(name)

    def __setattr__(self, name, value):
        if '_initialized' in self.__dict__:
            try:
                self.setfield(name, value)
            except KeyError:
                self.__dict__[name] = value
        else:
            self.__dict__[name] = value

    # Utilities

    def asVariable(self):
        if IsConstExpr(self):
            var = EUDVariable(self)
        else:
            var = EUDVariable()
            var << self
        return type(self)(var)

    def __lshift__(self, rhs):
        raise ut.EPError('Cannot reassign another value to eudstruct.')
