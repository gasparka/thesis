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

Shows how regular software constructs maps into hardware!

part of the value of this project is that it shows that even though stuff ends up as data flow stuff it is equal
to plain software code...this is the major difference.

Rather than forcing software construct to desciribe some hardware,
the Pyha way has been developed to just embrace what ever
is the output of the software approach.

Problem statement
-----------------

This work sets out to develop an alternative .


It is safe to say that Vivado HLS and others support everything that Pyha does and that makes sense they are devbelopd
by big companies and are years ahead.
However Pyha has some huge advantages:

    - Fully open source
    - No pragma TCL sctipting bullshit
    - Trival conversion to VHDL, no magic intended
    - Power of full RTL desing, but also abstractable by parametrizable classes (RLT and HLS in one thing)
    - Python vs C
    - Integration of model based designs to unit process
    - Testing simplification, share unit-tests for model and hardware!
    - Bridge to VHDL people, build castle and bridge

Biggest contribution is designed into the Pyha verification
processes, Pyha designs are **debuggable**, fully structured( no dataflow nonsense)
and provide functions to run all simulations.

One big goal is to enable simple connection of Pyha blocks,
so that for example GNURadio blocks could be mimiced.

Lazy fixed point types, simplify conversion. automatic
conversion ready design.

Objective/goal
--------------

Describe the implementation process, so that even if Pyha is not successful
something can be learned from it.

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

Others go for the dataflow way that is hard to understand for
normal porgrammers, Pyha explores the all.

This work tri

Design flow
~~~~~~~~~~~

The Suggested design flow for Pyha designs is model based development with test-driven approach.
This means that the unit tests should be developed to assert the performance of the model.
For unit tests use the Pyha ``simulate`` functions, so that the same tests can be later executed for hardware models.

The last step is to implement the synthesizable code (``main``); development is greatly simplified
if enough unit tests were collected while developing the model.

.. todo:: Needs more info, make figure, fixed point?


.. note:: The following examples in this chapter tend to ignore the model and unit-testing part and go straight to the
    hardware implementation, since this is the focus of this chapter.

Scope
-----
???
Focus on LimeSDR board and GnuRadio Pothos, frameworks.

Structure
---------
First chapter gives an short background about the context of this thesis and existing toolsets
that provide conversion from higher level languages to Gates.


Suggested design flow
---------------------

This text has left out the model implementation many times to focus on the hardware details.

.. todo:: move this to intro? make nice figure? Here say that we deviate from this to more focus on hardware side.

This text has built the examples in what way, but actually the optimal design flow should go as this:


    * make model
    * extract unit tests, same can be reused for hw sims
    * make hw using floats, handle register effects
    * convert to fixed point
    * unit tests pass? profit!

Siin võiks olla mingi figure?

Background
----------

.. todo:: TODO

.. a
    include:: background.rst




