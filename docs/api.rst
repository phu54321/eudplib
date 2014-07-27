:Author: whyask37

====================
eudtrglib API Reference
====================

This is eudtrglib API Reference. API Reference aims to hold any information needed
to use eudtrglib properly. If you think that this reference lacks essential
information, is too vague, is written in bad grammar, or lacks anything, feel
free to contact the author using whyask37@gmail.com.


Expressions
===========

Expression is a basic calculation unit of eudtrglib. Expression mean 'Object that
can be evaluated to some number'.

Base classes
------------

.. autoclass:: eudtrglib.Expr
    :members:

.. autoclass:: eudtrglib.EUDObject
    :members:

Basic objects
-------------
.. autoclass:: eudtrglib.Forward
    :members:

.. autoclass:: eudtrglib.Db
    :members:




Triggers
========

Trigger defines map logic.

Functions/Classes on trigger
----------------------------

.. autoclass:: eudtrglib.Trigger
    :members:
.. autoclass:: eudtrglib.Condition
    :members:
.. autoclass:: eudtrglib.Action
    :members:
.. autofunction:: eudtrglib.Disabled
.. autoclass:: eudtrglib.NextTrigger
    :members:


Trigger scope
-------------

Trigger scopes are used to specify scoping into triggers. Scopes groups
triggers together. Triggers in the same scope are eligable for
`nextptr auto linking`_.

.. autofunction:: eudtrglib.PushTriggerScope
.. autofunction:: eudtrglib.PopTriggerScope



Enumeration parser
------------------

Enumeration parsers are used to translate human-friendly identifiers to
intergal values. Consider following condition::

    Bring(Player1, AtLeast, 1, "Terran Marine", "Anywhere")

Each field is parsed by enumeration parser : player field is parsed by
:func:`eudtrglib.ParsePlayer` function, unit field is parsed by
:func:`eudtrglib.ParseUnit` function. ::

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

.. autofunction:: eudtrglib.ParseSwitchState
.. autofunction:: eudtrglib.ParseScore
.. autofunction:: eudtrglib.ParseComparison
.. autofunction:: eudtrglib.ParsePropState
.. autofunction:: eudtrglib.ParseModifier
.. autofunction:: eudtrglib.ParseOrder
.. autofunction:: eudtrglib.ParseResource
.. autofunction:: eudtrglib.ParseCount
.. autofunction:: eudtrglib.ParseAllyStatus
.. autofunction:: eudtrglib.ParsePlayer
.. autofunction:: eudtrglib.ParseAIScript
.. autofunction:: eudtrglib.ParseSwitchAction

.. autofunction:: eudtrglib.ParseUnit
.. autofunction:: eudtrglib.ParseLocation
.. autofunction:: eudtrglib.ParseString
.. autofunction:: eudtrglib.ParseProperty



Auxilary library
================

Variable Table
--------------

.. autoclass:: eudtrglib.EUDVTable
    :members:
.. autoclass:: eudtrglib.EUDVariable
    :members:
.. autofunction:: eudtrglib.EUDCreateVariables
.. autofunction:: eudtrglib.SeqCompute
.. autofunction:: eudtrglib.SetVariables
.. autofunction:: eudtrglib.VTProc

.. autoclass:: eudtrglib.EUDLightVariable
    :members:


Common control structures
-------------------------

.. autofunction:: eudtrglib.DoActions
.. autofunction:: eudtrglib.EUDJump
.. autofunction:: eudtrglib.EUDJumpIf
.. autofunction:: eudtrglib.EUDJumpIfNot
.. autofunction:: eudtrglib.EUDBranch

.. autofunction:: eudtrglib.EUDFunc
.. autofunction:: eudtrglib.InitPlayerSwitch



Common objects
--------------

String table
^^^^^^^^^^^^

.. autoclass:: eudtrglib.EUDTbl
    :members:
.. autofunction:: eudtrglib.f_reseteudtbl
.. autofunction:: eudtrglib.f_initeudtbl


Custom graphic (.GRP)
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: eudtrglib.EUDGrp
    :members:


Utility functions
-----------------

.. autofunction:: eudtrglib.EPD




Basic EUD Functions
===================

Arithmetics
-----------
.. autofunction:: eudtrglib.f_mul
.. autofunction:: eudtrglib.f_div

Memory I/O
----------
.. autofunction:: eudtrglib.f_epd
.. autofunction:: eudtrglib.f_dwread
.. autofunction:: eudtrglib.f_dwwrite
.. autofunction:: eudtrglib.f_dwbreak

.. autofunction:: eudtrglib.f_repmovsd
.. autofunction:: eudtrglib.f_memcpy
.. autofunction:: eudtrglib.f_strcpy


Map I/O Functions
=================

.. autofunction:: eudtrglib.SaveMap
.. autofunction:: eudtrglib.LoadMap















