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




