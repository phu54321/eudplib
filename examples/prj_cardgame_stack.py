#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
스택(Stack) 규칙

1. 카드는 다음 순서와 같이 강함이 정의된다.
> ♠A  > ♥A  > ♦A  > ♣A
> ♠K  > ♥K  > ♦K  > ♣K
> ♠Q  > ♥Q  > ♦Q  > ♣Q
> ♠J  > ♥J  > ♦J  > ♣J
> ♠10 > ♥10 > ♦10 > ♣10
> ♠9  > ♥9  > ♦9  > ♣9
> ♠8  > ♥8  > ♦8  > ♣8
> ♠7  > ♥7  > ♦7  > ♣7
> ♠6  > ♥6  > ♦6  > ♣6
> ♠5  > ♥5  > ♦5  > ♣5
> ♠4  > ♥4  > ♦4  > ♣4
> ♠3  > ♥3  > ♦3  > ♣3
> ♠2  > ♥2  > ♦2  > ♣2


즉, 스페이드 A는 클로버 10보다 강하다.


2. 트럼프 52장 (AKQJ10987654321 * (스페이드 하트 다이아몬드 클로버), 총 52장의 카드로 플레이한다.
 플레이어 수는 2~6명.

3. 게임 시작할 때 각 플레이어들에게 7장의 카드씩을 배분한다. 남는 카드는 모아서 뒤집어서 덮어놓는다. 이것을 덱이라 한다.

4. 각 라운드는 다음과 같이 진행한다.
  4-1 :​ 덱에서 카드 한장을 뽑아서 오픈(앞면이 보이게 둠)한다.

  4-2 : 각 플레이어마다
     1) 오픈된 마지막 카드보다 더 강한 카드를 내던가(새로 오픈)
        cf) 오픈된 마지막 카드가 A이면 그 카드보다 더 강한 A를 내거나 A가 아닌 카드를 아무거나 낼 수 있음

     2) 지금까지 오픈된 카드 숫자를 N이라 할 때
          N이 홀수면 (N + 1) / 2장을
          N이 짝수면 N / 2 장을
        덱에서 뽑은 다음, 지금까지 오픈된 모든 카드들을 덮어서 따로 모아둔다 (덱2라고 하자). 새로운 라운드를 다시 시작한다.
        새로운 라운드는 다음 플레이이어부터 시작한다.

  4-3 : 4-2를 라운드가 끝날때까지 반복한다.


5. 라운드 진행 중에 예외사항
   5-1 : 덱에 카드가 없는데 덱에서 카드를 뽑아야 할 경우
      5-1-1 : 4-1 에 따라서 덱에서 카드를 뽑아야 할 경우
          1) 지금까지 덱2에 쌓인 카드들을 섞어서 덱으로 옮기고 덱에서 옮긴다.
          2) 덱2가 원래 비었으면 각 플레이어는 카드를 자유롭게 하나씩 버릴 수 있다. 버린 카드들을 섞어 덱을 구성해서 게임을 진행한다.

      5-1-2: 4-2-2)에 따라서 덱에서 카드를 뽑아야 할 경우
          1) 일단 이미 있던 덱에서 최대한 카드를 뽑고, 해당 라운드에서 오픈되지 않았던 덱2의 카드들을 섞어서 덱으로 옮긴다.
         해당 라운드에서 오픈됬던 카드를 덱2로 삼는다. 즉, 해당 라운드에서 오픈됬던 카드는 3-2-2) 과정에서 뽑을 수 없다.
          2) 남아있던 덱과 이미 있던 덱 2의 카드를 합쳐서도 카드 갯수가 부족하면 이미 있던 덱2의 카드들을 모두 뽑은 다음에
         해당 라운드에서 오픈됬던 카드를로 덱을 재구성해서 카드를 뽑는다.

   5-2 : 어느 한 사람이 카드를 모두 소비했을 경우
      - 그 사람은 이긴 것으로 치며, 게임에서 빠진다.

6. 기타 규칙
  - 카드가 1장 남아있고 그 1장이 조커일 때, 조커를 라운드에서 낼 수 없다. (조커를 맨 마지막 카드로 낼 수 없습니다)
  - 스페이드 2, 하트 2, 다이아몬드 2, 클로버 2를 모두 모은 사람은 게임에서 즉시 이긴다. (2 포카드 규칙)


  *) 잘 일어나지 않는 일은 회색으로 표시했습니다.
"""

import sys
import os

sys.path.insert(0, os.path.abspath('..\\'))
from eudplib import *

# Global variable : card deck
deck1 = EUDArray(53)
deck2 = EUDArray(53)


def ShuffleArray(arr, n):
    i = EUDVariable()
    t = EUDVariable()
    i << 0

    if EUDWhile(i < n):
        j = i + f_div(f_rand(), n - i)[1]
        t << arr.get(i)
        arr.set(i, arr.get(j))
        arr.set(j, t)
        i << i + 1
    EUDEndWhile()


@EUDFunc
def InitDecks():
    for i in range(53):
        deck1.set(i, i)

    for i in range(53):
        deck2.set(i, 0xFFFFFFFF)

    ShuffleArray(deck1, 53)


@EUDFunc
def PopDeck():
    if EUDIf(deck1.get(0) == 0xFFFFFFFF):  # deck empty 5-1-1
        # copy deck2 to deck1
        deck2n = EUDVariable()
        deck2n << 0
        for i in range(53):
            card = deck2.get(i)
            EUDBreakIf(card == 0xFFFFFFFF)
            deck1.set(i, card)
            deck2n += 1

        if EUDIf(deck2n == 0):  # so sad
            # query each player to drop cards
            DoActions([
                (
                    SetCurrentPlayer(player),
                    DisplayExtText(SCMD2Text('''\
<0F>Rule 5-1-1 2) <04>덱, 덱2가 비었습니다.
<17>카드 한장씩을 버려주십시오.'''))
                ) for player in range(8)
            ])

            for player in range(8):
                if EUDIf(IsPlayerPlaying(player)):
                    QueuePlayerDraw(player)
                EUDEndIf()

            if EUDInfLoop():
                flag = EUDVariable()
                flag << 0
                for player in range(8):
                    if EUDIfNot([IsPlayerPlaying(player), HasPlayerDrawn(player)]):
                        flag << 1
                    EUDEndIf()
                EUDBreakIf(flag == 0)
            EUDEndInfLoop()

        if EUDElse():
            DoActions([
                (
                    SetCurrentPlayer(player),
                    DisplayExtText(SCMD2Text('''\
<0F>Rule 5-1-1 1) <04>덱이 비워졌으므로 덱2에서 보충합니다.'''))
                ) for player in range(8)
            ])
        EUDEndIf()
    EUDEndIf()

    ret = deck1.get(0)
    for i in range(52):
        deck1.set(i, deck1.get(i + 1))
    deck1.set(52, 0xFFFFFFFF)  # no card
    return ret


def main():
    if EUDInfLoop():
        PrepareDeck()
        EUDDoEvents()
    EUDEndInfLoop()


LoadMap('basemap/basemap_stack.scx')
# CompressPayload(True)
SaveMap('outputmap/Card Game [Stack].scx', main)
