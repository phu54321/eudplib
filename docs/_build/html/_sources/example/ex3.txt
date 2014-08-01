.. _example3:

튜토리얼 3 : nextptr 자동 연결, Trigger Scope
=============================================


소스
----

::

    from eudtrg import *

    LoadMap("basemap.scx")

    pstart = NextTrigger() # NextTrigger는 '바로 다음 트리거'를 나타냅니다. 여기서는 1번 트리거.

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


    Trigger( actions = [DisplayText("8")] ) # 8번 트리거
    Trigger( nextptr = c, actions = [DisplayText("9")] ) # 9번 트리거
    Trigger( actions = [DisplayText("10")] ) # 10번 트리거


    psw = InitPlayerSwitch([pstart, pstart, pstart, pstart, pstart, pstart, None, None])


    SaveMap("ex3.scx", psw)





결과
------

::
    1
    2
    8
    9
    3
    4
    5
    6
    


코드 설명
---------

1. nexptr 자동 연결
^^^^^^^^^^^^^^^^^^^

nextptr를 지정하지 않은 트리거의 nextptr는 다음에 만들어진 트리거로 자동으로
지정됩니다. 예를 들어 ::
    
    Trigger( actions = [DisplayText("1")] ) # 1번 트리거
    Trigger( actions = [DisplayText("2")] ) # 2번 트리거

는 다음과 같습니다. ##

    t = Forward()
    Trigger( nextptr = t, actions = [DisplayText("1")] ) # 1번 트리거
    t << Trigger( actions = [DisplayText("2")] ) # 2번 트리거


2. :class:`NextTrigger`
^^^^^^^^^^^^^^^^^^^^^^^

NextTrigger는 '다음에 만들어진 Trigger'를 말합니다. 예를 들어 ::

    t = Forward()
    Trigger( nextptr = t, actions = [DisplayText("1")] ) # 1번 트리거
    t << NextTrigger()
    Trigger( actions = [DisplayText("2")] ) # 2번 트리거

에서 t는 NextTrigger()가 불린 후 처음으로 불린 Trigger(), 즉 2번 트리거를
가르킵니다.

..note::

    NextTrigger()를 Trigger()의 인자로 넣으면 안됩니다. 예를 들어서 ::

        t = Trigger( nextptr = NextTrigger() )

    에서 NextTrigger()가 불린 뒤에 Trigger( nextptr = ... ) 가 불리므로
    NextTrigger는 t를 가르키게 됩니다. 즉, t.nextptr = t가 됩니다. 
    NextTrigger()는 Trigger() 밖에서 사용하세요.


3. Trigger Scope
^^^^^^^^^^^^^^^^

nextptr 자동 연결을 설명하는 김에 Trigger Scope도 설명하겠습니다. Scope는
파이썬의 함수나 클래스 등으로 트리거를 생성할 때 자주 씁니다. 트리거를 짜다보면
nextptr 자동 연결이 안됬으면 하는 경우가 있는데, Trigger Scope를 이용해서
트리거간에 nextptr 자동 연결을 조절할 수 있습니다.

- :func:`PushTriggerScope` : Trigger Scope를 하나 만든다.
- :func:`PopTriggerScope` : Trigger Scope 하나를 해제한다.
  :func:`PushTriggerScope` 랑 쌍으로 사용된다.

예를 들어서 ::

    if 1:
        PushTriggerScope()
        c = Trigger( actions = [DisplayText("3")] ) # 3번 트리거
        Trigger( actions = [DisplayText("4")] ) # 4번 트리거
        Trigger( actions = [DisplayText("5")] ) # 5번 트리거
        Trigger( actions = [DisplayText("6")] ) # 6번 트리거
        Trigger(nextptr = triggerend) # 7번 트리거
        PopTriggerScope()

    Trigger( actions = [DisplayText("8")] ) # 8번 트리거

에서 3, 4, 5, 6, 7번 트리거는 :func:`PushTriggerScope`와
:func:`PopTriggerScope` 사이에 있습니다. 이 때

#. PushTriggerScope를 이용해서 Scope를 하나 만듭니다.
#. 3, 4, 5, 6, 7번 트리거를 Scope 안에서 만듭니다.
#. PopTriggerScope로 Scope를 해제합니다.
#. Scope가 해제된 후 만들어진 8번 트리거는 Scope 밖에 있습니다.

따라서 3, 4, 5, 6, 7번 트리거는 Scope 안에 있고, 1, 2, 8, 9, 10번 트리거는
Scope 밖에 있습니다.

nextptr 자동 연결은 같은 Scope 안에 있는 트리거들끼리만 적용됩니다. 즉,
3, 4, 5, 6, 7번 트리거끼리 nextptr가 자동으로 설정되고, 1, 2, 8, 9, 10번
트리거끼리 nextptr가 자동으로 설정됩니다. 따라서 트리거 실행이 1->2->8->9
순서로 진행됩니다. 9번 트리거의 nextptr는 3번 트리거로 설정되어있으므로
9번 트리거 이후로는 9->3->4->5->6->7->끝 순서로 트리거가 실행되는거고요.

Scope는 중첩될 수 있습니다. 예를 들어서 ::

    Trigger() -  트리거 A

    PushTriggerScope()-----------+
    Trigger() -  트리거 B        |
                                 |
    PushTriggerScope()--------+  |
    Trigger() -  트리거 C     |  |
    PopTriggerScope()---------+  |
                                 |
    Trigger() -  트리거 D        |
    PopTriggerScope()------------+

    Trigger() -  트리거 E

    PushTriggerScope()-----------+
    Trigger() -  트리거 F        |
    PopTriggerScope()------------+

일 때, (A, E), (B, D), (C), (F) 가 각각 같은 Scope에 있게 됩니다.

Scope는 보통 외부 트리거랑 별로 연관이 없는 트리거를 트리거 중간에 선언할 때
많이 씁니다. :ref:`example6` 에서 변수에 대해서 배우는데, 이 때
:class:`EUDVTable` 를 쓰게 됩니다. 이 클래스는 생성자에서 트리거를 하나
만드는데, EUDVTable이 만드는 트리거랑 다른 트리거랑 엮이면 안되기 때문에
EUDVTable에서는 트리거를 Scope에 넣어둡니다. Scope는 생각보다 의외로 유용한
기능이라서 알아두면 좋습니다.