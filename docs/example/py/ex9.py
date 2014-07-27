'''
트리거 프로그래밍 예제입니다.
SetMemory 액션을 실시간으로 변형합니다.
약간 난이도가 있습니다.
'''

from eudtrglib import *

LoadMap('basemap.scx')

act0 = Forward()
loopstart = Forward()
loopend = Forward()

a = NextTrigger()


loopstart << Trigger(
    conditions = [
        Memory(act0 + 20, Exactly, 320) # act0의 number가 320이 됬을 때
    ],
    actions = [
        SetNextPtr(loopstart, loopend) # loopstart 트리거의 nextptr를 loopend로 설정
    ]
)

Trigger(
    actions = [
        ######################################################################################
        act0 << SetMemory(0x0058D740, SetTo, 0) # <----------------- 이 액션을 계속 변형합니다.
        ######################################################################################

    ]
)

Trigger(
    nextptr = loopstart,
    actions = [
        SetMemory(act0 + 16, Add, 1), # act0의 player를 1 증가
        SetMemory(act0 + 20, Add, 1)  # act0의 number를 1 증가
    ]
)

loopend << Trigger( nextptr = triggerend )


SaveMap('ex9.scx', loopstart)

'''
이 예제를 이해하기 위해서는 액션이 메모리에 어떻게 들어가는지부터 알아볼 필요가 있습니다.

    Trigger(
        actions = [
            act0 << SetMemory(0x0058D740, SetTo, 0)

        ]
    )

에서 'act0 << SetMemory(0x0058D740, SetTo, 0)' 라고 하는 걸로 act0은 SetMemory 액션의 주소가 됩니다.
즉, 오프셋 act0에 SetMemory 액션문이 있다는 뜻이죠. act0의 정확한 값은 스타 맵이 실행된 후에 결정됩니다.





조건문과 액션문의 메모리 구조를 알아봅시다. 먼저 dword, word, byte를 각각 4, 2, 1byte짜리 변수라고 합시다.

  1. 조건문
    조건문은 dword 3개, word 1개, byte 4개와 2byte의 padding으로 이루어져있습니다. (총 20byte)
    padding은 스타 내부적으로 쓰이는 메모리를 뜻합니다.

    예를 들어서

        cond0 << Bring(CurrentPlayer, Exactly, 1234, 'Terran Medic', Anywhere)

    라고 했을 때, cond0 ~ cond0 + 19 까지의 메모리는 다음과 같이 됩니다.

                |  00  |  01  |  02  |  03  |
      cond0 +  0| [40     00     00     00] | -> 0x00000040 = 64 ( Anywhere 로케이션 )
      cond0 +  4| [0D     00     00     00] | -> 0x0000000D = 13 ( Current Player )
      cond0 +  8| [D2     04     00     00] | -> 0x000004D2 = 1234
      cond0 + 12| [22     00]   [0A]   [03] | -> 0x0022 = 34 (Terran Medic), 0x0A (Exactly), 0x03 (Bring)
      cond0 + 16| [00]   [00]   [00     00] | -> 0x00, 0x00, padding 2byte (00 00)



    이 때 cond0 + 8 (Bring에서 유닛 갯수)를 아래와 같은 액션으로 조작하게 되면

        SetMemory(cond0 + 8, SetTo, 5678)

    cond0 조건문이 Bring(CurrentPlayer, Exactly, 5678, 'Terran Medic', Anywhere) 로 바뀌게 됩니다.

      cond0 +  8| [2E     16     00     00] | -> 0x0000162E = 5678

    이와 같이 트리거 조건문을 바꿀 수 있습니다. Bring 조건문이 위와 같은 구조로 되어있다는건
    eudtrglib.base.stocktrg를 통해서 알 수 있습니다. stocktrg.py를 열면
     ( C:\\Python[파이썬버젼명]\\Lib\\site-packages\\eudtrglib\\base 등을 열면 됩니다. )

        def Bring(Player, Comparison, Number, Unit, Location):
            Player = ParsePlayer(Player)
            Comparison = ParseComparison(Comparison)
            Unit = ParseUnit(Unit)
            Location = ParseLocation(Location)
            return Condition(Location, Player, Number, Unit, Comparison, 3, 0, 0)

    와 같이 Bring 조건문이 정의된것을 볼 수 있습니다. 여기서
    return Condition(Location, Player, Number, Unit, Comparison, 3, 0, 0)
    Location, Player, Number, Unit, Comparison, 3, 0, 0 순서대로 조건문의
    1번째 dword, 2번째 dword, 3번째 dword, 1번째 word, 1번째 byte, 2번쨰 byte, 3번째 byte, 4번째 byte
    의 역할을 합니다.


  2. 액션문
    액션문은 dword 6개, word 1개, byte 3개, padding 3byte로 이루어져있습니다. 예를 들어

        act0 << SetMemory(0x0058D740, SetTo, 5678)

    와 같이 act0을 SetMemory 액션의 오프셋으로 설정했을 때, act0 ~ act0 + 31 까지의 오프셋은 다음과 같습니다.

                |  00  |  01  |  02  |  03  |
      act0 +  0 | [00     00     00     00] | -> 0x00000000
      act0 +  4 | [00     00     00     00] | -> 0x00000000
      act0 +  8 | [00     00     00     00] | -> 0x00000000
      act0 + 12 | [00     00     00     00] | -> 0x00000000
      act0 + 16 | [07     CF     00     00] | -> 0x000007CF = 3319, 0x0058D740에 해당하는 EPD 플레이어 번호
      act0 + 20 | [2E     16     00     00] | -> 0x0000162E = 5678
      act0 + 24 | [00     00]   [2D]   [07] | -> 0x0000 = 0 (UnitID = 0) , 0x2D (SetDeaths), 0x07 (SetTo)
      act0 + 28 | [00]   [00     00     00] | -> 0x00, padding 3byte (00 00 00)

    (SetMemory 액션은 사실 SetDeaths 액션과 동일합니다)

    따라서 SetMemory(act0 + 16, SetTo, EPD(0x5993D4))는 SetDeaths의 플레이어 번호를 0x5993D4에 해당하는 EPD 번호인 15388 로 바꾸고,
     ( EPD(0x5993D4) = 15388 )
    SetMemory(act0 + 20, SetTo, 4567)은 SetDeaths문의 숫자 부분을 4567로 바꿉니다.

    SetMemory의 구조도 역시 stocktrg.py에서 볼 수 있습니다.



이제 이 기초지식을 가지고 위의 트리거를 해석해보시기 바랍니다.
ex9의 난이도는 조금 어렵습니다. 이해하고 넘어가세요.

'''





'''

사족)

조건과 액션에 관한 지식이 있으면 빈 메모리 공간에 새로 조건문을 만들고 새로 액션문을 만들 수 있습니다.
    - 트리거는 dword 2개(각각 prevptr(안쓰임), nextptr ), 조건 16개(20 * 16 = 320byte),
      액션 64개(32 * 64 = 2048byte), dword 1개(스타 내부적으로 쓰입니다. 기본값 0.
      preserve trigger 적용시 4), byte 27개(안쓰임), byte 1개(기본값 0) 으로 총 2408byte
      짜리 byte입니다.

    - 2408byte 메모리에 저 형식만 맞추어 값들을 넣어주면 새로 트리거가 만들어집니다.

'''