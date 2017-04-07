VHDL as intermediate language
=============================

This chapter aims

Todo

    - What features do i want to support?
    - Why do it?

In this section we try to do things the other way around, that is adapt VHDL to Python.

Major goal of this project is to support object-oriented hardware design. Goal is to provide simple object
support, advanced features like inherintance and overloadings are not considerted at this moment.

Lay down a common ground on which VHDL and Python coold be connected.

While other HDL converters use VHDL/Verilog as low level conversion target.
Pyha goes other way around, as shown by the Gardner study :cite:`structvhdl_gaisler`, VHDL language can be used
with quite high level progrmaming constructs. Pyha tries to take advantage of this.

This chapter tries to enchance the VHDL language with some basic Python elements in order
to provide some common ground for the conversion task.

Background
----------

What is IR, how VHDl has been used before?
What is going to be different here?
Chisel and FIRRTL.
Basesd on gaisler stydy try to do differently.

As stated by the goal of this work, converting Object-oriented designs into HDL.
While it may seem that VHDL has no support for OOP, it is actually not true.

There have been previous study regarding OOP in VHDL before. In :cite:`Benzakki1997` proposal was
made to extend VHDL language with OOP semantics, this effort ended with development of
OO-VHDL :cite:`oovhdl`, that is VHDL preprocessor that could turn proposend extensions to standard
VHDL. This work was done in ~2000, current status is unknown, it certanly did not make it to the
VHDL standard.

While the :cite:`oovhdl` tried to extend VHDLs data-flow side of OOP, there actually exsists another
way to do it, that is inherited from ADA.

What is combinatory logic and what is sequantial logic?

A sequential circuit, on the other hand, has an internal
state, or memory. Its output is a function of current input as well as the internal state. The
internal state essentially “memorizes” the effect of the past input values. The output thus is
affected by current input value as well as past input values (or the entire sequence of input
values). That is why we call a circuit with internal state a sequential circuit.
:cite:`chu_vhdl`


Problem statement
-----------------

What do we want from this IR? What does it have to support?

.. code-block:: python
    :caption: Pipelined multiply-accumulate(MAC) implemented in Pyha
    :name: mac-pyha

    class MultiplyAccumulate(HW):
        def __init__(self):
            self.coef = 123
            self.mul = 0
            self.acc = 0

        def main(self, a):
            self.next.mul = a * self.coef
            self.next.acc = self.acc + self.mul
            return self.acc


.. _mac_rtl:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    RTL of MAC (Intel Quartus RTL viewer)

.. note:: In order to keep examples simple, only :code:`integer` types are used in this section.





Now

    - There may be more user defined functions
    - Object may be have subobjects
    - Subobjects may have their own subobjects, maybe even a list of objects.
    - Easy to map to Python, data model goes to stcuture and all methods just convert. profit





High-level functions in VHDL
----------------------------

**Show how combinatory logic can be made with simple function**

As shown in :cite:`structvhdl_gaisler`, VHDL functions can be used to infer combinatory logic. We can test
this out by defining similiar :code:`main` function, as in :numref:`mac-pyha`.

A combinational circuit, by definition, is a circuit whose output, after the initial transient
period, is a function of current input. It has no internal state and therefore is “memoryless”
about the past events (or past inputs) :cite:`chu_vhdl`. In other words, combinatory circuits have
no registers, i like to call it 'stuff between registers'.
Arguably better name for combinatory logic is 'stuff between two registers'.

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

.. todo:: Would like to show Python vs VHDL code here?

:numref:`comb-vhdl` show the MAC function in VHDL. It is functionally broken as the acc should save state
outside of the function.

.. _comb_mac_rtl:
.. figure:: img/comb_mac_rtl.png
    :align: center
    :figclass: align-center

    RTL of comb MAC (Intel Quartus RTL viewer)


Synthesisying this results in a RTL shown in :numref:`comb_mac_rtl`. Good news is that
it has all the required arithmetic elements. However, as expected it lacks the registers, making it
basically useless.

Benefit here is that the function in VHDL is very similiar to the Python one, conversion process would
surely be simple. Another result is that VHDL and Python have same result for local variables.


Long term state
~~~~~~~~~~~~~~~

In conventional programming languages, longer term state then local variables can be represented by global
variables or Object-oriented programming.

It is a known knowledge that using global variables is not going to get you far. It may work out in small
programs, but as programs grow, it gets out of hand quickly. :cite:`globals_harmful` (fake cite)

For these reasons we focus our efforts on OOP. Basic idea of OOP is to define some data and also define
functions that can do operations on this data. Note that this idea could fit well with defining hardware
'data' would be registers and operations on 'data' would be combinatory functions.

However VHDL does not come with OOP support, even so, it can be done by using records.

.. code-block:: vhdl
    :caption: Data portion in VHDL
    :name: vhdl-oop-data

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

:numref:`vhdl-oop-data` constructs an 'data model' for the OOP model. Next we can modify the 'main' function
to make use of the datamodel.

.. code-block:: vhdl
    :caption: VHDL OOP function
    :name: vhdl-oop-function

    procedure main(self: inout self_t; a: integer; ret_0: out integer) is
    begin
        self.mul := a * self.coef;
        self.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;

:numref:`vhdl-oop-function` shows new main function. Incorporating the OOP like datamodel required some changes:

    - First argument to the function is the datamodel, it must be 'inout'.
    - VHDL 'function' supports only 'in' arguments, for that reasons we had to go for procedures
    - VHDL procedues cannot return values, but can have 'out' arguments.


.. _ghetto_comb_mac_rtl:
.. figure:: img/ghetto_comb_mac_rtl.png
    :align: center
    :figclass: align-center

    RTL of OOP style MAC (Intel Quartus RTL viewer)


:numref:`ghetto_comb_mac_rtl` shows the synthesis result of such structure. We have managed to infer one register, but
even that is on wrong place. Functionally this result would work implement and MAC operation, thanks to that one register.

However as far as hardware goes, this is total junk, because there are no registers on the signal path. That is,
signal path from **in0** to **out0** is purely combinatory, not what we want for digital designs.


Better way of defining registers
--------------------------------
**getting rid of signal assigment**

It is clear from the previous section that the way of defining registers is not working correctly.

Problem is that we tried to use 'long term state' of conventional programming languages, but in hardware
registers work a bit differently.

Understanding registers
~~~~~~~~~~~~~~~~~~~~~~~


In conventional programming, using the 'long-term state' is very similiar of just using a local variable.
We can assign an value and the only difference with local variable is that it will remember the value to
the next call of the function.

Hardware registers are very similiar to this and really have just one striking difference, namely value assigned
to register does not take effect immediately, rather on the next clock edge. Thats just how registers are, they
take next value on the clock edge.

In software world we could say that assigments to registers are delayed by one

Here we can abstract away the **clock signal** by thinking that clock edge = function call.

VHDL defines a special assignment operator for this kind of delayed stuff, it is called 'signal assignment'.
It is defined like :code:`a <= b`.

Using an signal assigment inside a clocked process always infers a register.


Signal assignment for variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Problem with the 'signal assignment operator' is that it can only be used on **signals**, that are some
special objects of VHDL. In this work we would rather like to use **variables**, because they are the same
in every other programming language.

As the final goal of this project is to convert Python into VHDL, signal assigment is a major problem
because it cannot easily be mapped to Python. We would like to save registers as our class object values,
and to get rid of signal assignment.

Luckly simulating signal assignment, using variables, is not very complex or hard.


Conventional method to this is to define two variables, for **current** and **next** values of the register.
Pong P. Chu suggest the usage of similiar system even with VHDL signals,

Author of MyHDL package has written a good writeup on how it handles signal assigment :cite:`jan_myhdl_signals`, in short
they use the same 'next' idiom. Even Pong P. Chu, author of one of the best VHDL books, teaches the
reader to write registers with two variables, one for the current value and another one for 'next'.

In case of our MAC example, we could make dublicate registers for each variable,
this is shown in :numref:`mac-next-data`.

.. code-block:: vhdl
    :caption: Datamodel with **next** section
    :name: mac-next-data

    type next_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;

        nexts: next_t;
    end record;

For example now reading the 'acc' register can be done with :code:`self.acc` and writing next value
:code:`self.nexts.acc := 0`.

New style should also incoporated to the 'main' function. Instead of writing to **current** values it should
now write to **next**, this is shown on :numref:`mac-next-main`.

.. code-block:: vhdl
    :caption: Updated 'main' function
    :name: mac-next-main

    procedure main(self: inout self_t; a: integer; ret_0: out integer) is
    begin
        self.nexts.mul := a * self.coef;
        self.nexts.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;


One thing that signal assignment automates is the loading of **next** value into **current**. By using
variables we have to take care of this ourselves. For this we can define new function that handles the
update for all the registers, this is shown on :numref:`mac-next-update`.


.. code-block:: vhdl
    :caption: Function to update registers
    :name: mac-next-update

    procedure update_register(self: inout self_t) is
    begin
        self.mul := self.nexts.mul;
        self.acc := self.nexts.acc;
        self.coef:= self.nexts.coef;
    end procedure;

.. note:: Function 'update_registers' is called on clock raising edge.


.. _mac_rtl_end:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    RTL of MAC (Intel Quartus RTL viewer)

:numref:`mac_rtl_end` shows the synthsis result of the last code. It is clear that this is now equal to the goal
system, exactly what we want.


Class model for VHDL
--------------------

Previous chapters showed that OOP style syhntesisable VHDL is possible. This chapter investigates how to
put togather previous results. How to make instances etc..

Currently we have following elements required for one 'class' definition:

    - Record definition for 'next'
    - Record definition for 'self'
    - Any user defined functions (like 'main')
    - 'Update registers' function


Initial register values
~~~~~~~~~~~~~~~~~~~~~~~

Currently one bit of information the 'class model' is missing are the initial values for the registers.
In VHDL structures can be initialized on defining the variable, like
:code:`variable name: type := (elem1 => 1, elem2 => 2);`.

Problem with this method is that it requires the values for all fields (including 'next'). This can get
unmanageably complex very quickly, imagine an class having sub-objects and arrays, all of these must be initialized.

Conventional programming languages use class constructor for inititialization purposes, that is just a function
that is ran when object is made.

In hardware we can make a similiar 'reset' function, difference once again is that we have to call it ourselves.

Alternative is to require that each 'class' provides an 'reset' function that writes correct values
into the registers.

.. code-block:: vhdl
    :caption: Reset function for MAC
    :name: mac-vhdl-reset

    procedure reset(self: inout self_t) is
    begin
        self.nexts.coef := 123;
        self.nexts.mul := 0;
        self.nexts.sum := 0;
        update_registers(self);
    end procedure;

:numref:`mac-vhdl-reset` shows a possible 'reset' implementation for MAC, it writes
 initial values to 'next' and then use the predefined update function to transfer
them to current values. This function can be called in case reset signal is asserted.



Using package
~~~~~~~~~~~~~

VHDL supports 'packages' to group common types and functions into one namespace. Package in VHDL
must contain an declaration and body (same concept as header and source files in C).



.. code-block:: vhdl
   :caption: OOP in VHDL
   :name: oop_vhdl

    package MAC is
        type next_t is record
            coef: integer;
            mul: integer;
            acc: integer;
        end record;

        type self_t is record
            coef: integer;
            mul: integer;
            acc: integer;

            nexts: next_t;
        end record;

        procedure reset(self: inout self_t);
        procedure update_registers(self: inout self_t);
        procedure main(self:inout self_t; a: integer; ret_0:out integer);
    end package;

    package body MAC is

        procedure reset(self: inout self_t) is
        begin
            self.nexts.coef := 123;
            self.nexts.mul := 0;
            self.nexts.acc := 0;
            update_registers(self);
        end procedure;

        procedure update_registers(self: inout self_t) is
        begin
            self.coef := self.nexts.coef;
            self.mul := self.nexts.mul;
            self.acc := self.nexts.acc;
        end procedure;

        procedure main(self:inout self_t; a: integer; ret_0:out integer) is
        begin
            self.nexts.mul := self.coef * a;
            self.nexts.acc := self.acc + self.mul;
            ret_0 := self.acc;
            return;
        end procedure;
    end package body;



:numref:`oop_vhdl` gives basic example on how to write OOP in VHDL. Base point of OOP is to define
some data and then functions that can perform operations with this data structure. In the example
we have used 'record' (like struct in C) to construct an datamodel for the object, to keep it simple
it only consists of one integer variable.

This method of writing OOP code is quite common in C also, principle is the same. Make a structure
to hold the datamodel and then always pass this structure as the first parameter to functions.



Creating instances
~~~~~~~~~~~~~~~~~~
Basically forced to create separate file for each instance.
Major problem if used in VHDL world, not problem at all if converted.

Multiple instances example
~~~~~~~~~~~~~~~~~~~~~~~~~~



Conclusion
----------

This chapter shows how to OOP in VHDL, we demonstrate that the approach is fully synthesisable.

Advantages
~~~~~~~~~~

It may look like a major overkill? Same thing with signal assignments so easy?

.. todo:: compare the oop way vs signal assignments way. Is it worth it?

Every register of the model is kept in record, it is easy to create shadow registers for the whole module.
Everything is concurrent, can debug and understand.


Disadvantage is that it can be only converted to VHDL. Advantages are numerous:

    - Similiar code in VHDL and Python
    - Clean conversion output
    - Easy to use VHDL Fixed point package


Synthesisability
~~~~~~~~~~~~~~~~


Multiple clock-domains
~~~~~~~~~~~~~~~~~~~~~~

This model has no restrictions on multiple clock domains??

.. todo:: Here talk about top level stuff also?


About SystemVerilog
~~~~~~~~~~~~~~~~~~~

My experience with SystemVerilog is limited, but to me it seems that it extends the Verilog with mostly
features that already exsist in VHDL. It higly likely that methods developed in this chapter would also
apply for SystemVerilog.

.. http://www.amiq.com/consulting/2016/01/26/gotcha-access-an-out-of-bounds-index-for-a-systemverilog-fixed-size-array/

However note that SystemVerilog is much much worse IR language, as it is not as strict as VHDL. For example
in SystemVerilog you can happly index arrays over bounds, without any error. There are some knobs to turn
bound cheking on..but still the default values show the mentality of the language.

Only motivation for using SystemVerilog over VHDL is somekind of Verilog tool support. For example Yosys, but
as of my knowledge this currently does not support advanced SV features.

VHDL is perfect IR for Python, because you can do many stupid things in Python, that will be flagged as errors
in VHDl, this will save alot of development time.
