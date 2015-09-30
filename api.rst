==============================
eudplib 간단정리 (Cheat Sheet)
==============================

eudplib에서 쓰이는 함수들을 간단정리한겁니다. eudplib에서 가능한 웬만한 것들은
모두 이 문서 안에서 해결할 수 있을겁니다. 질문이 있으시다면 phu54321@naver.com
을 통하거나 http://cafe.naver.com/edac 카페를 통해 연락해주세요.


.. contents:: 목차

eudplib 버젼은 이 함수로 체크하면 됩니다. 이 api.rst는 0.50버젼 기준입니다.

.. autofunction:: eudplib.eudtrgVersion

맵 로드/세이브
==============

eudplib 자체에 관한 것들은 이렇게 있습니다.

.. autofunction:: eudplib.LoadMap
.. autofunction:: eudplib.SaveMap
.. autofunction:: eudplib.CompressPayload






트리거
======

게임에 관련한 많은 것들을 트리거에서 처리합니다.


조건, 액션
----------

.. note:: 부록을 참고하세요.

조건이나 액션 목록은 부록을 참고하시고, 여기서는 조건/액션을 Disabled시키는
법이나 간단하게 알아봅시다. (별로 안쓰는 함수긴 합니다만)

.. autofunction:: eudplib.Disabled



트리거
------

트리거에는 조건/액션을 모두 갖춘 Trigger, 액션만 있는 (조건이 Always)
DoActions, Current Player를 인식하는 PTrigger가 있고요.

.. autofunction:: eudplib.Trigger
.. autofunction:: eudplib.DoActions
.. autofunction:: eudplib.PTrigger





변수
====

eud 변수는 EUDVariable로 만듭니다. +, -, \*, //, % 등의 연산자가 기본적으로
지원됩니다.

.. autoclass:: eudplib.EUDVariable
    :members:
    :show-inheritance:

.. autofunction:: eudplib.EUDCreateVariables

변수간 대입은 기본적으로 <<를 통해서 합니다. 여러 변수에다 값들을 동시에
대입할때는 아래 2개 함수를 쓸 수 있습니다.

.. autofunction:: eudplib.SeqCompute
.. autofunction:: eudplib.SetVariables

그 외에 값을 저장하는 기능만 있는 Light Variable도 있습니다.

.. autoclass:: eudplib.EUDLightVariable
    :members:
    :show-inheritance:





제어문
======

전체 프로그램 관련
------------------

여기 있는 함수들은 흔히 제어문이라 부르는 종류는 아니지만, eudplib 트리거 전체
관점에서 볼 때에 프로그램 흐름을 제어하기 때문에 여기 넣었습니다.

.. autofunction:: eudplib.EUDDoEvents
.. autofunction:: eudplib.RunTrigTrigger


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
Forward랑 NextTrigger가 있습니다.

.. autoclass:: eudplib.Forward
.. autofunction:: eudplib.NextTrigger




EUD 함수
========

함수도 eudplib에서 중요한 부분이라 할 수 있죠. EUD 함수를 만들때는 EUDFunc를
씁니다. 클래스 메서드를 EUDFunc처럼 쓰고싶을땐 EUDFuncMethod를 쓰고요.

.. autofunction:: eudplib.EUDFunc
.. autofunction:: eudplib.EUDFuncMethod


각 분야별 함수를 정리하면 다음과 같습니다.


메모리 관련
-----------

.. autofunction:: eudplib.EPD

.. autofunction:: eudplib.f_dwepdread_epd
.. autofunction:: eudplib.f_dwread_epd
.. autofunction:: eudplib.f_epdread_epd
.. autofunction:: eudplib.f_dwbreak

.. autofunction:: eudplib.f_dwwrite_epd
.. autofunction:: eudplib.f_dwadd_epd
.. autofunction:: eudplib.f_dwsubtract_epd

.. autofunction:: eudplib.f_repmovsd_epd
.. autofunction:: eudplib.f_memcpy
.. autofunction:: eudplib.f_strcpy

.. autofunction:: eudplib.f_dwpatch_epd
.. autofunction:: eudplib.f_unpatchall

.. autoclass:: eudplib.EUDByteReader
.. autoclass:: eudplib.EUDByteWriter


연산 관련
---------

산술 연산자
^^^^^^^^^^^

.. autofunction:: eudplib.f_mul
.. autofunction:: eudplib.f_div

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

.. autoclass:: eudplib.DBString
    :members:
    :show-inheritance:


.. autofunction:: eudplib.f_initextstr

.. autofunction:: eudplib.f_dbstr_adddw
.. autofunction:: eudplib.f_dbstr_print
.. autofunction:: eudplib.f_dbstr_addstr

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



비공유 → 공유 전환 관련
------------------------

.. autofunction:: eudplib.QueueGameCommand
.. autofunction:: eudplib.QueueGameCommand_RightClick



기타
----

.. autofunction:: eudplib.f_playerexist




트리거 상수/번호 관련
=====================

트리거에서는 모든것을 번호와 수로 처리합니다. 아래 함수들은 여러 상수들
(OreAndGas (자원 종류), Custom (스코어 종류), "Terran Marine" (유닛))를
해당하는 수나 번호로 바꾸는 함수들입니다.

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

아래 함수에서는 basemap에 있는 유닛 이름 등의 정보를 활용합니다.

.. autofunction:: eudplib.EncodeUnit
.. autofunction:: eudplib.EncodeLocation
.. autofunction:: eudplib.EncodeSwitch
.. autofunction:: eudplib.EncodeString
.. autofunction:: eudplib.EncodeProperty




맵 정보 관련
============

플레이어 정보는 이 함수를 씁니다.

.. autofunction:: eudplib.GetPlayerInfo

아래 함수들은 Encode~ 함수에서 쓰는 함수들입니다. 특히 GetStringIndex와
GetPropertyIndex에서는 해당하는 스트링이나 UPRP이 없는 경우 새로 스트링을
만들거나 UPRP를 만들 수 있습니다.

.. autofunction:: eudplib.GetUnitIndex
.. autofunction:: eudplib.GetLocationIndex
.. autofunction:: eudplib.GetSwitchIndex
.. autofunction:: eudplib.GetStringIndex
.. autofunction:: eudplib.GetPropertyIndex

.. warning::
    Encode~ 함수와 Get~Index 함수를 혼동하면 안됩니다. 예를 들어서 Location 0의
    GetLocationIndex 결과는 0(0번 로케이션)인 반면에, EncodeLocation 결과는 1
    (트리거 조건/액션에서 실제로 쓰는 값)이 나옵니다. 둘은 다른 함수입니다.



잡다한 것들
===========

유니코드str - bytes 변환
------------------------

.. autofunction:: eudplib.b2u
.. autofunction:: eudplib.u2b



bytes - DWORD / WORD / BYTE 변환
--------------------------------

.. autofunction:: eudplib.b2i1
.. autofunction:: eudplib.b2i2
.. autofunction:: eudplib.b2i4
.. autofunction:: eudplib.i2b1
.. autofunction:: eudplib.i2b2
.. autofunction:: eudplib.i2b4


기타
----

.. autofunction:: eudplib.Assignable2List
.. autofunction:: eudplib.List2Assignable
.. autofunction:: eudplib.FlattenList
.. autofunction:: eudplib.SCMD2Text
.. autoclass:: eudplib.TBL



eudplib로 유틸리티를 만들 때
============================

.. autofunction:: eudplib.IsMapdataInitalized
.. autoclass:: eudplib.EPError
.. autofunction:: eudplib.ep_assert


EUD 데이터 관련
===============

eudplib 코드에서 기본적으로 다룰 수 있는 데이터/리소스는 다음과 같습니다.

.. autoclass:: eudplib.Db
.. autoclass:: eudplib.EUDArray
.. autoclass:: eudplib.EUDGrp





커스텀 데이터/리소스 객체 관련
==============================

.. note::
    커스텀 리소스를 만들기 위해서는 eudplib 내부를 이해해야 합니다. 일반적인
    eudplib 사용자는 이 주제를 읽을 필요가 없습니다.

커스텀 리소스는 EUDObject를 부모 클래스삼아서 만들면 됩니다. 예제 리소스로
:class:`eudplib.Db` , :class:`eudplib.EUDGrp` 를 참고하세요.

.. autoclass:: eudplib.Expr
    :members:
    :show-inheritance:

.. autoclass:: eudplib.EUDObject
    :members:
    :show-inheritance:

EUDObject.Evaluate를 override할 때 쓸만한 함수들은 다음이 있습니다.

.. autofunction:: eudplib.IsValidExpr
.. autofunction:: eudplib.GetObjectAddr
.. autofunction:: eudplib.Evaluate

그 외에, 다음 함수들도 있습니다.

.. autofunction:: eudplib.RegisterCreatePayloadCallback
.. autofunction:: eudplib.CreatePayload


Raw Trigger
===========

.. note::
    성능에 목을 매달 정도로 성능이 중요할때나 만져볼만한 주제입니다. 일반적인
    eudplib 사용자는 이 주제를 읽을 필요가 없습니다.


기초 클래스
-----------

.. autoclass:: eudplib.Condition
    :members:
    :show-inheritance:

.. autoclass:: eudplib.Action
    :members:
    :show-inheritance:

.. autoclass:: eudplib.RawTrigger
    :members:
    :show-inheritance:



Trigger Scope
-------------

같은 Trigger Scope 안에 있는 RawTrigger끼리는 자동으로 nextptr이 연결됩니다.

.. autofunction:: eudplib.PushTriggerScope
.. autofunction:: eudplib.PopTriggerScope



커스텀 제어문 관련
==================

제어문을 새로 정의하고싶을 때 쓸 수 있는 함수들입니다.

.. autoclass:: eudplib.CtrlStruOpener

.. autofunction:: eudplib.EUDCreateBlock
.. autofunction:: eudplib.EUDPeekBlock
.. autofunction:: eudplib.EUDPopBlock

.. autofunction:: eudplib.EUDGetLastBlock
.. autofunction:: eudplib.EUDGetLastBlockOfName

.. autofunction:: eudplib.EUDGetBlockList


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
