'''
트리거 자동 연결, Trigger Scope에 대해 배워봅니다.
'''

from eudtrg import *

LoadMap("basemap.scx")

# 공통 트리거에 쓰이는 것
pstart = NextTrigger() # pstart는 '바로 다음 트리거'를 나타냅니다. 여기서는 1번 트리거.

Trigger( actions = [DisplayText("1")] ) # 1번 트리거
Trigger( actions = [DisplayText("2")] ) # 2번 트리거

if 1:
    PushTriggerScope()
    c = Trigger( actions = [DisplayText("3")] ) # 3번 트리거
    Trigger( actions = [DisplayText("4")] ) # 4번 트리거
    Trigger( actions = [DisplayText("5")] ) # 5번 트리거
    Trigger( actions = [DisplayText("6")] ) # 6번 트리거
    Trigger(nextptr = triggerend) # 7번 트리거
    PopTriggerScope()


y = Forward()
x = Trigger( actions = [DisplayText("8")] ) # 8번 트리거
y << Trigger( nextptr = c, actions = [DisplayText("9")] ) # 9번 트리거
Trigger( actions = [DisplayText("10")] ) # 10번 트리거


psw = InitPlayerSwitch([pstart, pstart, pstart, pstart, pstart, pstart, None, None])


SaveMap("ex6.scx", psw)

'''
3, 4, 5, 6, 7번 트리거가 PushTriggerScope()와 PopTriggerScope() 사이에 들어가있는걸 볼 수 있는데

 - PushTriggerScope() : Trigger Scope를 하나 만든다.
 - PopTriggerScope() : Trigger Scope를 하나 해제한다.

 란 의미를 가지고 있습니다.

 3, 4, 5, 6, 7번 트리거는 PushTriggerScope()에 의해 만들어진 Trigger Scope 안에 들어있으며
 이 Trigger Scope는 PopTriggerScope에 의해서 해제합니다.


1, 2는 Base Scope (초기 Scope)에 들어있고
Scope를 하나 만들고 (S라 합시다)
3, 4, 5, 6, 7는 S 안에 들어있고
PopTriggerScope를 이용해서 S를 해제하고
8, 9번 트리거는 Base Scope (S가 설정되기 전의 Trigger Scope)에 들어가게 됩니다.


-------


같은 Scope 안에 있는 Trigger끼리는 Trigger가 만들어진 순서대로 nextptr가 설정됩니다.

Base Scope 안에서는 1번, 2번, 8번, 9번 순서대로 Trigger가 만들어졌기 때문에
1 -> 2 -> 8 -> 9 번 순서대로 nextptr가 자동으로 이어지고,
9 -> 3(c)번 트리거로 이어지고 (9번 트리거의 nextptr)
Scope S 안에 있는 3 -> 4 -> 5 -> 6 -> 7번 트리거끼리 nextptr가 이어져서
결국 전체적인 트리거 순서는 1->2->8->9->3->4->5->6->7 이 됩니다.


9번 트리거는 nextptr를 직접 지정해줬기 때문에 nextptr가 자동으로 10번 트리거로 설정되지 않습니다.
nextptr을 생략한 트리거들에 한해서 nextptr가 자동으로 설정됩니다.


-------

결과는 이렇습니다.
1
2
8
9
3
4
5
6

'''