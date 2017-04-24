Introduction
============

Major goal of this project is to support object-oriented hardware design.

While other high level tools convert to very low-level VHDL, then Pyha takes and different approach by
first developing an feasible model in VHDL and then using Python to get around VHDL ugly parts.

Sell this!!!. Has good integration for model, is debuggable. Running simulations is extreamly
easy. Good fixed point support. Modern software dev tools in hw.

Essentially this is a Python to VHDL converter, with a specific focus on implementing DSP systems.


Pyha is exploratory project, to see how well software approach could fit into hardware world.

Pyha is a tool that allows writing of digital hardware in Python language. Currently it focuses mostly on the DSP
applications.

Main features:

    - Simulate hardware in Python. Integration to run RTL and GATE simulations.
    - Structured, all-sequential and object oriented designs
    - Fixed point type support(maps to `VHDL fixed point library`_)
    - Semi-automatic conversion to fixed-point
    - Decent quality VHDL conversion output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)
    - Tools to simplify verification


Contributions:

    - Show HW vs SW differences
    - Development of Object-oriented VHDL model
    - Ease hardware development for software engineers

Pyha specifically focuses on making testing of the DSP algorithms simpler.
While many alternatives are based on C language, but most of the hardware design time is used up in
the process of testing and verification, who would like to do this in C, Python is much better language
for this!

Pyha proposes to use classes as a way of describing hardware. More specifically all the class variables
are to be interpreted as hardware registers, this fits well as they are long term state elements.


This chapter focuses on the Python side of Pyha, while the next chapter gives details on how Pyha details are
converted to VHDL and how they can be synthesised.

Pyha tries to be as like to software programming as possible, some things written for soft vs hardware can give
suprisingly different results, this thesis tries to keep this in mind and hinglight such cases.

Target software people, make it easy to transition.

Introduces Pyha and shows how hardware design differs from software design.

Problem statement
-----------------



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


Background
----------

.. include:: background.rst




