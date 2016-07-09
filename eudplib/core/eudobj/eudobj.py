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

from ..allocator import ConstExpr
from ..allocator.payload import GetObjectAddr
from eudplib import utils as ut


class EUDObject(ConstExpr):

    """
    스타크래프트 메모리에서 올라가는 독립적인 객체를 정의합니다.

    .. note::
        EUDObject들이 스타크래프트 메모리로 올라가기 위해서는 먼저 맵에 쓰이는
        모든 EUDObject들을 하나의 큰 메모리 덩어리로 만들 필요가 있습니다. 이
        과정을 페이로드 생성이라고 합니다. 이 과정은 3단계로 이루어집니다.

        - 객체 수집 단계 : 맵에 쓰이는 모든 EUDObject를 모읍니다. 이 과정에서
            :method:`Evaluate` , :method:`WritePayload` 가 쓰입니다.
        - 주소 할당 단계 : 각 EUDObject에 주소를 할당합니다. 이 과정에서
            :method:`GetDataSize` , :method:`Evaluate` , :method:`WritePayload`
            가 쓰입니다.
        - 페이로드 생성 단계 : 각 EUDObject의 주소에 따라서 EUDObject의 내용을
            씁니다. :method:`GetDataSize` , :method:`WritePayload` 와
            :method:`Evaluate` 가 쓰입니다.
    """

    def __init__(self):
        super().__init__(self)

    def DynamicConstructed(self):
        """ 동적 생성 객체인지를 판단합니다. 기본값은 False입니다.

        맵에 쓰이는 객체들의 종류에 따라 내용물이 달라지는 객체인지를 봅니다.
        예를 들어 모든 생성된 트리거의 오프셋을 모아놓는 객체가 있다면, 이
        객체의 크기나 데이터는 실제로 생성된 트리거의 갯수에 따라 달라집니다.

        동적 생성 객체인 경우 객체 수집 단계에서 객체의 내용물과 크기가
        확정되어야 합니다.
        """
        return False

    def Evaluate(self):
        """ 이 객체가 ConstExpr로 쓰였을 때 의미하는 값입니다.

        :return: 기본값으로 객체의 주소가 나옵니다.

        .. note::
             이 메소드를 오버라이드할 때 func:`GetObjectAddr` 를 쓸 수
             있습니다.
        """
        return GetObjectAddr(self)

    def GetDataSize(self):
        """ 객체의 메모리 크기  """
        raise ut.EPError('Override')

    def WritePayload(self, pbuffer):
        """ 객체 내용물을 pbuffer에 씁니다. """
        raise ut.EPError('Override')
