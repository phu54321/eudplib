====================
eudtrg API Reference
====================

This is eudtrg API Reference. API Reference aims to hold any information needed
to use eudtrg properly. If you think that this reference lacks essential
information, is too vague, is written in bad grammar, or lacks anything, feel
free to contact the author using whyask37@gmail.com.


Expressions
===========

Expression is a basic calculation unit of eudtrg. Expression mean 'Object that
can be evaluated to some number'.

Base classes
------------

.. autoclass:: eudtrg.Expr
    :members:
    :show-inheritance:

.. autoclass:: eudtrg.EUDObject
    :members:
    :show-inheritance:

Basic objects
-------------
.. autoclass:: eudtrg.Forward
    :members:
    :show-inheritance:

.. autoclass:: eudtrg.Db
    :members:
    :show-inheritance:




Triggers
========

Trigger defines map logic.

Functions/Classes on trigger
----------------------------

.. autoclass:: eudtrg.Trigger
    :members:
    :show-inheritance:
.. autoclass:: eudtrg.Condition
    :members:
    :show-inheritance:
.. autoclass:: eudtrg.Action
    :members:
    :show-inheritance:
.. autofunction:: eudtrg.Disabled
.. autoclass:: eudtrg.NextTrigger
    :members:
    :show-inheritance:


Trigger scope
-------------

Trigger scopes are used to specify scoping into triggers. Scopes groups
triggers together. Triggers in the same scope are eligable for
`nextptr auto linking`_.

.. autofunction:: eudtrg.PushTriggerScope
.. autofunction:: eudtrg.PopTriggerScope



Enumeration parser
------------------

Enumeration parsers are used to translate human-friendly identifiers to
intergal values. Consider following condition::

    Bring(Player1, AtLeast, 1, "Terran Marine", "Anywhere")

Each field is parsed by enumeration parser : player field is parsed by
:func:`eudtrg.ParsePlayer` function, unit field is parsed by
:func:`eudtrg.ParseUnit` function. ::

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

.. autofunction:: eudtrg.ParseSwitchState
.. autofunction:: eudtrg.ParseScore
.. autofunction:: eudtrg.ParseComparison
.. autofunction:: eudtrg.ParsePropState
.. autofunction:: eudtrg.ParseModifier
.. autofunction:: eudtrg.ParseOrder
.. autofunction:: eudtrg.ParseResource
.. autofunction:: eudtrg.ParseCount
.. autofunction:: eudtrg.ParseAllyStatus
.. autofunction:: eudtrg.ParsePlayer
.. autofunction:: eudtrg.ParseAIScript
.. autofunction:: eudtrg.ParseSwitchAction

.. autofunction:: eudtrg.ParseUnit
.. autofunction:: eudtrg.ParseLocation
.. autofunction:: eudtrg.ParseString
.. autofunction:: eudtrg.ParseProperty



Auxilary library
================

Variable Table
--------------

.. autoclass:: eudtrg.EUDVTable
    :members:
    :show-inheritance:
.. autoclass:: eudtrg.EUDVariable
    :members:
    :show-inheritance:
.. autofunction:: eudtrg.EUDCreateVariables
.. autofunction:: eudtrg.SeqCompute
.. autofunction:: eudtrg.SetVariables
.. autofunction:: eudtrg.VTProc

.. autoclass:: eudtrg.EUDLightVariable
    :members:
    :show-inheritance:


Common control structures
-------------------------

.. autofunction:: eudtrg.DoActions
.. autofunction:: eudtrg.EUDJump
.. autofunction:: eudtrg.EUDJumpIf
.. autofunction:: eudtrg.EUDJumpIfNot
.. autofunction:: eudtrg.EUDBranch

.. autofunction:: eudtrg.EUDFunc
.. autofunction:: eudtrg.InitPlayerSwitch



Common objects
--------------

String table
^^^^^^^^^^^^

.. autoclass:: eudtrg.EUDTbl
    :members:
    :show-inheritance:
.. autofunction:: eudtrg.f_reseteudtbl
.. autofunction:: eudtrg.f_initeudtbl


Custom graphic (.GRP)
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: eudtrg.EUDGrp
    :members:
    :show-inheritance:


Utility functions
-----------------

.. autofunction:: eudtrg.EPD
.. autofunction:: eudtrg.CreateOffsetMapping



Basic EUD Functions
===================

Arithmetics
-----------
.. autofunction:: eudtrg.f_mul
.. autofunction:: eudtrg.f_div

Memory I/O
----------
.. autofunction:: eudtrg.f_epd
.. autofunction:: eudtrg.f_dwread
.. autofunction:: eudtrg.f_dwwrite
.. autofunction:: eudtrg.f_dwbreak

.. autofunction:: eudtrg.f_repmovsd
.. autofunction:: eudtrg.f_memcpy
.. autofunction:: eudtrg.f_strcpy


Map I/O Functions
=================

.. autofunction:: eudtrg.SaveMap
.. autofunction:: eudtrg.LoadMap















