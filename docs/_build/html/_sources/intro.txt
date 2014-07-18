.. _introduction:

Introduction
============

eudtrg is a tool for systematically generating Self-modifying trigger, trigger
that can be modified by EUD actions. With eudtrg, you can easily create
triggers that modify triggers. We call this technique 'Trigger programming'.
With trigger programming, you can

- Create control flow such as conditional branch and loop.
- Customize conditions and actions ingame.
- Use variables that supports fast assignment and calculation.
- Make functions out of triggers.

As a result, programming is possible. Any C code without APIs can be converted
to equivilant eudtrg trigger. eudtrg is harder than assembly, but it can do
anything.


Example map:
 - :download:`CreepDependentZergling <examplemap/CreepDependentZergling.scx>` :
   Zergling gets slower as they move out of the creep. This map checks position
   and creep for every zergling and controls their speed respectively.

SEN article for trigger programming : `<http://www.staredit.net/topic/16214/>`_

