.. _5_conclusion:

Conclusion
==========

The task of implementing digital signal processing (DSP) on hardware is often carried out by using high level tools
such as MATLAB, which offers good productivity. The problem is that such tools can be costly, thus not available
for everyone and open-source designs. Other high-level C based tools may not be suitable for modeling.
Given the limitations and drawbacks of existing solutions,
this thesis proposes Pyha, a new Python based hardware description language aimed at simplifying DSP hardware
development in an open-source manner.

Overview of main features of Pyha features have been given and shown that the proposes tool is usable for
describing hardware components. It was also demonstrated that Pyha supports
fixed point types and semi-automatic conversion from floating point types.
Pyha also provides good support for unit test and designs are debuggable.

Two use cases presented in :numref:`4_examples` show that the developed solution is already usable on solving
real life problems. Firstly the moving average filter was implemented and demonstrated as a matched filter.
The second example showed how the object-oriented nature of Pyha can be used for simple design reuse,
developed linear phase DC removal filter by reusing the moving average filter.
Synthesisability was demonstrated on a Cyclone IV device.
One major advantage of Pyha is that existing blocks can be connected together in purely Python way, the
designer needs to know nothing about hardware design or underlying RTL implementation.

The comparison to other similiar tools show that Pyha is comparing well. It may be usable for software programmers
to enter the field of hardware design more simply.

Contributions
~~~~~~~~~~~~~

.. this section is inspired by thesis_C_Baaij.pdf

This work contributes the object-oriented VHDL design way that allows defining registers in sequential code.

The main contributions of this thesis are:

    - Sequential object-oriented VHDL model -
    - New Python based object-oriented HDL tool -

Future work
~~~~~~~~~~~

The technical part of Pyha has been developed in the period of last year by one person, thus not everything
has been fully finished. For example the automatic conversion from floating-point to fixed-point, while the
conversion process is designed to allow for this. In addition currently the scope of Python modules are on
single clock systems, which is not a huge constraint on DSP systems.

One of the most interesting enchantments would be to extend the conversion process to convert the Python code
into a HLS language instead (such as VivadoHLS). then the designer could choose to to either design for RTL or HLS.

Long term work is to implement more DSP blocks, so that in the future there
could be possible GUI based connect stuff program.

Integration to bus structures is another item in the wish-list. Streaming blocks already exist in very basic form.
Ideally AvalonMM like buses should be supported, with automatic HAL generation, that would allow design of reconfigurable FIR filters for example.


