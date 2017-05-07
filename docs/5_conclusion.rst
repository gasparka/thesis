.. _5_conclusion:

Conclusion
==========

The task of implementing DSP systems on hardware is often carried out by using high level tools, such as MATLAB. The problem with this approach is the the costly, thus not available for everyone and unsuitable for open-source designs. Other high-level tools are mostly based on C, that is not optimal for modeling purposes.
Given the limitations and drawbacks of existing solutions,
this thesis proposes Pyha, a new Python based hardware description language aimed at simplifying DSP hardware
development in an open-source manner.

Overview of main features of Pyha features have been given and shown that the proposed tool is usable for
describing hardware components. It was also demonstrated that Pyha supports
fixed point types and semi-automatic conversion from floating point types.
Pyha also provides good support for unit test and designs are debuggable.

Two use cases presented in :numref:`4_examples` show that the developed solution is already usable on solving
real life problems. Firstly the moving average filter was implemented and demonstrated as a matched filter.
The second example showed how the object-oriented nature of Pyha can be used for simple design reuse by
developing linear phase DC removal filter by reusing the moving average filter.

One major advantage of Pyha is that existing blocks can be connected together in a purely Python way, the
designer needs to know nothing about hardware design or underlying RTL implementation.

The comparison to other similar tools show that Pyha is comparing well. It may be usable for software programmers
to enter the field of hardware design more simply.
Programming hardware in Pyha looks very much like a regular Python program, that is one big drive on the C based
high-level synthesis tools.


Contributions
~~~~~~~~~~~~~

The contributions of this thesis are:

    * Hardware simulation and debugging in Python - major contribution, allows simulating and debugging hardware designs in Python domain;
    * Sequential object-oriented VHDL model - this work contributes the object-oriented VHDL design way that allows defining registers in sequential code;
    * Method for converting Python to X - the synhesisability has been gained by converting Python into VHDL, however the method could be used to convert into other languages aswell;
    * Fixed-point arithmetic library for Python - fixed-point library was developed to support cycle-accurate simulation with the converted VHDL code, however this library can be used for other purposes as well;
    * Simplified simulation functions - this work develops simulation functions that can execute multiple layers of simulations (Python, RTL, GATE) without any boilerplate code, this contribution significantly improves the unit-testing.

Future work
~~~~~~~~~~~

The technical part of Pyha has been developed by one person during the period of one year and while the work is already usable, it could see many enchantments. For example, the implementation of automatic conversion from floating-point to fixed-point, which is already supported by the simulation code. The current scope of the Python simulator has been limited to single clock domain, which is suitable for most DSP systems, lifting this limitation could make Pyha acceptable for wider community.
One of the most interesting enchantments would be the extension of the conversion process to support some HLS backend (such as VivadoHLS). This coud allow the designer an choice between describing the RTL with VHDL backend or higher-level abstarctions with HLS backend.

Long term work is to implement more DSP blocks in Pyha, so that complex systems could be built faster. In addtion the installation system should be improved to make Pyha easier to test for people that may be interested.


