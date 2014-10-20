# !/usr/bin/python
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
Unicode(python) <-> Binary(starcraft) conversion. Used internally in eudtrg.
'''

 

charset = 'cp949'  # default : korean


def UbconvUseCharset(newencoding):
    global charset
    charset = newencoding


def Unicode2Bytes(string):
    if isinstance(string, bytes):
        return string

    elif isinstance(string, str):
        return string.encode(charset)

    else:
        raise TypeError(
            'Unknown type %s given to Unicode2Bytes' % type(string))


def Bytes2Unicode(b):
    if isinstance(b, str):
        return b

    elif isinstance(b, bytes):
        return b.decode(charset)

    else:
        raise TypeError('Unknown type %s given to Bytes2Unicode' % type(b))


def main():
    print("Performing unicode - multibyte conversion library")

if __name__ == "__main__":
    main()

# shorter names
u2b = Unicode2Bytes
b2u = Bytes2Unicode
