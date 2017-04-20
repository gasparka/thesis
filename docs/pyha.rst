Introduction to Pyha and hardware design
========================================

This chapter introduces the main contribution of this thesis, Pyha, that is a way of designing digital hardware using
Python programming language.

First part of this chapter gives an short introduction to the hardware design with Pyha. Just as Pyha tries to bring
software world practices to hardware world, i trie to write this chapter in readable way to software people.

This chapter is written in mind software developers that could start hardware programming, for that reason
many references and abstractsions are made.

The second half of this chapter shows off Pyha features for fixed point design, by gradually designing an FIR filter.


Introduction
------------

Pyha is a tool that allows writing of digital hardware in Python language. Currently it focuses mostly on the DSP
applications.

Main features:

    - Simulate hardware in Python. Integration to run RTL and GATE simulations.
    - Structured, all-sequential and object oriented designs
    - Fixed point type support(maps to `VHDL fixed point library`_)
    - Semi-automatic conversion to fixed-point
    - Decent quality VHDL conversion output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)
    - Tools to simplify verification


Pyha specifically focuses on making testing of the DSP algorithms simpler.
While many alternatives are based on C language, but most of the hardware design time is used up in
the process of testing and verification, who would like to do this in C, Python is much better language
for this!

Pyha proposes to use classes as a way of describing hardware. More specifically all the class variables
are to be interpreted as hardware registers, this fits well as they are long term state elements.


This chapter focuses on the Python side of Pyha, while the next chapter gives details on how Pyha details are
converted to VHDL and how they can be synthesised.

Pyha tries to be as like to software programming as possible, some things written for soft vs hardware can give
suprisingly different results, this thesis tries to keep this in mind and hinglight such cases.

Model based design
~~~~~~~~~~~~~~~~~~

Pyha encourages model based design, it is optional. Idea of the model is to provide a simples possible solution for the problem, this can also serve as some form of
documentation to the module. Also as programmer guarantees equality of model and RTL, model can be used to run fast
simulations and experiments. Model can be verified against RTL.




Describing hardware
-------------------

    * Model
    * Clocking abstraction
    * Hardware is parallel, for is unrolled, comb example
    * Register needed for longer term state
    * Register adds delay
    * Register for pipelines and clock stuff
    * Sample based processing to block processing
    * Design reuse
    * Fixed point design?
    * Demonstrate multi-clock output?
    * Float conversions?
    * State machines
    * Multiply?


Stateless is also called combinatory logic. In the sense of software we could think that a function is stateless
if it only uses local variables, has no side effects, returns are based on inputs only. That is, it may use
local variables of function but cannot use the class variables, as these are stateful.

This first chapter uses integer types only, as they are well undestood by anyone and also fully synthesizable (to 32 bit logic).

Basic adder
~~~~~~~~~~~

Basic Pyha module is a Python class, that is derived from HW subclass. Simple adder with model implementaion is shown
on :numref:`adder-model`.

.. code-block:: python
    :caption: Simple adder model
    :name: adder-model

    class Adder(HW):
        def main(self, x):
            y = x + 1
            return y

        def model_main(self, xl):
            yl = [x + 1 for x in xl]
            return yl

.. note:: Pyha reserves the function name :code:`model_main` for defining the model and :code:`main` for the top
    level function. Designers may freely use other function names as pleased.

:numref:`adder-model` shows the model implementation for the adder. The code loops over the input list 'xl' and adds 1 to each element.
Important thing to notice is that the model code works on lists, it takes input as list and outputs a list.

Key difference beteween the 'model_main' and 'main' is that the later works on singe samples while the model works
on lists, it is vectorized. This is big difference because model code has access to all the samples of the scope, while
main only has the single sample.

.. todo:: rtl image

One of the key abstractions that Pyha uses is that the 'main' is called on each clock. One could imagine that
it is wrapped in a higher level for loop that continously supplies the samples.

.. todo:: sim image

The :numref:`fake` shows that all the simulations are equal. Pyha runs automatically Model, Python, VHDL and GATE simulations.

Clock abstracted as forever running loop. In hardware determines how long time we need to wait before
next call to function so that all signals can propagate.


More adding
~~~~~~~~~~~

Next example is a simple modification of the previous adder. Instead of :code:`y = x + 1` we write
:code:`y = x + 1 + 2 + 3 + 4`.

.. todo:: rtl image

The :numref:`fake` shows the RTL result. It may be suprising for software ppl.


.. todo:: sim image

Debuggability? Demonstrate that even tho different, can be fully debugged! For example if we have variable at some stage
then in hardware at same point the value will be same.

Main idea here to understand is that while the software and hardware approach do different thing, they result in
same output, so in that sense they are equal. Just the natural state of software is to execute stuff in sequence, while
hardware is parallel (tho, the order of operations still matter).

Also note that just like in software any operation has a price on the execution time, in hardware any operation has
a price in term on resource usage.

One of the key differences.

In software operations consume time, but in hardware they consume resources, general rule.


Control statements
~~~~~~~~~~~~~~~~~~

if

For if note that we pay for both branches, while in software we only pay for what branch is executing.
Also note that the in hardware both of the branches are constantly 'executing', the if condition just selects
which element is routed to the output.

There are differences..but still software and hardware approac give same result.

for

Lesson for for is that it will be fully unrolled. Also the for hardware the for control statement must be constant, since
it is impossible to unroll dynamic stuff.


Conclusions
~~~~~~~~~~~

This chapter dealt

Basic points:

    - Clock asbtaction
    - Everything costs in hardware
    - Debuggable
    - Sample based processing for model
    - Sample rate abstraction


Sequential logic
----------------

Registers and Accumulator
~~~~~~~~~~~~~~~~~~~~~~~~~

All that we have looked so far would actually not work on the FPGA?
Show how to use class vars as registers.

Delay of 1 seems like not an big deal, but really it very much is. In general big part of the hardware design is
fighting with bugs introduced by register delays, this is especially true for beginners. Delays can drasticly change
the operation of a circuit and what is even worse, they may not change the operation drasticly. Delay of one signal path
must be matched with delay of all sequnetial signal paths. Thats why it is important to always have a model and
unit tests, this is essential for hardware design.

Show register on two signal paths??

Running the same testing code results in a :numref:`mac_seq_sim_delay`. It shows that while the
Python, RTL and GATE simulations are equal, model simulation differs. This is the effect of added register,
it adds one delay to the harwdware simulations.

This is an standard hardware behaviour. Pyha provides special variable
:code:`self._delay` that specifies the delay of the model, it is useful:

- Document the delay of your blocks
- Upper level blocks can use it to define their own delay
- Pyha simulations will adjust for the delay, so you can easily compare to your model.

.. note:: Use :code:`self._delay` to match hardware delay against models

After setting the :code:`self._delay = 1` in the __init__, we get:


.. _mac_seq_sim:
.. figure:: ../examples/fir_mac/integer_based/img/seq_sim.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)


In Pyha, registers are inferred from the ogject storage, that is everything defined in 'self' will be made registers.

Understanding registers
^^^^^^^^^^^^^^^^^^^^^^^


In traditional programming, class variables are very similar to local variables. The difference is that
class variables can 'remember' the value, while local variables exist only during the function
execution.

Hardware registers have just one difference to class variables, the value assigned to them does not take
effect immediately, but rather on the next clock edge. That is the basic idea of registers, they take a new value
on clock edge. When the value is set at **this** clock edge, it will be taken on **next** clock edge.

Trying to stay in the software world, we can abstract away the clock edge by thinking that it denotes the
call to the 'main' function. Meaning that registers take the assigned value on the next function call,
meaning assignment is delayed by one function call.

VHDL defines a special assignment operator for this kind of delayed assignment, it is called 'signal assignment'.
It must be used on VHDL signal objects like :code:`a <= b`.

Jan Decaluwe, the author of MyHDL package, has written a relevant article about the necessity of signal assignment semantics
:cite:`jan_myhdl_signals`.

Using an signal assignment inside a clocked process always infers a register, because it exactly represents the
register model.

Pipelining
~~~~~~~~~~

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

Block processing
~~~~~~~~~~~~~~~~


Conclusion
~~~~~~~~~~

Class variables can be used in hardware, but they are delayed by one sample clock.

In digital design signals are assumed to exist between registers. Total delay between the registers determines the
maximum sample rate.



Fixed-point designs
-------------------

One of the nuiciannce for software ppl in hardware is registers the second one are floating point calculations, or
to be more clear, the lack of them in the FPGA context. Pyha tries to simplyfy the usage of fixed point stuff.

Semi-automatic conversion
~~~~~~~~~~~~~~~~~~~~~~~~~



Extended example
----------------

One change required to the MAC element is to add an 'sum_in' input rather than accumulating the sum.

.. _fir_freqz:
.. figure:: ../examples/fir_mac/fir/img/fir_freqz.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)

Note that design uses only 2 18 bit multipliers.

.. _fir_rtl:
.. figure:: ../examples/fir_mac/fir/img/fir_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)


.. _fir_sim:
.. figure:: ../examples/fir_mac/fir/img/fir_sim.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)

This may not be the best way of writing an FIR filter in Pyha, but it well demonstrates the ease of reusing
components.

Conclusions
-----------

This chapter showed how Python OOP code can be converted into VHDL OOP code.

It is clear that Pyha provides many conveneince functions to greatly simplyfy the testing of
model based designs.

Future stuff:
Make it easier to use, windows build?