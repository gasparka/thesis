============
Introduction
============

Essentially this is a Python to VHDL converter, with a specific focus on implementing DSP systems.

Main features:

    - Simulate in Python. Integration to run RTL and GATE simulations.
    - Structured, all-sequential and object oriented designs
    - Fixed point type support(maps to `VHDL fixed point library`_)
    - Decent quality VHDL output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)
    - Tools to simplify verification


Long term goal is to implement more DSP blocks, especially by using GNURadio blocks as models.
In future it may be possible to turn GNURadio flow-graphs into FPGA designs, assuming we have matching FPGA blocks available.

.. _VHDL fixed point library: https://github.com/FPHDL/fphdl

Objective/goal
--------------
Provide simpler way of turning DSP blocks to FPGA

Structure
---------
Thesis structure.




