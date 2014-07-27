'''
약간 복잡한 트리거 예제입니다.

 - P1는 a->b->c->d->e->f->g->h 순서대로
 - P23456은 a->e->f->g 순서대로

다음과 같이 짜려고 합니다.

a ->
    [P1 전용]
    b -> c -> d ->
e -> f -> g ->
    [P1 전용]
    h

이번 예제부터 EUDJumpIf같은 이상한게 등장할겁니다.
'''

from eudtrglib import *

currentplayer = 0x006509B0 # Current Player 값은 여기 오프셋에 저장되어있습니다.
# ex5.py처럼 짜기 싫으시면 이 오프셋을 쓰셔야 합니다.

LoadMap("basemap.scx")


pstart = NextTrigger()


Trigger( actions = [DisplayText('Trigger A')] )


block1end = Forward()
EUDJumpIfNot( [Memory(currentplayer, Exactly, 0)], block1end ) # Current Player가 P1(0)이 아니면 block1end로 갑니다.
Trigger( actions = [DisplayText('Trigger B')] )
Trigger( actions = [DisplayText('Trigger C')] )
Trigger( actions = [DisplayText('Trigger D')] )
block1end << NextTrigger() # block1end는 다음 트리거(Next Trigger)를 나타냅니다. (트리거 E)


Trigger( actions = [DisplayText('Trigger E')] )
Trigger( actions = [DisplayText('Trigger F')] )
Trigger( actions = [DisplayText('Trigger G')] )


block2end = Forward()
EUDJumpIfNot( [Memory(currentplayer, Exactly, 0)], block2end) # Current Player가 P1(0)가 아니면 block2end로 갑니다.
Trigger( actions = [DisplayText('Trigger H')] )
block2end << NextTrigger() # block2end는 다음 트리거(Next Trigger)를 나타냅니다. (트리거 I)


Trigger( nextptr = triggerend ) # 트리거 I



psw = InitPlayerSwitch([
    pstart, pstart, pstart, pstart, pstart, pstart, None, None
]) # pstart 리스트에 주어진대로 각 플레이어의 시작 트리거 설정.


SaveMap("ex7.scx", psw)


# 결과는 ex6과 동일합니다.