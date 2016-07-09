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

from .rlocint import RlocInt
from ... import utils as ut


class ConstExpr:

    """ 컴파일할 때 알 수 있는 값을 나타내는 클래스입니다.
    """

    def __init__(self, baseobj, offset=0, rlocmode=4):
        """ 생성자입니다.

        모든 ConstExpr 객체는 기준이 되는 객체와 그 객체로부터 얼마나 떨어져
        있는지를 이용해서 계산합니다. 예를 들어서 트리거의 주소를 값으로 하는
        ConstExpr는 해당 트리거를 baseobj로, offset은 0이 됩니다.

        rlocmode는 EUD 트리거때문에 생긴 겁니다. rlocmode가 1이면 baseobj // 4
        의 값이 계산됩니다.

        :param baseobj: ConstExpr 계산에서 기준이 되는 값입니다.
        :param offset: ConstExpr의 값이 baseobj로부터 얼마나 떨어져있는지를
            나타냅니다.
        :param rlocmode: 내부적으로 쓰는 값입니다. rlocmode에 따라 ConstExpr의
            계산법이 달라집니다. 자세한건 :method:`Evaluate` 를 참고하세요.
        """
        self.baseobj = baseobj
        self.offset = offset
        self.rlocmode = rlocmode

    def Evaluate(self):
        """ ConstExpr 값을 RlocInt로 계산하는 함수입니다.

        계산식은 다음과 같습니다. :

            return Evaluate(self.baseobj) * self.rlocmode // 4 + self.offset

        :return: 계산 결과
        """
        return Evaluate(self.baseobj) * self.rlocmode // 4 + self.offset

    def __add__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return ConstExpr(self.baseobj, self.offset + other, self.rlocmode)

    def __radd__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return ConstExpr(self.baseobj, self.offset + other, self.rlocmode)

    def __sub__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        if isinstance(other, ConstExpr):
            ut.ep_assert(
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode,
                'Cannot subtract between addresses btw two objects'
            )
            return self.offset - other.offset

        else:
            return ConstExpr(self.baseobj, self.offset - other, self.rlocmode)

    def __rsub__(self, other):
        if isinstance(other, ConstExpr):
            ut.ep_assert(
                self.baseobj == other.baseobj and
                self.rlocmode == other.rlocmode,
                'Cannot subtract between addresses btw two distinct objects'
            )
            return other.offset - self.offset

        elif not isinstance(other, int):
            return NotImplemented

        else:
            return ConstExpr(self.baseobj, other - self.offset, -self.rlocmode)

    def __mul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return ConstExpr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __rmul__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        return ConstExpr(self.baseobj, self.offset * k, self.rlocmode * k)

    def __floordiv__(self, k):
        if not isinstance(k, int):
            return NotImplemented
        ut.ep_assert(
            (self.rlocmode == 0) or
            (self.rlocmode % k == 0 and self.offset % k == 0),
            'Address not divisible'
        )
        return ConstExpr(self.baseobj, self.offset // k, self.rlocmode // k)


class Forward(ConstExpr):

    """ 전방 선언(Forward Declaration)을 위한 클래스입니다.

    eudplib 코드에서 객체들이 서로를 참조하는 경우가 있습니다. 예를 들어
    반복문에서는 반복문의 시작 트리거 A와 반복문의 끝 트리거 B가 서로를
    가르킬 수 있겠죠. 이 때 A와 B의 생성자에서 각각 B와 A가 필요할 수
    있습니다. 이런 식으로 순환 참조가 필요할 경우, :

        A = Forward()
        B = RawTrigger(nextptr=A)
        A << RawTrigger(nextptr=B)

    처럼 ``Forward`` 객체를 이용해 순환 참조를 깰 수 있습니다.
    """

    def __init__(self):
        super().__init__(self)
        self._expr = None

    def __lshift__(self, expr):
        """ Forward에 해당하는 값을 직접 대응시켜줍니다. """

        ut.ep_assert(
            self._expr is None,
            'Reforwarding without reset is not allowed'
        )
        ut.ep_assert(expr is not None, 'Cannot forward to None')
        self._expr = expr
        return expr

    def IsSet(self):
        """ Forward에 값이 설정되었는지를 알아봅니다. """
        return self._expr is not None

    def Reset(self):
        """ Forward에 대응되는 값을 해제시킵니다. """
        self._expr = None

    def Evaluate(self):
        ut.ep_assert(self._expr is not None, 'Forward not initialized')
        return Evaluate(self._expr)


def Evaluate(x):
    """ int나 ConstExpr 값을 실제로 계산합니다. """
    if isinstance(x, int):
        return RlocInt(x, 0)
    try:
        return x.Evaluate()
    except AttributeError:
        return x


def IsConstExpr(x):
    """ 객체가 ConstExpr인지 알아봅니다. """
    x = ut.unProxy(x)
    return isinstance(x, int) or hasattr(x, 'Evaluate')
