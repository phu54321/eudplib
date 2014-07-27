'''
Hello world!
'''

from eudtrglib import *

LoadMap("basemap.scx") # basemap.scx 에서 잡다한 정보들을 모음.


ptrg = Trigger(
    nextptr = triggerend, # ptrg를 끝으로 트리거 실행을 마친다.
    actions = [
        DisplayText("Hello World!") # Hello World! 라고 출력한다.
    ]
) # 모든 트리거에는 Preserve Trigger가 자동으로 적용되기 때문에 Hello World! 라고 계속 출력될겁니다.




psw = InitPlayerSwitch([
    ptrg, ptrg, ptrg, ptrg, ptrg, ptrg, # P1 ~ P6까지는 ptrg에서 트리거 시작
    None, None # P7, P8은 아무 트리거도 쓰지 않음.
])


SaveMap("ex1.scx", psw) # ex1.scx에 psw를 시작 트리거로 저장한다.
# 일단 eudtrg에서는 맵을 이런 식으로 만든다고 외우세요.