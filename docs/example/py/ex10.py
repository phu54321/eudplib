'''
Variable Table에 대해 다룹니다.
'''

from eudtrglib import *

LoadMap('basemap.scx')

vt = EUDVTable(5) # 변수 5개가 들어있는 Variable Table을 만듭니다.
a, b, c, d, e = vt.GetVariables() # vt에서 변수 5개를 뽑아냅니다.

trgstart = NextTrigger()




Trigger(
    actions = [
        a.SetNumber(2),
        b.SetNumber(6),
        c.SetNumber(10),
        d.SetNumber(14),
        e.SetNumber(18)
    ]
)
# a = 2, b = 6, c = 10, d = 14, e = 18를 대입합니다.




Trigger(
    actions = [
        a.AddNumber(1),
        b.AddNumber(3),
        c.AddNumber(7),
        d.SubtractNumber(15),
        e.SetNumber(31)
    ]
)
# a = 3, b = 9, c = 17, d = 0, e = 31
# d = 0인 이유는 밑에 설명합니다.



Trigger(
    actions = [
        a.AddNumber(-1),
    ]
)
# a = 2



t = Forward()
Trigger(
    nextptr = vt,
    actions = [
        a.QueueAddTo(e),
        SetNextPtr(vt, t)
    ]
)
t << NextTrigger()
# e += a를 한다. e = 33가 된다.



VTProc(vt, [
    b.QueueAddTo(c)
])
# c += b를 한다. c = 26



SeqCompute([
    (a, SetTo, b),
    (d, Add, e),
    (d, Subtract, a)
])
# a = b, d += e, d -= c를 순서대로 실행한다.
# a가 9가 되고, d가 33가 되고, d가 24이 된다.
# 여기에서 a, b, c, d, e는 각각 9, 9, 26, 24, 33



t = Forward()
Trigger(
    nextptr = vt,
    actions = [
        a.QueueAssignTo(EPD(0x58A364)),
        b.QueueAssignTo(EPD(0x58A368)),
        c.QueueAssignTo(EPD(0x58A36C)),
        d.QueueAssignTo(EPD(0x58A370)),
        e.QueueAssignTo(EPD(0x58A374)),
        SetNextPtr(vt, t) # 여기 t는 54번 줄에서 만든 t가 아니라 85번 줄에서 만든 t다.
    ]
)
t << NextTrigger()
# 오프셋 0x58A364, 0x58A368, 0x58A36C, 0x58A370, 0x58A374 에 각각 a, b, c, d, e의 값을 저장한다.
# 각각 9, 9, 26, 43, 52가 저장될것이다.
# 치트엔진으로 이 값들을 확인해보라.


Trigger( nextptr = triggerend )

SaveMap('ex10.scx', trgstart)



'''
EUDVTable도은 덧셈/뺄셈/곱셈이 아주 쉽게 되는 변수를 만들어주는 기능입니다.
EUDVTable도 그냥 변수 몇개가 들어있는 트리거입니다.
ex11부터는 SeqCompute를 주로 쓸 것이고, 가끔가다 VTProc 정도만 쓸겁니다.





    Trigger(
        actions = [
            a.AddNumber(1),
            b.AddNumber(3),
            c.AddNumber(7),
            d.SubtractNumber(15),
            e.SetNumber(31)
        ]
    )

x.AddNumber / SubtractNumber / SetNumber (e)는 각각 x 변수에 e만큼 더하기/빼기/대입 한다는 뜻입니다.

d의 값이 14였는데 d에서 15를 뺐더니 d가 0이 되는건 스타크래프트 특성입니다.
스타에서 SetDeaths를 Subtract로 쓰면
 - 원래 데스값이 뺄 값보다 크면 (원래 데스값) - (뺄 데스값)
 - 아니면 0 # 작은 값에서 큰 값을 빼는 경우 : 언더플로우
로 데스값을 설정하게 됩니다.
14 < 15이므로 d = 0으로 설정되게 됩니다.





    Trigger(
        actions = [
            a.AddNumber(-1),
        ]
    )
    # a = 2

에서 -1은 0xFFFFFFFF를 나타냅니다.
예를 들어서 0x00001234에 0xFFFFFFFF 를 더하면 0x100001233 이 되는데,
스타에서 데스값은 4byte이므로 4byte를 넘어가는 0x100000000 은 버려지고 (오버플로우)
따라서 0x00001234 + 0xFFFFFFFF = 0x00001233 이 됩니다.
오버플로우는 스타에서 따로 체크하지 않습니다.





    t = Forward()
    Trigger(
        nextptr = vt,
        actions = [
            a.QueueAddTo(e),
            SetNextPtr(vt, t)
        ]
    )
    t << NextTrigger()
    # e += a를 한다. e = 33가 된다.

a.QueueAddTo(e)는 'a의 값을 e에 더하도록 예약(Queue)한다' 는 뜻입니다.
vt 트리거가 실행될 때 a의 값이 e에 실제로 더해지게 됩니다.

 - e가 EUDVTable같은데 안에 들어있는 변수라면 a.QueueAddTo(e)는 'e 변수에 a 변수 값을 더한다'라는 의미가 되고,
 - e가 오프셋이라면 a.QueueAddTo(e) 는 'e라는 EPD 플레이어에 해당하는 오프셋에 a 더하기'라는 뜻이 됩니다.

트리거가 실행 된 후 vt가 실행되고, vt 다음에 다음 트리거(t)가 실행됩니다.

QueueAssignTo (대입), QueueSubtractTo (설정) 도 마찬가지입니다.





    VTProc(vt, [
        b.QueueAddTo(c)
    ])
    # c += b를 한다. c = 26

t = Forward(), nextptr = vt, SetNextPtr(vt, t), t << NextTrigger() 를 합쳐서 VTProc(vt, [액션들]) 이라 할 수 있습니다.
VTProc에서는 conditions이 없습니다.





    SeqCompute([
        (a, SetTo, b),
        (d, Add, e),
        (d, Subtract, a)
    ])

AddNumber, SubtractNumber, SetNumber, QueueAddTo, QueueSubtractTo, QueueAssignTo를 잘 이용해서
 - ( 변수/오프셋(dst), SetTo/Add/Subtract, 변수/오프셋(src) ) -> src의 값을 dst에 대입/덧셈/뺄셈 한다
라는 계산 여러개를 위에서부터 아래 순서대로 한다는 뜻입니다.
'''