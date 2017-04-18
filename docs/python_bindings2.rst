Pyha
====

Pyha is an tool that allows writing of digital hardware in Python language. Currently it focuses mostly on the DSP
applications.

Main features:

    - Simulate hardware in Python. Integration to run RTL and GATE simulations.
    - Structured, all-sequential and object oriented designs
    - Fixed point type support(maps to `VHDL fixed point library`_)
    - Decent quality VHDL conversion output (get what you write, keeps hierarchy)
    - Integration to Intel Quartus (run GATE level simulations)
    - Tools to simplify verification


Introduction
------------

This chapter focuses on the Python side of Pyha, while the next chapter gives details on how Pyha details are
converted to VHDL and how they can be synthesised.

A multiply-accumulate(MAC) circuit is used as a demonstration circuit throughout the rest of this chapter.
It is a good choice as it is powerful element yet not very complex.
Last chapter of this thesis peresents more serious use cases.


Model based design
------------------

Generally before the hardware system is implemented, it is useful to first experiment with the idea and maybe
even do some performance figures like SNR. For this, model is constructed. In general the model is the
simplest way to archive the task, it is not optimized.

Model allows to focus on the algorithmical side of things.
Also model comes in handy when verifying the operation of the hardware model. Output of the model and hardware
can be compared to verify that the hardware is working as expected.


In :cite:`blade_adsb`, open-sourced a ADS-B decoder, implemented in hardware. In this work the authors first implement
the model in MATLAB for rapid prototyping. Next they converted the model into C and implemented it using fixed-point
arithmetic. Lastly they converted the C model to VHDL.

More common approach is to use MATLAB stack for also the fixed-point simulations and for conversion to VHDL.
Also Simulink can be used.

Simulink based design flow has been reported to be used in Berkeley Wireless Research Center (BWRC) :cite:`borph`.
Using this design flow, users describe their designs in Simulink using blocks provided by Xilinx System Generator
:cite:`borph`.

The problem with such kind of design flow is that it costs alot. Only the MATLAB based parts can easly cost close
to 20000 EUR, as the packages depend on eachother. For example for reasonable flow user must buy the Simulink software
but that also requires the MATLAB software, in addtion to do DSP, DSP toolbox is needed.. etc.

Also the FPGA vendor based tools, like Xilinx System Generator are also expensive and billed annually.

While this workflow is powerful indeed.

Model based design, this is also called behavioral model (
.. https://books.google.ee/books?hl=en&lr=&id=XbZr8DurZYEC&oi=fnd&pg=PP1&dq=vhdl&ots=PberwiAymP&sig=zqc4BUSmFZaL3hxRilU-J9Pa_5I&redir_esc=y#v=onepage&q=vhdl&f=false)


Pyha flow
~~~~~~~~~

Pyha is fully open-source software, meaning it is a free tool to use by anyone.
Since Pyha is based on the Python programming language, it gets all the goodness of this environment.

Python is a popular programming language which has lately gained big support in the scientific world,
especially in the world of machine learning and data science.
It has vast support of scientific packages like Numpy for matrix math or  Scipy for scientific
computing in addition it has many superb plotting libraries.
Many people see Python scientific stack as a better and free MATLAB.

As far as what goes for model writing, Python comes with extensive schinetific stuff. For example
Scipy and Numpy. In addition all the GNURadio blocks have Python mappings.

VHDL uuendused? VUNIT VUEM?

Test-driven development / unit-tests

.. http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1034&context=csse_fac

Model based development
How MyHDl and other stuffs contribute here?

Since Pyha brings the development into Python domain, it opens this whole ecosystem for writing
testing code.


.. code-block:: python
    :caption: Multiply-accumulate written in Python
    :name: mac-pyha

    class MAC:
        def __init__(self, coef):
            self.coef = coef

        def model_main(self, sample_in, sum_in):
            import numpy as np

            muls = np.array(sample_in) * self.coef
            sums = muls + sum_in
            return sums


:numref:`mac-pyha` shows the MAC model written in Python. It uses the Numpy package for numeric calculations.



Simplifying testing
~~~~~~~~~~~~~~~~~~~

One problem for model based designs is that the model is generally written in some higher
level language and so testing the model needs to have different tests than HDL testing. That
is one ov the problems with CocoTB.

Pyha simplifies this by providing an one function that can repeat the test on model, hardware-model, RTL
and GATE level simulations.

    * Siin all ka unit testid?

Python ships with many unit-test libraries, for example PyTest, that is the main one used for
Pyha.

Siin peaks olema test funksioonid?

Testing/debugging and verification
----------------------------------


Describing hardware
-------------------

Main idea of Pyha is to enable hardware design in Python ecosystem.

Pyha extends the VHDL language by allowing objective-oriented designs. Unit object is Python class as shown on

.. code-block:: python
   :caption: Basic Pyha unit
   :name: basic-pyha

    class PyhaUnit(HW):
        def __init__(self, coef):
            pass

        def main(self, input):
            pass

        def model_main(self, input_list):
            pass

:numref:`basic-pyha` shows the besic design unit of the developend tool, it is a standard Python class, that is derived
from a baseclass *HW, purpos of this baseclass is to do some metaclass stuff and register this class as Pyha module.

Metaclass actions:



Stateless logic
~~~~~~~~~~~~~~~

Stateless is also called combinatory logic. In the sense of software we could think that a function is stateless
if it only uses local variables, has no side effects, returns are based on inputs only. That is, it may use
local variables of function but cannot use the class variables, as these are stateful.


.. code-block:: python
   :caption: Basic combinatory circuit in Pyha
   :name: pyha-comb

    class MAC(HW):
        def main(self, a, sum_in):

            mul = self.coef * a
            acc = sum_in + mul
            return acc



:numref:`pyha-comb` shows the design of a combinatory logic. In this case it is a simple xor operation between
two input operands. It is a standard Python class, that is derived from a baseclass *HW,
purpose of the baseclass is to do some metaclass stuff and register this class as Pyha module.

Class contains an function 'main', that is considered as the top level function for all Pyha designs. This function
performs the xor between two inputs 'a' and 'b' and then returns the result.

In general all assigments to local variables are interpreted as combinatory logic.

.. todo:: how this turns to VHDL and RTL picture?

In software operations consume time, but in hardware they consume resources, general rule.



Sequential logic
----------------

Registers in hardware have more purposes:

    - delay
    - max clock speed - how this corresponds to sample rate?

.. todo:: Ref comb logic.

.. code-block:: python
   :caption: Basic sequential circuit in Pyha
   :name: pyha-reg

    class Reg(HW):
        def __init__(self):
            self.reg = 0

        def main(self, a, b):
            self.next.reg = a + b
            return self.reg

:numref:`pyha-reg` shows the design of a registered adder.

In Pyha, registers are inferred from the ogject storage, that is everything defined in 'self' will be made registers.


The 'main' function performs addition between two inputs 'a' and 'b' and then returns the result.
It can be noted that the sum is assigned to 'self.next' indicating that this is the next value register takes on
next clock.

Also returned is self.reg, that is the current value of the register.

In general this system is similiar to VHDL signals:

    - Reading of the signal returns the old value
    - Register takes the next value in next clock cycle (that is self.next.reg becomes self.reg)
    - Last value written to register dominates the next value

However there is one huge difference aswell, namely that VHDL signals do not have order, while all Pyha code is stctural.


.. todo:: how this turns to VHDL and RTL picture?



Simulation a


Fixed-point designs
-------------------




Extended example
----------------

MAC ist saab FIR?


Conclusions
-----------

This chapter showed how Python OOP code can be converted into VHDL OOP code.

It is clear that Pyha provides many conveneince functions to greatly simplyfy the testing of
model based designs.