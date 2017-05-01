Introduction
============


Abstract
--------

Lately the digital designs made have raised in complexity.
There are now many open-source tools that enable fast construction in software domain, for example
GNURadio and Pothos. These tools provide users the simple way of connectin blocks togather and designing
complex systems in this way. Downside of the software approach is that designs are slow to execute, for example
the Wify core that cannot repsond to ACK packets in real life. There are works in progress on GPU accelerators but
and RFNoC, but these are not suitable for embedded design.
liiga spetsiifiline?

In FPGA implementation is hard even though there exsists model.
Implementaton the DSP blocks for FPGAs is not easy as the design progess still makes use of old Verilog and VHDL
languages. Best way to do is MATLAB but it is expensive.

This thesis presents a new Python based hardware descripton language(HDL) called Pyha, that focuses on
simplifying development and testing process of DSP systems. Pyha aims to raise the abstraction level by
providing sequential and object-oriented design flow. Pyha is based on a OOP VHDL model that is also one
contribution of this thesis. Simulatable in Python. Fixed point and semi-automatic conversion.

One goal of this project is to make model based designs simpler, for this reason Pyha has been designed to provide
simple unit-testing simulation functions that can work against model.


Background
----------

Main way to desing digital hardware today is still VHDL and SystemVerilog(SV). SV is aggressively promoted by
the big EDA (Cadence, Mentor, Synopsys) along with Universal Verification Methodology (UVM).
At 2003, Aart de Geus, Synopsys CEO, has stated that SystemVerilog will replace VHDL :numref:`vhdl_dead`.

Meanwhile the VHDL development is going on mostly in the open-source sphere where people are working on an VHDL-2017
standard :cite:`vhdl_iee`. In addition, there is active work going on GHDL, that is open-source VHDL simulator.
Lately more useful tools for VHDL has been realeased like
Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm` and VUnit (unit testing in VHDL) :cite:`vunit`.

While these improvements work on the verification side, the synthesisable parts of VHDL and SV has stayed the same
for the past 20 years. Verification is big part on the other hand...

High-level synthesis (HLS) aims to improve design productivity by automating the refinement from
the algorithmic level to RTL :cite:`hls_overview`. In general the HLS world is dominated by the C type languages.
Many HLS languages have been developed in both commercially and academically.
For example LegUp :cite:`hls_legup` is C based HLS, being developed at the University of Toronto.
From commercial systems, lately the
Vivado HLS, developed by Xilinx, has been gaining some traction. As of 2015, it is included in the
free design suite of Vivado (device limited).
Problem with HLS tools is that they often need manual code transformations and guidlines for the compiler in order
to archive reasonable performance :cite:`vivado_hls_case_study`. Another problem with HLS languages is that often
they are promoted as simple C to RTL tools, but in reality to get reasonable results designer needs to understand the
RTL level reasonably well.

On the other front there are projects that raise the abstraction by improving the
hardware description lannguages (HDL). For example, MyHDL turns
Python into a hardware description and verification language,
providing hardware engineers with the power of the Python ecosystem :cite:`myhdlweb`.
Chisel is an open-source hardware construction language developed at UC Berkeley that uses Scala
programming language, they providing concepts including object orientation, functional programming, parameterized types,
and type inference :cite:`chisel`.

DSP systems can be described in existing HLS and HDL languages, but currently the most popular ways is to use
MATLAB/Simuling/HDLConverter flow :cite:`borph`.
Using this design flow, users describe their designs in Simulink using blocks provided by Xilinx System Generator
:cite:`borph`.


Objective and scope
-------------------

The scope of this thesis is on DSP systems. As mentioned in the previous section, this domain is largly dominated
by MATLAB products. One goal of this thesis is to to provide an open-source alternative to this.

There is no doubt that MATLAB based tools are powerful and get the job done. The problem with these kind of
workflows is the cost. Succesful workflow requires many tools from the MATLAB portfolio, like MATLAB, Simulink, HDLCoder
, HDLVerifier, DSPToolbox...etc. Price of this package can easly grow over tens of thousands euros. In addition,
often the FPGA vendor tools are required :cite:`borph`, like Xilinx System Generator, that costs ~5000 EUR annually.
Even if someone could afford these kind of tools, it is clear that most of the people have no such possibilities,
thus this flow is completely unacceptable for open-source designs.
Thus the designers must turn to alternative methods, for example
in :cite:`blade_adsb` an open-source a ADS-B decoder is implemented in hardware. First they implemented
the model in MATLAB for prototyping purposes. Next they converted the model into C and implemented it using fixed-point
arithmetic. Lastly they converted the C model to VHDL.

Pyha, developed in the process of this thesis project, aims to aims to bring all the development into the Python domain.
Long term goal of this project is to develop enough blocks
that match the performance of GNURadio, so that flow-grapsh could be simply converted to FPGA designs.

Python is especially well suited for rapid prototyping and testing.
Lately the scientific world has started shifting from MATLAB to Python, even full research groups are transitioning.
:cite:`matlab_to_python`. Python is free, open-source and offers most of what MATLAB has, for example Numpy package
for numerical computing. In domain of communication systems, all the GNURadio blocks have Python mappings.

In Python domain there already exist two projects that allow design of RTL in Python domain. The MyHDL is fully working
based on the event-driven approach. It does not provide a lot of abstraction. Migen is more following the
structured approach, the abstraction level is higher than of MyHDL, but it archieves this by using 'metaprogramming' in
Python, that greatly affects the readability and bla of code. Neither the MyHDL nor Migen provide an support for
fixed-point type, they are not DSP oriented.

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

Structure
---------

First chapter of this thesis gives an overview of the developed tool Pyha and how it can be used for hardware design.
Follows the examples that show how Pyha can be used to relatively easly construct moving-average filter and by reusing
it the DC-removal filter.
Final chapter describes the one of the contribtutions of this thesis, the sequential VHDL OOP model and how Python
is converted to it.

