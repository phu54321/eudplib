eudtrglib 시작하기
===============

eudtrglib 설치하기
---------------

eudtrg는 파이썬 3용 라이브러리입니다. eudtrg는 pip를 이용해서 설치할 수 
있습니다. ::

    pip install eudtrglib

.. note::
    eudtrg는 32비트 SFmpq.dll을 이용해서 맵을 읽습니다. 따라서

    - eudtrg는 아직은 윈도에서만 돌아갑니다.
    - eudtrg는 32비트 파이썬 3.x 버젼에서 돌아갑니다.


예제맵 따라하기
---------------

#. test.py에 아래 코드를 붙여놓고 적당한 곳에 저장합니다. ::

    from eudtrglib import *

    LoadMap('basemap.scx')
    
    b = Forward()
    
    a = Trigger(
       nextptr = b, # Trigger executed after a is b
       actions = [
           SetDeaths(Player1, Add, 1, 'Terran Marine')
       ]
    )
    
    b << Trigger(
       nextptr = a, # Trigger executed after b is a
       actions = [
           SetDeaths(Player2, Add, 1, 'Terran Marine')
       ]
    )
    
    SaveMap('output.scx', a) # save map with a as starting trigger.

#. test.py가 있는 폴더에 컴퓨터 플레이어가 적어도 하나 있는 맵 basemap.scx를
   만듭니다.

#. test.py를 실행시키면 test.py가 있는 폴더에 output.scx라고 맵이 하나
   생성될겁니다.

#. 스타크래프트를 EUD Enabler + 창모드로 실행시키고 (풀스크린으로 실행시키면
   컴퓨터 전체가 멈출 위험이 있습니다) output.scx를 실행시킵니다.

#. 스타가 멈추고 P1, P2의 마린 데스값이 계속 증가할겁니다. (아트머니이나
   치트엔진으로 확인 가능) 작업 관리자로 스타를 강제종료시킵니다.


eudtrg가 재미있어보이면 :ref:`튜토리얼 <tutorial>` 을 보세요.