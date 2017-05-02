Summary
=======

This work introduced new Python based HDL language called Pyha. That is an sequential object-oriented HDL language.
Overview of Pyha features have been given and
shown that the tool is suitable to use with model based DSP systems. It was also demonstrated that Pyha supports
fixed point types and semi-automatic onversion from floating point types.
Pyha also provides good support for unit test and designs are debuggable.

Two case studies were presented, first the moving average filter that was implemented in RTL level. Second example
demonstrated that blocks written in Pyha can be reused in pure Python way, developed linear phase DC removal filter
by reusing the implementation of moving average filter. Synthesisability has been demonstrated on Cyclone IV
device (BladeRF).

Another contribution of this thesis is the sequential object-oriented VHDL model. This was developed to enable
simple conversion of Pyha to VHDL. One of the advantages of this work compared to other tools is the simplicyty
of how it works.

.. Lastly we showed that Pyha is already usable to convert some mdeium complexity designs, like
FSK demodulator, that was used on Phantom 2 stuff..

Future perspectives are to implement more DSP blocks, especially by using GNURadio blocks as models. That may
enable developing an work-flow where GNURadio designs can easily be converted to FPGA.
In addition, the Pyha system could be improved to add automatic fixed point conversion and support for multiple
clock domains.

.. Integration to bus structures is another item in the wish-list. Streaming blocks already exist in very basic form.
Ideally AvalonMM like buses should be supported, with automatic HAL generation, that would allow design of reconfigurable FIR filters for example.



In this work Pyha has been designed to add DSP related features to the Python conversion scope, this includes
fixed-point type and semi-automatic conversion from floating point. In addition Pyha integrates the model to designs
and test functions simplification. Pyha includes functions
that help verification by automatically running all the simulations, asserting that model is equvalent to the
synthesis result, tests defined for model can be reused for RTL, model based verificaiton.
Pyha designs are also simulatable and debuggable in Python domain.
.The design of Pyha also supports fully automatic conversion but currently this is left as a future work.

Pyha is a fully sequential language that works on purely Python code. However Pyha resides in the RTL
level, allowing to define each and every register. In that sende Pyha is at somewhere between the HLS and HDL
language. Pyha aims to raise the abstraction level by using the object-oriented style, so that the RTL details
can be easily abstracted away.
One major advantage of Pyha is that existing blocks can be connected together in purely Python way, the
designer needs to know nothing about hardware design or underlying RTL implementation.

The design choices done in the process of Pyha design have focused on simplicity. The conversion process of
Python code to VHDL is straight-forward as the synthesis tools are already capable of elaborating sequential VHDL code.
This work contributes the object-oriented VHDL desing way that allows defining registers in sequential code.
Thanks to that, the OOP Python code can be simply mapped to OOP VHDL code. Result is readable (keeps hirarchy) VHDL
code that may provide an bridge for people that already know VHDL.

Limited to one clock domain?
In some seneses the Python part could be considers as Python binding to VHDL OOP model.
Convert to HLS langauge instead of VHDL, then the designer could choose to to either design for RTL or HLS, this is
more as an futures perspective, this thesis works only with the RTL part.

Long term goal of the project is to develop enough blocks that are functionally equal to GNURadio blocks, so that
flow-graphs could be converted to FPGA designs, thus providing an open-source alternative for Simulink
based flows.

