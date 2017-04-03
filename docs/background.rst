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

CocoTb
~~~~~~
