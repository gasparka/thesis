A sequential circuit, on the other hand, has an internal
state, or memory. Its output is a function of current input as well as the internal state. The
internal state essentially “memorizes” the effect of the past input values. The output thus is
affected by current input value as well as past input values (or the entire sequence of input
values). That is why we call a circuit with internal state a sequential circuit.
:cite:`chu_vhdl`


A combinational circuit, by definition, is a circuit whose output, after the initial transient
period, is a function of current input. It has no internal state and therefore is “memoryless”
about the past events (or past inputs) :cite:`chu_vhdl`. In other words, combinatory circuits have
no registers, i like to call it 'stuff between registers'.
Arguably better name for combinatory logic is 'stuff between two registers'.



Structured programming in VHDL
------------------------------

While VHDL is mostly known as a dataflow programming, it is actually derived from ADA programming lanugage,
where it inherits strong structurial semantics. As shown by :cite:`structvhdl_gaisler`,
using these higher-level programming constructs can be used to infer combinatory logic.


.. todo:: May be better to just delete this section as it has funnctionally bad example. + it used function instead
    of prcedure. However it is useful as it shows in a simple way how functions go to combinatory logic.

.. code-block:: vhdl
    :caption: Combinatory
    :name: comb-vhdl

    function main(a: integer) return integer is
        variable mul, acc: integer;
    begin
        mul := a * 123;
        acc := acc + mul;
        return acc;
    end function;


:numref:`comb-vhdl` show the MAC function in VHDL. It is functionally broken as the acc should save state
outside of the function.

.. _comb_mac_rtl:
.. figure:: img/comb_mac_rtl.png
    :align: center
    :figclass: align-center

    RTL of comb MAC (Intel Quartus RTL viewer)


Synthesisying this results in a RTL shown in :numref:`comb_mac_rtl`. Good news is that
it has all the required arithmetic elements. However, as expected it lacks the registers, rendering the design
functionally incorrect.

Benefit here is that the function in VHDL is very similiar to the Python one, conversion process would
surely be simple. Another result is that VHDL and Python have same result for local variables.


Pipelining
~~~~~~~~~~

In hardware class variables must be often used when we actually dont need to store anything, the need rises from
the need for clock speed.

The block adder built in last section is quite decent, in sense that it is following the digital design approach by
having all stuff between registers.

The synthesis result gives that the maximum clock rate for this design is ~170 Mhz.
Imagine that we want to make this design generic, that is make the summing window size easily changeable. Then we will
see problems, for example going from 4 to 6 changes the max clock speed to ~120 Mhz. Chaning it to 16 gives
already only ~60 Mhz max clock.

.. todo:: appendix for FPGA chip used

.. _rtl_6_critical:
.. figure:: ../examples/block_adder/img/rtl_6_critical.png
    :align: center
    :figclass: align-center

    Critical path RTL


In that sense, it is not a good design since reusing it hard.

The obious solution of adding registes between adder stages would not actually work, when delays come into play
stuff gets complicated!

.. todo:: CONFUSING!!! adding registers on adders WONT work, need to go transposed solution.

.. todo:: Arvan,et pipelining on liiga raske teema, parem loobuda sellest?

In general we expect all the signals to start from a register and end to a register. This is to avoid all the
analog gliches that go on during the transimission process.
The delay from one register to
other determines the maximum clock rate (how fast registers can update). The slowest register pair determines the
delay for the whole design, weakest link priciple.

While registers can be used as class storage in software designs, they are also used as checkpoints on the
signal paths, thus allowing high clock rates.

In Digital signal processing applications we have sampling rate, that is basically equal to the clock rate. Think that
for each input sample the 'main' function is called, that is for each sample the clock ticks.


Registers also used for pipelines.
Sometimes registers only used for delay.

This could have example on pipelining issues, like delay matching?

Pyha way is to register all the outputs, that way i can be assumed that all the inputs are already registered.

Every rule has exeception, for example delays on the feedback paths (data flows backward) are pure evil.

Pipelining is something that does not exist in software world.

Why bother with pipelining?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

It determines the maximum samplerate for the design. In that sense, designs with low max sample rate are not easly
reusable, so pipelines mean reusability. Remember that hardware work on the weakest link principe, lowest clock rate
determines the whole clock rate for the design.

But why pipeline over lets say 20Mhz, thats the largest Wifiy band. One point is that it is just easier to
add register after each arithmetic operation, than to calculate in mind that maybe we can do 3 or 4 operations berofer
register.

Retiming?

Another point is clock TDA. Run the design on higher clock rate to save resources. Imagine Wify receiver for 20M band,
this has to have sample rate of 20M. But when we run it with say 100M we can push 4 different wify signals trough the same
circuit. That however depends on the synthesys tool ability to share common resources.

Negatives of pipelining is that the delay of the block is not constant in all configurations also pipelining increases
resource usage.

Also algorithm becomes more complex and harder to understand.


The only motivation for using SystemVerilog over VHDL is tool support. For example Yosys :cite:`yosys`, an open-source
synthesis tool, supports only Verilog; however, to the best of my knowledge it does not yet support SystemVerilog features. There have
been also some efforts in adding a VHDL frontend :cite:`vhdl_yosys`.



Simulations results (:numref:`block_adder_sim`) show that the hardware design behaves exactly as the software model.
Note that the class sets ``self._delay=1`` to compensate for the register delay.

.. _block_adder_sim:
.. figure:: ../examples/block_adder/img/sim.png
    :align: center
    :figclass: align-center

    Simulation results for ``OptimalSlideAdd(window_len=4)``


..  Class variables can be used to define registers. In Pyha, class variables must be assigned to
    ``self.next`` as this mimics the **delayed** nature of registers.