Introduction
============

The most commonly used tools today for designing digital hardware are VHDL and :abbr:`SV (SystemVerilog)`.
:abbr:`SV (SystemVerilog)` is aggressively promoted by
the big :abbr:`EDA (electronic design automation)` companies (Cadence, Mentor, Synopsys)
along with :abbr:`UVM (Universal Verification Methodology)`.
In 2003, Aart de Geus, Synopsys CEO, stated that :abbr:`SV (SystemVerilog)`
will replace VHDL in 10 years :cite:`vhdl_dead`.
It is true that tool vendors have stopped improving VHDL support, but advancements are being made in the
open source community e.g. VHDL-2017 standard :cite:`vhdl_iee`. In addition, active development is done for the open
source simulator GHDL :cite:`ghdl`, Open Source VHDL Verification Methodology (OSVVM) :cite:`osvvm` and unit-testing library
VUnit :cite:`vunit`.
All of these advancements aim to ease the verification aspects while the synthesis part
has mostly stayed the same for the past 10 years.

Numerous projects exist that propose to use higher level :abbr:`HDL (hardware description language)`,
in order to raise the abstraction level.
For example, MyHDL turns Python into a hardware description and verification language :cite:`myhdlweb`,
or CλaSH :cite:`clash`, purely Haskell based functional language developed at University of Twente.
Recently Chisel :cite:`chisel` has been gaining some popularity,
it is an hardware construction language developed at UC Berkeley that uses Scala programming language,
providing functional and object-oriented features.

.. Still none of these tools have seen widespread adaption.

On the other front, :abbr:`HLS (high-level synthesis)` tools aim to automate the refinement from the algorithmic level to
:abbr:`RTL (register-transfer level)` :cite:`hls_overview`.
Lately the Vivado HLS, developed by Xilinx, has been gaining popularity. As of 2015, it is included in the
free design suite of Vivado (device limited).
The problem with HLS tools is that they are often promoted as direct C to RTL tools but in reality
often manual code transformations and guidelines are needed, in order
to archive reasonable performance :cite:`vivado_hls_case_study`.

The :abbr:`DSP (digital signal processing)` systems can be described in previously mentioned HLS or HDL languages,
but the most productive way is to use MATLAB/Simulink/HDLConverter flow, which allows
users to describe their designs in Simulink or MATLAB and use HDL convertible blocks provided by MATLAB or FPGA tool
vendor :cite:`borph`.

Problem statement
-----------------

There is no doubt that MATLAB based workflow offers a highly productive path from DSP models to hardware. However,
these tools can easily cost over tens of thousands of euros and often FPGA vendor tools are required, which adds
additional annual cost :cite:`borph`. Using these tools is not suitable for reproducible
research and is completely unusable for open source designs.
Thus, the designers must turn to alternative design flows; for example :cite:`blade_adsb` provides a
hardware implementation of an ADS-B (automatic dependent surveillance – broadcast) receiver. First, they did the prototyping
in the MATLAB environment, the working model was then translated to C for real-time testing and fixed-point modeling.
Lastly, the C model was manually converted to VHDL.

Given the limitations and drawbacks of existing solutions,
this thesis proposes Pyha, a new Python based hardware description language aimed at simplifying DSP hardware
development in an open-source [#pyharepo]_ manner.
Pyha raises the RTL design abstraction level by enabling sequential and object-oriented style.
DSP systems can be built by using the fixed-point type and semi-automatic conversion from floating point.
In addition, this work makes an effort to simplify the testing process of hardware systems by
providing better simulation interface for unit-testing.

.. [#pyharepo] Repository: https://github.com/gasparka/pyha

The basis of Pyha is Python, a general purpose programming language that is especially well suited for
rapid prototyping and modeling. Python has also found its place in scientific projects and academia by offering
most of what is familiar from MATLAB, free of charge. Scientists are already shifting from MATLAB to Python in order
to conduct research that is reproducible and accessible by everyone :cite:`matlab_to_python`.
:numref:`pypl_py_vs_mat` shows the popularity comparison (based on Google searches) of Python, MATLAB and C.
The positive trend of Python should soon push it past Java to the most popular programming language.

.. _pypl_py_vs_mat:
.. figure:: /img/pypl_py_vs_mat.png
    :align: center
    :figclass: align-center

    PYPL(PopularitY of Programming Language) :cite:`pypl`. Python 15.1%, C 6.9%, MATLAB 2.7%

Structure of the thesis
-----------------------

After gaining the context and problem statement in the current chapter, :numref:`2_pyha` presents the proposed hardware
description language Pyha. Next, :numref:`3_synthesis` develops the object-oriented VHDL model and deals with the
problem of converting Python to VHDL. :numref:`4_examples` shows how Pyha can be used to implement medium complexity
DSP systems and gives a comparison to existing tools. :numref:`5_conclusion` concludes this thesis and suggest ideas
for future work. The related work is introduced and discussed throughout this thesis,
thus no specific literature review chapter has been included.