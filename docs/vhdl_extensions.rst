VHDL as intermediate language
=============================

This chapter develops synthesisable and object-oriented (OOP) programming model for VHDL. Main motivation of it
is to act as an intermediate language for High-Level synthesis, that is, to allow higher level OOP langues to easly
convert into VHDL.


Objective
---------

Conventioanal VHDL programming is very different from normal programming. In VHDL programmers deal with concurrent
statemetns, signals and wirering together components, that is all very far from the normal programming languages.

Gaols is to introduce alternative model, where same things can be achieved but with programming model much closer to
everyday programmers.

Problem with VHDL is that it is so very different from normal programming languages, that makes
conversion hard and error prone.


.. code-block:: python
    :caption: Pipelined multiply-accumulate(MAC) implemented in Pyha
    :name: mac-pyha

    class MAC:
        def __init__(self, coef):
            self.coef = coef
            self.mul = 0
            self.acc = 0

        def main(self, a):
            self.next.mul = a * self.coef
            self.next.acc = self.acc + self.mul
            return self.acc

.. note:: In order to keep examples simple, only :code:`integer` types are used in this section.

:numref:`mac-pyha` shows a MAC component implementend in Pyha
Pyha is experimental Python to VHDL compiler implemented in the next chapter of this thesis.
Operation of this circuit is to multiply the input with some coefficent and then accumulate the result.
This code synthesizes to logic as shown on :numref:`mac_rtl`.

.. _mac_rtl:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-pyha` (Intel Quartus RTL viewer)

This chapter tries to find and VHDL model that could easly accomodate this OOP based style.

The main reason to pursue the OOP approach is the modularity and the ease of reuse.

One prolem in VHDL is that reusing components is not trivial, programmers must do 'wiring' work that is error
prone. Making arrays of components is even harder.

On the other hand these operations are very easy with OOP approach, for example :numref:`mac-pyha-serial` defines
new class, that has two MACs in series, as expected, this is very easy to achieve in OOP style.
As expected it synthesizes to a structure where two MACs are connected in series,
shown on :numref:`pyha_mac_reuse_stack`.

.. code-block:: python
    :caption: Two MAC's connected in series
    :name: mac-pyha-serial

    class SeriesMAC:
        def __init__(self, coef):
            self.mac0 = MAC(123)
            self.mac1 = MAC(321)

        def main(self, a):
            out0 = self.mac0.main(a)
            out1 = self.mac1.main(out0)
            return out1

.. _pyha_mac_reuse_stack:
.. figure:: img/mac_reuse_stack.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-pyha-serial` (Intel Quartus RTL viewer)

:numref:`mac-pyha-parallel` shows that by modiyfing the main function,
it is possible to infer two parallel MACs instead
As expected this would synthesize to parallel MACS as shown on :numref:`pyha_mac_reuse_parallel`.

.. code-block:: python
    :caption: Two MAC's in parallel
    :name: mac-pyha-parallel

    def main(self, a):
        out0 = self.mac0.main(a)
        out1 = self.mac1.main(a)
        return out0, out1


.. _pyha_mac_reuse_parallel:
.. figure:: img/mac_reuse_parallel.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-pyha-parallel` (Intel Quartus RTL viewer)

Note that it would also be possible to create lists of objects..etc.
It is clear that such kind of programming would be useful for hardware.


Basically in this chapter we are looking to develop an VHDL model that could easly describe these
previously listed examples.

Major features that we are looking for:

    - OOP style for conversion ease
    - Familiarity to normal programmers
    - Must be fully synthesisable
    - Should not limit the hardware description stuff, like multiple clocks
    - Unify/simplify Python to VHDL conversion



Background
----------

What is IR, how VHDl has been used before?
What is going to be different here?
Chisel and FIRRTL, skip?


There have been previous study regarding OOP in VHDL. In :cite:`Benzakki1997` proposal was
made to extend VHDL language with OOP semantics, this effort ended with development of
OO-VHDL :cite:`oovhdl`, that is VHDL preprocessor that could turn proposend extensions to standard
VHDL. This work was done in ~2000, current status is unknown, it certanly did not make it to the
VHDL standard.

While the :cite:`oovhdl` tried to extend VHDLs data-flow side of OOP, there actually exsists another
way to do it, that is inherited from ADA.

There are many tools on the market that convert some higher level language to VHDL, for example MyHDL converts
Python to VHDL and Verilog. However these tools only make use of the very basic elements of VHDL language. The result
of this is that coneversion process is complex and hard to understand. Also the output VHDL generally does not
keep design hirarchy and is very hard to read for humans.

While other HDL converters use VHDL/Verilog as low level conversion target.
Pyha goes other way around, as shown by the Gardner study :cite:`structvhdl_gaisler`, VHDL language can be used
with quite high level progrmaming constructs. Pyha tries to take advantage of this.

The author of MyHDL package has written some good blog posts about signal assigmennts and software side of hardware
design :cite:`jan_myhdl_signals` :cite:`jan_myhdl_soft`. These ideas are relaveant for this chapter.


Jiri Gaisler has proposed an 'Structured VHDL design method' in the ~2000 :cite:`structvhdl_gaisler`. He proposes
to raise the hardware design abstraction level by instead of writing 'dataflow' style. Use two process method
where the algorithmic part is described by the regular function in one process and registers are in another process.

Gaisler notest that functions only good for combinatory logic and in one clock domian, try to improve that.

The goal of the two-process method is to:

    - Provide uniform algorithm encoding
    - Increase abstraction level
    - Improve readability
    - Clearly identify sequential logic
    - Simplify debugging
    - Improve simulation speed
    - Provide one model for both synthesis and simulation

This work improves upon the work of Jiri Gaisler.

Siin v]ib ka kirjutada VHDL vs Verilog asjadest, Verilog populaarsem? OS tools.


Object-oriented style in VHDL
-----------------------------

While VHDL is mostly known as a dataflow programming, it is actually derived from ADA programming lanugage,
where it inherits strong structurial semantics. As shown by :cite:`structvhdl_gaisler`,
using these higher-level programming constructs can be used to infer combinatory logic.

Basic idea of OOP is to bundle up some common data and define functions that can perform actions on this data.
This idea could fit well with hardware design, we could define 'data' as registers and functions as combinatory logic.

VHDL has an 'class' like strucutre called protected types :cite:`vhdl-lrm`, but unfortionatly these are not working for
synthesis.

Even so, OOP style can be mimiced in VHDL, by combining data in records and passing it as a first
parameter to all functions that work on it. This is the same way how C programmers do it.

.. code-block:: vhdl
    :caption: MAC datamodel in VHDL
    :name: vhdl-oop-data

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

:numref:`vhdl-oop-data` constructs the datamodel for the MAC. We expect that these will be turned to registers by
the synthesise tool.

.. code-block:: vhdl
    :caption: MAC main function in VHDL
    :name: vhdl-oop-function

    procedure main(self: inout self_t; a: in integer; ret_0: out integer) is
    begin
        self.mul := a * self.coef;
        self.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;

:numref:`vhdl-oop-function` shows new MAC main function. In VHDL procedure arguments must have a direction, for example
the first argument 'self' is of direction 'inout', this means it can be read and also written to. One downside of
procedures is that they cannot return a value, instead 'out' direction arguments must be used, advantage is that
multiple return values can be supported.

.. _ghetto_comb_mac_rtl:
.. figure:: img/ghetto_comb_mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`vhdl-oop-function` (Intel Quartus RTL viewer)

.. note:: Top level file can be see here.

:numref:`ghetto_comb_mac_rtl` shows that functionally correct MAC has been implemented. However it is not quite
what we want in terms of hardware. In the datamodel we hoped to have 3 registers, but only the one for 'acc' is present
and even this is on wrong location.

In fact the signal path from **in0** to **out0** contains no registers at all, making this design rather useless.

Understanding registers
~~~~~~~~~~~~~~~~~~~~~~~

Clearly the way of defining registers is not working properly.
Problem is that we expected the registers to work in the same way as 'class variables' in conventional programming
languages, but in hardware registers work a bit differently.

In conventional programming, class variables is very similiar of just using a local variable.
Only difference to the local variables is that the value will remember the value to the next call of the function.

Hardware registers as class variables have just one striking difference, value assigned to register does not take
effect immediately, rather on the next clock edge. Thats just how registers are, they
take next value on the clock edge.

As we are trying to stay in the software world, we can abstract away the **clock edge** by thinking that it is the
same as function call. That is on very clock edge our 'main' function is executed. This means that hardware registers
take the assigned value on the next function call, we could say that the assignment is delayed by one.

VHDL defines an special type of objects, called signals, for these kind of variables.
VHDL defines a special assignment operator for this kind of delayed stuff, it is called 'signal assignment'.
It is defined like :code:`a <= b`.

VHDL signals really come down to just having to variables. One to represent the next value and other for the current
value. The signal assignment assigns to the 'next' and in the next simulation delta loads the value to the current.

Using an signal assigment inside a clocked process always infers a register.


Inferring registers with variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While 'signals' and 'signal assignment' is the VHDL way of defining registers, it poses a major problem because they
are hard to map to any other language than VHDL, making conversion hard. In this work we would rather like to
use variables, because they are the same in every other programming language.

In order to j2rjepidevalt infer registers we must mimic the signal assignment semantics with variables.

VHDL signals really come down to just having two variables, representing the current and next values.
The signal assignment assigns to the 'next' and in the next simulation delta loads the value to the current.

This two variable method is not anything new, for example Pong P. Chu, author of one of the best VHDL books,
suggests to use this style in defining sequential logic in VHDL :cite:`chu_vhdl`. Same semantics are also used in
MyHDL.

First step in adapting the MAC to this style would be to define duplicate variables for the OOP datamodel.
:numref:`mac-next-data` shows one way to do this.

alternative way? each element signal object?

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

New datamodel allows reading the register value as before, but extends the structure to include the 'nexts' keyword
that can be used to assign new value for the register, for example :code:`self.nexts.acc := 0`.


New style should also be incorporated to the 'main' function. Next register values shall be written to the
'nexts', this is shown on :numref:`mac-next-main`.

.. code-block:: vhdl
    :caption: Main function using 'nexts'
    :name: mac-next-main

    procedure main(self: inout self_t; a: integer; ret_0: out integer) is
    begin
        self.nexts.mul := a * self.coef;
        self.nexts.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;

Another thing that must be handled it loading the 'next' values to current values, that is updating the registers.
In VHDL this is done automatically if signal assignment is used.By using
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

.. note:: Function 'update_registers' is called on clock raising edge. This determines their clock domain.
    It is possible to infer multiclock systems by updating some subeset of registers at different clock edge.

.. _mac_rtl_end:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of the upgraded code (Intel Quartus RTL viewer)

:numref:`mac_rtl_end` shows the synthesis result of the last code. It is clear that this is now equal to the system
presented at the start of this chapter, exactly what we wanted.

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

One bit of information the 'class model' is missing are the initial values for the registers.
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
   :caption: Full code of OOP style MAC
   :name: package-mac

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



:numref:`package-mac` lists the final code for the MAC example. It is using the OOP style and is wrappen inside
of a VHDL package, this method of writing OOP code is quite common in C also, principle is the same. Make a structure
to hold the datamodel and then always pass this structure as the first parameter to functions.


Creating instances
~~~~~~~~~~~~~~~~~~

One major operation that we would lik to do with classes is to create instances of them, that is considering
the example, creating multiple MAC elements.

In case we want to create instances with same reset values everything is easy. Just need to define multiple record
values.

However problem arises when two instances shall have a different inital values for registers. Imagine one MAC with coef
12 and another with 32. In that case we have a problem as the reset values are hardcoded into the class declaration.

Basically forced to create separate file for each instance.
Major problem if used in VHDL world, not problem at all if converted.

Resets are kind of like a weakpoint of this model

Multiple instances example
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo:: Images have sinngle constant coef

in the beginning we also showed examples of multiple instances...

This paragraph shows how to create a new class that itself includes two MAC elements.
Situation is that we want to use first MAC with coeficient of '123' and the second one with '321'. According
to the previosu text we need to create two packages, first is MAC_0, and second MAC_1.

Now creating a new class using these is as simple as in convertional programming, in datamodel we must define
these:

.. code-block:: vhdl
    :caption: Datamodel for multiple MAC
    :name: multi-mac-data

    type self_t is record
        mac0: MAC_0.self_t;
        mac1: MAC_1.self_t;

        nexts: next_t;
    end record;

Then in main function, as expected we need to call the main functions of submodules:

.. code-block:: vhdl
    :caption: Datamodel for multiple MAC
    :name: multi-mac-main-stack

    procedure main(self:inout self_t; a: integer; ret_0:out integer) is
        variable out_tmp: integer;
    begin
        MAC_0.main(self.mac0, a, ret_0=>out_tmp);
        MAC_1.main(self.mac1, out_tmp, ret_0=>out_tmp);
        ret_0 := out_tmp;
    end procedure;

:numref:`multi-mac-main-stack` shows implementation of main function in case we would like to chain up
the two MAC functions, that is, signal flows is as in -> MAC0 -> MAC1 -> out.

.. _mac_reuse_stack:
.. figure:: img/mac_reuse_stack.png
    :align: center
    :figclass: align-center

    RTL of stacked MAC (Intel Quartus RTL viewer)

:numref:`mac_reuse_stack` shows the synthsis result of the last code.


Alternatively we could code the two MACs to work in parallel by just changing the code in main:

.. code-block:: vhdl
    :caption: Datamodel for multiple MAC
    :name: multi-mac-main-stack

    procedure main(self:inout self_t; a: integer; ret_0:out integer; ret_1:out integer) is
        variable out0: integer;
        variable out1: integer;
    begin
        MAC_0.main(self.mac0, a, ret_0=>out0);
        MAC_1.main(self.mac1, a, ret_0=>out1);
        ret_0 := out0;
        ret_1 := out1;
    end procedure;

.. _mac_reuse_parallel:
.. figure:: img/mac_reuse_parallel.png
    :align: center
    :figclass: align-center

    RTL of parallel MAC (Intel Quartus RTL viewer)

:numref:`mac_reuse_parallel` shows the synthsis result of the last code.


Discussion
----------

.. todo:: compare the oop way vs signal assignments way. Is it worth it?
Presented model has some advantages and disadvantages, lets analyze these.



Advantages
~~~~~~~~~~

Every register of the model is kept in record, it is easy to create shadow registers for the whole module.
Everything is concurrent, can debug and understand.

Easier to understand for new programmers, this model contains only elements that should be already familiar for
programmers dealing with normal languages.

Creating

Synthesisability
~~~~~~~~~~~~~~~~

In this chapter simple example about synthesizable MAC operation and in parallel and stacked form.
This model has also been tested in real life designs which being much more complex. There has been no problems
with this model, even for big designs.

Real life experiments have been done on Altera Cyclone IV device, syhtesizing software used is Quartus.


Multiple clock-domains
~~~~~~~~~~~~~~~~~~~~~~

All depends on what clock domain are the registers updated ('update_registers' function called).
One limitaion of this model is that all of these subinstances are executed by the same clock.
So basically instances are limited to one clock domain.

There is a way around this by upgrading registers in separate clock domains..


Today this is not a major problem as generally hardware sistems are mostly composed of a few clock domains.
So all of these can be written separately and then use connection interfaces to connect them.

For example Intel provides Qsys tool, that allows connecting stuff togather and handles clock crossings itself.

That is one thing that does not translate well to conventional prol=gamming languages.

It is perfetct for IP core design!

The method is applicable to any synchrounous single-clock design, which represents the majority of all designs.
Actually not limited to one clock at all.

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


Conclusion
----------

This chapter developed an alternative method to write synthesisable VHDL. It meets all the initial requirements, like
OOP support. Major advantage of this model is that it uses only VHDL language featurest that are common for
normal programming also. Meaning that it is easy to translate from those other languages to synthesisablae VHDL.

This chapter shows how to OOP in VHDL, we demonstrate that the approach is fully synthesisable.

