#!/usr/bin/python
# -*- coding: utf-8 -*-

import locale

g_encoding = locale.getpreferredencoding()


def UbconvSetEncoding(encoding):
    global g_encoding
    g_encoding = encoding


def u2b(s):
    if isinstance(s, str):
        return s.encode(g_encoding)
    elif isinstance(s, int):
        raise TypeError('Invalid type %s' % type(s))
    else:
        return bytes(s)


def b2u(b):
    if isinstance(b, bytes):
        return b.decode(g_encoding)
    elif isinstance(b, int):
        raise TypeError('Invalid type %s' % type(b))
    else:
        return str(b)
