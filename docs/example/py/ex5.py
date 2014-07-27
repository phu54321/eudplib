'''
약간 복잡한 트리거 예제입니다.

 - P1는 a->b->c->d->e->f->g->h 순서대로
 - P23456은 a->e->f->g 순서대로

먼저 스타가 트리거를 다루는 방식대로 eudtrg에서 트리거를 만들면 다음과 같습니다.
'''

from eudtrglib import *

LoadMap("basemap.scx")

# P1의 트리거 생성

pstart = [None] * 8 # None 8개가 들어있는 리스트 생성

if 1:
    a = Forward()
    b = Forward()
    c = Forward()
    d = Forward()
    e = Forward()
    f = Forward()
    g = Forward()
    h = Forward()


    a << Trigger(nextptr = b, actions = [ DisplayText('Trigger A') ])
    b << Trigger(nextptr = c, actions = [ DisplayText('Trigger B') ])
    c << Trigger(nextptr = d, actions = [ DisplayText('Trigger C') ])
    d << Trigger(nextptr = e, actions = [ DisplayText('Trigger D') ])
    e << Trigger(nextptr = f, actions = [ DisplayText('Trigger E') ])
    f << Trigger(nextptr = g, actions = [ DisplayText('Trigger F') ])
    g << Trigger(nextptr = h, actions = [ DisplayText('Trigger G') ])
    h << Trigger(nextptr = triggerend, actions = [ DisplayText('Trigger H') ])
    

    pstart[0] = a # P1(0)의 시작 트리거는 위에서 정의된 a 트리거.



# P2 ~ P6의 트리거 생성 
for i in range(1, 6): # P2~P6 (1~5) 까지 i를 반복시킵니다.
    a = Forward()
    e = Forward()
    f = Forward()
    g = Forward()


    a << Trigger(nextptr = e, actions = [ DisplayText('Trigger A') ])
    e << Trigger(nextptr = f, actions = [ DisplayText('Trigger E') ])
    f << Trigger(nextptr = g, actions = [ DisplayText('Trigger F') ])
    g << Trigger(nextptr = triggerend, actions = [ DisplayText('Trigger G') ])

    pstart[i] = a # 위에서 정의한 a 트리거. pstart[0]에 대입한 a랑은 다른 a입니다.



psw = InitPlayerSwitch(pstart) # pstart 리스트에 주어진대로 각 플레이어의 시작 트리거 설정.


SaveMap("ex5.scx", psw)


# 실제로 스타에서 이 짓을 합니다.
# 진짜로요.

# eudtrg에서도 이게 정석이면 좀 그렇겠죠.
# eudtrg에서 방법은 ex7 참고.