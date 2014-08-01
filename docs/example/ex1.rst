.. _example1:

튜토리얼 1 : Hello World!
=========================

간단한 eudtrg 예제입니다. 아마 :ref:`getting_Started` 다음으로 본 첫번째 코드
이실텐데요, eudtrg 코드가 어떻게 생겼는지를 대략적으로 알아보시면 됩니다.


소스
----

::

    from eudtrg import *

    LoadMap("basemap.scx") # basemap.scx를 불러옵니다.

    ptrg = Trigger(
        nextptr = triggerend, # ptrg를 끝으로 트리거 실행 종료
        actions = [
            DisplayText("Hello World!") # Hello World!
        ]
    )
    # 모든 트리거에는 Preserve Trigger가 기본적으로 적용됩니다. Preserve
    # Trigger를 풀기 위해서는 직접 Preserve Trigger를 해제해줘야 합니다.
    #  ex) Trigger( preserved = False )


    psw = InitPlayerSwitch([ptrg, ptrg, ptrg, ptrg, ptrg, ptrg, None, None])
    # P1, P2, P3, P4, P5, P6의 시작 트리거를 ptrg로 설정합니다.
    # P7, P8의 시작 트리거는 없습니다.

    SaveMap("ex1.scx", psw) # 맵이 시작할 때 psw가 바로 실행되도록 합니다.
    # 즉, 맵이 시작될 때 P1~P6의 시작 트리거를 ptrg로 설정합니다.

    # InitPlayerSwitch와 SaveMap은 뒤에서 설명할겁니다.


결과
----

::

    Hello World!
    Hello World!
    Hello World!
    Hello World!
    (무한반복)


코드 설명
---------

이 예제에서는 eudtrg 코드가 보통 어떻게 생겼는지를 다룹니다.

:code:`from eudtrg import *` 는 eudtrg의 모든 함수들을 불러온다는 뜻입니다.
eudtrg는 \'import *\' 로 불러올 수 있도록 만들었으며, 앞으로의 예제에서도
\'import *\' 를 이용해서 eudtrg를 사용할겁니다.

:code:`LoadMap("basemap.scx")` 는 basemap.scx를 불러옵니다. basemap.scx는
트리거를 제외한 모든 것들을 가지고 있는 맵으로, SCMDraft2 등의 에디터로 수정할
수 있습니다. basemap.scx를 통해서 지형, 유닛 배치, 로케이션 배치, 브리핑
등을 수정할 수 있습니다. basemap.scx에 원래 있던 트리거는 없어집니다.

::

    ptrg = Trigger(
        nextptr = triggerend, # End trigger execution after ptrg
        actions = [
            DisplayText("Hello World!")
        ]
    )

:class:`Trigger` 객체를 하나 만들어서 ptrg에 대입합니다. 이 때

- 각 트리거가 무슨 플레이어에 의해 실행되는지는 정해져있지 않습니다.
- 트리거의 nextptr를 triggerend로 설정했습니다. nextptr에 대한 자세한 설명은
  :ref:`example2` 에서 합니다.
- 트리거에 조건이 없습니다. 조건이 없는 트리거는 Always 조건 하나만 있는
  트리거와 동일하며, 항상 실행됩니다.

::

    psw = InitPlayerSwitch([ptrg, ptrg, ptrg, ptrg, ptrg, ptrg, None, None])
    SaveMap("ex1.scx", psw)

InitPlayerSwitch를 이용해서 각 플레이어의 시작 트리거를 지정해줍니다.
InitPlayerSwitch의 자세한 사용법은 :ref:`example2` 에서 하겠습니다.