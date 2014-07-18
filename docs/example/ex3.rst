.. _example3:

Example 3 : Emultating player field of stock trigger
====================================================

eudtrg triggers don't have any concept of 'executing player'. In this example,
we demonstrate two methods for specifying executors for each triggers.

Code 1
------

::

    from eudtrg import *

    LoadMap("basemap.scx")


    pstart = [None] * 8

    # Generate triggers for p1.
    if 1:
        a = Forward() # starting trigger for player 1 (0)
        b = Forward()
        c = Forward()
        d = Forward()
        e = Forward()
        f = Forward()
        g = Forward()
        h = Forward()


        a << Trigger(nextptr = b, actions = [ DisplayText('Trigger A') ])
        b << Trigger(nextptr = c, actions = [ DisplayText('Trigger B') ])
        c << Trigger(nextptr = d, actions = [ DisplayText('Trigger C') ])
        d << Trigger(nextptr = e, actions = [ DisplayText('Trigger D') ])
        e << Trigger(nextptr = f, actions = [ DisplayText('Trigger E') ])
        f << Trigger(nextptr = g, actions = [ DisplayText('Trigger F') ])
        g << Trigger(nextptr = h, actions = [ DisplayText('Trigger G') ])
        h << Trigger(nextptr = triggerend, actions = [ DisplayText('Trigger H') ])
        

        pstart[0] = a



    # Generate triggers for p2~p5.
    for i in range(1, 6):
        a = Forward() # Starting trigger for player 2~6 (1~5)
        e = Forward()
        f = Forward()
        g = Forward()


        a << Trigger(nextptr = e, actions = [ DisplayText('Trigger A') ])
        e << Trigger(nextptr = f, actions = [ DisplayText('Trigger E') ])
        f << Trigger(nextptr = g, actions = [ DisplayText('Trigger F') ])
        g << Trigger(nextptr = triggerend, actions = [ DisplayText('Trigger G') ])

        pstart[i] = a



    psw = InitPlayerSwitch(pstart)
    # P1~8 starts trigger execution with pstart[0~7] respectively.


    SaveMap("ex3_1.scx", psw)




Output 1
--------

::

    P1
    Trigger A
    Trigger B
    Trigger C
    Trigger D
    Trigger E
    Trigger F
    Trigger G

    P2~6
    Trigger A
    Trigger E
    Trigger F
    Trigger G

    (Text are repeated for all players)


Description
-----------

In this example, we created seperate trigger set for each players. This is the
easiest way to generate player-basis triggers, but also the most trigger
consuming methods. This simple map takes about 0.5Mib. It's how starcraft
really processes player fields of trigger: SC reads trigger, checks its
player field, and paste their copy for every matching players.