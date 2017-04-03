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



Objective/goal
--------------

Testing and verifying is hard.
The goal of this study is to implement experimental Python to VHDL compiler.
Provide an model and unit test based workflow, where tests that are defined for the
model can be reused for RTL and GATE level simulations.

Provide simpler way of turning DSP blocks to FPGA.
Reduce the gap between regular programming and hardware design.
Turn GNURadio flowgraphs to FPGA?
Model based verification!
Why do it?
opensource

How far can we go with the oneprocess design? Everyone else uses
VHDL as a very low level interface.

Scope
-----
???
Focus on LimeSDR board and GnuRadio Pothos, frameworks.

Structure
---------
First chapter gives an short background about the context of this thesis and existing toolsets
that provide conversion from higher level languages to Gates.




