Python bindings and simulator
=============================


Kohe alguses avada MAC näitega?
Kogu thesis põhineb MAC näitel?


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

As shown in previous chapter, traditional language features can be used to infer hardware components.
One must still keep in mind of how the code will convert to hardware. For example all loops (For) will be unrolled,
this dentotes that the loop control must have finitive limit.

Another point to note is that every arithmetical operator used will use up resorce. There is a big difference between
hardware and software programming, using operators in software takes up time but in hardware they will all run in parallel
so no addtional time is used BUT resource. There are ways to share the operators to trade resource for time.

One thing that is not natively supported in python is registers, for this we did special stuff in VHDL section,
basically the same can be done in Python domain.

statemachines?

Adding registers support
~~~~~~~~~~~~~~~~~~~~~~~~

The init function is used to determine the startup valu

Working with registers is implemented in a same way as in VHDL model. Meaning there are buffered.
For this there is metaclass action, that allows chaning the process of class creation.
Metaclass copies all the object data model to a new variable called 'next'. Thus automating the creation
of the buffer values.

How signal assignments can work in Python.

Moreover, automatically function is created for updating the registers, it was named 'update registers' in VHDL
model, now it is named '_pyha_update_self'. The effect of it is exactly the same, it copies 'next' variables
to 'current', thus mimicing the register progress.


Reset values
~~~~~~~~~~~~

In hardware is is important to be able to set the reset/power on values for the registers. In same sense this is
important for class instance creation.


.. code-block:: python
   :caption: Reset example
   :name: pyha-reset

    class SimpleClass(HW):
        def __init__(self):
            self.reg0 = 123
            self.reg1 = 321

:numref:`pyha-reset` shows an example class, that defines two registers. Initial values for them will be also their
hardware reset values.

State-machines
~~~~~~~~~~~~~~



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