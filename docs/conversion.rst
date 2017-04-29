.. _ch_vhdl:

Conversion to VHDL
==================

This chapter shows how Pyha converts to VHDL.


Introduction
------------

.. todo:: Pilt converterist

    * Simulatsioon tüüpide leidmiseks
    * Python AST modifikatsioonid
    * Pythont to VHDL
    * Sequential OOP VHDL IR



VHDL as intermediate language
-----------------------------

This chapter is a fair bit more techincal and requires some knowledge of VHDL and
hardware synthesis.

This chapter develops synthesizable object-oriented (OOP) programming model for VHDL.
The main motivation is to use it as an intermediate language for High-Level synthesis of
hardware.

Introduction
------------



Background
~~~~~~~~~~

The most commonly used design ’style’ for synthesizable VHDL models is what can
be called the ’dataflow’ style. A larger number of concurrent VHDL statements and
small processes connected through signals are used to implement the desired functionality.
Reading and understanding dataflow VHDL code is often deemed difficult since the concurrent
statements and processes do not execute in the order they are written, but when any of
their input signals change value :cite:`structvhdl_gaisler`.

The biggest difference between a program in VHDL and standard programming language such as C,
is that VHDL allows concurrent statements and processes that are scheduled
for execution by events rather than in then order they are written. This reflects
indeed the dataflow behaviour of real hardware, but is  difficult to understand and analyse.
On the other hand, analysing the behaviour of programs written in sequential programming languages
does not become a problem even if the program tends to grow, since execution is done sequentially
from top to bottom :cite:`structvhdl_gaisler`.


Jiri Gaisler has proposed a 'Structured VHDL design method :cite:`structvhdl_gaisler`' in the ~2000
.He suggests to raise the hardware design abstraction level by using a two-process
method.

The two-process method only uses two processes per entity: one process
that contains all combinatory (asynchronous) logic, and one process that contains all
sequential logic (registers). Using this structure, the complete algorithm can be coded
in sequential (non-concurrent) statements in the combinational process while the
sequential process only contains registers, i.e. the state :cite:`structvhdl_gaisler`.


Object-oriented style in VHDL has been studied before. In :cite:`Benzakki1997` a proposal was
made to extend the VHDL language with OOP semantics (dataflow based), this effort ended with the development of
OO-VHDL :cite:`oovhdl`, a VHDL preprocessor, turning proposed extensions to standard
VHDL. This work did not make it the VHDL standard, the status of compiler is unknown, latest publicly
available document dates to year 1999.


Objective
~~~~~~~~~

The main motivation of this work is to use VHDL as an intermediate language for High-Level synthesis.

While the work of Jiri Gaisler greatly simplifies the programming experience of VHDL, it still
has some major drawbacks:

    - It is applicable only to single-clock designs:cite:`structvhdl_gaisler`;
    - The 'structured' part can be only used to define combinatory logic, registers must be still inferred by signals assignments;
    - It still relies on many of the VHDL dataflow features, for example, design reuse is achieved trough the use of entities and port maps;

This work aims at improving the 'two process' model by proposing an Object-oriented approach for VHDL,
lifting all the previously listed drawbacks.

This section uses examples in Python language in order to demonstrate the Python to VHDL converter (developed in the next chapter)
and set some targets for the intermediate language.

A multiply-accumulate(MAC) circuit is used as a demonstration circuit throughout the rest of this chapter.

.. todo:: Need to introduce Pyha before.

.. code-block:: python
    :caption: Pipelined multiply-accumulate(MAC) specified in Pyha
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

.. note:: In order to keep examples simple, only :code:`integer` types are used in this chapter.

:numref:`mac-pyha` shows a MAC component implemented in Pyha
(Python to VHDL compiler implemented in the next chapter of this thesis).
The purpose of this circuit is to multiply the input with the coefficient and accumulate the result.
It synthesizes to logic as shown in :numref:`mac_rtl`.

.. _mac_rtl:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-pyha` (Intel Quartus RTL viewer)

The main reason to pursue the OOP approach is the modularity and the ease of reuse. :numref:`mac-pyha-serial` defines
a new class, containing two MACs that are to be connected in series.
As expected it synthesizes to a series structure (:numref:`pyha_mac_reuse_stack`).

.. code-block:: python
    :caption: Two MAC's connected in series, specified in Pyha
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

.. todo:: Names on the figure should match the names on the code!
    Explain that 'a' is the input on the left-hand side (fed into B of the 1st MAC),
    out0 is output of the 1st MAC (fed into B of the 2nd MAC) and 'out1' in the source code is actually out0 in the RTL view (or am I mistaken?)

With slight modification to the 'main' function (:numref:`mac-pyha-parallel`),
two MAC's can be connected in a way that synthesizes to a parallel structure (:numref:`pyha_mac_reuse_parallel`).

.. code-block:: python
    :caption: Two MAC's in parallel, specified in Pyha
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


It is clear that the OOP style could significantly simplify hardware design.
The objective of this work is to develop a synthesizable VHDL model that could easily map to these MAC examples.

.. todo:: Elaborate on what you mean with 'clear' and 'simplify'.


Object-oriented style in VHDL
-----------------------------

.. todo:: Remind the reader that what follows is your proposal (one of the thesis contributions). Also briefly explain what is done differently as compared to previous approaches (especially those that you cited earlier).

While VHDL is mostly known as a dataflow language, it inherits strong support for structured
programming from ADA.

.. todo:: Need to reference that statement.

The basic idea of OOP is to bundle up some common data and define functions that can perform actions on it.
Then one could define multiple sets of the data.
This idea fits well with hardware design, as 'data' can be thought as registers and combinatory logic as functions that
perform operations on the data.

VHDL includes a 'class' like structure called 'protected types' :cite:`vhdl-lrm`, unfortunately these are not meant for
synthesis. Even so, OOP style can be imitated, by combining data in records and passing them as a
parameters to 'class functions'. This is essentially the same way how C programmers do it.

.. code-block:: vhdl
    :caption: MAC data model in VHDL
    :name: vhdl-oop-data

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

Constructing the data model for the MAC example can be done by using VHDL 'records' (:numref:`vhdl-oop-data`).
In the sense of hardware, we expect that the contents of this record will be synthesised as registers.

.. note:: We label the data model as 'self', to be equivalent with the Python world.

.. code-block:: vhdl
    :caption: OOP style function in VHDL (implementing MAC)
    :name: vhdl-oop-function

    procedure main(self: inout self_t; a: in integer; ret_0: out integer) is
    begin
        self.mul := a * self.coef;
        self.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;

An OOP style function can be constructed by adding a first argument that points to the data model object (:numref:`vhdl-oop-function`).
In VHDL, procedure arguments must have a direction, for example the first argument 'self' is of direction 'inout',
this means it can be read and also written to.

One drawback of VHDL procedures is that they cannot return a value, instead 'out' direction arguments must be used.
The advantage of this is that the procedure may 'output/return' multiple values, as can Python functions.

.. _ghetto_comb_mac_rtl:
.. figure:: img/ghetto_comb_mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`vhdl-oop-function` (Intel Quartus RTL viewer)


The synthesis results (:numref:`ghetto_comb_mac_rtl`) show that a functionally correct MAC has been implemented.
However, in terms of hardware, it is not quite what was wanted.
The data model specified 3 registers, but only the one for 'acc' is present and even this is at the wrong location.

In fact, the signal path from **in0** to **out0** contains no registers at all, making this design hard
to use in real designs.

Understanding registers
~~~~~~~~~~~~~~~~~~~~~~~

Clearly the way of defining registers is not working properly.
The mistake was to expect that the registers work in the same way as 'class variables' in traditional programming
languages.

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

Inferring registers with variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While 'signals' and 'signal assignment' are the VHDL way of defining registers, they pose a major problem because they
are hard to map to any other language than VHDL. This work aims to
use variables instead, because they are the same in every other programming language.

VHDL signals really come down to just having two variables, to represent the **next** and **current** values.
Signal assignment operator sets the value of **next** variable. On the next simulation delta, **current** is automatically
set to equal **next**.

This two variable method has been used before, for example Pong P. Chu, author of one of the most reputed VHDL books,
suggests to use this style in defining sequential logic in VHDL :cite:`chu_vhdl`. The same semantics are also used in
MyHDL :cite:`jan_myhdl_signals`.

Adapting this style for the OOP data model is shown on :numref:`mac-next-data`.

.. code-block:: vhdl
    :caption: Data model with **next**, in OOP-style VHDL
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

The new data model allows reading the register value as before and extends the structure to include the 'nexts' object,
so that it can used to assign new value for registers, for example :code:`self.nexts.acc := 0`.

Integration of the new data model to the 'main' function is shown on :numref:`mac-next-main`. The only changes are
that all the 'register writes' go to the 'nexts' object.

.. code-block:: vhdl
    :caption: Main function using 'nexts', in OOP-style VHDL
    :name: mac-next-main

    procedure main(self: inout self_t; a: integer; ret_0: out integer) is
    begin
        self.nexts.mul := a * self.coef;
        self.nexts.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;

The last thing that must be handled is loading the **next** to **current**.
As stated before, this is done automatically by VHDL for signal assignment; by using
variables we have to take care of this ourselves. :numref:`mac-next-update` defines new function
'update_registers', taking care of this task.

.. code-block:: vhdl
    :caption: Function to update registers, in OOP-style VHDL
    :name: mac-next-update

    procedure update_register(self: inout self_t) is
    begin
        self.mul := self.nexts.mul;
        self.acc := self.nexts.acc;
        self.coef:= self.nexts.coef;
    end procedure;

.. note:: Function 'update_registers' is called on clock raising edge.
    It is possible to infer multi-clock systems by updating a subset of registers at a different clock edge.

.. _mac_rtl_end:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)

:numref:`mac_rtl_end` shows the synthesis result of the source code shown in :numref:`mac-next-update`.
It is clear that this is now equal to the system presented at the start of this chapter.



Creating instances
~~~~~~~~~~~~~~~~~~

The general approach of creating instances is to define new variables of the 'self_t' type, :numref:`vhdl-instance`
gives an example of this.

.. code-block:: vhdl
    :caption: Class instances by defining records, in OOP-style VHDL
    :name: vhdl-instance

    variable mac0: MAC.self_t;
    variable mac1: MAC.self_t;

The next step is to initialize the variables, this can be done at the variable definition, for example:
:code:`variable mac0: self_t := (mul=>0, acc=>0, coef=>123, nexts=>(mul=>0, acc=>0, coef=>123));`

The problem with this method is that all data-model must be initialized (including 'nexts'),
this will get unmaintainable very quickly, imagine having an instance that contains another instance or
even array of instances. In some cases it may also be required to run some calculations in order to determine
the initial values.

Traditional programming languages solve this problem by defining class constructor,
executing automatically for new objects.

In the sense of hardware, this operation can be called 'reset' function. :numref:`mac-vhdl-reset` is a reset function for
the MAC circuit. It sets the initial values for the data model and can also be used when reset signal is asserted.

.. code-block:: vhdl
    :caption: Reset function for MAC, in OOP-style VHDL
    :name: mac-vhdl-reset

    procedure reset(self: inout self_t) is
    begin
        self.nexts.coef := 123;
        self.nexts.mul := 0;
        self.nexts.sum := 0;
        update_registers(self);
    end procedure;

But now the problem is that we need to create a new reset function for each instance.

This can be solved by using VHDL 'generic packages' and 'package instantiation declaration' semantics :cite:`vhdl-lrm`.
Package in VHDL just groups common declarations to one namespace.

In case of the MAC class, the 'coef' reset value could be set as package generic. Then each new package
initialization could define new reset value for it (:numref:`vhdl-package-init`).

.. code-block:: vhdl
    :caption: Initialize new package MAC_0, with 'coef' 123
    :name: vhdl-package-init

    package MAC_0 is new MAC
       generic map (COEF => 123);

Unfortunately, these advanced language features are not supported by most of the synthesis tools.
A workaround is to either use explicit record initialization (as at the start of this chapter)
or manually make new package for each instance.

Both of these solutions require unnecessary workload.

The Python to VHDL converter (developed in the next chapter), uses the later option, it is not a problem as everything
is automated.

Final OOP model
~~~~~~~~~~~~~~~

Currently the OOP model consists of following elements:

    - Record for 'next'
    - Record for 'self'
    - User defined functions (like 'main')
    - 'Update registers' function
    - 'Reset' function

VHDL supports 'packages' to group common types and functions into one namespace. A package in VHDL
must contain an declaration and body (same concept as header and source files in C).

:numref:`package-mac` shows the template package for VHDL 'class'.
All the class functionality is now in one common namespace.

.. code-block:: vhdl
   :caption: Package template for OOP style VHDL
   :name: package-mac

    package MAC is
        type next_t is record
            ...
        end record;

        type self_t is record
            ...
            nexts: next_t;
        end record;

        procedure reset(self: inout self_t);
        procedure update_registers(self: inout self_t);
        procedure main(self:inout self_t);
        -- other user defined functions
    end package;

    package body MAC is
        procedure reset(self: inout self_t) is
        begin
            ...
        end procedure;

        procedure update_registers(self: inout self_t) is
        begin
            ...
        end procedure;

        procedure main(self:inout self_t) is
        begin
            ...
        end procedure;
        -- other user defined functions
    end package body;


Examples
--------

This section provides some simple examples based on the MAC component and OOP model, that were developed in previous chapter.

Instances in series
~~~~~~~~~~~~~~~~~~~

Creating a new class that connects two MAC instances in series is simple, first we need to create two
MAC instances called MAC_0 and MAC_1 and add them to the data model (:numref:`mac-series-data`).

.. code-block:: vhdl
    :caption: Datamodel of 'series' class, in OOP-style VHDL
    :name: mac-series-data

    type self_t is record
        mac0: MAC_0.self_t;
        mac1: MAC_1.self_t;

        nexts: next_t;
    end record;

The next step is to call MAC_0 operation on the input and then pass the output
trough MAC_1, whose output is the final output (:numref:`mac-series-main`).

.. code-block:: vhdl
    :caption: Function that connects two MAC's in series, in OOP-style VHDL
    :name: mac-series-main

    procedure main(self:inout self_t; a: integer; ret_0:out integer) is
        variable out_tmp: integer;
    begin
        MAC_0.main(self.mac0, a, ret_0=>out_tmp);
        MAC_1.main(self.mac1, out_tmp, ret_0=>ret_0);
    end procedure;


.. _mac_reuse_stack:
.. figure:: img/mac_reuse_stack.png
    :align: center
    :figclass: align-center

    Synthesis result of the new class (Intel Quartus RTL viewer)

Logic is synthesized in series (:numref:`mac_reuse_stack`). That is exactly what was specified.


Instances in parallel
~~~~~~~~~~~~~~~~~~~~~

Connecting two MAC's in parallel can be done by just returning output of MAC_0 and MAC_1 (:numref:`mac-parallel`).

.. code-block:: vhdl
    :caption: Main function for parallel instances, in OOP-style VHDL
    :name: mac-parallel

    procedure main(self:inout self_t; a: integer; ret_0:out integer; ret_1:out integer) is
    begin
        MAC_0.main(self.mac0, a, ret_0=>ret_0);
        MAC_1.main(self.mac1, a, ret_0=>ret_1);
    end procedure;

.. _mac_reuse_parallel:
.. figure:: img/mac_reuse_parallel.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-parallel` (Intel Quartus RTL viewer)

Two MAC's are synthesized in parallel, as shown in :numref:`mac_reuse_parallel`.

Parallel instances in different clock domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiple clock domains can be easily supported by updating registers at specified clock domains.
:numref:`mac-parallel-clocks` shows the contents of a top-level process, where 'mac0' is updated by 'clk0' and
'mac1' by 'clk1'.
Note that nothing has to be changed in the data model or main function.

.. code-block:: vhdl
    :caption: Top-level for multiple clocks, in OOP-style VHDL
    :name: mac-parallel-clocks

    if (not rst_n) then
        ReuseParallel_0.reset(self);
    else
        if rising_edge(clk0) then
            MAC_0.update_registers(self.mac0);
        end if;

        if rising_edge(clk1) then
            MAC_1.update_registers(self.mac1);
        end if;
    end if;

.. _mac_parallel_two_clocks:
.. figure:: img/mac_parallel_two_clocks.png
    :align: center
    :figclass: align-center

    Synthesis result with modified top-level process (Intel Quartus RTL viewer)

Synthesis result (:numref:`mac_parallel_two_clocks`) is as expected, MAC's are still in parallel but now the
registers are clocked by different clocks. The reset signal is common for the whole design.



Conversion methodology
----------------------

Conversion process is based heavily on the results of last chapter, that developed OOP style for VHDL.
This simplifies the conversion process in a way, that mostly no complex conversions are not needed.
Basically the converter should only care about syntax conversion, that is Python syntax to VHDL.

Thats why this can be called Python bindings.. everything you write in Python has a direct mapping to VHDL, most
of the time mapping is just syntax difference.

Still converting Python syntax to VHDL syntax poses some problems. First, there is a need to traverse the Python
source code and convert it. Next problem is the types, while VHDL is strongly types language, Python is not, somehow the
conversion progress should find out all the types.

This chapter deals with these problems.

This chapter aims to convert the Python based model into VHDL, with the goal of synthesis.


Problem of types
~~~~~~~~~~~~~~~~

The biggest challenge in conversion from Python to VHDL is types, namely Python does not have them, while VHDL has.

For example in VHDL, when we want to use local variable, it must be defined with type.

.. code-block:: vhdl
    :caption: VHDL variable action
    :name: vhdl-variable

    -- define variable a as integer
    variable a: integer;

    -- assign 'b' to 'a', this requires that 'b' is same type as 'a'
    a := b;


.. code-block:: python
    :caption: Python variable action
    :name: python-variable

    # assign 'b' to 'a', 'a' will inherit type of 'b'
    a = b

:numref:`vhdl-variable` and :numref:`python-variable` show the variable difference in VHDl and Python.
In general this can be interpreted in a way that VHDL icludes all the information required but Python leaves
some things open.
In Python it is even possible that 'a' is different type for different function callers.
Python way is called dynamic-typing while VHDl way is static. Dynamic, meaning that
types only come into play when the code is executing.

The advantage of the Python way is that it is easier to program, no need to define variables and ponder about the types.
Downsides are that there may be unexpected bugs when some variable changes type also the code readability suffers.

In sense of conversion, dynamic typing poses a major problem, somehow the missing type info should be recovered for the
VHDL code.

Most straightforward  way to tackle this problem is to request the user to provide top level input types on conversion.
As the main types are known, clearly all other types can be derived from them. Problem with this method is that is much more
complex than it initially appears. For example :code:`a = b`. To find the type of 'a' converter would need to lookup type
of 'b', also the the assign could be part of expression like :code:`a = b < 1`, anyhow this solution gets complex really fast
and is not feasible option.


Alternative would be to embrace the dynamic typing of Python and simulate the design before conversion, in that way
all the variables resolve some type, thanks to running the code.


Class
^^^^^

Class variables are easy to infer after code has been executed as all of them can be readily accessed.


.. code-block:: python
    :caption: Type problems
    :name: cond-main

    class SimpleClass(HW):
        def __init__(self, coef):
            self.coef = coef

        def main(self, a):
            local_var = a

Class variables types can be extracted even without 'simulation'. On class creation '__init__' function runs that also
assigns something to all class variables, that is enough to determine type. Still simulation can help Lazy types to converge.

Example:

.. code-block:: python
    :caption: Class variable type
    :name: class-vars

    >>> dut = SimpleClass(5)
    >>> dut.coef
    5
    >>> type(dut.coef)
    <class 'int'>

:numref:`class-vars` show example for getting the type of class variable. It initializes the class with argument 5, that is
passed to the 'coef' variable. After Python 'type' can be used to determine the variable type. Clearly this variables could
be converted to VHDL 'integer' type (not really...Python is infinite).


Locals
^^^^^^

Locals mean here the local variables of a function including the function arguments, in VHDL these also require to be
typed.

Inferring the type of function local variables is much harder as Python provides no standard way of doing so. This task
is hard as locals only exsist in the stack, thus they will be gone once the function exection is done.
Luckly this problem has been encountered before in :cite:`py_locals_decorator`, whicp provides an solution.


This approach works by defining a profile tracer function, which has access to the internal frame of a function,
and is called at the entry and exit of functions and when an exception is called. :cite:`py_locals_decorator`

Solution is to wrap the function under inspection in other function that sets a traceback function on the return and
saves the result of the last locals call.

That way all the locals can be found on each call. Pyha uses this approach to keep track of the local values.
Below is an example:

.. code-block:: python
    :caption: Function locals variable type
    :name: class-locals

    >>> dut.main.locals # before any call, locals are empty
    {}
    >>> dut.main(1) # call function
    >>> dut.main.locals # locals can be extracted
    {'a': 1, 'local_var': 1}
    >>> type(dut.main.locals['local_var'])
    <class 'int'>



Advantages
^^^^^^^^^^

Major advantage of this method is that the type info is extracted easily and complexity is low. Potential perk in the
future is that this way could keep track of all values that any variable takes during the simulation, this will be
essential if in the future some automatic float to fixed point compiler is to be implementend.

Other advantages this way makes possible to use 'lazy' coding, meaning that only the type after the end of simulation
matters.

Another advantage is that programming in Python can be even more lazy..


Disadvantages
^^^^^^^^^^^^^

Downside of this solution is obviously that the desing must be simulated in Python domain before it can be converted to
VHDL.
First clear is that the design must be simulated in Python domain before conversion is possible, this may be
inconvenient.

Also the simulation data must cover all the cases, for example consider the function with conditional local variable,
as shown on :numref:`cond-main`. If the simulaton passes only True values to the function, value of variable 'b' will
be unknown ad vice-versa. Of course such kinf of problem is detected in the conversion process. Also in hardware
we generally have much less branches than in software also all of thes branches are likely to be important as each
of them will **always** take up resources.

.. code-block:: python
    :caption: Type problems
    :name: cond-main

    def main(c):
        if c:
            a = 0
        else:
            b = False



Conversion methodology
~~~~~~~~~~~~~~~~~~~~~~

After the type problem has been solved, next step is to convert the Python code into VHDL.

Chapter :ref:`ch_vhdl` developed a way to write OOP VHDL, thanks to this, the conversion from Python to VHDL is
much simplified. Mostly the converter needs to convert the syntax parts. Conversion progress requires no understanding
of the source code nor big modifications.

This task requires a way of parsing the input Python code, making modifications and then outputting VHDL compilant
syntax.

In general this step involves using an abstract syntax tree (AST). This reads in the source file and turns it into
traversable tree stucture of all the operations done in the program.

There are many tools in the Python ecosystem that allow this task, for example lib2to3 etc.

Converter of this project uses the RedBaron :cite:`redbaron`. RedBaron is an Python library with an aim to
significantly simply operations with source code parsing.

RedBaron is a python library with intent of making the process of writing code that modify source code as easy and
as simple as possible. That include writing custom
refactoring, generic refactoring, tools, IDE or directly modifying you source code into IPython with a higher and
more powerful abstraction than the advanced texts modification tools that you find in advanced text editors and IDE.
:cite:`redbaron`



RedBaron turns all the blocks in the code into special 'nodes'. Help function provides an example:

Simple example of RedBaron operation is shown on :numref:`red-simple`. It uses a simple :code:`a = 5` assigment as
the input and shows how RedBaron turns the code into special 'nodes'.

.. code-block:: python
    :caption: Radbaron output for :code:`a = 5`
    :name: red-simple

    >>> red = RedBaron('a = 5')
    >>> red.help()
    0 -----------------------------------------------------
    AssignmentNode()
      # identifiers: assign, assignment, assignment_, assignmentnode
      operator=''
      target ->
        NameNode()
          # identifiers: name, name_, namenode
          value='a'
      value ->
        IntNode()
          # identifiers: int, int_, intnode
          value='5'

It shows that the input code is turned into 'AssigmentNode' object, that has 3 parameters:

    * Operator -
    * Target - assignment target
    * Value - value assigned to target


The power of RedBaron is that, these objects can be very easly modified. For example, one could set
:code:`red[0].value = '5 + 1'` and this would turn the overall code to :code:`a = 5 + 1`.
RedBaron also provides methods to, for example 'find' can be used to find all the 'assignment' nodes in the code.


Pyha handles the conversion to VHDL by overwriting the RedBaron nodes. For example for the 'AssignmentNode'
Pyha inherits from the base node but changes the string output so that assignment operator '=' is changed to
':=' and at the end of the expression ';' is added. So the output would be :code:`a := 5;`, that is VHDL compatible
statement.

For example in the above example main node is AssignmentNode, this could be modified to change the '=' into
':=' and add ';' to the end of line. Resulting in a VHDL compatible statement :code:`a := 5;`.




Basic conversions
~~~~~~~~~~~~~~~~~

Supporting VHDL variable assignment in Python code is trivial, only the VHDl assignment notation must be
changed from :code:`:=` to :code:`=`.


Converting functions
~~~~~~~~~~~~~~~~~~~~

First of all, all the convertable functions are assumed to be class functions, that means they have the first argument
:code:`self`.

Python is very liberal in syntax rules, for example functions and even classes can be defined inside functions.
In this work we focus on functons that dont contain these advanced features.

VHDL supports two style of functions:

    - Functions - classical functions, that have input values and can return one value
    - Procedures - these cannot return a value, but can have agument that is of type 'out', thus returing trough an output argument. Also it allows argument to be of type 'inout' that is perfect for class object.

All the Python functions are to be converted to VHDL procedures as they provide more wider interface.

Python functions can return multiple values and define local variables. In order to support multiple return,
multiple output arguments are appended to the argument list with prefix :code:`ret_`. So for example first return
would be assigned to :code:`ret_0` and the second one to :code:`ret_1`.

Here is an simple Python function that contains most of the features required by conversion, these are:

    - First argument self
    - Input argument
    - Local variables
    - Multiple return values

.. code-block:: python

    def main(self, a):
        b = a
        return a, b



.. code-block:: vhdl
    :caption: VHDL example procedure
    :name: vhdl-int-arr2
    :linenos:

    procedure main(self:inout self_t; a: integer; ret_0:out integer; ret_1:out integer) is
        variable b: integer;
    begin
        b := a;
        ret_0 := a;
        ret_1 := b;
        return;
    end procedure;

In VHDL local variables must be defined in a special region before the procedure body. Converter can handle these
caese thanks to the previously discussed types stuff.

The fact that Python functions can return into multiple variables requires and conversion on
VHDL side:

.. code-block:: python

    ret0, ret1 = self.main(b)

.. code-block:: vhdl

    main(self, b, ret_0=>ret0, ret_1=>ret1);



Conclusion
----------

This chapter presented the proposed, fully synthesizable, object-oriented model for VHDL.

Its major advantage is that none of the VHDL data-flow semantics are used (except for top level entity). This makes
development similar to regular software. Programmers new to the VHDL language can learn this way much faster
as their previous knowledge of other languages transfers.

Moreover, this model is not restricted to one clock domain and allows simple way of describing registers.

The major motivation for this model was to ease converting higher level languages into VHDL. This goal has been definitely
reached, next section of this thesis develops Python bindings with relative ease. Conversion is drastically simplified as
Python class maps to VHDL class, Python function maps to VHDL function and so on.

.. todo:: Careful. You have only used relatively simple examples.
    To say 'definitely reached' you should have substantial evidence based on a large number of cases and/or some sort of formal proof.

Synthesizability has been demonstrated using Intel Quartus toolset. Bigger designs, like frequency-shift-keying receiver,
have been implemented on Intel Cyclone IV device. There has been
no problems with hierarchy depth, objects may contain objects which themselves may contain arrays of objects.




.. bibliography:: bibliography.bib
    :style: unsrt