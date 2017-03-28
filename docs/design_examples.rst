Design examples
===============
This chapter provides some example designs implemented in Pyha.

First example developes and moving-average filter.

First three examples will interatively implement
DC-removal system. First design implements an simple fixed-point accumulator. Second one builds upon this and implements
moving average filter. Lastly multiple moving average filters are chained to form a DC removal circuit.

Second example is an FIR filter, with reloadable switchable taps ?

Third design example shows how to chain togather already exsisting Pyha blocks to implement greater systems.
In this case it is FSK receiver. This examples does not go into details.


Moving Average
--------------
Use accumulator and shift register to develope Moving Average algorithm



Linear phase DC Removal
-----------------------
.. todo:: What is DC and why to remove it?


FIR filter
----------
Maybe skip this one?


FSK receiver
------------
Glue blocks togather...needs explanation...




`Pyhacores <https://github.com/petspats/pyhacores>`__ is a repository collecting cores implemented in Pyha,
for example it includes CORDIC, FSK modulator and FSK demodulator cores.

