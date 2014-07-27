.. _example5:

튜토리얼 5 : 기초적인 트리거 프로그래밍
=======================================

이번 강좌에서는 eudtrg를 이용해서 트리거를 변형하는 트리거를 짜보겠습니다.
트리거를 변형하는 트리거를 이용한 방법을 트리거 프로그래밍이라고 하는데,
트리거 프로그래밍의 난이도는 꽤 높은 편입니다. 이번 강좌에서는 nextptr를
트리거로 변형하는, 상대적으로 간단한 트리거 프로그래밍을 해보겠습니다.

소스
----

::

    from eudtrglib import *

    LoadMap('basemap.scx')

    a = Forward()
    b = Forward()
    c = Forward()


    # 저글링이 없으면 a의 nextptr를 c로 설정합니다.
    a << Trigger(
        nextptr = b,
        conditions = [
            Command(Player1, Exactly, 0, 'Zerg Zergling')
        ],
        actions = [
            SetNextPtr(a, c)
        ]
    )
    # 저글링이 없으면 a의 nextptr가 c가 될것이므로 c 트리거가 실행될거고
    # 아니면 a의 nextptr가 b가 될것이므로 b 트리거가 실행될겁니다.



    # 저글링이 있으면 (a트리거의 Command 조건으로 체크했습니다) 저글링을 죽이고 그 위치에 스카웃 생성
    # b의 nextptr는 a니까 b 다음에는 a가 실행되겠죠.
    b << Trigger(
        nextptr = a,
        actions = [
            MoveLocation('ztrace', 'Zerg Zergling', Player1, 'Anywhere'),
            GiveUnits(1, 'Zerg Zergling', Player1, 'ztrace', Player7),
            RemoveUnitAt(1, 'Zerg Zergling', 'ztrace', Player7),
            CreateUnit(1, 'Protoss Scout', 'ztrace', Player1)
        ]
    )


    # 저글링이 없으면 a에서 c로 점프합니다.
    c << Trigger(
        nextptr = triggerend,
        actions = [
            SetNextPtr(a, b) # 다시 a의 nextptr를 b로 설정해둡니다.
        ]
    )


    psw = InitPlayerSwitch([None, None, None, None, None, None, a, None])
    SaveMap('ex5.scx', psw)


결과
----

::
    
    저글링이 있던 자리에 스카웃이 생성된다.


코드 설명
---------


코드 주석에 대부분의 설명이 되어있습니다. :func:`SetNextPtr` 액션이 새로
등장했는데요 SetNextPtr 함수는 트리거의 nextptr에 다른 트리거의 주소를
대입하는 액션입니다.