====================
eudplib API Reference
====================

This is eudplib API Reference. API Reference aims to hold any information needed
to use eudplib properly. If you think that this reference lacks essential
information, is too vague, is written in bad grammar, or lacks anything, feel
free to contact the author using whyask37@gmail.com.


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




Triggers
========

Trigger defines map logic.

Functions/Classes on trigger
----------------------------

.. autoclass:: eudplib.Trigger
    :members:
    :show-inheritance:
.. autoclass:: eudplib.Condition
    :members:
    :show-inheritance:
.. autoclass:: eudplib.Action
    :members:
    :show-inheritance:
.. autofunction:: eudplib.Disabled
.. autoclass:: eudplib.NextTrigger
    :members:
    :show-inheritance:


Trigger scope
-------------

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

.. autofunction:: eudplib.ParseSwitchState
.. autofunction:: eudplib.ParseScore
.. autofunction:: eudplib.ParseComparison
.. autofunction:: eudplib.ParsePropState
.. autofunction:: eudplib.ParseModifier
.. autofunction:: eudplib.ParseOrder
.. autofunction:: eudplib.ParseResource
.. autofunction:: eudplib.ParseCount
.. autofunction:: eudplib.ParseAllyStatus
.. autofunction:: eudplib.ParsePlayer
.. autofunction:: eudplib.ParseAIScript
.. autofunction:: eudplib.ParseSwitchAction

.. autofunction:: eudplib.ParseUnit
.. autofunction:: eudplib.ParseLocation
.. autofunction:: eudplib.ParseString
.. autofunction:: eudplib.ParseProperty



Auxilary library
================

Variable Table
--------------

.. autoclass:: eudplib.EUDVTable
    :members:
    :show-inheritance:
.. autoclass:: eudplib.EUDVariable
    :members:
    :show-inheritance:
.. autofunction:: eudplib.EUDCreateVariables
.. autofunction:: eudplib.SeqCompute
.. autofunction:: eudplib.SetVariables
.. autofunction:: eudplib.VTProc

.. autoclass:: eudplib.EUDLightVariable
    :members:
    :show-inheritance:


Common control structures
-------------------------

.. autofunction:: eudplib.DoActions
.. autofunction:: eudplib.EUDJump
.. autofunction:: eudplib.EUDJumpIf
.. autofunction:: eudplib.EUDJumpIfNot
.. autofunction:: eudplib.EUDBranch

.. autofunction:: eudplib.EUDFunc
.. autofunction:: eudplib.InitPlayerSwitch



Common objects
--------------

String table
^^^^^^^^^^^^

.. autoclass:: eudplib.EUDTbl
    :members:
    :show-inheritance:
.. autofunction:: eudplib.f_reseteudtbl
.. autofunction:: eudplib.f_initeudtbl


Custom graphic (.GRP)
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: eudplib.EUDGrp
    :members:
    :show-inheritance:


Utility functions
-----------------

.. autofunction:: eudplib.EPD
.. autofunction:: eudplib.CreateOffsetMapping



Basic EUD Functions
===================


Memory I/O
----------
.. autofunction:: eudplib.f_epd
.. autofunction:: eudplib.f_dwread
.. autofunction:: eudplib.f_dwwrite
.. autofunction:: eudplib.f_dwbreak

.. autofunction:: eudplib.f_repmovsd
.. autofunction:: eudplib.f_memcpy
.. autofunction:: eudplib.f_strcpy


Map I/O Functions
=================

.. autofunction:: eudplib.SaveMap
.. autofunction:: eudplib.LoadMap














