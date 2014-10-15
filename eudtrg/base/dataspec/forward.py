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


from .expr import Expr, Evaluate


class Forward(Expr):

    '''
    Forward declaration for expressions. Example::

        b = Forward() # Forward declaration
        a = Trigger( nextptr = b ) # b is defined here, so no error occurs.
        b << Trigger( nextptr = a ) # put in value later.

    Forward() class can be assigned a value only once.
    '''

    def __init__(self):
        super().__init__()
        self.target = None
        self._ct = None

    def __lshift__(self, item):
        return self.Assign(item)

    def Assign(self, item):
        '''
        Assign expression to self. The object will evaluate to assigned
        expressions afterwards.

        :raises AssertionError:
            - Forward has already been assigned.
            - Non-expression types are being assigned into.
        '''
        assert isinstance(
            item, Expr), 'Non-expr types cannot be assigned to Forward object.'
        assert self.target is None, 'Duplicate assignment'
        self.target = item
        return item

    def ForwardEmpty(self):
        return self.target is None

    def GetDependencyList(self):
        return [self.target]

    def EvalImpl(self):
        '''
        :raises AssertionError: Forward hasn't been assigned to any values by
            :meth:`Assign`.
        '''
        assert self.target is not None, (
            'Forward has not been properly initalized')
        return Evaluate(self.target)
