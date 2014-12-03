#!/usr/bin/python
#-*- coding: utf-8 -*-

import locale

g_encoding = locale.getpreferredencoding()


def UbconvSetEncoding(encoding):
    global g_encoding
    g_encoding = encoding


def u2b(s):
    return s.encode(g_encoding)


def b2u(b):
    return b.decode(g_encoding)
