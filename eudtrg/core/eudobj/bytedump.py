#!/usr/bin/python
#-*- coding: utf-8 -*-

from .eudobj import EUDObject


class Db(EUDObject):

    def __init__(self, b):
        super().__init__()
        self.content = bytes(b)

    def GetDataSize(self):
        return len(self.content)

    def WritePayload(self, pbuffer):
        pbuffer.WriteBytes(self.content)
