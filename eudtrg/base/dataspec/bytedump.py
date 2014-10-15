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
Defines Db class for uploading arbitary bytes data on SC memory.
'''

from .eudobj import EUDObject


class Db(EUDObject):

    '''
    Db object inserts binary data into starcraft memory. Db object evaluates to
    address where bytes are stored.
    '''

    def __init__(self, content):
        '''
        :param bytes content: Content to put in.
        '''
        super(Db, self).__init__()

        # convert & store
        content = bytes(content)
        self._content = content

    def GetDataSize(self):
        return len(self._content)

    def GetDependencyList(self):
        return []

    def WritePayload(self, buf):
        buf.EmitBytes(self._content)
