'''
간단한 트리거 프로그래밍 예제입니다.
nextptr를 실시간으로 변경하는 예제입니다.

맵에 존재하는 모든 저글링을 스카웃으로 바꿉니다.
'''

from eudtrg import *

LoadMap('basemap.scx')

# 0058D740 ~ 0058DC40 을 0 ~ 319 로 채워봅시다.

c = Forward()


# 저글링이 없으면 a의 nextptr를 c로 설정합니다.
a = Forward()
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
b = Trigger(
    nextptr = a,
    actions = [
        MoveLocation('ztrace', 'Zerg Zergling', Player1, 'Anywhere'),
        KillUnitAt(1, 'Zerg Zergling', 'ztrace', Player1),
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



SaveMap('a.scx', loopstart)

# InitPlayerSwitch가 이번 맵에서는 쓰이지 않았습니다.


'''
a : 저글링이 있으면 b로, 없으면 c로
b : 저글링을 스카웃으로 바꾸고 a로
c : 끝

저글링이 있는 동안 a->b->a->b->...->a->b 꼴로 트리거가 실행되고
이후 저글링이 없으면 a->c로 트리거가 실행됩니다.
c에서 a의 nextptr를 b로 설정해서 다음 트리거루프때 저글링이 새로 생겼다면 다시 a->b로 갈 수 있도록 합니다.



여담으로, ex7에서 사용한 EUDJumpIfNot 트리거는 아래와 같이 변형됩니다.

    EUDJumpIfNot( [Memory(currentplayer, Exactly, 0)], block1end )

    ->

    a = Forward()

    a << Trigger(
        nextptr = b
        conditions = [Memory(currentplayer, Exactly, 0)],
        actions = [ SetNextPtr(a, c) ]
    )

    b = Trigger(
        nextptr = block1end
    )

    c << Trigger(
        actions = [ SetNextPtr(a, b) ]
    )

    # c의 nextptr는 c 다음에 만들어진 Trigger()로 자동설정됨


이와 같이 EUDJumpIf, EUDJumpIfNot, 나중에 다룰 EUDVTable, f_mul, f_div 등등 eudtrg 안에 있는 것들은
모두 Trigger같이 기초적인 것들을 조합해서 만들어진 파이썬 함수/클래스 입니다.




간략하게 InitPlayerSwitch에 대해 설명하자면, eudtrg의 기본 동작은

    SaveMap('out.scx', triggerstart)

라고 했을 때, 매 트리거루프마다 컴퓨터 플레이어 하나가 triggerstart부터 시작해서 트리거를 한번 돌도록 되있습니다.
InitPlayerSwitch 는 조금 복잡한 트리거인데, 보통 

    psw = InitPlayerSwitch(...)
    SaveMap('out.scx', psw)

처럼 써서 InitPlayerSwitch를 맵이 시작하자마자 실행시킵니다.


InitPlayerSwitch 트리거는 SaveMap에서 지정해준 시작 트리거를 무시하고 각 플레이어의 시작 트리거를 새로 지정해줍니다.
이 원리를 응용하면 맵 시작할때 딱 한번만 실행되도록 하는 트리거는 이렇게 만들수도 있습니다.


    psw = Forward()
    executeonce = Trigger(nextptr = psw) # nextptr를 직접 설정해줘야 합니다.
    psw << InitPlayerSwitch(...) # InitPlayerSwitch 안에 트리거는 Scope 안에 있기 때문.

    SaveMap('out.scx', executeonce) # 맵 시작시에 executeonce가 실행되고 그 다음 InitPlayerSwitch 실행
'''