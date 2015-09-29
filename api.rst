==============================
eudplib 간단정리 (Cheat Sheet)
==============================

eudplib에서 쓰이는 함수들을 간단정리한겁니다. eudplib에서 가능한 웬만한 것들은
모두 이 문서 안에서 해결할 수 있을겁니다. 질문이 있으시다면 phu54321@naver.com
을 통하거나 http://cafe.naver.com/edac 카페를 통해 연락해주세요.


.. contents:: 목차



잡다한 함수
===========

eudplib 자체에 관한 것들은 이렇게 있습니다.

.. autofunction:: eudplib.eudtrgVersion





기초 트리거 관련
================

게임에 관련한 많은 것들을 트리거에서 처리합니다.


조건, 액션
----------

.. note:: 부록을 참고하세요.

조건이나 액션 목록은 부록을 참고하시고, 여기서는 조건/액션을 Disabled시키는
법이나 간단하게 알아봅시다. 이 함수도 쓸 일이 사실 없을거에요.

.. autofunction:: eudplib.Disabled



트리거
------

트리거에는 조건/액션을 모두 갖춘 Trigger, 액션만 있는 (조건이 Always)
DoActions가 있습니다.

.. autofunction:: eudplib.Trigger
.. autofunction:: eudplib.DoActions





제어문
======

조건문
------

조건문에는 EUDIf, EUDSwitch, EUDJumpIf가 있습니다.

EUDIf류
^^^^^^^

.. autofunction:: eudplib.EUDIf
.. autofunction:: eudplib.EUDIfNot
.. autofunction:: eudplib.EUDElseIf
.. autofunction:: eudplib.EUDElseIfNot
.. autofunction:: eudplib.EUDElse
.. autofunction:: eudplib.EUDEndIf


EUDSwitch류
^^^^^^^^^^^

C언어의 switch에 해당합니다. EUDIf ~ EUDElseIf 로 하나하나 체크하는것보다
속도가 빠릅니다.

.. autofunction:: eudplib.EUDSwitch
.. autofunction:: eudplib.EUDSwitchCase
.. autofunction:: eudplib.EUDSwitchDefault
.. autofunction:: eudplib.EUDEndSwitch

C언어에서의 break는 EUDBreak류 함수를 이용해서 따라합니다.

.. note:: 반복문의 EUDBreak류 함수 참고


EUDJumpIf류
^^^^^^^^^^^
.. autofunction:: eudplib.EUDJumpIf
.. autofunction:: eudplib.EUDJumpIfNot
.. autofunction:: eudplib.EUDBranch



반복문
------

반복문에는 EUDWhile, EUDInfLoop, EUDLoopN, EUDPlayerLoop가 있고, 이들을
도와주는 EUDContinue, EUDBreak가 있습니다.


제일 기초적인 while문에 해당하는 EUDWhile문이 있겠죠.

.. autofunction:: eudplib.EUDWhile
.. autofunction:: eudplib.EUDWhileNot
.. autofunction:: eudplib.EUDEndWhile

여기서 파생된 EUDLoopN도 있습니다.

.. autofunction:: eudplib.EUDLoopN
.. autofunction:: eudplib.EUDEndLoopN


C언어에서 while(1)에 해당하는 무한루프는 EUDInfLoop를 사용합니다.

.. autofunction:: eudplib.EUDInfLoop
.. autofunction:: eudplib.EUDEndInfLoop


현재 존재하는 플레이어에 대해 반복하는 EUDPlayerLoop도 있습니다.

.. autofunction:: eudplib.EUDPlayerLoop
.. autofunction:: eudplib.EUDEndPlayerLoop

반복문이니까 continue도 있죠.

.. autofunction:: eudplib.EUDContinue
.. autofunction:: eudplib.EUDContinueIf
.. autofunction:: eudplib.EUDContinueIfNot

C언어에 for문에 해당하는걸 쉽게 만들도록 도와주는 Continue Point도 있고요.

.. autofunction:: eudplib.EUDIsContinuePointSet
.. autofunction:: eudplib.EUDSetContinuePoint

break류도 있습니다.

.. autofunction:: eudplib.EUDBreak
.. autofunction:: eudplib.EUDBreakIf
.. autofunction:: eudplib.EUDBreakIfNot



기타 제어문
^^^^^^^^^^^

.. autofunction:: eudplib.EUDExecuteOnce
.. autofunction:: eudplib.EUDEndExecuteOnce
.. autofunction:: eudplib.EUDJump

그 외에, EUDJumpIf나 EUDJump같은 Jump류 제어문을 쓸 때 자주 쓸만한 것으로
NextTrigger가 있습니다.

.. autofunction:: eudplib.NextTrigger





함수 관련
=========

함수도 eudplib에서 중요한 부분이라 할 수 있죠. EUD 함수를 만들때는 EUDFunc를
씁니다.

.. autofunction:: eudplib.EUDFunc

각 분야별 함수를 정리하면 다음과 같습니다.


메모리 관련
-----------

먼저 오프셋을 EPD 플레이어로 바꾸는 함수입니다.

.. autofunction:: eudplib.f_epd

그 다음엔 읽기 관련 함수

.. autofunction:: eudplib.f_dwepdread_epd
.. autofunction:: eudplib.f_dwread_epd
.. autofunction:: eudplib.f_epdread_epd

.. autofunction:: eudplib.f_dwbreak

그 다음엔 쓰기 관련 함수

.. autofunction:: eudplib.f_dwwrite_epd
.. autofunction:: eudplib.f_dwadd_epd
.. autofunction:: eudplib.f_dwsubtract_epd

메모리 블럭 단위 읽기/쓰기 함수

.. autofunction:: eudplib.f_repmovsd_epd
.. autofunction:: eudplib.f_memcpy
.. autofunction:: eudplib.f_strcpy

메모리 패치 & 복구용 함수인데, 쓸 일은 별로 없을꺼에요.

.. autofunction:: eudplib.f_dwpatch_epd
.. autofunction:: eudplib.f_unpatchall

.. note:: f_unpatchall을 수동으로 불러줘야만 f_dwpatch_epd한게 전부 복구됩니다.


연산 관련
---------

곱셈/나눗셈은 그냥 \*나 //, %로 해도 되지만 이런 함수도 있긴 있어요.

.. autofunction:: eudplib.f_mul
.. autofunction:: eudplib.f_div

비트연산자들은 이렇게 있어요.

.. autofunction:: eudplib.f_bitand
.. autofunction:: eudplib.f_bitor
.. autofunction:: eudplib.f_bitnot
.. autofunction:: eudplib.f_bitxor

.. autofunction:: eudplib.f_bitnand
.. autofunction:: eudplib.f_bitnor
.. autofunction:: eudplib.f_bitnxor

.. autofunction:: eudplib.f_bitlshift
.. autofunction:: eudplib.f_bitrshift

.. autofunction:: eudplib.f_bitsplit



DB스트링 관련
-------------

DB스트링은 스트링 테이블과는 별개 메모리에 있는 스트링을 뜻합니다.

.. autoclass:: eudplib.DBString
    :members:
    :show-inheritance:


DB스트링 초기화는 f_initextstr를 통해서 합니다.

.. autofunction:: eudplib.f_initextstr

.. warning:: DB스트링을 쓰기 전에 먼저 f_initextstr를 꼭 불러야 합니다.


DB스트링과 아래 함수들을 이용해서 더 자유롭게 스트링을 출력할 수 있습니다.

.. autofunction:: eudplib.f_dbstr_adddw
.. autofunction:: eudplib.f_dbstr_print
.. autofunction:: eudplib.f_dbstr_addstr


DisplayExtText 을 쓰면 DB스트링을 이용해 스트링을 출력하기 때문에 스트링 제한
(1024개, 65536byte 등) 없이 스트링 출력을 할 수 있습니다.

.. autofunction:: eudplib.DisplayExtText



랜덤 관련
---------

.. autofunction:: eudplib.f_rand
.. autofunction:: eudplib.f_dwrand

.. autofunction:: eudplib.f_randomize
.. autofunction:: eudplib.f_srand
.. autofunction:: eudplib.f_getseed



Current Player 관련
-------------------

.. autofunction:: eudplib.f_getuserplayerid
.. autofunction:: eudplib.f_getcurpl
.. autofunction:: eudplib.f_setcurpl



수학 관련
---------

.. autofunction:: eudplib.f_lengthdir


기타
----

.. autofunction:: eudplib.f_playerexist




맵 정보 관련
============

basemap에 관한 정보는 이 함수들을 통해 얻을 수 있습니다.

.. autofunction:: eudplib.GetPlayerInfo

.. autofunction:: eudplib.GetUnitIndex
.. autofunction:: eudplib.GetSwitchIndex
.. autofunction:: eudplib.GetLocationIndex

GetStringIndex와  GetPropertyIndex에서는 해당하는 스트링이나 UPRP이 없는 경우
새로 스트링을 만들거나 UPRP를 만들 수 있습니다.

.. autofunction:: eudplib.GetStringIndex
.. autofunction:: eudplib.GetPropertyIndex


Expressions
===========

Expression is a basic calculation unit of eudplib. Expression mean 'Object that
can be evaluated to some number'.

Base classes
------------

.. autoclass:: eudplib.Expr
    :members:
    :show-inheritance:

.. autoclass:: eudplib.EUDObject
    :members:
    :show-inheritance:

Basic objects
-------------
.. autoclass:: eudplib.Forward
    :members:
    :show-inheritance:

.. autoclass:: eudplib.Db
    :members:
    :show-inheritance:



Raw Trigger
===========

.. autoclass:: eudplib.Condition
    :members:
    :show-inheritance:

.. autoclass:: eudplib.Action
    :members:
    :show-inheritance:

.. autoclass:: eudplib.RawTrigger
    :members:
    :show-inheritance:



Raw Trigger scope
-----------------

Trigger scopes are used to specify scoping into triggers. Scopes groups
triggers together. Triggers in the same scope are eligable for
`nextptr auto linking`_.

.. autofunction:: eudplib.PushTriggerScope
.. autofunction:: eudplib.PopTriggerScope



Enumeration parser
------------------

Enumeration parsers are used to translate human-friendly identifiers to
intergal values. Consider following condition::

    Bring(Player1, AtLeast, 1, "Terran Marine", "Anywhere")

Each field is parsed by enumeration parser : player field is parsed by
:func:`eudplib.ParsePlayer` function, unit field is parsed by
:func:`eudplib.ParseUnit` function. ::

    Player1 -> ParsePlayer(Player1) = 0
    AtLeast -> ParseComparison(AtLeast) = 0
    1
    "Terran Marine" -> ParseUnit("Terran Marine") = 0
    "Anywhere" -> ParseLocation("Anywhere") = 64

So, the condition is translated as::

    1. Bring(Player1, AtLeast, 1, "Terran Marine", "Anywhere")
    2. Bring(0, 0, 1, 0, 64)
    3. Condition(64, 0, 1, 0, 0, 3, 0, 0)

Enumeration parsers can also be used inside user code. For instance, consider
following function changing unit's graphic to other sprite::

    ChangeUnitGraphics(0, 123) # Set Terran Marine's graphics to Sprite #123.

This code can be rewritten to::

    ChangeUnitGraphics(ParseUnit("Terran Marine"), 123)

Or even better, ChangeUnitGraphics function can use ParseUnit internally.

.. autofunction:: eudplib.EncodeSwitchState
.. autofunction:: eudplib.EncodeScore
.. autofunction:: eudplib.EncodeComparison
.. autofunction:: eudplib.EncodePropState
.. autofunction:: eudplib.EncodeModifier
.. autofunction:: eudplib.EncodeOrder
.. autofunction:: eudplib.EncodeResource
.. autofunction:: eudplib.EncodeCount
.. autofunction:: eudplib.EncodeAllyStatus
.. autofunction:: eudplib.EncodePlayer
.. autofunction:: eudplib.EncodeAIScript
.. autofunction:: eudplib.EncodeSwitchAction
.. autofunction:: eudplib.EncodeSwitch

.. autofunction:: eudplib.EncodeUnit
.. autofunction:: eudplib.EncodeLocation
.. autofunction:: eudplib.EncodeString
.. autofunction:: eudplib.EncodeProperty



Auxilary library
================

블럭 구조 라이브러리
--------------------

.. autofunction:: eudplib.EUDCreateBlock
.. autofunction:: eudplib.EUDGetBlockList
.. autofunction:: eudplib.EUDGetLastBlock
.. autofunction:: eudplib.EUDGetLastBlockOfName
.. autofunction:: eudplib.EUDPeekBlock
.. autofunction:: eudplib.EUDPopBlock


Variable Table
--------------

.. autoclass:: eudplib.EUDVariable
    :members:
    :show-inheritance:
.. autofunction:: eudplib.EUDCreateVariables
.. autofunction:: eudplib.SeqCompute
.. autofunction:: eudplib.SetVariables

.. autoclass:: eudplib.EUDLightVariable
    :members:
    :show-inheritance:


Common control structures
-------------------------





Common objects
--------------

String table
^^^^^^^^^^^^




Custom graphic (.GRP)
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: eudplib.EUDGrp
    :members:
    :show-inheritance:


Utility functions
-----------------

.. autofunction:: eudplib.EPD



Basic EUD Functions
===================




Map I/O Functions
=================

.. autofunction:: eudplib.SaveMap
.. autofunction:: eudplib.LoadMap







부록
====

너무 긴것들은 여기다 모아놓았습니다.

조건 목록
---------

.. autofunction:: eudplib.Accumulate
.. autofunction:: eudplib.Always
.. autofunction:: eudplib.Bring
.. autofunction:: eudplib.Command
.. autofunction:: eudplib.CommandLeast
.. autofunction:: eudplib.CommandLeastAt
.. autofunction:: eudplib.CommandMost
.. autofunction:: eudplib.CommandMostAt
.. autofunction:: eudplib.CountdownTimer
.. autofunction:: eudplib.Deaths
.. autofunction:: eudplib.ElapsedTime
.. autofunction:: eudplib.HighestScore
.. autofunction:: eudplib.LeastKills
.. autofunction:: eudplib.LeastResources
.. autofunction:: eudplib.LowestScore
.. autofunction:: eudplib.Memory
.. autofunction:: eudplib.MostKills
.. autofunction:: eudplib.MostResources
.. autofunction:: eudplib.Never
.. autofunction:: eudplib.Opponents
.. autofunction:: eudplib.Score
.. autofunction:: eudplib.Switch


액션 목록
---------

.. autofunction:: eudplib.CenterView
.. autofunction:: eudplib.Comment
.. autofunction:: eudplib.CreateUnit
.. autofunction:: eudplib.CreateUnitWithProperties
.. autofunction:: eudplib.Defeat
.. autofunction:: eudplib.DisplayText
.. autofunction:: eudplib.Draw
.. autofunction:: eudplib.GiveUnits
.. autofunction:: eudplib.KillUnit
.. autofunction:: eudplib.KillUnitAt
.. autofunction:: eudplib.LeaderBoardComputerPlayers
.. autofunction:: eudplib.LeaderBoardControl
.. autofunction:: eudplib.LeaderBoardControlAt
.. autofunction:: eudplib.LeaderBoardGoalControl
.. autofunction:: eudplib.LeaderBoardGoalControlAt
.. autofunction:: eudplib.LeaderBoardGoalKills
.. autofunction:: eudplib.LeaderBoardGoalResources
.. autofunction:: eudplib.LeaderBoardGoalScore
.. autofunction:: eudplib.LeaderBoardGreed
.. autofunction:: eudplib.LeaderBoardKills
.. autofunction:: eudplib.LeaderBoardResources
.. autofunction:: eudplib.LeaderBoardScore
.. autofunction:: eudplib.MinimapPing
.. autofunction:: eudplib.ModifyUnitEnergy
.. autofunction:: eudplib.ModifyUnitHangarCount
.. autofunction:: eudplib.ModifyUnitHitPoints
.. autofunction:: eudplib.ModifyUnitResourceAmount
.. autofunction:: eudplib.ModifyUnitShields
.. autofunction:: eudplib.MoveLocation
.. autofunction:: eudplib.MoveUnit
.. autofunction:: eudplib.MuteUnitSpeech
.. autofunction:: eudplib.Order
.. autofunction:: eudplib.PauseGame
.. autofunction:: eudplib.PauseTimer
.. autofunction:: eudplib.PlayWAV
.. autofunction:: eudplib.PreserveTrigger
.. autofunction:: eudplib.RemoveUnit
.. autofunction:: eudplib.RemoveUnitAt
.. autofunction:: eudplib.RunAIScript
.. autofunction:: eudplib.RunAIScriptAt
.. autofunction:: eudplib.SetAllianceStatus
.. autofunction:: eudplib.SetCountdownTimer
.. autofunction:: eudplib.SetCurrentPlayer
.. autofunction:: eudplib.SetDeaths
.. autofunction:: eudplib.SetDoodadState
.. autofunction:: eudplib.SetInvincibility
.. autofunction:: eudplib.SetMemory
.. autofunction:: eudplib.SetMissionObjectives
.. autofunction:: eudplib.SetNextPtr
.. autofunction:: eudplib.SetNextScenario
.. autofunction:: eudplib.SetResources
.. autofunction:: eudplib.SetScore
.. autofunction:: eudplib.SetSwitch
.. autofunction:: eudplib.TalkingPortrait
.. autofunction:: eudplib.Transmission
.. autofunction:: eudplib.UnMuteUnitSpeech
.. autofunction:: eudplib.UnpauseGame
.. autofunction:: eudplib.UnpauseTimer
.. autofunction:: eudplib.Victory
.. autofunction:: eudplib.Wait
