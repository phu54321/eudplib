.. _example1:

Example 1 : Hello World!
========================

Simple eudtrg example.


Code
----

::

    from eudtrg import *

    LoadMap("basemap.scx") # Collect various map-related informations from basemap.scx

    ptrg = Trigger(
        nextptr = triggerend, # End trigger execution after ptrg
        actions = [
            DisplayText("Hello World!") # Hello World!
        ]
    )
    # Every triggers are automatically preserved. You need to explicitly
    # unpreserve them if you want to.
    #  ex) Trigger( preserved = False )


    psw = InitPlayerSwitch([ptrg, ptrg, ptrg, ptrg, ptrg, ptrg, None, None])
    # InitPlayerSwitch will be explained at example 8


    SaveMap("ex1.scx", psw) # Set psw as starting trigger.

Output
------

::

    Hello World!
    Hello World!
    Hello World!
    Hello World!
    (continues)


Description
-----------

This example covers how eudtrg code is structured.

:code:`from eudtrg import *` imports all functions from eudtrg. eudtrg is
designed to be used with asterisk import.

:code:`LoadMap("basemap.scx")` loads template map basemap.scx. Template map
stores everything except trigger, such as unit preplacement, location, terrain,
map name/description, mission briefing.::

    ptrg = Trigger(
        nextptr = triggerend, # End trigger execution after ptrg
        actions = [
            DisplayText("Hello World!")
        ]
    )

We create :class:`Trigger` object and assign it to ptrg. Trigger object created
has following properties:
- nextptr is set to triggerend, which means end of trigger execution. When SC
encounters triggerend, SC exits trigger execution.
- No conditions are specified. Since there won't be any false condition, 
trigger will be always executed if SC encounters it.
- There is one DisplayText action, which displays text 'Hello World!' for
current player. When P1 executes this action, P1 get the text printed.
- Even if there are no Preserve Trigger actions, trigger is preserved by
default. You can explicitly unpreserve them by constructing them with preserved
set to false. :code:`Trigger( preserved = False )`

InitPlayerSwitch will be explained at :ref:`example8`