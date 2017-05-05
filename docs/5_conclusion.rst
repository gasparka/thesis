Conclusion
==========

.. todo:: recall the problem first!

This work proposed a new Python based HDL language called Pyha. That is a sequential object-oriented HDL language.
Overview of Pyha features have been given and
shown that the tool is suitable to use with model based DSP systems. It was also demonstrated that Pyha supports
fixed point types and semi-automatic conversion from floating point types.
Pyha also provides good support for unit test and designs are debuggable.

Two case studies were presented. Firstly the moving average filter that was implemented in RTL level. Second example
demonstrated that blocks written in Pyha can be reused in pure Python way, developed linear phase DC removal filter
by reusing the implementation of moving average filter. Synthesisability has been demonstrated on a Cyclone IV
device.

Another contribution of this thesis is the sequential object-oriented VHDL model. This was developed to enable
simple conversion of Pyha to VHDL. One of the advantages of this work compared to other tools is the simplicity
of how it works.

In this work Pyha has been designed to add DSP related features to the Python conversion scope; this includes
fixed-point type and semi-automatic conversion from floating point. In addition, Pyha integrates the model to designs
and test functions simplification. Pyha includes functions
that help verification by automatically running all the simulations, asserting that model is equivalent to the
synthesis result, tests defined for model can be reused for RTL, model based verification.
Pyha designs are also simulatable and debuggable in Python domain.
The design of Pyha also supports fully automatic conversion but currently this is left as a future work.

Pyha is a fully sequential language that works on purely Python code. However Pyha resides in the RTL
level, allowing to define each and every register. In that sense Pyha is at somewhere between a HLS and a HDL
language. Pyha aims to raise the abstraction level by using the object-oriented style, so that the RTL details
can be easily abstracted away.
One major advantage of Pyha is that existing blocks can be connected together in purely Python way, the
designer needs to know nothing about hardware design or underlying RTL implementation.

Future perspectives are to implement more DSP blocks, especially by using GNURadio blocks as models. That may
enable developing a work-flow where GNURadio designs can easily be converted to FPGA.
In addition, the Pyha system could be improved to add automatic fixed point conversion and support for multiple
clock domains.

The design choices done in the process of Pyha design have focused on simplicity. The conversion process of
Python code to VHDL is straight-forward as the synthesis tools are already capable of elaborating sequential VHDL code.
This work contributes the object-oriented VHDL design way that allows defining registers in sequential code.
Thanks to that, the OOP Python code can be simply mapped to OOP VHDL code. Result is readable (keeps hierarchy) VHDL
code that may provide an bridge for people that already know VHDL.

