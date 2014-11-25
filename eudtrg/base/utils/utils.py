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
Useful utilities. You may freely use these functions.
'''


def EPD(offset):
    '''
    Offset to EPD player.
    '''
    return (offset - 0x0058A364) // 4


'''
Nested list / Single item -> Flat list
 ex) FlattenList([a, [b, c], d]) -> [a, b, c, d]
 ex) FlattenList([a, b, c])      -> [a, b, c]
 ex) FlattenList(a)              -> [a]
'''


def FlattenList(l):
    try:
        ret = []
        for item in l:
            ret.extend(FlattenList(item))
        return ret

    except TypeError:  # l is not iterable
        return [l]


'''
Parses SCMDraft2 style text message
'''


def SCM2Text(s):
    #
    # normal -> xdigitinput1 -> xdigitinput2 -> xdigitinput3 -> normal
    #        '<'           xdigit          xdigit            '>'
    #                        -> normal
    #                       '>' emit '<>'
    #                                        -> normal
    #                                        '>' emit x00
    #                                                        -> normal
    # xdigit/normal  emit '<xx'
    def toxdigit(i):
        if '0' <= i <= '9':
            return ord(i) - 48
        elif 'a' <= i <= 'z':
            return ord(i) - 97 + 10
        elif 'A' <= i <= 'Z':
            return ord(i) - 65 + 10
        else:
            return None

    state = 0
    buf = [None, None]
    bufch = [None, None]
    out = []

    # simple fsm
    for i in s:
        if state == 0:
            if i == '<':
                state = 1
            else:
                out.append(i)

        elif state == 1:
            xdi = toxdigit(i)
            if xdi is not None:
                buf[0] = xdi
                bufch[0] = i
                state = 2

            else:
                out.extend(['<', i])
                state = 0

        elif state == 2:
            xdi = toxdigit(i)
            if xdi is not None:
                buf[1] = xdi
                bufch[1] = i
                state = 3

            elif i == '>':
                out.append(chr(buf[0]))
                state = 0

            else:
                out.extend(['<', bufch[0], i])
                state = 0

        elif state == 3:
            if i == '>':
                out.append(chr(buf[0] * 16 + buf[1]))
                state = 0

            else:
                out.extend(['<', bufch[0], bufch[1], i])
                state = 0

    return ''.join(out)


'''
To support syntax like this:
 a = f(1)     # f(1) returns 1 (not [1])
 a,b = f(2)   # f(2) returns [1,2]
 a,b,c = f(3) # f(3) returns [1,2,3]
'''


def List2Assignable(l):
    if len(l) == 1:
        return l[0]

    else:
        return l


def Assignable2List(a):
    if a is None:
        return []

    elif hasattr(a, '__iter__'):
        return list(a)

    else:
        return [a]
