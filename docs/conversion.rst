.. _ch_vhdl:

Conversion to VHDL
==================

This chapter shows how Pyha converts to VHDL.

.. todo:: Pilt converterist

    * Simulatsioon tüüpide leidmiseks
    * Python syntax to VHDL
    * Sequential OOP VHDL IR

First part of this chapter introduces the Sequential OOP VHDL IR.

While other high level tools convert to very low-level VHDL, then Pyha takes and different approach by
first developing an feasible model in VHDL and then using Python to get around VHDL ugly parts.

Many tools on the market are capable of converting higher level language to VHDL.
However, these tools only make use of the very basic dataflow semantics of VHDL language,
resulting in complex conversion process and typically unreadable VHDL output.


Sequential, Object-oriented style for VHDL
------------------------------------------

This chapter develops sequential synthesizable object-oriented (OOP) programming model for VHDL.
The main motivation is to use it as an intermediate language for High-Level synthesis of
hardware.

VHDL has been chosen over SystemVerilog(SV) because it is a strict language and forbids many mistakes during compile time.
SV on the other hand is much more permissive, for example allowing out-of-bounds array indexing :cite:`sysverilog_gotcha`.

Sequential programming in VHDL has been studied by Jiri Gaislter in :cite:`structvhdl_gaisler`. He showed that
combinatory logic is easily described by fully sequential functions. He proposesed the 'two-process'
design method, where one of the processes is for comb and other for registers. Hes work is limited to one clock domain.

This sections contribution is the extension of the 'two process' model by adding an Object-oriented approach.
The basic idea of OOP is to bundle data and define functions that perform actions on this data.
This idea fits well with hardware design, as 'data' can be thought as registers and combinatory logic as functions that
perform operations on the data.

VHDL has no direct support, but the OOP style can be still used by by combining data in records (same as 'C' struct)
and passing them as a parameters to functions. This is essentially the same way how C programmers do it.

:numref:`vhdl_oop` demonstrates pipelined multiply-accumuluate(MAC), written in OOP VHDL. Recall that all the items
in the ``self_t`` are to be registers. One inconvenience is that VHDL procedures cannot 'return' ,
instead 'out' direction arguments must be used. On the other hand this helps to handle Python functions that can
return multiple values.

.. code-block:: vhdl
    :caption: OOP style multiply-accumulate in VHDL
    :name: vhdl_oop

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

    procedure main(self: inout self_t; a: in integer; ret_0: out integer) is
    begin
        self.mul := a * self.coef;
        self.acc := self.acc + self.mul;
        ret_0 := self.acc;
    end procedure;


The synthesis results (:numref:`ghetto_comb_mac_rtl`) show that a functionally correct MAC has been implemented.
However, in terms of hardware, it is not quite what was wanted.
The data model specified 3 registers, but only the one for 'acc' is present and even this is at the wrong location.

.. _ghetto_comb_mac_rtl:
.. figure:: img/ghetto_comb_mac_rtl.png
    :align: center
    :figclass: align-center

    Unexpected synthesis result of :numref:`vhdl_oop` (Intel Quartus RTL viewer)


Defining registers with variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clearly the way of defining registers is not working properly.
The mistake was to expect that the registers work in the same way as 'class variables' in traditional programming
languages.

Hardware registers have just one difference to class variables, the value assigned to them does not take
effect immediately, but rather on the next clock edge. That is the basic idea of registers, they take a new value
on clock edge. When the value is set at **this** clock edge, it will be taken on **next** clock edge.

Trying to stay in the software world, we can abstract away the clock edge by thinking that it denotes the
call to the 'main' function. Meaning that registers take the assigned value on the next function call,
meaning assignment is delayed by one function call.

VHDL defines a special assignment operator for this kind of delayed assignment, it is called 'signal assignment'.
It must be used on VHDL signal objects like :code:`a <= b`.

VHDL signals really come down to just having two variables, to represent the **next** and **current** values.
Signal assignment operator sets the value of **next** variable. On the next simulation delta, **current** is automatically
set to equal **next**.

This two variable method has been used before, for example Pong P. Chu, author of one of the most reputed VHDL books,
suggests to use this style in defining sequential logic in VHDL :cite:`chu_vhdl`. The same semantics are also used in
MyHDL signal objects :cite:`jan_myhdl_signals`.

Adapting this style for the OOP data model is shown in :numref:`mac-next-data`.
The new data model extends the structure to include the 'nexts' object,
that can used to assign **next** value for registers, for example :code:`self.nexts.acc := 0`.

.. code-block:: vhdl
    :caption: Data model with **next**, in OOP-style VHDL
    :name: mac_next

    type next_t is record
        mul: integer;
        acc: integer;
        coef: integer;
    end record;

    type self_t is record
        mul: integer;
        acc: integer;
        coef: integer;

        nexts: next_t; -- new element to hold 'next state' value
    end record;

    procedure main(self: inout self_t; a: integer; ret_0: out integer) is
    begin
        self.nexts.mul := a * self.coef;        -- now assigns to self.nexts
        self.nexts.acc := self.acc + self.mul;  -- now assigns to self.nexts
        ret_0 := self.acc;
    end procedure;

Now the loading of **next** to **current** must now be done manually.
:numref:`mac-next-update` defines new function
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

.. note:: Function 'update_registers' is called on clock raising edge. While the 'main' is called as combinatory function.

.. todo:: add simple top level example here?


Synthesising this results in expected logic, that is MAC with pipelined registers (:numref:`mac_rtl_end`).

.. _mac_rtl_end:
.. figure:: img/mac_rtl.png
    :align: center
    :figclass: align-center

    Synthesis result of the revised code (Intel Quartus RTL viewer)


Creating instances
~~~~~~~~~~~~~~~~~~

.. todo:: consider removing this section, quite useless..

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

VHDL supports 'packages' to group common types and functions into one namespace.

:numref:`package-mac` shows the template package for VHDL 'class'.
All the class functionality is now in common namespace.

.. code-block:: vhdl
   :caption: Package template for OOP style VHDL
   :name: package-mac

    package Class is
        type next_t is record
            ...
        end record;

        type self_t is record
            ...
            nexts: next_t;
        end record;

        -- function prototypes
    end package;

    package body Class is
        procedure reset(self: inout self_t) is
            ...
        procedure update_registers(self: inout self_t) is
            ...
        procedure main(self:inout self_t) is
            ...
        -- other user defined functions
    end package body;



Examples
~~~~~~~~

Creating a new class that connects two MAC instances in series is simple, first we need to create two
MAC packages called MAC_0 and MAC_1 and add them to the data model (:numref:`mac-series-data`).
The next step is to call MAC_0 operation on the input and then pass the output
trough MAC_1, whose output is the final output (:numref:`mac-series-main`).

.. todo:: why MAC_0 and MAC_1?

.. code-block:: vhdl
    :caption: Series MACs in OOP-style VHDL
    :name: mac-series-data

    type self_t is record
        mac0: MAC_0.self_t; -- define 2 MACs as part of data model
        mac1: MAC_1.self_t;

        nexts: next_t;
    end record;

    procedure main(self:inout self_t; a: integer; ret_0:out integer) is
        variable out_tmp: integer;
    begin
        MAC_0.main(self.mac0, a, ret_0=>out_tmp);       -- connect MAC_0 output to MAC_1 input
        MAC_1.main(self.mac1, out_tmp, ret_0=>ret_0);
    end procedure;


Synthesis result shows that two MACs are connected in series :numref:`mac_reuse_stack`.

.. _mac_reuse_stack:
.. figure:: img/mac_reuse_stack.png
    :align: center
    :figclass: align-center

    Synthesis result of the new class (Intel Quartus RTL viewer)

Connecting two MAC's instead in parallel can be done with simple modification to 'main' function,
that instead now returns both outputs (:numref:`mac-parallel`).

.. code-block:: vhdl
    :caption: Main function for parallel instances, in OOP-style VHDL
    :name: mac-parallel

    procedure main(self:inout self_t; a: integer; ret_0:out integer; ret_1:out integer) is
    begin
        MAC_0.main(self.mac0, a, ret_0=>ret_0); -- return MAC_0 output
        MAC_1.main(self.mac1, a, ret_0=>ret_1); -- return MAC_1 output
    end procedure;

Two MAC's are synthesized in parallel, as shown in :numref:`mac_reuse_parallel`.

.. _mac_reuse_parallel:
.. figure:: img/mac_reuse_parallel.png
    :align: center
    :figclass: align-center

    Synthesis result of :numref:`mac-parallel` (Intel Quartus RTL viewer)


Multiple clock domains
~~~~~~~~~~~~~~~~~~~~~~

Multiple clock domains can be easily supported by updating registers at different clock domains.
By reusing the parallel MAC's example, consider that MAC_0 and MAC_1 work in different clock domain.
For this only the top level process must be modified (:numref:`mac-parallel-clocks`), rest of the code stays the same.


.. code-block:: vhdl
    :caption: Top-level for multiple clocks, in OOP-style VHDL
    :name: mac-parallel-clocks

    if (not rst_n) then
        ReuseParallel_0.reset(self);
    else
        if rising_edge(clk0) then
            MAC_0.update_registers(self.mac0); -- update 'mac0' on 'clk0' rising edge
        end if;

        if rising_edge(clk1) then
            MAC_1.update_registers(self.mac1); -- update 'mac1' on 'clk1' rising edge
        end if;
    end if;

Synthesis result (:numref:`mac_parallel_two_clocks`) show that
registers are clocked by different clocks. The reset signal is common for the whole design.

.. _mac_parallel_two_clocks:
.. figure:: img/mac_parallel_two_clocks.png
    :align: center
    :figclass: align-center

    Synthesis result with modified top-level process (Intel Quartus RTL viewer)


Converting Python to VHDL
-------------------------

The Python to VHDL conversion process relies heavily on the results of last chapter, that allows
sequential OOP Python code easily map to VHDL. Even so, converting Python syntax to VHDL poses some problems.

The biggest challenge in conversion from Python to VHDL is types, namely Python does not have them, while VHDL has.
Conversion process must find all the types for Python variables, the process of this is described in
:numref:`pyvhdl_types`.

After the types are all known, the design can be converted from Python to VHDL syntax. This requires some way
of traversing the Python source code and applying VHDL rated transforms.

Conversion progress requires no understanding
of the source code nor big modifications.
.. _pyvhdl_types:

Finding the types
~~~~~~~~~~~~~~~~~

Python is dynamically typed language, meaning that types come into play only when the code is running. On the
other hand VHDL is statically typed, all the types must be written in soruce code.

The advantage of the Python way is that it is easier to program, no need to define variables and ponder about the types.
Downsides are that there may be unexpected bugs when some variable changes type. In some cases dynamic typing may also
reduce code readability.

In sense of conversion, dynamic typing poses a major problem, somehow the missing type info should be recovered for the
VHDL code. Most straightforward way to solve this is to try finding the variables value from code, for example
``a = 5``, clearly type of ``a`` is integer. Problem with this method is that is much more
complex than it initially appears. For example :code:`a = b`. To find the type of 'a' converter would need to lookup type
of 'b', these kind of sutffs can get really complex.

Alternative, and what Pyha is using, is to run the Python code so all the variables get some value, the value can
be inspected programmically and type inferred.
For example, consider the class on :numref:`types_problem`.

.. code-block:: python
    :caption: Example Python class, what are the types?
    :name: types_problem

    class SimpleClass(HW):
        def __init__(self, coef):
            self.coef = coef

        def main(self, a):
            local_var = a

:numref:`class-vars` show example for getting the type of class variable. It initializes the class with argument ``5``,
that is assigned to the 'coef' variable. Then ``type()`` can be used to query the variable type. On the example
result is ``int``, so this can be converted to VHDL ``integer`` type.

.. code-block:: python
    :caption: Using ``type()`` to get type name
    :name: class-vars

    >>> dut = SimpleClass(5)
    >>> dut.coef
    5
    >>> type(dut.coef)
    <class 'int'>

Pyha deduces registers initial values in same way, only the first assigned value is considered.

Local variables, like ``local_var`` and argument ``a`` on :numref:`class-vars` are harder to deduce as Python provides
no way of accessing function locals scope. Note that locals exsist only in the stack, thus after the function call
they are lost forever.
Luckly this problem has been encountered before in :cite:`py_locals_decorator`, which 'hacks' the Python
profiling interface in order to save the locals for each function.
Pyha uses this approach to keep track of the local values.

.. code-block:: python
    :caption: Function locals variable type
    :name: class-locals

    >>> dut.main.locals # before any call, locals are unknown
    {}
    >>> dut.main(1) # call function
    >>> dut.main.locals # locals can be extracted
    {'a': 1, 'local_var': 1}
    >>> type(dut.main.locals['local_var'])
    <class 'int'>


Advantage of this method is low complexity, another perk is that this way could be used to keep track of
all the variable values, in future this can enable the automatic conversion from floating point to fixed point.
In addition, this way allows the 'lazy' coding, for example where fixed-point gains the bound limit only during the
execution of the design.

Downside is that each function in the design must be executed before conversion is possible.
Also the conversion result may depend on the data types that are inputed to the functions, but this can
also be an advantage.


Syntax conversion
~~~~~~~~~~~~~~~~~

The syntax of Python and VHDL is surprisingly similar. VHDL is just much more verbose, requires types and Python
has indention oriented blocks.

Python provides some tools that simplify the traversing of source files, like abstract syntax tree (AST) module and
lib2to3. These tools work by parsing the Python file into a tree structure, that can be then traversed and modified.
For example the MyHDL conversion is based on this. This method works but is quite complex and requires alot of code.

Lately new project has emerged called RedBaron :cite:`redbaron`,
that aims to simplify operations with Python source code. It features rich tools for searching and modifing the
source code. Unlike AST it also keeps all the formatting in the code, including comments.
RedBaron parses the source code into rich objects, for example the ``a = 5`` would result in a ``AssignmentNode``
object that has an ``__str__`` function that instruct how these kind of objects are written out.

Pyha overwrites the ``__str__`` method to instead of ``=`` print ``:=`` and also add ``;`` to the end of statement.
Resulting in a VHDL compatible statement :code:`a := 5;`. Beauty of this is that this simple modification
actually turns **all** the Python style assignments to VHDL style.

:numref:`syn_py` shows a more complex Python code that is converted to VHDL (:numref:`syn_vhdl`), by Pyha.
Most of the transforms are obtained by the same method described above. Some of the transforms are a bit more complex,
like figuring out what variables need to be defined in VHDL code.

.. code-block:: python
    :caption: Python function to be converted to VHDL
    :name: syn_py

    def main(self, x):
        y = x
        for i in range(4):
            y = y + i

        return y

.. code-block:: vhdl
    :caption: Conversion of :numref:`syn_py` assuming ``integer`` types
    :name: syn_vhdl

    procedure main(self:inout self_t; x: integer; ret_0:out integer) is
        variable y: integer;
    begin
        y := x;
        for i in 0 to (4) - 1 loop
            y := y + i;
        end loop;

        ret_0 := y;
    end procedure;

Comparison to other methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Like HLS must do much work to deduce registers..
Pyha can convert basically line by line, very simple.

.. todo:: ??


Summary
-------

The sequential object-oriented VHDL model is one of the contributions of this thesis. It has been developed to provide
simpler conversion from Python to VHDL.
Pyha converts directly to the VHDL model by using RedBaron based syntax conversions. Type information is reuqired
trough the simulation before conversion.


.. bibliography:: bibliography.bib
    :style: unsrt