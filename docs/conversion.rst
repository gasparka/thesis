Conversion
==========
This chapter examines the feasability and means of converting Python code to VHDL.

What about verilog?


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

Simulation and verification
---------------------------
Make separate chapter for testing and verification? Basics can be described here.
Requrements...want RTL sim, GATE sim, in loop etc

Implementation of the simulation code relies heavily on the signal assignment semantics.
Basically code writes to the 'next' element and thats it. After the top-level function call,
all the 'next' values must be propagated into the original registers. This process is basically an
clock tick

Essentially this comes downt to being and VHDL simulator inside VHDL simulator. it may sound stupid, but it works for
simulations and synthesys, so i guess it is not stupid.

Python simulation
~~~~~~~~~~~~~~~~~


RTL simulation
~~~~~~~~~~~~~~


Testing
-------

