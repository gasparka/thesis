Switching from VHDL to Python
=============================

This chapter examines the feasability and means of converting Python code to VHDL.

What about verilog?

While other high-level tools decide to use VHDL/Verilog as low level conversion target.
Pyha goes other way around, as shown by the Gardner study, VHDL language can be used
with quite high level progrmaming constructs. Pyha tries to take advantage of this.
Disadvantage is that it can be only converted to VHDL. Advantages are numerous:

    - Similiar code in VHDL and Python
    - Clean conversion output
    - ?

Python vs VHDL
--------------
VHDL is known as a strongly typed language in addition to that it is very verbose.
Python is dynamically typed and is basically as least verbose as possible.

Comparison of syntax
--------------------


Assignments
-----------

In VHDL
~~~~~~~

The syntax of a variable assignment statement is :code:`variable-name := value-expression;`
The immediate assignment notion, :=, is used for the variable assignment. There is no time
dimension (i.e., no propagation delay) and the assignment takes effect immediately. The
behavior of the variable assignment is just like that of a regular variable assignment used
in a traditional programming language. :cite:`chu_vhdl`

The syntax of a sequential signal assignment is identical to that of the simple concurrent
signal assignment of Chapter 4 except that the former is inside a process. It can be written
as signal-name <= projected-waveform;
The projected-waveform clause consists of a value expression and a time expression,
which is generally used to represent the propagation delay. As in the concurrent signal
assignment statement, the delay specification cannot be synthesized and we always use the
default &delay. The syntax becomes signal-name <= value-expression;
Note that the concurrent conditional and selected signal assignment statements cannot be
used inside the process.
For a signal assignment with 6-delay, the behavior of a sequential signal assignment
statement is somewhat different from that of its concurrent counterpart. If a process has
a sensitivity list, the execution of sequential statements is treated as a “single abstract
evaluation,” and the actual value of an expression will not be assigned to a signal until the
end of the process. This is consistent with the black box interpretation of the process; that
is, the entire process is treated as one indivisible circuit part, and the signal is assigned a
value only after the completion of all sequential statements.
Inside a process, a signal can be assigned multiple times. If all assignments are with
&delays, only the last assignment takes effect. Because the signal is not updated until the
end of the process, it never assumes any “intermediate” value. For example, consider the
following code segment: :cite:`chu_vhdl`

Python support
~~~~~~~~~~~~~~

Supporting VHDL variable assignment in Python code is trivial, only the VHDl assignment notation must be
changed from :code:`:=` to :code:`=`.

Pyhas solution simplifies the VHDL assignments by have unified style with still same functionality.

Support for VHDl simulation needs to after the clock tick update the next values into actual values.

.. :todo:: Siin oleks vaja next süsteemi kirjeldada, kuidas see VHDL asjaga võrdne on..sama süsteem kasutusel
    MyHDL jne..


Design resuse
-------------


Object-orientation support
--------------------------

Major goal of this project is to support object-oriented hardware design.

Goal is to provide simple object support, advanced features like inherintance and overloadings are not considerted
at this moment.

Python itself comes with a strong object-orientation support. On the other hand VHDL has no class support whatsoever.


.. code-block:: python
   :caption: Basic class in Python
   :name: python-class

    class Name:
        def __init__(self):
            self.instance_member = 0

        def function(self, a, b):
            self.instance_member = a + b
            return self.instance_member

:numref:`this-py` shows an simple example of Python class. It has two functions, :code:`__init__` in python is a
class constructor. :code:`function` is just and user defined function.

It can be used as follows:
    >>> a = Name()
    >>> a.instance_member
    0
    >>> a.function(1, 2)
    3
    >>> a.instance_member
    3

Turning this kind of structure to VHDL can be done by levraging VHDL support for struct types.


.. code-block:: vhdl
    :caption: VHDL conversion for integer array
    :name: vhdl-int-arr
    :linenos:

    type self_t is record
        instance_member: integer;
    end record;

    procedure main(self:inout self_t; a: integer; ret_0:out integer) is
    begin
        self.instance_member := a;
        ret_0 := self.instance_member;
        return;
    end procedure;

.. :todo:: What about multi objects, resets etc??

Convertings
-----------

Based on the results of previous chapter it is clear that specific Python code can be converted to VHDL.
Doing so requires some way of parsing the Python code and outputting VHDL.

In general this step involves using an abstract syntax tree (AST). MyHDL is using this solution.

However RedBaron offers a better solution. RedBaron is an Python library with an aim to significally simply
operations with source code parsing. Also it is not based on the AST, but on FST, that is full syntax tree
keeping all the comments and stuff.

Here is a simple example:
    >>> red = RedBaron('a = b')
    >>> red
    0   a = b

RedBaron turns all the blocks in the code into special 'nodes'. Help function provides an example:
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
        NameNode()
          # identifiers: name, name_, namenode
          value='b'


Now Pyha defined a mirror node for each of RedBaron nodes, with the goal of turning the code into VHDL.
For example in the above example main node is AssignmentNode, this could be modified to change the '=' into
':=' and add ';' to the end of line. Resulting in a VHDL compatible statement:

.. code-block:: vhdl

    a := b;

Converting functions
~~~~~~~~~~~~~~~~~~~~

First of all, all the convertable functions are assumed to be class functions, that means they have the first argument
:code:`self`.

Python is very liberal in syntax rules, for example functions and even classes can be defined inside functions.
In this work we focus on functons that dont contain these advanced features.

VHDL supports two style of functions:

    - Functions - classical functions, that have input values and can return one value
    - Procedures - these cannot return a value, but can have agument that is of type 'out', thus returing trough an
output argument. Also it allows argument to be of type 'inout' that is perfect for class object.

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
    :name: vhdl-int-arr
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



Problem of types
----------------

Biggest difference and problem between Python and VHDL is the type system.
While in VHDL everything must be typed, Python is fully dynamically typed language, meaning that
types only come into play when the code is executing.


In general there are some different approaches to solve this problem:

    - Determining types from Python source code
    - Determining types from one pass execution/initial execution
    - Using longer simulation

First option is attractive as it could convert without any side actions, problem with this approach is that
the converter would have to be extreamly complex in order to infer the variable types. For example :code:`a = 5` is a
simple example that type is integer, but for example :code:`a = b` type is not clear. Converter would have to look up the type
of b, but which b? in which scope? etc. It is clear that this solution is not reasonable to solve.

Second option would use the result of initial execution of classes. In python defining an class object automatically
executes its constructor(:code:`def __init__(self)`). Basically theis would allow to determine all the class variables
types, by just making the object. It would be as good as the first option really, but simplifies the type deduction significaly.
Still type info provided here is not enough, for example local variables are not covered. One way would e to use only
class variables, but this has slight downsides aswell.

Last option would simulate the whole design in order to figure out every type in the design. After each execution to the
function, latest call stack is preserved (this includes all the values of locals). PyPy also uses system like this.
Downside of this solution is obviously that the desing must be simulated in Python domain before it can be converted to
VHDL.

Also the simulation data must cover all the cases, for example consider the function with conditional local variable,
as shown on :numref:`cond-main`. If the simulaton passes only True values to the function, value of variable 'b' will
be unknown ad vice-versa. This is a problem but not a huge one because in hardware...

.. code-block:: python
    :caption: Type problems
    :name: cond-main

    def main(c):
        if c:
            a = 0
        else:
            b = False

Other advantages this way makes possible to use 'lazy' coding, meaning that only the type after the end of simulation
matters.


.. :todo:: much improvements very wow


Language differences...

Extensions..wehn you can do more in python domain.

Feasability of converting Python to VHDL


Basics
------
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



Combinatory logic
-----------------

.. todo:: Ref comb logic.

.. code-block:: python
   :caption: Basic combinatory circuit in Pyha
   :name: pyha-comb

    class Comb(HW):
        def main(self, a, b):
            xor_out = a xor b
            return xor_out



:numref:`pyha-comb` shows the design of a combinatory logic. In this case it is a simple xor operation between
two input operands. It is a standard Python class, that is derived from a baseclass *HW,
purpose of the baseclass is to do some metaclass stuff and register this class as Pyha module.

Class contains an function 'main', that is considered as the top level function for all Pyha designs. This function
performs the xor between two inputs 'a' and 'b' and then returns the result.

In general all assigments to local variables are interpreted as combinatory logic.

.. todo:: how this turns to VHDL and RTL picture?



Sequential logic
----------------

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


Types
-----
This chapter gives overview of types supported by Pyha.

Integers
~~~~~~~~
Integer types and operations are supported for FPGA conversion with a couple of limitations.
First of all, Python integers have unlimited precision :cite:`pythondoc`. This requirement is impossible to meet and
because of this converted integers are assumed to be 32 bits wide.

Conversion wize, all inger objectsa are mapped to VHDL type 'integer', that implements 32 bit signed integer.
In case integer object is returned to top-module, it is converted to 'std_logic_vector(31 downto 0)'.

Booleans
~~~~~~~~

Booleans in Python are truth values that can either be True or False.
Booleans are fully supported for conversion.
In VHDL type 'boolean' is used. In case of top-module, it is converted to 'std_logic' type.

Floats
~~~~~~

Floating point values can be synthesized as constants only if they find a way to become fixed_point type.
Generally Pyha does not support converting floating point values, however this could be useful because floating point
values can very much be used in RTL simulation, it could be used to verify design before fixed point conversion.

Floats can be used as constants only, in coperation with Fixed point class.


.. include:: fixed_point.rst



User defined types / Submodules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For design reuse it is needed to reuse previously generated designs. Traditional HDLs use entity declarations for
this purpose. One of the key assumption of these entities is that they all run in parallel. This has some advantages
and disadvantages. Good thing is that this is the most flexible solution, that is it supports as many clocks and clock
domains as neccessary. Disadvantage is that in the end much of the VHDL programing comes down to wiring togather different
entities, and this can be worksome and bugful process.

Another downside is that all of these entities must be simulated as a separate process, this has a cost on simulation speed
and more severily it makes debugging hard..think about debugging multi-threaded programs.

In contrast to traditional HDLs, Pyha has taken an approach where design reuse is archived trough regular objects.
This has numerous advantages:

    - Defining a module is as easy as making an class object
    - Using submodule is as easy as in traditional programming..just call the functions
    - Execution in same domain, one process design

Result of this design decision is that using submodules is basically the same as in normal programming.
This decision comes with a severe penalty aswell, namely all the submodules then must work with the same clock signal.
This essentially limits Pyha designs down to using only one clock. This is a serious constrain for real life systems, but
for now it can be lived with.

It is possible to get around this by using clock domain crossing interfacec between two Pyha modules.


Support for VHDl conversion is straightforward, as Pyha modules are converted into VHDL struct. So having a
submodule means just having a struct member of that module.



Lists
~~~~~
All the previously mentioned convertible types can be also used in a list form. Matching term in VHDL vocabulary is
array. The difference is that Python lists dont have a size limit, while VHDL arrays must be always constrained.
This is actually not a big problem as the final list size is already known.

VHDL being an very strictly typed language requires an definition of each array type.

For example writing  :code:`l = [1, 2]` in Python would trigger the code shown in :numref:`vhdl-int-arr`, where line 1
is a new array type definitiaon and a second line defines a variable :code:`a` of this type. Note that the elements
type is deduced from the type of first element in Python array the size of defined array is as :code:`len(l)-1`.


.. code-block:: vhdl
    :caption: VHDL conversion for integer array
    :name: vhdl-int-arr
    :linenos:

    type integer_list_t is array (natural range <>) of integer;
    l: integer_list_t(0 to 1);


Conclusions
-----------

This chapter showed how Python OOP code can be converted into VHDL OOP code.

