Linear phase DC Removal
-----------------------
Direct conversion (homodyne or zero-IF) receivers have become very popular recently especially in the realm of
software defined radio. There are many benefits to direct conversion receivers,
but there are also some serious drawbacks, the largest being DC offset and IQ imbalances.
DC offset manifests itself as a large spike in the center of the spectrum.
This happens in direct conversion receivers due to a few different factors.
One is at the ADC where being off by a single LSB will yield a DC offset.
Another is at the output of the low-pass filters where any DC bias will propagate through.
The last is at the mixer where the local oscillator (LO) being on the center of the desired
frequency will leak through to the receiver. :cite:`bladerfdoc`


In frequency domain, DC offset will look like a peak near the 0 Hz. In time domain, it manifests as a constant
component on the hermonic signal.


.. _dc_removal_b:
.. figure:: img/dc_removal_b.png
    :align: center
    :figclass: align-center

    Basic DC removal using moving averager :cite:`dcremoval_lyons`

In :cite:`dcremoval_lyons` Rick Lyons investigates the feasability of using moving average algorithm as a DC removal
circuit, as shown on  :numref:`dc_removal_b`. This structure has a few problems, first of that it forces to use
moving averager with length not power of 2, that would significally complicate the hardware implmenentation.



.. _dc_single_freqz:
.. figure:: img/dc_single_freqz.png
    :align: center
    :figclass: align-center

    Frequency response of DC removal circuit with Moving average length 31

Second problem is seen on :numref:`dc_single_freqz`. Total ripple of the filter is up to 3 dB, that is 2 times of a difference.


.. _dc_removal_multi:
.. figure:: img/dc_removal_multi.png
    :align: center
    :figclass: align-center

    Removing DC with chained moving averagers :cite:`dcremoval_lyons`

Much better performance can be arcieved by chaining multiple stages of moving averaging, as shown in :numref:`dc_removal_multi`.
Chaining them up also helps the power of 2 problem.


.. _dc_quad_freqz:
.. figure:: img/dc_quad_freqz.png
    :align: center
    :figclass: align-center

    Frequency response of DC removal, 4 cascaded moving averagers

New frequency response can be observer on :numref:`dc_quad_freqz`. It is clear that the passband ripple has significantly reduced.
In addition the cutoff is sharper.




Implementation with Pyha
~~~~~~~~~~~~~~~~~~~~~~~~
Implementation is rather straight forward, as shown on :numref:`dc_removal_multi`, algorithm must run
input signal over multiple moving average filters (that we have already implemented in previous chapter) and then substract
the filter chain output of the delayed input signal.

.. code-block:: python
    :caption: Parametrizable DC-Removal implementation
    :name: dc_removal

    class DCRemoval(HW):
        def __init__(self, window_len, averagers):
            self.mavg = [MovingAverage(window_len) for _ in range(averagers)]

            # this is total delay of moving averages
            hardware_delay = averagers * MovingAverage(window_len)._delay
            self.group_delay = int(averagers * MovingAverage(window_len)._group_delay)
            total_delay = hardware_delay +  self.group_delay

            #registers
            self.input_shr = [Sfix()] * total_delay
            self.out = Sfix(0, 0, -17)

            # module delay
            self._delay = total_delay + 1

        def main(self, x):
            tmp = x
            for mav in self.mavg:
                tmp = mav.main(tmp)

            self.next.input_shr = [x] + self.input_shr[:-1]
            self.next.out = self.input_shr[-1] - tmp
            return self.out

        def model_main(self, x):
            # run signal over all moving averagers
            tmp = x
            for mav in self.mavg:
                tmp = mav.model_main(tmp)

            # subtract from delayed input
            return x[:-self.group_delay] - tmp[self.group_delay:]


:numref:`dc_removal` shows the Python implementation. Class is parametrized so that count of moving averagers and the
window length can be changed on definiton. Overall it is a pretty straigth forward Python code.

One thing to note that the :code:`model_main` and :code:`main` are nearly identical. That shows that Pyha has archived
one of the goals by simplifying hardware design portion.


Unit test for this module have not been listed as most of the testing is done in Ipython Notebook environment, as written
in some chapter Pyha is capable or collecting these tests for unit-testing. Can be seen here.


GATE level simulation
^^^^^^^^^^^^^^^^^^^^^

As written in some chapter, Pyha supports also rupports running GATE-level simulations
by integrating with Intel Quartus software.


.. _dc_removal_multi_rtl:
.. figure:: img/dc_removal_multi_rtl.png
    :align: center
    :figclass: align-center

    RTL view of simplified DC-Removal (Intel Quartus RTL viewer)


:numref:`dc_removal_multi_rtl` shows an simplified RTL view of the DC removal circuit,
it uses averages with length 4 to make RTL plottable.
There are 4 averages in total, leftover logic is the delay line and the final substractor.

Quartus project can be seen at repo [#dcrepo]_.


Resource usage
^^^^^^^^^^^^^^

Resorce usage is returned for the full size circuit, that is 4 chained moving averages with each having 32 taps.
Synhesizing with Quartus gave following resorce usage:


    - Total logic elements: 341 / 39,600 ( < 1 % )
    - Total memory bits:    2,736 / 1,161,216 ( < 1 % )
    - Embedded multipliers: 0 / 232 ( 0 % )

Maximum reported clock speed is 188 MHz ( standard compilation).


.. [#dcrepo] https://github.com/petspats/thesis/tree/master/examples/dc_removal/conversion




Conclusions
~~~~~~~~~~~

This chapter showed how to use Pyha to design an efficient, linar phase DC removal circuit. It is clear that making these
kind of designs is possible in Pyha and is not significantly harder that coding for the 'model'. Also it showed how
design reuse is archieved in Pyha, by reusing Moving average stuff.


Further improvements
^^^^^^^^^^^^^^^^^^^^

Problem with this filter is the delay on the signal path. In this case we used 4 filters with 32 taps, this gives group delay of
64 samples + hardware related delays. Possible solution for this is to remove the synchronization delay chain and subtract with
0 delay. This could work if assumed that DC offset is more or less stable.

