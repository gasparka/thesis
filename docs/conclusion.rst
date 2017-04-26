Conclusion
==========

This work studied the feasability of implementing direct Python to VHDL converter.
Result is a way of converting Python object-oriented code into VHDL. It was described how this
conversion was made and what tradeoffs had to been taken.

In addition, fixed-point type was developed to support conversion of floating point models.
Automatix conversion to fixed-point was discussed.

Experimental compiler also bests the simulation/testing/verification side of HW development.
By providing simple functions that can run all simulations at once, this enables to use well known
unit test platforms like PyTest.

Lastly we showed that Pyha is already usable to convert some mdeium complexity designs, like
FSK demodulator, that was used on Phantom 2 stuff..


.. todo:: Moving VHDL programmers to this tool? problems?

Summary
-------

Limitations/future work
-----------------------

Long term goal is to implement more DSP blocks, especially by using GNURadio blocks as models.
In future it may be possible to turn GNURadio flow-graphs into FPGA designs, assuming we have matching FPGA blocks available.

Currently designs are limited to one clock signal, decimators are possible by using Streaming interface.
Future plans is to add support for multirate signal processing, this would involve automatic PLL configuration.
I am thinking about integration with Qsys to handle all the nasty clocking stuff.

Synthesizability has been tested on Intel Quartus software and on Cyclone IV device (one on BladeRF and LimeSDR).
I assume it will work on other Intel FPGAs as well, no guarantees.

Fixed point conversion must be done by hand, however Pyha can keep track of all class and local variables during
the simulations, so automatic conversion is very much possible in the future.

Integration to bus structures is another item in the wish-list. Streaming blocks already exist in very basic form.
Ideally AvalonMM like buses should be supported, with automatic HAL generation, that would allow design of reconfigurable FIR filters for example.

The initial goal of Pyha was to test ou how well could the software approach apply to the hardware world. As this
thesis shows that it is working well, the generated hardware output is unexpected to software people but resulting
output is the same. Pyha is an exploratory project, many things work and ca be done but still much improvements are needed
for example, inclusion of bus models like Wishbone, Avalon, AXI etc. Also currently Pyha works on single clock designs,
while its ok because mostly today desings are just many single clock designs connected with buses.



