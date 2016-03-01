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
SFmpq.dll wrapper. Used internally inside eudplib.
'''

from ctypes import *  # @UnusedWildImport
import struct
import os
import sys

from eudplib import utils as ut


"""
find where sfmpq.dll is.
"""

# These can be an argument to for MpqWrite.PutWave
WAVCOMP_NOCOMPRESSION = 0
WAVCOMP_HIGHQUALITY = 1
WAVCOMP_MIDQUALITY = 2
WAVCOMP_LOWQUALITY = 3

SFmpq = None


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


currentdir = os.path.dirname(__file__)


def InitMpqLibrary():
    global SFmpq

    try:
        if struct.calcsize("P") == 4:  # 32bit
            SFmpq = WinDLL(find_data_file('SFmpq32.dll'))
        else:
            SFmpq = WinDLL(find_data_file('SFmpq64.dll'))

        # for MpqRead
        SFmpq.SFileOpenArchive.restype = c_int
        SFmpq.SFileCloseArchive.restype = c_int
        SFmpq.SFileOpenFileEx.restype = c_int
        SFmpq.SFileGetFileSize.restype = c_int
        SFmpq.SFileReadFile.restype = c_int
        SFmpq.SFileCloseFile.restype = c_int

        SFmpq.SFileOpenArchive.argtypes = [c_char_p, c_int, c_int, c_void_p]
        SFmpq.SFileCloseArchive.argtypes = [c_void_p]
        SFmpq.SFileOpenFileEx.argtypes = [c_int, c_char_p, c_int, c_void_p]
        SFmpq.SFileGetFileSize.argtypes = [c_int, c_void_p]
        SFmpq.SFileReadFile.argtypes = [
            c_int, c_char_p, c_int, c_void_p, c_int]
        SFmpq.SFileCloseFile.argtypes = [c_int]

        # for MpqWrite
        SFmpq.MpqOpenArchiveForUpdate.restype = c_int
        SFmpq.MpqAddFileFromBuffer.restype = c_int
        SFmpq.MpqAddWaveFromBuffer.restype = c_int
        SFmpq.MpqRenameFile.restype = c_int
        SFmpq.MpqDeleteFile.restype = c_int
        SFmpq.MpqCloseUpdatedArchive.restype = c_int
        SFmpq.MpqCompactArchive.restype = c_int

        SFmpq.MpqOpenArchiveForUpdate.argtypes = [c_char_p, c_int, c_int]
        SFmpq.MpqAddFileFromBuffer.argtypes = [
            c_int, c_void_p, c_int, c_char_p, c_int, c_int, c_int]
        SFmpq.MpqAddWaveFromBuffer.argtypes = [
            c_int, c_void_p, c_int, c_char_p, c_int, c_int]
        SFmpq.MpqRenameFile.argtypes = [c_int, c_char_p, c_char_p]
        SFmpq.MpqDeleteFile.argtypes = [c_int, c_char_p]
        SFmpq.MpqCloseUpdatedArchive.argtypes = [c_int, c_int]
        SFmpq.MpqCompactArchive.argtypes = [c_int]

        return True

    except OSError:
        print('Loading SFmpq failed.')
        SFmpq = None
        return False


class MpqRead:

    def __init__(self):
        self.mpqh = None
        self.SFmpq = SFmpq  # SFmpq are global variable. We cannot rely on it

    def __del__(self):
        self.Close()

    def Open(self, fname):
        if self.mpqh is not None:
            raise ut.EPError("double open")

        h = c_int()
        ret = self.SFmpq.SFileOpenArchive(ut.u2b(fname), 0, 0, byref(h))
        if not ret:
            self.mpqh = None
            return False

        self.mpqh = h.value
        return True

    def Close(self):
        if self.mpqh is None:
            return None

        self.SFmpq.SFileCloseArchive(self.mpqh)
        self.mpqh = None
        return True

    def EnumFiles(self):
        # using listfile.
        lst = self.Extract('(listfile)')
        if lst is None:
            return []

        return ut.b2u(lst).replace('\r', '').split('\n')

    def Extract(self, fname):
        if self.mpqh is None:
            return None

        # Open file
        fileh = c_int()
        ret = self.SFmpq.SFileOpenFileEx(
            self.mpqh, ut.u2b(fname), 0, byref(fileh))
        if not ret:
            return None
        fileh = fileh.value

        # Get file size & allocate buffer
        # Note : this version only supports 32bit mpq file
        fsize = self.SFmpq.SFileGetFileSize(fileh, 0)
        f = create_string_buffer(fsize)
        readleft = fsize
        read = 0

        # read data
        while readleft > 0:
            buffer = create_string_buffer(readleft)
            readbyte = c_int()
            ret = self.SFmpq.SFileReadFile(
                fileh, buffer, readleft, byref(readbyte), 0)
            ut.ep_assert(readbyte.value <= readleft)
            if not ret or readbyte.value == 0:  # read failed
                self.SFmpq.SFileCloseFile(fileh)
                return None

            f[read:read + readbyte.value] = buffer[0:readbyte.value]
            readleft -= readbyte.value
            read += readbyte.value

        self.SFmpq.SFileCloseFile(fileh)
        return f.raw


# flags internally used by MpqWrite
MOAU_OPEN_ALWAYS = 0x20
MOAU_CREATE_ALWAYS = 0x08
MOAU_MAINTAIN_LISTFILE = 0x01

MAFA_MODCRYPTKEY = 0x00020000
MAFA_ENCRYPT = 0x00010000
MAFA_COMPRESS = 0x00000200
MAFA_REPLACE_EXISTING = 0x00000001
MAFA_COMPRESS_STANDARD = 0x08

# NEVER USE THESE FOR MpqWrite.PutWave!!!!!!
MAWA_QUALITY_HIGH = 1
MAWA_QUALITY_MEDIUM = 0
MAWA_QUALITY_LOW = 2
WaveCmpDict = {
    WAVCOMP_NOCOMPRESSION: -1,
    WAVCOMP_HIGHQUALITY: MAWA_QUALITY_HIGH,
    WAVCOMP_MIDQUALITY: MAWA_QUALITY_MEDIUM,
    WAVCOMP_LOWQUALITY: MAWA_QUALITY_LOW
}
# NEVER USE THESE FOR MpqWrite.PutWave!!!!!!


class MpqWrite:

    def __init__(self):
        self.mpqh = None

    def __del__(self):
        self.Close()

    def Open(self, fname, preserve_content=True):
        if self.mpqh:
            raise ut.EPError("double open")

        if preserve_content:
            flag = MOAU_OPEN_ALWAYS | MOAU_MAINTAIN_LISTFILE
        else:
            flag = MOAU_CREATE_ALWAYS | MOAU_MAINTAIN_LISTFILE

        ret = SFmpq.MpqOpenArchiveForUpdate(ut.u2b(fname), flag, 1024)
        if not ret:
            return False

        self.mpqh = ret
        return True

    def Close(self):
        if not self.mpqh:
            return None

        # Close archive
        ret = SFmpq.MpqCloseUpdatedArchive(self.mpqh, 0)
        if not ret:
            return False

        self.mpqh = None
        self.flist = None
        return True

    def PutFile(self, fname, buffer, replace=True):
        if not self.mpqh:
            return None

        # Replace file if existing
        flag = MAFA_ENCRYPT | MAFA_COMPRESS
        if replace:
            flag |= MAFA_REPLACE_EXISTING
        cmptype = MAFA_COMPRESS_STANDARD

        ret = SFmpq.MpqAddFileFromBufferEx(
            self.mpqh, buffer, len(buffer), ut.u2b(fname), flag, cmptype, 0)
        return bool(ret)

    def PutWave(self, fname, buffer, complev=WAVCOMP_LOWQUALITY, replace=True):
        if not self.mpqh:
            return None

        cmplevel = WaveCmpDict.get(complev, MAWA_QUALITY_HIGH)
        if cmplevel == -1:
            self.PutFile(fname, buffer)

        flag = MAFA_ENCRYPT | MAFA_COMPRESS
        if replace:
            flag |= MAFA_REPLACE_EXISTING

        ret = SFmpq.MpqAddWaveFromBuffer(
            self.mpqh, buffer, len(buffer), ut.u2b(fname), flag, cmplevel)
        return bool(ret)

    def DeleteFile(self, fname):
        if not self.mpqh:
            return None

        ret = SFmpq.MpqDeleteFile(self.mpqh, ut.u2b(fname))
        return bool(ret)

    def Compact(self):
        if not self.mpqh:
            return None

        ret = SFmpq.MpqCompactArchive(self.mpqh)
        return bool(ret)


if not InitMpqLibrary():
    raise ut.EPError("Cannot load SFmpq.dll. SFmpq not initalized")
