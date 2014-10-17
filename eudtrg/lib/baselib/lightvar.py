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


from eudtrg import base as b


class EUDLightVariable:

    '''
    Light variable. EUDLightVariable occupies only 4 bytes.
    '''

    def __init__(self):
        self._memory = b.Db(b'\0\0\0\0')

    def GetMemoryAddr(self):
        '''
        :returns: Memory address where values are stored.
        '''
        return self._memory

    def AtLeast(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at least
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.AtLeast, number)

    def AtMost(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at most
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.AtMost, number)

    def Exactly(self, number):
        '''
        :param number: Number to compare variable with.
        :returns: :class:`Condition` for checking if the variable is at exactly
            given number.
        '''
        return b.Memory(self.GetMemoryAddr(), b.Exactly, number)

    def SetNumber(self, number):
        '''
        :param number: Number to assign.
        :returns: :class:`Action` for assigning given number to variable.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.SetTo, number)

    def AddNumber(self, number):
        '''
        :param number: Number to add.
        :returns: :class:`Action` for adding given number to variable.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.Add, number)

    def SubtractNumber(self, number):
        '''
        :param number: Number to subtract.
        :returns: :class:`Action` for subtracting given number to variable.

        .. warning::
            Subtraction won't underflow. Subtracting values with bigger one
            will yield 0.
        '''
        return b.SetMemory(self.GetMemoryAddr(), b.Subtract, number)
