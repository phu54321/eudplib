Getting started
========

Installing eudtrg
-----------------

eudtrg requires Python 3. The easiest way to install eudtrg is by using pip. ::

    pip install eudtrg

.. note::
    eudtrg currently uses 32bit SFmpq.dll to run, so

    * eudtrg requires Windows installation.
    * eudtrg requires 32bit Python 3.x


First map
----------

Create test.py and write the following code::

    from eudtrg import *

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

Create basemap.scx with at least 1 computer players in the same directory with
test.py and run test.py. output.scx will be created. To test the map

- Run Starcraft in windowed mode with EUD Action Enabler. Running the map in
   fullscreen may freeze entire computer. You can use ChaosLauncher.

- Copy output.scx to Starcraft map folder and run it.

- Starcraft will freeze. Marine's deaths of P1 and P2 will increase infinitely.
   Check them with your favorate memory editing program. (Check addr 0x58A364)


