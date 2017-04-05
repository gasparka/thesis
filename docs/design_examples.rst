Case study
==========

This chapter provides some example designs implemented using the experimental compiler.

First example developes and moving-average filter.

First three examples will interatively implement
DC-removal system. First design implements an simple fixed-point accumulator. Second one builds upon this and implements
moving average filter. Lastly multiple moving average filters are chained to form a DC removal circuit.

Second example is an FIR filter, with reloadable switchable taps ?

Third design example shows how to chain togather already exsisting Pyha blocks to implement greater systems.
In this case it is FSK receiver. This examples does not go into details.


.. include:: moving_average.rst

.. include:: dc_removal.rst

.. include:: fsk_demodulator.rst

.. todo:: More stuff on results comparison..how good are they? etc. Yannic thinks this section will trigger
most of the questions in defence.



