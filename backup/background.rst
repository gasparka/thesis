Background
==========
Give a short overview of whats up.

A structured VHDL design method
-------------------------------
The base of this thesis builds on top of the work of Jiri Gaisler about 'Structured VHDL
design method' :cite:`structvhdl_gaisler`. This chapter gives an overview of what it is about.

Introduction
~~~~~~~~~~~~

The VHDL language [22] was developed to allow modelling of digital hardware. It can
be seen as a super-set of Ada, with a built-in message passing mechanism called sig-
nals.
When the language was first put to use, it was used for high-level behavioural simula-
tion only. ’Synthesis’ into VLSI devices was made by manually converting the models
into schematics using gates and building blocks from a target library. However, manual
conversion tended to be error-prone, and was likely to invalidate the effort of system
simulation. To address this problem, VHDL synthesis tools that could convert VHDL
code directly to a technology netlist started to emerge on the market in the begining of
1990’s. Since the VHDL code could now be directly synthesised, the development of
the models was primarily made by digital hardware designers rather than software engi-
neers. The hardware engineers were used to schematic entry as design method, and their
usage of VHDL resembled the dataflow design style of schematics. The functionality
was coded using a mix of concurrent statments and short processes, each decribing a
limited piece of functionality such as a register, multiplexer, adder or state machine. In
the early 1990’s, such a design style was acceptable since the complexity of the circuits
was relatively low (< 50 Kgates) and the synthesis tools could not handle more complex
VHDL structures. However, today the device complexity can reach several millions of
gates, and the synthesis tools accept a much larger part of the VHDL standard. It should
therefore be possible to use a more modern and efficient VHDL design method than the
traditional ’dataflow’ version. This chapter will describe such a method and compare it
to the ’dataflow’ version. :cite:`structvhdl_gaisler`


The problems with the ’dataflow’ design method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most commonly used design ’style’ for synthesisable VHDL models is what can
be called the ’dataflow’ style. A larger number of concurrent VHDL statements and
small processes connected through signals are used to implemenet the desired function-
ality. Reading and understanding dataflow VHDL code is difficult since the concurrent
statements and processes do not execute in the order they are written, but when any of
their input signals change value. It is not uncommon that to extract the functionality of
dataflow code, a block diagram has to be drawn to indentify the dataflow and depend-
ecies between the statements. The readability of dataflow VHDL code can compared to
an ordinary schematic where the wires connecting the various blocks have been
removed, and the block inputs and outputs are just labeled with signal names!
:cite:`structvhdl_gaisler`

A problem with the dataflow method is also the low abstraction level. The functionality
is coded with simple constructs typically consisting of multiplexers, bit-wise operators
and conditional assignments (if-then-else). The overall algorithm might be very difficult to recognize and debug.
:cite:`structvhdl_gaisler`


The goals and means of the ’two-process’ design method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To overcome the limitations of the dataflow design style, a new ’two-process’ coding
method is proposed. The method is applicable to any synchrounous single-clock
design, which represents the majority of all designs. The goal of the two-process
method is to:

    - Provide uniform algorithm encoding
    - Increase abstraction level
    - Improve readability
    - Clearly identify sequential logic
    - Simplify debugging
    - Improve simulation speed
    - Provide one model for both synthesis and simulation

The above goals are reached with suprisingly simple means:

    - Using record types in all port and signal declarations
    - Only using two processes per entity
    - Using high-level sequential statements to code the algorithm

The following section will outline how the two-process method works and how it com-
pares with the traditional dataflow method.
:cite:`structvhdl_gaisler`

Using two processes per entity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The biggest difference between a program in VHDL and standard programming lan-
guage such C, is that VHDL allows concurrent statements and processes that are sched-
uled for execution by events rather than in then order they are written. This reflects
indeed the dataflow behaviour of real hardware, but becomes difficult to understand
and analyse when the number of concurrent statments passes some threashold (e.g. 50).
On the other hand, analysing the behaviour of programs witten in sequential program-
ming languages does not become a problem even if the program tends to grow, since
there is only one thread of control and execution is done sequentially from top to bot-
tom.
In order to improve readability and provide a uniform way of encode the algorithm of
a VHDL entity, the two-process method only uses two processes per entity: one process
that contains all combinational (asynchronous) logic, and one process that contains all
sequential logic (registers). Using this structure, the complete algorithm can be coded
in sequential (non-concurrent) statements in the combinational process while the
sequential process only contains registers, i.e. the state.:cite:`structvhdl_gaisler`


Other improvements
~~~~~~~~~~~~~~~~~~
Gaisler also shows how to use records to group all the registers into one variable and
use records for port connections to improve design hirarcy. In addtion, Gaisler shows
that higher level constructs like sub-programs and loop statements are fully usable and
syhtnesisable.

Comparison MEC/LEON: :cite:`structvhdl_gaisler`

ERC32 memory contoller MEC

    - Ad-hoc method (15 designers)
    - 25,000 lines of code
    - 45 entities, 800 processes
    - 2000 signals
    - 3000 signal assigments
    - 30 Kgates, 10 man-years,numerous of bugs, 3 iterations

LEON SPARC V8 processor

    - Two process method (mostly)
    - 15,000 lines of code
    - 37 entities, 75 processes
    - 300 signals
    - 800 signal assignments
    - 100k gates, 2 man-years,
    - no bugs in first silicon

Summary and conclusions
~~~~~~~~~~~~~~~~~~~~~~~

The presented two-process method is a way of producing structured and readable
VHDL code, suitable for efficient simulation and synthesis. By defining a common
coding style, the algorithm can be easily identified and the code analysed and main-
tained also by other engineers than the main designer. Using sequential VHDL state-
ments to code the algorithm also allows the use of complex statements and a higher
abtraction level. Debugging and analysis is simplified due to the serial execution of
statements, rather than the parallel flow used in dataflow coding.:cite:`structvhdl_gaisler`




Contributions of this work
--------------------------

First part of this work builds on top of the Jiri Gaisler work, but makes significant improvements.
First this work adds synthesisable object-orientational support to VHDL language.

Next we provide a way of signal assignment that can be written without the use of
VHDL signal assignment semantics. The point of removing this is to make the
programming model more structured, and standard.

Lastly this work provides an Python to VHDL mapping, in order to speed up development time
also the Python program can be simulated.



Python
------
Python is a popular programming language which has lately gained big support in the scientific world,
especially in the world of machine learning and data science.
It has vast support of scientific packages like Numpy for matrix math or  Scipy for scientific
computing in addition it has many superb plotting libraries.
Many people see Python scientific stack as a better and free MATLAB.

Free Dev tools.
.. http://www.scipy-lectures.org/intro/intro.html#why-python
    %https://github.com/jrjohansson/scientific-python-lectures/blob/master/Lecture-0-Scientific-Computing-with-Python.ipynb

HDL related tools in Python
---------------------------
As the idea of converting higehr level languages to VHDL/Verilog is not new, this chapter
gives an overview of previous works and states how current work differs from them.

MyHDL
~~~~~
MyHDL is Python to VHDL/Verilog converter, first release dating back to 2003. It turns
Python into a hardware description and verification language,
providing hardware engineers with the power of the Python ecosystem.:cite:`myhdlweb`

MyHDL has been used in the design of multiple ASICs and numerious FPGA projects.:cite:`myhdlfelton`


MyHDL, like VHDL and Verilog,is a hardware description language. MyHDL does not include “IP” or cores directly :cite:`myhdlfelton`.

MyHDL	is	not	a	tool	to	take	arbitrary
Python code and	create	working	hardware [7].		MyHDL	is similar	to	existing	HDLs;
the	convertible	subset of	the	language	describes	hardware	behavior at	the	Register
Transfer	Level	(RTL)	of	abstraction.	 Clearly, this	indicates	MyHDL	is	not	a	HighLevel
Synthesis	(HLS)	language. :cite:`myhdlfelton`

MyHDL works with data-flow paradigm, not good, not good.

Example
^^^^^^^

Here is a simple example of describing and register with MyHDL.
:numref:`myhdl-register` shows an register code in MyHDL. One thing to note is that it uses Python
function as a base unit and :code:`always` blocks, that all is very similiar to Verilog language, clearly
this infers a process with separate clock and reset signals.

Another thing to note is the assignment of 'q' value. It uses the 'next' value. Pyha steals this.


.. code-block:: python
    :caption: Register in MyHDL :cite:`myhdlweb`
    :name: myhdl-register

    from myhdl import *

    def dffa(q, d, clk, rst):

        @always(clk.posedge, rst.negedge)
        def logic():
            if rst == 0:
                q.next = 0
            else:
                q.next = d

        return logic

:numref:`myhdl-sim` shows the code required to simulate the design. It is not important to understand
what goes on, but to see that simulating in MyHDL is not simple. It requires the user to handle clock
and reset etc. Dataflow principles even in testbench.

.. code-block:: python
    :caption: Register in MyHDL :cite:`myhdlweb`
    :name: myhdl-sim

    from random import randrange

    def test_dffa():

        q, d, clk, rst = [Signal(bool(0)) for i in range(4)]

        dffa_inst = dffa(q, d, clk, rst)

        @always(delay(10))
        def clkgen():
            clk.next = not clk

        @always(clk.negedge)
        def stimulus():
            d.next = randrange(2)

        @instance
        def rstgen():
            yield delay(5)
            rst.next = 1
            while True:
                yield delay(randrange(500, 1000))
                rst.next = 0
                yield delay(randrange(80, 140))
                rst.next = 1

        return dffa_inst, clkgen, stimulus, rstgen

    def simulate(timesteps):
        tb = traceSignals(test_dffa)
        sim = Simulation(tb)
        sim.run(timesteps)

    simulate(20000)

Problems with MyHDL
^^^^^^^^^^^^^^^^^^^

    - Writing testbenches is hard, dataflow is bad, have to handle clock and reset
    - Conversion very limited (jan rant)
Convertable subset is extreamly limited compared to the simulatable subset. Many users (including me)
have been dissapointed about this, this has even led the author of MyHDL, Jan Decaluwe to write an
blog post about how MyHDL is 'simulation-oriented language' :cite:`jan_sim`.


..
    http://www.jandecaluwe.com/blog/its-a-simulation-language.html
    myhdl sim language

    https://news.ycombinator.com/item?id=8298610
    system verilog rant

Migen
~~~~~
Migen is a Python-based tool that aims at automating further the VLSI design process.
Migen makes it possible to apply modern software concepts such as object-oriented programming
and metaprogramming to design hardware. This results in more elegant and easily maintained
designs and reduces the incidence of human errors. :cite:`migenweb`

Despite being faster than schematics entry, hardware design with Verilog and VHDL remains tedious
and inefficient for several reasons. The event-driven model introduces issues and manual coding
that are unnecessary for synchronous circuits, which represent the lion's share of today's
logic designs. Counter- intuitive arithmetic rules result in steeper learning curves and
provide a fertile ground for subtle bugs in designs. Finally, support for procedural
generation of logic (metaprogramming) through "generate" statements is very limited and
restricts the ways code can be made generic, reused and organized. :cite:`migenweb`

To address those issues, we have developed the Migen FHDL library that replaces the e
vent-driven paradigm with the notions of combinatorial and synchronous statements,
has arithmetic rules that make integers always behave like mathematical integers,
and most importantly allows the design's logic to be constructed by a Python program.
This last point enables hardware designers to take
advantage of the richness of the Python language -
object oriented programming, function parameters, generators, operator overloading, libraries,
etc. - to build well organized, reusable and elegant designs. :cite:`migenweb`

Other Migen libraries are built on FHDL and provide various tools such as a system-on-chip
interconnect infrastructure, a dataflow programming system, a more traditional high-level
synthesizer that compiles Python routines into state machines with datapaths,
and a simulator that allows test benches to be written in Python. :cite:`migenweb`

    - Python as a meta-language for HDL
    - Restricted to locally synchronous circuits (multiple clock domains are supported)
    - Designs are split into:
        - synchronous statements
        - combinatorial statements
    - Statements expressed using nested Python objects
    :cite:`migenpresentation`

Has some advanced features like BUS support:

    - Wishbone1
    - SRAM-like CSR
    - DFI 2
    - LASMI

:cite:`migenpresentation`

Able to generate hardware abstraction layer in C, for bus usage

The base idea is very similiar to of Pyha, to get rid of dataflow/event driven modeling.
It has a very strange way of programming. Pyha has clear edge here.
Simulation in Python support..looks weak, it relies more on Verilog simulator

Many systems build with this system. Now has more github stars then MyHDL.





Example
^^^^^^^

:numref:`migen-sim` showns a LED blinker module implemented in Migen, it consists of a counter
that when finished toggles the LED state.

As written before, Migen separates hardware design into combinatory and synch parts. What can be
seen is kind of a metaprogramming. That is in migen one cannot write :code:`counter = period` but
have to write :code:`counter.eq(period)`, same goes for if statements etc. That is the price you
have to pay in order to use Migen.

Much bigger problem of this approach is that the hardware part of the code is basically
not debuggable. Migen supports some kind of Python simulator but it is not much better than MyHDL one.

.. code-block:: python
    :caption: Register in MyHDL :cite:`migenweb`
    :name: migen-sim

    class Blinker(Module):
        def __init__(self, led, maxperiod):
            counter = Signal(max=maxperiod+1)
            period = Signal(max=maxperiod+1)
            self.comb += period.eq(maxperiod)
            self.sync += If(counter == 0,
                    led.eq(˜led),
                    counter.eq(period)
                ).Else(
                    counter.eq(counter - 1)
                )


Problems with MiGen
^^^^^^^^^^^^^^^^^^^
Migen is awesome but it also has some problems.

    - Simulation is not easy,
    - Not debuggable in Python domain

Migen cannot be debugged, this may not seem like a big upside for Pyha. But it is, steping trough the code
can greatly simplify finding bugs, after all this is the main way of debugging in conventional programming.
Also debugger is useful tool for understanding the codebase.


Cocotb
~~~~~~

EDAPLAYGROUND
Cocotb is a COroutine based COsimulation TestBench environment for verifying VHDL/Verilog RTL
using Python. :cite:`cocotbdoc`

Unlike MyHDL and Migen, Cocotb is not a Python to HDL converter, instead it is meant to simulate
VHDL/Verilog designs.

A typical cocotb testbench requires no additional RTL code.
The Design Under Test (DUT) is instantiated as the toplevel in the simulator without
any wrapper code. Cocotb drives stimulus onto the inputs to the DUT
(or further down the hierarchy) and monitors the outputs directly from Python. :cite:`cocotbdoc`

A test is simply a Python function. At any given time either the simulator is
advancing time or the Python code is executing. The yield keyword is used to indicate
when to pass control of execution back to the simulator. A test can spawn multiple coroutines,
allowing for independent flows of execution.



Problems with Cocotb
^^^^^^^^^^^^^^^^^^^^

Major problem with Cocotb is that the tests are to be written to test the HDL part only. Often
it happens that there is also some higher level model that could use unit-testing. With Cocotb
one would need to develope two sets of tests, one for the model and another for HDL, this situation
is bound to end badly.. unsynchronzed model and HDL.

Minor headace is that Cocotb runs Python test file started from C program, meaning that for debugging
one has to use remote debugger, that is not very convenient.


Other HDLS
----------

This thesis focuses on the Python to VHDL conversion. There exsist however many more tools that
instead of Python convert something else to VHDL/Verilog.

Chisel
^^^^^^

In this paper we introduce Chisel , a new hardware construction language
that supports advanced hardware design using highly parameterized generators
and layered domain-specific hardware languages.  By embedding Chisel in the Scala
programming language, we raise the level of hardware design ab straction by providing
concepts including object orientation, functional programming, parameterized types,
and type inference.  Chisel can generate a high-speed C++-based cycle-accurate
software simulator, or low-level Verilog designed to map to either FPGAs or to a standard
ASIC flow for synthesis.  This paper presents Chisel, its embedding in Scala, hardware examples,
 and results for C++ simulation, Verilog emulation and ASIC synthesis. :cite:`chisel`

Now there is a new version called Chisel3, that seemingly has not gained much ground yet.

Also there is a spinoff project called SpinalHDL that tries to fix many shortcomings of Chisel.
No sim support?

These are converters written in Scala. They seem to be very feature rich. Chisel developed by University of California.
Big acceptance on writing RISC instruction set processors.

Clash
^^^^^

CλaSH (pronounced ‘clash’) is a functional hardware description language that borrows
both its syntax and semantics from the functional programming language Haskell.
It provides a familiar structural design approach to both combinational and synchronous
sequential circuits. The CλaSH compiler transforms these high-level descriptions to low-level
synthesizable VHDL, Verilog, or SystemVerilog.

Features of CλaSH:

    - Strongly typed, but with a very high degree of type inference, enabling both safe and fast prototyping using concise descriptions.
    - Interactive REPL: load your designs in an interpreter and easily test all your component without needing to setup a test bench.
    - Compile your designs for fast simulation.
    - Higher-order functions, in combination with type inference, result in designs that are fully parametric by default.
    - Synchronous sequential circuit design based on streams of values, called Signals, lead to natural descriptions of feedback loops.
    - Multiple clock domains, with type safe clock domain crossing.
    - Template language for introducing new VHDL/(System)Verilog primitives.
:cite:`clash`


OpenCL
^^^^^^
.. https://www.altera.com/content/dam/altera-www/global/en_US/pdfs/literature/po/ps-opencl.pdf


C-based tools
^^^^^^^^^^^^^

VivadoHLS
^^^^^^^^^
.. https://www.xilinx.com/products/design-tools/vivado/integration/esl-design.html
https://www.xilinx.com/support/documentation/sw_manuals/xilinx2016_1/ug902-vivado-high-level-synthesis.pdf


Matlab, simulink, LabView
^^^^^^^^^^^^^^^^^^^^^^^^^

Todo. maybe skip?

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





Testing/debugging and verification
----------------------------------

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

Ipython testing...show example with two unit tests and plots.