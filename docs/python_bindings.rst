Python bindings and simulator
=============================


.. note:: No need to go too detailed here!

Why Python? Easy to hack.

Last chapter developed OOP VHDL way. This chapter build on top of this and develops Python bindings.
Developing in Python has multiple advantages

    - Rich librarys
    - Simpler syntax
    - Free development tools

Moreover, simulator is provided that so Python designs can be simulated before conversion.
Fixed point support is added and described.

Last chapter shows how Python ecosystem can be used to greatly simply the testing/verifying of systems.
Model based design.

Python model and Simulation
---------------------------

This chapter introduces the way of writing hardware designs in Python. Simulator info is provided also.
This chapter does not worry about conversion process.

Object-orientation in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unit object is Python class as shown on

.. code-block:: python
   :caption: Basic Pyha unit
   :name: basic-pyha

    class SimpleClass:
        def __init__(self, coef):
            self.coef = coef

        def main(self, input):
            pass


:numref:`basic-pyha` shows the besic design unit of the developend tool, it is a standard Python class, that is derived
from a baseclass HW, purpos of this baseclass is to do some metaclass stuff and register this class as Pyha module.

As for the VHDL model, we can assume that all the variables in the 'self' scope are registers.


Writing hardware in Python
~~~~~~~~~~~~~~~~~~~~~~~~~~


Adding registers support
~~~~~~~~~~~~~~~~~~~~~~~~

Working with registers is implemented in a same way as in VHDL model. Meaning there are buffered.
For this there is metaclass action, that allows chaning the process of class creation.
Metaclass copies all the object data model to a new variable called 'next'. Thus automating the creation
of the buffer values.

How signal assignments can work in Python.

Moreover, automatically function is created for updating the registers, it was named 'update registers' in VHDL
model, now it is named '_pyha_update_self'. The effect of it is exactly the same, it copies 'next' variables
to 'current', thus mimicing the register progress.

Simulation
~~~~~~~~~~

Simulation of single clock designs is trivial. Main function must be called and then '_pyha_update_self'. This
basically is an action for one clock edge.

Here is an example that pushes some data twough the MAC component. This simulation result is equal to
the GHDL simulation and generated netlist GATE simulation.

.. todo:: add fixed point type here? rather keep separte? Convertable subset?

Last chapter shows how to further improve the simulation process by using helper function provided by Pyha.

Conclusions
~~~~~~~~~~~

Pyha extends Python language to add support for hardware also simulation is possible.


Conversion
----------

This chapter aims to convert the Python based model into VHDL, with the goal of synthesis.


Problem of types
~~~~~~~~~~~~~~~~

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


Conversion methodology
~~~~~~~~~~~~~~~~~~~~~~

Methodology is RedBaron.

VHDL is known as a strongly typed language in addition to that it is very verbose.
Python is dynamically typed and is basically as least verbose as possible.

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

Converting classes
~~~~~~~~~~~~~~~~~~


Extracting the data model
^^^^^^^^^^^^^^^^^^^^^^^^^

Instances
^^^^^^^^^


Overall converting classes is simple as they consist of functions.



Types
~~~~~
This chapter gives overview of types supported by Pyha.

Integers
^^^^^^^^

Integer types and operations are supported for FPGA conversion with a couple of limitations.
First of all, Python integers have unlimited precision :cite:`pythondoc`. This requirement is impossible to meet and
because of this converted integers are assumed to be 32 bits wide.

Conversion wize, all inger objectsa are mapped to VHDL type 'integer', that implements 32 bit signed integer.
In case integer object is returned to top-module, it is converted to 'std_logic_vector(31 downto 0)'.

Booleans
^^^^^^^^

Booleans in Python are truth values that can either be True or False.
Booleans are fully supported for conversion.
In VHDL type 'boolean' is used. In case of top-module, it is converted to 'std_logic' type.

Floats
^^^^^^

Floating point values can be synthesized as constants only if they find a way to become fixed_point type.
Generally Pyha does not support converting floating point values, however this could be useful because floating point
values can very much be used in RTL simulation, it could be used to verify design before fixed point conversion.

Floats can be used as constants only, in coperation with Fixed point class.


User defined types / Submodules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    :name: vhdl-int-arr3
    :linenos:

    type integer_list_t is array (natural range <>) of integer;
    l: integer_list_t(0 to 1);

Constants? Interfaces?


Testing, debugging and verification
-----------------------------------

This chapter aims to investigate how modern software development techniques coulde be used
in design of hardware.

While MyHDL brings development to the Python world, it still requires the make of testbenches
and stuff. Pyha aimst to simplify this by providing higl level simulation functions.

Background
~~~~~~~~~~

VHDL uuendused? VUNIT VUEM?

Test-driven development / unit-tests

.. http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1034&context=csse_fac

Model based development
How MyHDl and other stuffs contribute here?

Since Pyha brings the development into Python domain, it opens this whole ecosystem for writing
testing code.

Python ships with many unit-test libraries, for example PyTest, that is the main one used for
Pyha.

As far as what goes for model writing, Python comes with extensive schinetific stuff. For example
Scipy and Numpy. In addition all the GNURadio blocks have Python mappings.


Model based design, this is also called behavioral model (
.. https://books.google.ee/books?hl=en&lr=&id=XbZr8DurZYEC&oi=fnd&pg=PP1&dq=vhdl&ots=PberwiAymP&sig=zqc4BUSmFZaL3hxRilU-J9Pa_5I&redir_esc=y#v=onepage&q=vhdl&f=false)


Simplifying testing
~~~~~~~~~~~~~~~~~~~

One problem for model based designs is that the model is generally written in some higher
level language and so testing the model needs to have different tests than HDL testing. That
is one ov the problems with CocoTB.

Pyha simplifies this by providing an one function that can repeat the test on model, hardware-model, RTL
and GATE level simulations.


Ipython notebook
~~~~~~~~~~~~~~~~

Simple example of docu + test combo.
It is interactive environment for python.
Show how this can be used.


Conclusions
-----------

This chapter showed how Python OOP code can be converted into VHDL OOP code.

It is clear that Pyha provides many conveneince functions to greatly simplyfy the testing of
model based designs.