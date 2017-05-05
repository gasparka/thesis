Abstract
========


Lately the digital designs made have raised in complexity.
There are now many open source tools that enable fast construction in software domain, for example
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

