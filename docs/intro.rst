Introduction
============

Pyha is an new Python based hardware description language focusing on simplifying the testing process and DSP
systems. In a sense, Pyha can be considered as Python bindings for the object-oriented VHDL style, developed in this
thesis.

Main features:

    - Simulate hardware in Python. Integration to run RTL and GATE simulations.
    - Structured, all-sequential and object oriented designs
    - Fixed point type support(maps to `VHDL fixed point library`_)
    - Semi-automatic conversion to fixed-point
    - Decent quality VHDL conversion output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)
    - Tools to simplify verification

Background
----------

High level synthesis (HLS) languages try to raise the abstraction by enabling writing hardware algortihms in
software ways. HLS tools must do complex analysis of input code to match the RTL output, data dependencies and such.
In general the HLS world is dominated by C type languages. There have been countless numbers of them
both in commercially and academically, for example LegUp is C based tool being developed at the University of Toronto.

In commercial front lately the Vivado HLS have gained some traction, as of Vivado (2015.4) software release
it is included in the free downloadable set. It works with C, C++ or SystemC inputs, that can be rather confsing..
In general Xilinx has reportet great adoption for this tools, however there are also people who are sceptical about this.
Downside of the HLS languages is that they use C language that is not expressive for the job, witch starts the need
for macro statements to instrcut the synthesis process. Xilinx even suggest in using TCL (long dead scripting language)
in cororation with VivadoHLS.

On the other front there are projects that aim to enchance the hardware description languages(HDL). Difference between
the HDL and HLS is that the former exactly describe the hardware while the HLS derive the hardware from higher level
description. Here are MyHDL, MyHDL is Python to VHDL/Verilog converter, first release dating back to 2003. It turns
Python into a hardware description and verification language,
providing hardware engineers with the power of the Python ecosystem :cite:`myhdlweb`.
MyHDL has been used in the design of multiple ASICs and numerious FPGA projects :cite:`myhdlfelton`.

Recently a new Scala based HDL has been gaining traction, called Chisel.
Chisel is an open-source hardware construction language developed at UC Berkeley that uses Scala
programming language, they raise the level of hardware design abstraction by providing
concepts including object orientation, functional programming, parameterized types,
and type inference :cite:`chisel`.
Recently the Chisel has introcuded version 3, that is kind of a rewrite. FIRRTL!

.. todo:: Clash...or remove?

DSP systems in general fall you yet another product line where MATLAB is the boss, very expensive.
In :cite:`blade_adsb`, open-sourced a ADS-B decoder, implemented in hardware. In this work the authors first implement
the model in MATLAB for rapid prototyping. Next they converted the model into C and implemented it using fixed-point
arithmetic. Lastly they converted the C model to VHDL.

More common approach is to use MATLAB stack for also the fixed-point simulations and for conversion to VHDL.
Also Simulink can be used.

Simulink based design flow has been reported to be used in Berkeley Wireless Research Center (BWRC) :cite:`borph`.
Using this design flow, users describe their designs in Simulink using blocks provided by Xilinx System Generator
:cite:`borph`.

The problem with such kind of design flow is that it costs alot. Only the MATLAB based parts can easly cost close
to 20000 EUR, as the packages depend on eachother. For example for reasonable flow user must buy the Simulink software
but that also requires the MATLAB software, in addtion to do DSP, DSP toolbox is needed.. etc.
Also the FPGA vendor based tools, like Xilinx System Generator are also expensive and billed annually.

Traditional HDL languages like VHDL and Verilog are not standing still either.
SystemVerilog (SV) is the new standard for Verilog language, it adds significant amount of new features to the language
:cite:`sysverilog`. Most of the added synthesizable features already existed in VHDL, making the synthesizable subset
of these two languages almost equal. In that sense it is highly likely that ideas developed in this chapter could
apply for both programming languages.

On the same time the traditional VLSI languages are not standing still -> VHDL OSVM, UNIT TESTS etc..

In the design verification role, SystemVerilog is widely used in the chip-design industry.
The three largest EDA vendors (Cadence, Mentor, Synopsys) have incorporated SystemVerilog into
their mixed-language HDL-simulators.
Although no simulator can yet claim support for the entire SystemVerilog LRM, making testbench interoperability a challenge,
efforts to promote cross-vendor compatibility are underway. In 2008, Cadence and Mentor released the Open Verification Methodology,
an open-source class-library and usage-framework to facilitate the development of re-usable testbenches and canned
verification-IP. Synopsys, which had been the first to publish a SystemVerilog class-library (VMM), subsequently
responded by opening its proprietary VMM to the general public. Many third-party providers have announced or already
released SystemVerilog verification IP. [WIKIST]
In general the big EDA is pushing the SystemVerilog hard, Aart de Geus, Synopsys CEO, has stated that
SystemVerilog will replace VHDL :numref:`vhdl_dead`. That was in 2003.

Meanwhile the VHDL development is going on mostly in the open-source sphere. Currently there is an VHDL-2017
standard in the works :cite:`vhdl_iee`. There are active work going on GHDL, that is open-source VHDL simulator.
In addtion, lately more tools have been released like Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm`
and VUnit, that simplifies unit-testing in VHDL.


Objective
---------

The tool, designed in the process of this thesis, aims to provide an open-source alternative to the
mostly MATLAB based DSP flows. Not limited to this. Long term goal of this project is to develop enough blocks
that match the performance of GNURadio, so that flow-grapsh could be simply converted to FPGA designs.

Main design method in Pyha is model based design with test-driven approach. Designing the model in Python language
is definetly easier considering there are now many libraries that can be used. Pyha includes functions
that help verification by automatically running all the simulations, asserting that model is equvalent to the
synthesis result, tests defined for model can be reused for RTL, model based verificaiton.
Pyha designs are also simulatable and debuggable in Python domain.
Pyha also provides an fixed-point type with semi-automatic conversion to it from the floating point values. The design
of Pyha also supports fully automatic conversion but currently this is left as a future work.

Pyha aims to raise the abstraction level by embracing the object-oriented style. That gives full power of RTL design
and good way to abstract away the complexity. Thing that makes Pyha special is that it is an fully
sequential language, which would classify it in the HLS category.

One of the strentgths of this tool is that it converts to VHDL very simply. That is possible as the  synthesis tools
are already capable of elobarating (combinatory) sequnetial VHDL code. This thesis contributes the object-oriented
VHDL desing way that allows defining registers in sequential code. Thanks to that, the OOP Python code can be
simply converet to OOP VHDL code. This is big difference to HLS methods that have to go trough black magic to synthesise the
design.

It is safe to say that Vivado HLS and others support everything that Pyha does and that makes sense they are devbelopd
by big companies and are years ahead.
However Pyha has some advantages:

    - Trival conversion to VHDL, no magic intended
    - Power of full RTL desing, but also abstractable by parametrizable classes (RLT and HLS in one thing)
    - Python vs C
    - Integration of model based designs to unit process
    - Testing simplification, share unit-tests for model and hardware!
    - Bridge to VHDL people, build castle and bridge
    - This tool actually shows how it works

While other high level tools convert to very low-level VHDL, then Pyha takes and different approach by
first developing an feasible model in VHDL and then using Python to get around VHDL ugly parts.

Sell this!!!. Has good integration for model, is debuggable. Running simulations is extreamly
easy. Good fixed point support. Modern software dev tools in hw.

.. todo::
    Comparison to tools already in Python domain?
    Why do it?
    SELL
    Key feature is simplicity?
