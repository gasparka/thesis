Introduction
============


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
providing sequential and object-oriented design model. Pyha is based on a OOP VHDL model that is also one
contribution of this thesis. Simulatable in Python. Fixed point and semi-automatic conversion.

One goal of this project is to make model based designs simpler, for this reason Pyha has been designed to provide
simple unit-testing simulation functions that can work against model.

Background
----------

Main way to desing digital hardware today is still VHDL and SystemVerilog(SV). SV is aggressively promoted by
the big EDA (Cadence, Mentor, Synopsys) along with Universal Verification Methodology (UVM).
At 2003, Aart de Geus, Synopsys CEO, has stated that SystemVerilog will replace VHDL in 10 years :cite:`vhdl_dead`.

Meanwhile the VHDL development is going on mostly in the open-source sphere where VHDL-2017
standard :cite:`vhdl_iee` is in development. In addition, active work is going on with VHDL tools, for example
open source VHDL simulator GHDL and unit-testing library VUnit:cite:`vunit`.
Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm`.

While these improvements work on the verification side, the synthesizable parts of VHDL and SV have stayed mostly
the same for the past 20 years.

Many projects propose to raise the RTL design abstraction level by using higher level programming
constructs. For example, MyHDL turns Python into a hardware description and verification language,
providing hardware engineers with the power of the Python ecosystem :cite:`myhdlweb`.
Recently Chisel :cite:`chisel` has been gaining some attention,
it is an hardware construction language developed at UC Berkeley that uses Scala programming language,
they providing concepts including object orientation, functional programming, parameterized types,
and type inference.
From purely functional languages, there is CλaSH, an haskell based HDL, developed at University of Twente,
that support higher order functions :cite:`clash`.
None of these languages have gained widespread acceptance. Why?

On the other front high-level syntehsis(HLS) tools aim to automate the refinement from the algorithmic level to RTL :cite:`hls_overview`.
Lately the Vivado HLS, developed by Xilinx, has been gaining some traction. As of 2015, it is included in the
free design suite of Vivado (device limited). It works with C, C++ or SystemC input.
Problem with HLS tools is that they are often promoted as direct C to RTL tools but in reality
often manual code transformations and guidlines are needed, in order
to archive reasonable performance :cite:`vivado_hls_case_study`. The designer must already know how the RTL works in
order to give these instructions. HLS tools are almost exclusevly based on C languages, another critisism has been
that C is not that far from Verilog/VHDL.

The DSP systems can be described in previously mentioned HLS or HDL languages,
but the most productive way is to use MATLAB/Simuling/HDLConverter flow, which allows
users to describe their designs in Simulink using HDL convertable blocks provided by MATLAB or Xilinx System Generator
:cite:`borph`.


Objective and scope
-------------------

The scope of this thesis is on DSP systems conversion. As mentioned in the previous section, this domain is largely dominated
by MATLAB products. One goal of this thesis is to to provide an open-source alternative to this.

There is no doubt that MATLAB based workflow offers an highly productive path from DSP models to hardware. However
these tools can easily cost over tens of thousands euros, in addition they often require FPGA vendor tools that can add
additional annual cost :cite:`borph`. Using these tools is not a good way for reproducible
research and is completely unusable for open-source designs.
Thus the designers must turn to alternative methods, for example :cite:`blade_adsb` provides an hardware implementation of
an ADS-B (automatic dependent surveillance – broadcast). First, they did the prototyping in the MATLAB environment, the
working model was then translated to C in order for real-time testing and fixed-point implementation. Lastly the C
model was manually converted to VHDL.
In this work, Pyha has been designed in a way that all of this workflow could be done in the Python domain.
Long term goal is to develop enough blocks that
that match the performance of GNURadio, so that flow-graphs could be simply converted to FPGA designs.

Python is general purpose programming language that is especially well suited for rapid prototyping.
Moreover, Python has also found its place in scientific projects and academia. Python offers most of what is
familiar from MATLAB and lately in the world on data science and machine-learning, Python is the go to tool.
Lately the scientific world has started shifting from MATLAB to Python, even full research groups are transitioning.
:cite:`matlab_to_python`. In domain of communication systems, all the GNURadio blocks have Python mappings.
:numref:`pypl_py_vs_mat` shows the popularity comparison (based on Google searches) of Python, MATLAB and C. Python is
the 2. popular language just behind Java with an rising trend.

.. _pypl_py_vs_mat:
.. figure:: /img/pypl_py_vs_mat.png
    :align: center
    :figclass: align-center

    PYPL(PopularitY of Programming Language) :cite:`pypl`. Python 15.1%, C 6.9%, MATLAB 2.7%

MyHDL is following the event-driven approach which is a trait of the classical HDL's. It features an function based
design that is very similar to Verilog processes. In general the synthesizable subset of MyHDL is very limited,
it has been found that the tool is more useful for high-level modeling purposes :cite:`jan_sim`.
Another package in the Python ecosystem is Migen, that replaces the event-driven paradigm with the notions of
combinatorial and synchronous statements :cite:`migenweb`. Migen can be considered as meta-programming in Python so
it is a bit complicated. Both Migen and MyHDL are more aimed at the control logic, neither implements the fixed-point
data type, that is a standard for hardware DSP designs.

This thesis introduces Pyha, a new Python based HDL, that was developed during the masters thesis program.
Pyha focuses clearly on the DSP systems by providing the fixed-point type and semi-automatic conversion from
floating point. In addition, this work makes an effort to simplify the testing process of hardware systems, by
providing one function that runs all the simulations.
Pyha aims to raise the abstraction level by using sequential object-oriented style, major advantage of this
is that existing blocks can be connected together in purely Pythonic way, the
designer needs to know nothing about the underlying RTL implementation.

Furthermore, this work introduces the sequential OOP VHDL model, that is developed to allow trivial conversion
from Python to VHDL.
Side contribution

Structure
---------

This thesis is divided into 3 chapters. In chapter :numref:`pyha_intro`, main concepts of Pyha are introduced.
Following chapter shows
First chapter of this thesis gives an overview of the developed tool Pyha and how it can be used for hardware design.
Follows the examples that show how Pyha can be used to relatively easly construct moving-average filter and by reusing
it the DC-removal filter.
Final chapter describes the one of the contribtutions of this thesis, the sequential VHDL OOP model and how Python
is converted to it.

