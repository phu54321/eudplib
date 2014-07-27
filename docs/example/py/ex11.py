'''
EUDFunc 간단한 맛보기.
'''

from eudtrglib import *

LoadMap('basemap.scx')


# 변수 선언.
vt = EUDVTable(4)
a, b, ret, remainder = vt.GetVariables()



trgstart = NextTrigger()

SeqCompute([
    (a, SetTo, 13572468),
    (b, SetTo, 567)
])


SetVariables([ret, remainder], f_div.call(a, b)[0:2])

# f_div.call(x, y)는 x를 y로 나눈 몫과 나머지를 리턴합니다.
# ret, remainder에 f_div.call(a,b)의 리턴값 (몫, 나머지)를 대입하고
# 따라서 ret = 23937, remainder = 189 이 될겁니다.
#   13572468 = 567 * 23937 + 189

SeqCompute([
    ( EPD(0x58A364), SetTo, ret ),
    ( EPD(0x58A368), SetTo, remainder )
])

Trigger( nextptr = triggerend )

SaveMap('ex11.scx', trgstart)



'''
f_div 라는 EUD 함수가 있습니다.
f_div.call( f_div에 넘겨줄 값들 ) -> 적당한 값들이 계산되서 나온다 -> SetVariables로 적당한 변수에 저장시킬 수 있다.
'''