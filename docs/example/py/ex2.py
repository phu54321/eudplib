'''
example 2에서는 트리거의 실행 순서를 다룹니다.
'''

from eudtrg import *

LoadMap("basemap.scx") # basemap.scx 에서 잡다한 정보들을 모음.

a = Forward() # Forward의 역할은 ex3에서 설명합니다.
b = Forward()
c = Forward()
d = Forward()
e = Forward()
f = Forward()


a << Trigger(nextptr = b,          actions = [DisplayText("Trigger A")]) # a 다음에 실행되는 트리거는 b
b << Trigger(nextptr = d,          actions = [DisplayText("Trigger B")]) # b 다음에 실행되는 트리거는 d
c << Trigger(nextptr = e,          actions = [DisplayText("Trigger C")]) # c 다음에 실행되는 트리거는 e
d << Trigger(nextptr = c,          actions = [DisplayText("Trigger D")]) # d 다음에 실행되는 트리거는 c
e << Trigger(nextptr = f,          actions = [DisplayText("Trigger E")]) # e 다음에 실행되는 트리거는 f
f << Trigger(nextptr = triggerend, actions = [DisplayText("Trigger F")]) # f 다음에 실행되는 트리거는 없다. (f로 트리거 실행이 끝남)



psw = InitPlayerSwitch([
    a, b, c, d, e, f, # P1 ~ P6은 각각 a, b, c, d, e, f를 시작 트리거로 한다.
    None, None # P7, P8은 아무 트리거도 쓰지 않는다.
])


SaveMap("ex2.scx", psw) # ex2.scx에 트리거를 넣는다.



'''
P1 : 트리거 실행순서가 a -> b -> d -> c -> e -> f
P2 : 트리거 실행순서가 b -> d -> c -> e -> f
P3 : 트리거 실행순서가 c -> e -> f
P4 : 트리거 실행순서가 d -> c -> e -> f
P5 : 트리거 실행순서가 e -> f
P6 : 트리거 실행순서가 f

트리거의 실행순서는 nextptr를 따릅니다.


eudtrg의 트리거에서 플레이어 개념은 없습니다.
트리거 실행순서에 있는 모든 트리거는 실행됩니다.

'''
