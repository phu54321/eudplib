eudtrglib
=========

eudtrglib is a simple library for generating eud programming triggers. It's
quite easier to use than eudasm, yet more powerful.


What is eudtrglib
--------------

   eudtrglib is python library for automatically generating EUD Programming(EUDP) triggers. With EUDP, you can

   - Modify trigger execution order directly.
   - Modify triggers online.
   - Do almost anything you wanted.

   eudtrglib is still in prototype phase, but I will make this gradually better.



How to use eudtrglib in 5 minute.
------------------------------

   1. Install eudtrglib using pip. ``pip install eudtrglib``
   2. Create a map 'basemap.scx' with at least 2 computer players.
   3. Copy collowing code to ``test.py`` and place it at the same directory with ``basemap.scx``

   ```
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
   ```

   4. Run test.py. You will get output.scx
   5. Run the map. SC will freeze, and Death value of P1/P2's Terran Marine (0x58A364, 0x58A368) will increase indefinitely.
      **Run your map in W-Mode, or your entire COMPUTER will freeze.**

 3) More functions.

   eudtrglib has small set of function for EUDP. See ``__doc__`` of each files for more info.
