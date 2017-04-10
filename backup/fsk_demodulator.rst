FSK demodulator
---------------

FSK is basicaly like FM, but with clear deviationf for 1 and 0.

This chapter gives an example on how to build FSK demodulator with Pyha. Goal of this chapter
is to show how previously built complex blocks can be connected togather in an easy way.


.. _fsk_spectrum:
.. figure:: img/fsk_spectrum.png
    :align: center
    :figclass: align-center

    Sample FSK spectrum, 1e5 deviation.


:numref:`fsk_spectrum` show a spectrum of sample FSK spectrum. Carried data is :code:`[1, 0, 1, 0, 0]`.
As can be seen, for bit 1 there is positive frequency content ant fro bit 0 negative (relative to carrier).

In the process of demodulation, we would like to recover the bits from the frequency content. There are
multiple ways to demodulate FM signal, for example Baseband Delay Demodulator (also known as
quadrature demodulator) and using Phase-Locked loop :cite:`fskthesis`.

Most popular choice in the SDR world is the Quadrature Demodulaotr, since signal is already at
baseband and it does not contain feedback loops. :cite:`fskthesis` shows that this demodulator
has better performance comparet to PLL method.


Quadrature Demodulator involves some complex arithmetic like complex multiplyer and arcsin calculation.
The purpos of this chapter is not to go into details but rather show how such kind of block
could be used in Pyha.

.. _fsk_quad_demod:
.. figure:: img/fsk_quad_demod.png
    :align: center
    :figclass: align-center

    Output of Qaudrature Demodulator


:numref:`fsk_quad_demod` show the Quadrature Demodulator output where input is the signal
shown in :numref:`fsk_spectrum`. Note that the result looks already like digital signal.
Result is a bit noisy as the input was noisy aswell.

Next step in the demodulator path is matched filtering. Since we are dealing with squared signals
we can use the moving average algorithm for this purpose.

.. :todo:: Output picture has sim offset, sucks.

Implementation with Pyha
~~~~~~~~~~~~~~~~~~~~~~~~

Implementation is rather straight forward, as shown on :numref:`dc_removal_multi`, algorithm must run
input signal over multiple moving average filters (that we have already implemented in previous chapter) and then substract
the filter chain output of the delayed input signal.

.. code-block:: python
    :caption: Parametrizable demodulator
    :name: fsk_demodulator_code

    class FSKDemodulator(HW):
        def __init__(self, deviation, fs, sps):
            self.demod = QuadratureDemodulator(self.gain)
            self.match = MovingAverage(sps)
            self._delay = self.demod._delay + self.match._delay

        def main(self, input):
            demod = self.demod.main(input)
            match = self.match.main(demod)
            return match

        def model_main(self, input_list):
            demod = self.demod.model_main(input_list)
            match = self.match.model_main(demod)
            return match


:numref:`fsk_demodulator_code` shows the Python implementation.
Overall it is a pretty straigth forward Python code. Quadrature demodulator and Moving average
are defined in the constructor bit, then 'main' and 'model main' make use of them.

One thing to note that the :code:`model_main` and :code:`main` are nearly identical. That shows that Pyha has archived
one of the goals by simplifying hardware design portion.


Unit test for this module have not been listed as most of the testing is done in Ipython Notebook environment, as written
in some chapter Pyha is capable or collecting these tests for unit-testing. Can be seen here.

Resource usage
^^^^^^^^^^^^^^
RTL is too big to include a screenshot, project can be opened here..

Synhesizing with Quartus gave following resorce usage:


    - Total logic elements: 1,499 / 39,600 ( 4 % )
    - Total memory bits:    36 / 1,161,216 ( < 1 % )
    - Embedded multipliers: 10 / 232 ( 4 % )

Maximum reported clock speed is 173 MHz ( standard compilation).


.. [#dcrepo] https://github.com/petspats/thesis/tree/master/examples/dc_removal/conversion


Conclusions
~~~~~~~~~~~

This chapter showed how to use existing Pyha components to synthesise complex system.


Further improvements
^^^^^^^^^^^^^^^^^^^^
Next step would be to add some sort of clock recovery component in order to sample te bits.

