 #!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 trgk

# This software is provided 'as-is', without any express or implied
# warranty. In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:

#    1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
#    2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
#    3. This notice may not be removed or altered from any source
#    distribution.
#
# See eudtrg.LICENSE for more info


'''
SFmpq.dll wrapper. Used internally inside eudtrg.
'''

from ctypes import *  # @UnusedWildImport
from ..utils.ubconv import u2b


import sys
import os

"""
find where sfmpq.dll is.
"""


def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


# These can be an argument to for MpqWrite.PutWave
WAVCOMP_NOCOMPRESSION = 0
WAVCOMP_HIGHQUALITY = 1
WAVCOMP_MIDQUALITY = 2
WAVCOMP_LOWQUALITY = 3

SFmpq = None


def InitMpqLibrary():
    global SFmpq

    try:
        SFmpq = WinDLL(find_data_file('SFmpq.dll'))

        # for MpqRead
        # BOOL      SFMPQAPI WINAPI SFileOpenArchive(LPCSTR lpFileName, DWORD dwPriority, DWORD dwFlags, MPQHANDLE *hMPQ);
        # BOOL      SFMPQAPI WINAPI SFileCloseArchive(MPQHANDLE hMPQ);
        # BOOL      SFMPQAPI WINAPI SFileOpenFileEx(MPQHANDLE hMPQ, LPCSTR lpFileName, DWORD dwSearchScope, MPQHANDLE *hFile);
        # DWORD     SFMPQAPI WINAPI SFileGetFileSize(MPQHANDLE hFile, LPDWORD lpFileSizeHigh);
        # BOOL      SFMPQAPI WINAPI SFileReadFile(MPQHANDLE hFile,LPVOID lpBuffer,DWORD nNumberOfBytesToRead,LPDWORD lpNumberOfBytesRead,LPOVERLAPPED lpOverlapped);
        # BOOL      SFMPQAPI WINAPI SFileCloseFile(MPQHANDLE hFile);

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
        # MPQHANDLE SFMPQAPI WINAPI MpqOpenArchiveForUpdate(LPCSTR lpFileName, DWORD dwFlags, DWORD dwMaximumFilesInArchive);
        # BOOL      SFMPQAPI WINAPI MpqAddFileFromBuffer(MPQHANDLE hMPQ, LPVOID lpBuffer, DWORD dwLength, LPCSTR lpFileName, DWORD dwFlags, DWORD dwCompressionType, DWORD dwCompressLevel);
        # BOOL      SFMPQAPI WINAPI MpqAddWaveFromBuffer(MPQHANDLE hMPQ, LPVOID lpBuffer, DWORD dwLength, LPCSTR lpFileName, DWORD dwFlags, DWORD dwQuality);
        # BOOL      SFMPQAPI WINAPI MpqRenameFile(MPQHANDLE hMPQ, LPCSTR lpcOldFileName, LPCSTR lpcNewFileName);
        # BOOL      SFMPQAPI WINAPI MpqDeleteFile(MPQHANDLE hMPQ, LPCSTR lpFileName);
        # DWORD     SFMPQAPI WINAPI MpqCloseUpdatedArchive(MPQHANDLE hMPQ, DWORD dwUnknown2);
        # BOOL      SFMPQAPI WINAPI MpqCompactArchive(MPQHANDLE hMPQ);

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
        print('Loading SFmpq failed. '
              'If you are using 64bit python, change to 32bit one.')
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
            raise RuntimeError("double open")

        h = c_int()
        ret = self.SFmpq.SFileOpenArchive(u2b(fname), 0, 0, byref(h))
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

        return lst.replace('\n', '').split('\r\n')

    def Extract(self, fname):
        if self.mpqh is None:
            return None

        # Open file
        fileh = c_int()
        ret = self.SFmpq.SFileOpenFileEx(
            self.mpqh, u2b(fname), 0, byref(fileh))
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
            assert readbyte.value <= readleft
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
            raise RuntimeError("double open")

        if preserve_content:
            flag = MOAU_OPEN_ALWAYS | MOAU_MAINTAIN_LISTFILE
        else:
            flag = MOAU_CREATE_ALWAYS | MOAU_MAINTAIN_LISTFILE

        ret = SFmpq.MpqOpenArchiveForUpdate(u2b(fname), flag, 1024)
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

    def PutFile(self, fname, buffer):
        if not self.mpqh:
            return None

        # Replace file if existing
        flag = MAFA_ENCRYPT | MAFA_COMPRESS | MAFA_REPLACE_EXISTING
        cmptype = MAFA_COMPRESS_STANDARD

        ret = SFmpq.MpqAddFileFromBufferEx(
            self.mpqh, buffer, len(buffer), u2b(fname), flag, cmptype, 0)
        if not ret:
            return False

        return True

    def PutWave(self, fname, buffer, complev=WAVCOMP_LOWQUALITY):
        if not self.mpqh:
            return None

        cmplevel = WaveCmpDict.get(complev, MAWA_QUALITY_HIGH)
        if cmplevel == -1:
            self.PutFile(fname, buffer)

        flag = MAFA_ENCRYPT | MAFA_COMPRESS | MAFA_REPLACE_EXISTING

        ret = SFmpq.MpqAddWaveFromBuffer(
            self.mpqh, buffer, len(buffer), u2b(fname), flag, cmplevel)
        if not ret:
            return False
        return True

    def Compact(self):
        if not self.mpqh:
            return None

        ret = SFmpq.MpqCompactArchive(self.mpqh)
        if not ret:
            return False
        return True


if not InitMpqLibrary():
    raise RuntimeError("Cannot load SFmpq.dll. SFmpq not initalized")


def main():
    print("Testing MPQAPI...")

    origcontent = u2b("abababababab")

    mw = MpqWrite()
    mw.Open("test.mpq", False)

    mw.PutFile("test1.txt", origcontent)
    mw.Close()

    mr = MpqRead()
    mr.Open("test.mpq")
    f = mr.Extract("test1.txt")
    mr.Close()

    mr.Open("")
    f2 = mr.Extract("mpqapi.py")
    mr.Close()

    print(f, origcontent, f2)
    print(f == origcontent)


if __name__ == "__main__":
    main()
