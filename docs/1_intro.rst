Introduction
============

Main tools today for designing digital hardware are VHDL and SystemVerilog (SV). SV is aggressively promoted by
the big EDA (Cadence, Mentor, Synopsys) along with Universal Verification Methodology (UVM).
At 2003, Aart de Geus, Synopsys CEO, has stated that SV will replace VHDL in 10 years :cite:`vhdl_dead`.
It is true that tool vendors have stopped enchanting VHDL support, even so the development is going on in the
open-source sphere,
where VHDL-2017 standard :cite:`vhdl_iee` is in the development. In addition, active development is going on open
source simulator GHDL, Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm` and unit-testing library
VUnit:cite:`vunit`.
All the improvements the traditional languages receive aim to ease the verification task,
the synthesizable parts of VHDL and SV have stayed mostly the same for the past 10 years.

Numerous projects exist that propose to use higher level HDL languages in order to raise the abstraction level.
For example, MyHDL turns Python into a hardware description and verification language :cite:`myhdlweb`.
Or CλaSH :cite:`clash`, purely Haskell based functional language developed at University of Twente.
Recently Chisel :cite:`chisel` has been gaining some traction,
it is an hardware construction language developed at UC Berkeley that uses Scala programming language,
providing functional and object-oriented features.
Still none of these tools have seen widespread adaption.

On the other front, high-level synthesis(HLS) tools aim to automate the refinement from the algorithmic level to RTL
:cite:`hls_overview`.
Lately the Vivado HLS, developed by Xilinx, has been gaining popularity. As of 2015, it is included in the
free design suite of Vivado (device limited).
Problem with HLS tools is that they are often promoted as direct C to RTL tools but in reality
often manual code transformations and guidlines are needed, in order
to archive reasonable performance :cite:`vivado_hls_case_study`. The designer must already know how the RTL works in
order to give these instructions.

The DSP systems can be described in previously mentioned HLS or HDL languages,
but the most productive way is to use MATLAB/Simuling/HDLConverter flow, which allows
users to describe their designs in Simulink or MATLAB and using HDL convertible blocks provided by MATLAB or FPGA tool
vendor :cite:`borph`.

Problem statement
-----------------

There is no doubt that MATLAB based workflow offers an highly productive path from DSP models to hardware. However
these tools can easily cost over tens of thousands euros, often FPGA vendor tools are required that add
additional annual cost :cite:`borph`. Using these tools is not suitable for reproducible
research and is completely unusable for open-source designs.
Thus the designers must turn to alternative design flows, for example :cite:`blade_adsb` provides an
hardware implementation of an ADS-B (automatic dependent surveillance – broadcast). First, they did the prototyping
in the MATLAB environment, the working model was then translated to C for real-time testing and fixed-point modeling.
Lastly the C model was manually converted to VHDL.

This thesis introduces Pyha, a new Python based HDL developed during the masters thesis program, with an goal
to provide open-source alternative for the MATLAB based flows.
Pyha raises the RTL design abstraction by enabling sequential and object-oriented style.
DSP systems can be built by using the fixed-point type and semi-automatic conversion from floating point.
In addition, this work makes an effort to simplify the testing process of hardware systems by
providing better simulation interface for unit-testing.

Basis of Pyha is the Python, a general purpose programming language that is especially well suited for
rapid prototyping and modeling. Python has also found its place in scientific projects and academia by offering
most of what is familiar from MATLAB, free of charge. Scientist are already shifting from MATLAB to Python in order
to conduct research that is reproducible and accessible by everyone :cite:`matlab_to_python`.
:numref:`pypl_py_vs_mat` shows the popularity comparison (based on Google searches) of Python, MATLAB and C.
Python is far ahead and the only one with positive trend.

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


Furthermore, this work introduces the sequential OOP VHDL model, that is developed to allow simpler conversion
from Python to VHDL.
Side contribution

Structure
---------

This thesis is divided into 3 chapters. In chapter 1, main concepts of Pyha are introduced.
Following chapter shows
First chapter of this thesis gives an overview of the developed tool Pyha and how it can be used for hardware design.
Follows the examples that show how Pyha can be used to relatively easly construct moving-average filter and by reusing
it the DC-removal filter.
Final chapter describes the one of the contribtutions of this thesis, the sequential VHDL OOP model and how Python
is converted to it.
