Case studies
============

This chapter demonstrates that Pyha is already usable for real designs.
First designs an moving average filter and later reuses this for linear-phase DC removal filter.
Last chapter also compares the developed tool to other available toolsets.

.. todo:: fix

Pyha is based on the object-oriented design practices, this greatly simplifies the design reuse as the classes
can be used to initiate objects.
Another benefit is that classes can abstract away the implementation details, in that sense Pyha can become a
high-level synthesis (HLS) language.

Moving average filter
---------------------

The moving average (MA) is the easiest digital filter to understand and use.
It is optimal filter for for reducing random noise while retaining a sharp step response :cite:`dspbook`. In
communication systems, MA is widely used as an matched filter for rectangular pulses.
:numref:`moving_average_noise` shows an example of applying MA filter to reduce noise on harmonic signal.
Higher window length (averaged over more elements) reduces more noise but also increases the complexity and delay of
the filter (MA is a special case of FIR filter :cite:`dspbook`).


.. _moving_average_noise:
.. figure:: ../examples/moving_average/img/moving_average_noise.png
    :align: center
    :figclass: align-center

    Moving average filter applied on noisy signal

Good noise reduction performance can be explained by the frequency response of the MA filter (:numref:`mavg_freqz`),
showing that it is a low-pass filter. Passband width and stopband attenuation are controlled by the
window length.

.. _mavg_freqz:
.. figure:: ../examples/moving_average/img/moving_average_freqz.png
    :align: center
    :figclass: align-center

    Frequency response of moving average filter

MA filter is implemented by sliding sum, that is divided by the sliding window length. The division can be
carried out by a shift operation if divisor is power of two.
In addition, division can be performed on each sample instead of on the sum, that is ``(a + b) / c = a/c + b/c``. This
guarantees that the ``sum`` is always in the [-1;1] range and no saturation logic is needed.

:numref:`mavg-pyha` shows the MA filter implementation in Pyha. It is based on the sliding sum, that was implemented
in :numref:`ch_fp_sliding_adder`. Minor modifications are commented in the code.

.. code-block:: python
    :caption: MA implementation in Pyha
    :name: mavg-pyha
    :linenos:

    class MovingAverage(HW):
        def __init__(self, window_len):
            # calculate power of 2 value of 'window_len', used for division
            self.window_pow = Const(int(np.log2(window_len)))

            # 'overflow_style' turns the saturation off
            self.sum = Sfix(0, 0, -17, overflow_style=fixed_wrap)
            self.shr = [Sfix()] * window_len
            self._delay = 1

        def main(self, x):
            # divide by shifting
            div = x >> self.window_pow

            self.next.shr = [div] + self.shr[:-1]
            self.next.sum = self.sum + div - self.shr[-1]
            return self.sum

:numref:`mavg_rtl` shows the synthesized result of this work; as expected it looks very similar to the
sliding sum RTL schematics. In general, shift operators are hard to notice on the RTL schematics because they are implemented
by routing semantics.

.. _mavg_rtl:
.. figure:: ../examples/moving_average/img/mavg_rtl.png
    :align: center
    :figclass: align-center

    RTL view of moving average (Intel Quartus RTL viewer)



:numref:`mavg_matched` shows simulation results of MA filter used for matched filtering.
The plot on (a) shows digital input signal that is corrupted by noise.
Plot (b) shows that the MA with window length equal to samples per symbol can recover (optimal result) the
signal from the noise. Next the signal could be sampled to recover bit values (0.5=1, -0.5=0).

.. _mavg_matched:
.. figure:: ../examples/moving_average/img/moving_average_matched.png
    :align: center
    :figclass: align-center

    Moving average as matched filter. (b) noisy input signal, (a) averaged by 16, Pyha simulations


Linear-phase DC removal Filter
------------------------------

This design demonstrates how the object-oriented nature of Pyha can be used for simple design reuse by chaining
multiple MA filters to implement linear-phase DC removal filter.

Direct conversion (homodyne or zero-IF) receivers have become very popular recently especially in the realm of
software defined radio. There are many benefits to direct conversion receivers,
but there are also some serious drawbacks, the largest being DC offset and IQ imbalances :cite:`bladerfdoc`.
DC offset looks like a peak near the 0 Hz on the frequency response. In time domain it manifests as a constant
component on the harmonic signal.

In :cite:`dcremoval_lyons`, Rick Lyons investigates the use of moving average algorithm as a DC removal
circuit. This works by subtracting the MA output from the input signal. The problem of this approach is the
3 dB passband ripple. However, by connecting multiple stages of MA's in series, the ripple can be avoided
(:numref:`dc_freqz`) :cite:`dcremoval_lyons`.

.. _dc_freqz:
.. figure:: ../examples/dc_removal/img/dc_freqz.png
    :align: center
    :figclass: align-center

    Frequency response of DC removal filter (MA window length is 8)


The algorithm is composed of two parts. First, four MA's are connected in series, outputting the DC component of the
signal. Second, the MA's output is subtracted from the input signal, thus giving the signal without
DC component. :numref:`dc_removal` shows the Pyha implementation.


.. code-block:: python
    :caption: DC-Removal implementation
    :name: dc_removal

    class DCRemoval(HW):
        def __init__(self, window_len):
            self.mavg = [MovingAverage(window_len), MovingAverage(window_len),
                         MovingAverage(window_len), MovingAverage(window_len)]
            self.y = Sfix(0, 0, -17)

            self._delay = 1

        def main(self, x):
            # run input signal over all the MA's
            dc = x
            for mav in self.mavg:
                dc = mav.main(dc)

            # dc-free signal
            self.next.y = x - dc
            return self.y
        ...


This implementation is not exactly following that of :cite:`dcremoval_lyons`. They suggest to delay-match the
step 1 and 2 of the algorithm, but since the DC component is more more or less stable, this can be
omitted.

:numref:`dc_rtl_annotated` shows that the synthesis generated 4 MA filters that are connected in series,
output of this is subtracted from the input.

.. _dc_rtl_annotated:
.. figure:: ../examples/dc_removal/img/dc_rtl_annotated.png
    :align: center
    :figclass: align-center

    Synthesis result of ``DCRemoval(window_len=4)`` (Intel Quartus RTL viewer)


In a real application, one would want to use this component with larger ``window_len``. Here 4 was chosen to keep
the synthesis result simple. For example, using ``window_len=64`` gives much better cutoff frequency (:numref:`dc_comp`);
FIR filter with the same performance would require hundreds of taps :cite:`dcremoval_lyons`.

.. _dc_comp:
.. figure:: ../examples/dc_removal/img/dc_comp.png
    :align: center
    :figclass: align-center

    Comparison of frequency response


This implementation is also very light on the FPGA resource usage (:numref:`resource_usage`).

.. code-block:: text
    :caption: Cyclone IV FPGA resource usage for ``DCRemoval(window_len=64)``
    :name: resource_usage

    Total logic elements                242 / 39,600 ( < 1 % )
    Total memory bits                   2,964 / 1,161,216 ( < 1 % )
    Embedded Multiplier 9-bit elements	0 / 232 ( 0 % )


:numref:`dc_sim` shows the simulation results for input signal with DC component of +0.5,
the output of the filter starts countering the DC component until it is removed.

.. _dc_sim:
.. figure:: ../examples/dc_removal/img/dc_sim.png
    :align: center
    :figclass: align-center

    Simulation of DC-removal filter in the time domain


Comparison to other tools
-------------------------

MyHDL is following the event-driven approach which is a trait of the classical HDL's. It features an function based
design that is very similar to Verilog processes. In general the synthesizable subset of MyHDL is very limited,
it has been found that the tool is more useful for high-level modeling purposes :cite:`jan_sim`.
Another package in the Python ecosystem is Migen, that replaces the event-driven paradigm with the notions of
combinatorial and synchronous statements :cite:`migenweb`. Migen can be considered as meta-programming in Python so
it is a bit complicated. Both Migen and MyHDL are more aimed at the control logic, neither implements the fixed-point
data type, that is a standard for hardware DSP designs.

Overall i would say that both MyHDL and Migen are awesome tools, in the future merging of Pyha to either MyHDL or Migen
can defiantly be considered.

Pyha aims to raise the abstraction level by using sequential object-oriented style, major advantage of this
is that existing blocks can be connected together in purely Pythonic way, the
designer needs to know nothing about the underlying RTL implementation.

The design choices done in the process of Pyha design have focused on simplicity. The conversion process of
Python code to VHDL is straight-forward as the synthesis tools are already capable of elaborating sequential VHDL code.
This work contributes the object-oriented VHDL desing way that allows defining registers in sequential code.
Thanks to that, the OOP Python code can be simply mapped to OOP VHDL code. Result is readable (keeps hirarchy) VHDL
code that may provide an bridge for people that already know VHDL.

.. bibliography:: bibliography.bib
    :style: unsrt