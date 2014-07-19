.. _example2:

튜토리얼 2 : nextptr를 이용해서 트리거 실행 순서 지정하기
=========================================================

이 튜토리얼에서는 nextptr를 이용해서 트리거 실행 순서를 지정하는 방법을
다룹니다.

소스
----

::

    from eudtrg import *

    LoadMap("basemap.scx")

    a, b, c, d, e, f = [Forward() for _ in range(6)]

    a << Trigger(nextptr = b,          actions = [DisplayText("Trigger A")]) # a 다음에 b
    b << Trigger(nextptr = d,          actions = [DisplayText("Trigger B")]) # b 다음에 d
    c << Trigger(nextptr = e,          actions = [DisplayText("Trigger C")]) # c 다음에 e
    d << Trigger(nextptr = c,          actions = [DisplayText("Trigger D")]) # d 다음에 c
    e << Trigger(nextptr = f,          actions = [DisplayText("Trigger E")]) # e 다음에 f
    f << Trigger(nextptr = triggerend, actions = [DisplayText("Trigger F")]) # f로 끝


    psw = InitPlayerSwitch([a, b, c, d, e, f, None, None])
    # P1, P2, P3, P4, P5, P6은 각각 a, b, c, d, e, f부터 트리거를 실행


    SaveMap("ex2.scx", psw)


결과
----

::

    [P1 화면]
    Trigger A
    Trigger B
    Trigger D
    Trigger C
    Trigger E
    Trigger F

    [P2 화면]
    Trigger B
    Trigger D
    Trigger C
    Trigger E
    Trigger F

    [P3 화면]
    Trigger C
    Trigger E
    Trigger F

    [P4 화면]
    Trigger D
    Trigger C
    Trigger E
    Trigger F

    [P5 화면]
    Trigger E
    Trigger F

    [P6 화면]
    Trigger F
    
    (무한반복)


코드 설명
---------

1. :class:`Forward` 클래스
^^^^^^^^^^^^^^^^^^^^^^^^^^

Forward 클래스는 트리거같은 객체들을 가르킬 수 있는 객체입니다. 주로 뒤에서
만드는 트리거나 변수들을 앞쪽에서 다루기 위해 사용합니다. 예를 들어 ::

    a = Trigger( nextptr = b )
    b = Trigger( nextptr = a )

에서 :code:`a = Trigger( nextptr = b )` 에서는 a가 정의될 때에는 b가 아직
정의되지 않았기 때문에 에러가 납니다. 이럴 때 b를 미리 Forward()로 정의하면 ::

    b = Forward()
    a = Trigger( nextptr = b )
    b << Trigger( nextptr = a ) # b에 실제 트리거 넣기

:code:`a = Trigger( nextptr = b )` 에서 b가 앞에 Forward()로 정의되어있으므로
에러가 나지 않습니다. 나중에 :code:`b << Trigger( nextptr = a )` 에서 Forward에
실제로 트리거를 채워넣게 됩니다.

.. note::
    
    Forward()로 선언한 변수에 다른 트리거를 대입할 때 조심하세요. ::

        b = Forward()
        a = Trigger( nextptr = b ) # Forward를 a의 nextptr에 넣어주고 있다.
        b = Trigger() # Forward에 트리거를 넣는게 아니라 그냥 새로 트리거를 만듬.
        # a라는 Trigger의 nextptr (Forward 객체)에 값이 안넣어졌기 때문에
        # 'Forward has not been properly initalized' 라고 에러메세지가 뜸



2. 스타크래프트 트리거 엔진의 원리
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

아마 여러분들은 기존의 SCMDraft2같은 맵에디터로 트리거를 만들어왔을겁니다.
맵에디터에서 만드는 트리거는 P1~P8 순서대로, 위에서 아래 순서대로 트리거가
실행되었죠. eudtrg에서 만드는 트리거도 비슷한 원리를 따라가지만, eudtrg 자체가
맵에디터의 트리거 에디터랑은 원리가 완전히 다르기 때문에 eudtrg에서 만드는
트리거의 실행 순서는 일반적인 트리거랑 차이가 있습니다.

스타크래프트에서 각 트리거는 크게 6개의 값을 가지고 있습니다.

- prevptr : 바로 전 트리거
- nextptr : 바로 뒤 트리거
- conditions : 트리거 조건들. (16개) SCMDraft2의 Conditions 탭에 해당.
- actions : 트리거 액션들. (64개) SCMDraft2의 Actions 탭에 해당.
- internal : preserve trigger 등의 속성.
- effplayer : 이 트리거가 어떤 플레이어에게 작동하는가. SCMDraft2의 Players
  탭에 해당


prevptr, nextptr는 기존 트리거 에디터로 다룰 수 없고, internal은 SCMDraft2에서
수정을 지원하지 않습니다.


트리거 실행은 대략적으로 아래처럼 진행됩니다. ::

    i = 0~7에 대해서:
        trg = 플레이어 i (i=0이면 Player 1) 의 첫번째 트리거

        trg가 triggerend가 아닌 동안:
            trg 트리거를 실행한다 (조건 체크, 액션 실행)
            # 플레이어 체크는 하지 않습니다.
            trg = trg의 nextptr (다음 트리거로 간다)


즉, 각 트리거의 nextptr은 그 트리거 다음에 실행될 트리거를 나타냅니다. 또한
각 플레이어의 첫번째 트리거부터 트리거 실행이 시작됩니다.


기존의 맵에디터로 만든 트리거는 스타에서 아래와 같은 과정으로 읽습니다. ::

    trgarr := 맵에 있는 트리거들

    i = 0~7에 대해서:
        trgarr에 있는 각 트리거 trg에 대해서:
            Player i가 trg를 실행시킬 수 있으면:
                trg를 복사한다 (trg1)
                Player i의 마지막 트리거를 trg1로 설정한다. 원래 Player i의 마지막 트리거의 nextptr는 trg1로, trg1의 prevptr은 원래 Player i의 마지막 트리거로 설정.
                trg1은 각 플레이어마다 다르기 때문에 맵에 있던 트리거는 트리거가 실행되는 플레이어 갯수만큼 복제되서 각 플레이어가 하나씩 복사본을 가집니다.

따라서 트리거를 스타에서 실행할 때 각 플레이어가 각 트리거를 실행시킬 수
있는지를 체크할 필요가 없습니다. Preserve Trigger가 걸리지 않은 트리거라도
Player 1에서 한번 실행됬더라도 Player 2에선 실행할 수 있는 이유이기도 합니다.



eudtrg로 만든 트리거는 스타에서 대략 아래 과정으로 초기화됩니다. ::

    trgs := eudtrg로 만든 트리거들
    pstart[0~7] := InitPlayerSwitch에서 지정해준 각 플레이어의 시작 트리거

    Player 1의 첫번째 트리거를 pstart[0]으로 지정한다.
    Player 2의 첫번째 트리거를 pstart[1]으로 지정한다.
    Player 3의 첫번째 트리거를 pstart[2]으로 지정한다.
    Player 4의 첫번째 트리거를 pstart[3]으로 지정한다.
    Player 5의 첫번째 트리거를 pstart[4]으로 지정한다.
    Player 6의 첫번째 트리거를 pstart[5]으로 지정한다.
    Player 7의 첫번째 트리거를 pstart[6]으로 지정한다.
    Player 8의 첫번째 트리거를 pstart[7]으로 지정한다.
    
애초에 스타에서는 eudtrg로 만든 트리거를 인식하지 못하기 때문에 eudtrg
라이브러리에서 스타가 트리거를 강제로 인식하게 만드는 초기화 트리거를
만듭니다. 스타에서 트리거를 불러오는게 아니기 때문에 기존 트리거랑 트리거
초기화 방식이 꽤 다릅니다.

eudtrg로 만든 맵을 SCMDraft2 트리거 에디터로 열었을때 보이는 엄청난 양의
EUD 트리거가 바로 트리거 초기화 트리거입니다. eudtrg로 컴파일한 트리거 자체는
SCMDraft2로 바로 볼 수 없습니다.


3. nextptr
^^^^^^^^^^

스타에서 prevptr는 사실 별 의미가 없고, nextptr만 의미가 있습니다. 트리거의
nextptr는 \'이 트리거 다음에 실행되는 트리거\'를 나타냅니다. nextptr를 통해서
트리거의 실행 순서를 지정할 수 있습니다.

예제맵에서 Player 4는 d 트리거부터 실행을 시작합니다.

- d.nextptr = c
- c.nextptr = e
- e.nextptr = f
- f.nextptr = triggerend ( 트리거 실행 끝 )

따라서 Player 4는 d -> c -> e -> f 순서대로 트리거를 실행합니다. nextptr를
이용해서 트리거 실행 순서를 마음대로 바꾸는 방법은 두루두루 쓰이므로 잘 알아둘
필요가 있습니다.