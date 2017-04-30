Introduction
============

Pyha is an new Python based hardware description language focusing on simplifying development and testing process of DSP
systems. Pyha is an sequential HDL based on Python language. One part of the Pyha is the OOP VHDL model that helps
converting simply to hardware.
In a sense, Pyha can be considered as Python bindings for the object-oriented VHDL style, developed in this
thesis.

Main features:

    - Describe, test and simulate hardware in Python.
    - Integration to run RTL and GATE simulations.
    - Structured, sequential and object oriented designs
    - Fixed point support and semi-automatic conversion from floating point
    - Decent quality VHDL conversion output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)

Background
----------

High-level synthesis (HLS) improves design productivity by automating the refinement from
the algorithmic level to RTL :cite:`hls_overview`. In general the HLS world is dominated by C type languages, they
are popular in both in commercially and academically,
for example LegUp :cite:`hls_legup` is C based tool being developed at the University of Toronto.

Lately the Vivado HLS, developed by Xilinx, has been gaining some traction. As of 2015, it is included in the
free design suite of Vivado, however that is device limited.
Problem with HLS tools is that they often need manual code transformations and guidlines for the compiler in order
to archive reasonable performance :cite:`vivado_hls_case_study`.

On the other front there are projects that aim to raise the abstraction by improving the
hardware description lannguages (HDL), working on the RTL level. For example,
MyHDL is Python to VHDL/Verilog converter, first release dating back to 2003. It turns
Python into a hardware description and verification language,
providing hardware engineers with the power of the Python ecosystem :cite:`myhdlweb`.

Chisel is an open-source hardware construction language developed at UC Berkeley that uses Scala
programming language, they raise the level of hardware design abstraction by providing
concepts including object orientation, functional programming, parameterized types,
and type inference :cite:`chisel`.

DSP systems can be described in existing HLS and HDL languages, but currently the most popular ways is to use
MATLAB/Simuling/HDLConverter flow. Simulink based design flow has been reported to be used in Berkeley Wireless Research Center (BWRC) :cite:`borph`.
Using this design flow, users describe their designs in Simulink using blocks provided by Xilinx System Generator
:cite:`borph`.

Traditional HDL languages like VHDL and Verilog are not standing still either.
SystemVerilog (SV) is the new standard for Verilog language, it adds significant amount of new features to the language
:cite:`sysverilog`. Most of the added synthesizable features already existed in VHDL, making the synthesizable subset
of these two languages almost equal. In the design verification role, SystemVerilog(SV) is widely used in the chip-design industry.
The big EDA (Cadence, Mentor, Synopsys) are pushing SV with Open Verification Methodology (OVM).
At 2003, Aart de Geus, Synopsys CEO, has stated that SystemVerilog will replace VHDL :numref:`vhdl_dead`.

Meanwhile the VHDL development is going on mostly in the open-source sphere. Currently there is an VHDL-2017
standard in the works :cite:`vhdl_iee`. There are active work going on GHDL, that is open-source VHDL simulator.
In addtion, lately more tools have been released like Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm`
and VUnit :cite:`vunit`, that simplifies unit-testing in VHDL.


Objective and scope
-------------------

This thesis aims itself on the DSP systems. As mentioned in previos section, this domain is dominated by
the MATLAB products.
The tool, developed in the process of this thesis project, aims to provide an open-source alternative to the
mostly MATLAB based DSP to hw flows.

The problem with MATLAB based workflows is the toolset cost. MATLAB has cleverly divided their products into multiple
separade programs that each cost money. For HDL flow one would need MATLAB, Simulink, HDLCoder, HDLVerifier, DSPToolbox
... etc. The total price can easly go over 20000 EUR. In addition, the DSP flows require the use of FPGA Vendor synthesis
tools and DSP generators like Xilinx System Generator, that furthermore cost 5000 EUR annually.
Even if such kind of tooling could be afforded, the designs are not shareable. Thus this way to completely
unaceptable for open-source designs.

Thus the open-source designers must turn to alternative methods, for example
in :cite:`blade_adsb`, open-sourced a ADS-B decoder is implemented in hardware. In this work the authors first implement
the model in MATLAB for rapid prototyping. Next they converted the model into C and implemented it using fixed-point
arithmetic. Lastly they converted the C model to VHDL.

Pyha, developed in the process of this thesis project, aims to aims to bring all the development into the Python domain.

Python is especially suitable for writing the model, rapid prototyping and testing code.
Lately Python has been gaining traction over MATLAB in scinetific world, even full resource groups are transitioning
:cite:`matlab_to_python`. Python offers most of what MATLAB has, for example Numpy for numerical computing and
Scipy. Matplotlib for figures. In domain of communication systems all the GNURadio blocks have Python mappings.
Reproducible research, data and ML.

This thesis proposes an model based design with test-driven approach. Designing the model in Python language
is definetly easier considering there are now many libraries that can be used. Pyha includes functions
that help verification by automatically running all the simulations, asserting that model is equvalent to the
synthesis result, tests defined for model can be reused for RTL, model based verificaiton.
Pyha designs are also simulatable and debuggable in Python domain.
Pyha also provides an fixed-point type with semi-automatic conversion to it from the floating point values. The design
of Pyha also supports fully automatic conversion but currently this is left as a future work.

One major advantage of Pyha is that existing blocks can be connected together in purely Pythonic way, the
designer needs to know nothing about hardware design or underlying RTL implementation.

Pyha aims to raise the abstraction level by embracing the object-oriented style. That gives full power of RTL design
and good way to abstract away the complexity. Thing that makes Pyha special is that it is an fully
sequential language, which would classify it in the HLS category.
conclude that BlueSpec is at an intermediate abstraction level between a high level design
language (e.g. C) and RTL. Because of this, BlueSpec can handle both data-oriented and
control-oriented applications well. [daes]

One of the strentgths of this tool is that it converts to VHDL very simply. That is possible as the  synthesis tools
are already capable of elobarating (combinatory) sequnetial VHDL code. This thesis contributes the object-oriented
VHDL desing way that allows defining registers in sequential code. Thanks to that, the OOP Python code can be
simply converet to OOP VHDL code. This is big difference to HLS methods that have to go trough black magic to synthesise the
design. This may provide a bridge for VHLD ppl to move to Pyha.

Not limited to this. Long term goal of this project is to develop enough blocks
that match the performance of GNURadio, so that flow-grapsh could be simply converted to FPGA designs.

Structure
---------


