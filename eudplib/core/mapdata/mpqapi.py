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
from ctypes import *
import os, sys, struct, platform
from tempfile import NamedTemporaryFile
from eudplib.utils import u2b, b2u


filename_u2b = None


# Constants
MPQ_FILE_COMPRESS = 0x00000200
MPQ_FILE_ENCRYPTED = 0x00010000
MPQ_FILE_FIX_KEY = 0x00020000
MPQ_FILE_REPLACEEXISTING = 0x80000000

MPQ_WAVE_QUALITY_MEDIUM = 0x1

# Logic
ffi = FFI()

ffi.cdef("""
typedef void *HANDLE, *LPOVERLAPPED;
typedef unsigned int DWORD, BOOL;
typedef unsigned short WORD;
typedef unsigned char BYTE;

BOOL WINAPI SFileOpenArchive(const char*, DWORD, DWORD, HANDLE*);
BOOL WINAPI SFileCompactArchive(HANDLE, const char*, BOOL);
BOOL WINAPI SFileCloseArchive(HANDLE);
BOOL WINAPI SFileOpenFileEx(HANDLE, const char*, DWORD, HANDLE*);
DWORD WINAPI SFileGetFileSize(HANDLE, DWORD*);
BOOL WINAPI SFileReadFile(HANDLE, VOID*, DWORD, DWORD*, LPOVERLAPPED);
BOOL WINAPI SFileCloseFile(HANDLE);
BOOL WINAPI SFileAddFile(HANDLE, const char*, const char*, DWORD);
BOOL WINAPI SFileAddWave(HANDLE, const char*, const char*, DWORD, DWORD);

""")


libstorm = None


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


def InitMpqLibrary():
    global libstorm, filename_u2b

    try:
        platformName = platform.system()
        if platformName == 'Windows':  # windows
            if struct.calcsize("P") == 4:  # 32bit
                libstorm = ffi.dlopen(find_data_file('StormLib32.dll'))
            else:  # 64bit
                libstorm = ffi.dlopen(find_data_file('StormLib64.dll'))
            filename_u2b = u2b

        elif platformName == 'Darwin':  # mac
            try:
                libstorm = ffi.dlopen('libstorm.dylib')
                filename_u2b = (lambda x: x.encode('utf-8'))
            except OSError:
                print('You need to install stormlib before using eudplib.')
                print(' $ brew install homebrew/games/stormlib')
                return False

        return True

    except OSError:
        print('Loading SFmpq failed.')
        libstorm = None
        return False


class MPQ:
    def __init__(self):
        self.mpqh = None
        self.libstorm = libstorm

    def __del__(self):
        self.Close()

    def Open(self, fname):
        if self.mpqh is not None:
            raise RuntimeError('Duplicate opening')

        h = ffi.new("HANDLE*")
        ret = self.libstorm.SFileOpenArchive(filename_u2b(fname), 0, 0, h)
        if not ret:
            self.mpqh = None
            return False

        self.mpqh = h[0]
        return True

    def Close(self):
        if self.mpqh is None:
            return None

        self.libstorm.SFileCloseArchive(self.mpqh)
        self.mpqh = None
        return True

    def EnumFiles(self):
        # using listfile.
        lst = self.Extract('(listfile)')
        if lst is None:
            return []

        return b2u(lst).replace('\r', '').split('\n')

    # Extract
    def Extract(self, fname):
        if self.libstorm is None:
            return None
        elif not self.mpqh:
            return None

        # Open file
        fileh = ffi.new("HANDLE*")
        ret = self.libstorm.SFileOpenFileEx(
            self.mpqh,
            u2b(fname),
            0,
            fileh
        )
        if not ret:
            return None
        fileh = fileh[0]

        # Get file size & allocate buffer
        # Note : this version only supports 32bit mpq file
        fsize = self.libstorm.SFileGetFileSize(fileh, ffi.NULL)
        fdata = ffi.new("BYTE[]", fsize)

        # Read file
        pfread = ffi.new("DWORD*")
        self.libstorm.SFileReadFile(fileh, fdata, fsize, pfread, ffi.NULL)
        self.libstorm.SFileCloseFile(fileh)

        if pfread[0] == fsize:
            return ffi.buffer(fdata)[:]
        else:
            return None

    # Writer

    def PutFile(self, fname, buffer):
        if not self.mpqh:
            return None

        # Create temporary file
        f = NamedTemporaryFile(delete=False)
        f.write(buffer)
        tmpfname = f.name
        f.close()

        # Add to mpq
        ret = self.libstorm.SFileAddFile(
            self.mpqh,
            filename_u2b(tmpfname),
            u2b(fname),
            MPQ_FILE_COMPRESS | MPQ_FILE_ENCRYPTED | MPQ_FILE_REPLACEEXISTING,
        )
        os.unlink(tmpfname)
        return ret

    def PutWave(self, fname, buffer):
        if not self.mpqh:
            return None

        # Create temporary file
        f = NamedTemporaryFile(delete=False)
        f.write(buffer)
        tmpfname = f.name
        f.close()

        # Add to mpq
        ret = self.libstorm.SFileAddWave(
            self.mpqh,
            filename_u2b(tmpfname),
            u2b(fname),
            MPQ_FILE_COMPRESS | MPQ_FILE_ENCRYPTED | MPQ_FILE_FIX_KEY,
            MPQ_WAVE_QUALITY_MEDIUM
        )
        os.unlink(tmpfname)
        return ret

    def Compact(self):
        self.libstorm.SFileCompactArchive(self.mpqh, ffi.NULL, 0)


InitMpqLibrary()

if __name__ == '__main__':
    mr = MPQ()
    mr.Open('basemap.scx')
    a = mr.Extract('staredit\\scenario.chk')
    mr.Close()
    print(len(a))

    if os.path.exists('test.scx'):
        os.unlink('test.scx')
    open('test.scx', 'wb').write(open('basemap.scx', 'rb').read())

    mr.Open('test.scx')
    a = mr.Extract('staredit\\scenario.chk')
    print(len(a))
    mr.PutFile('test', b'1234')
    b = mr.Extract('test')
    mr.Compact()
    print(b)
