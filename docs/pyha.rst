Pyha
====
This paragraph gives an basic overview of the developed tool.

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

Floats can be used as constants only, in coperation with Fixed point class.


.. include:: fixed_point.rst




Lists
~~~~~


Metaclass
---------

Conversion to VHDL
------------------


Simulation and verification
---------------------------

Python simulation
~~~~~~~~~~~~~~~~~


RTL simulation
~~~~~~~~~~~~~~


Testing
-------