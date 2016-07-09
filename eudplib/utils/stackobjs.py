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

from cffi import FFI
import os
import sys


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


#  initFFI()
ffi = FFI()
ffi.cdef("""
typedef struct
{
    size_t _size;
    int* _data;
} OccupMap;

void StackOccupmaps(OccupMap occupList[], size_t* ret, int size);
""")
stackObjDLL = ffi.dlopen(find_data_file("StackOccupmap.dll"))


# Function def

def StackObjects(found_objects, dwoccupmap_dict, alloctable):
    occupListPy = []
    objn = len(found_objects)

    for obj in found_objects:
        dwoccupmap = dwoccupmap_dict[obj]
        dwOccupmapData = ffi.new("int[]", dwoccupmap)
        occupListPy.append((len(dwoccupmap), dwOccupmapData))

    occupList = ffi.new("OccupMap[]", occupListPy)
    retList = ffi.new("size_t[]", objn)
    stackObjDLL.StackOccupmaps(occupList, retList, objn)

    for i, obj in enumerate(found_objects):
        alloctable[obj] = retList[i]
