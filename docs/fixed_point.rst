Fixed-point type
----------------
Fixed point numbers can be to effectively turn floating point models into FPGA.


.. todo::
    ref http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.129.5579&rep=rep1&type=pdf
    https://www.dsprelated.com/showarticle/139.php

Fixed point numbers are defined to have bits for integer size and fractional size.
Integer bits determine the maximum size of the number.
Fractional bits determine the minimum resolution.

Main type of Pyha is Sfix, that is an signed fixed point number.

>>> Sfix(0.123, left=0, right=-17)
0.1230010986328125 [0:-17]
>>> Sfix(0.123, left=0, right=-7)
0.125 [0:-7]

Overflows and Saturation
~~~~~~~~~~~~~~~~~~~~~~~~

Practical fixed-point variables can store only a part of what floating point value could. Converting a design from floatin
to fixed point opens up a possiblity of overflows. That is, when the value grows bigger or smaller than the format
can reprsent. This condition is known as overflow.

By default Pyha uses fixed-point numbers that have saturaton enabled, meaning that if value goes over maximum
possible value, it is instead kept at the maximum value. Some examples:

    >>> Sfix(2.5, left=0, right=-17)
    WARNING:pyha.common.sfix:Saturation 2.5 -> 0.9999923706054688
    0.9999923706054688 [0:-17]
    >>> Sfix(2.5, left=1, right=-17)
    WARNING:pyha.common.sfix:Saturation 2.5 -> 1.9999923706054688
    1.9999923706054688 [1:-17]
    >>> Sfix(2.5, left=2, right=-17)
    2.5 [2:-17]

On the other hand, sometimes overflow can be a feature. For example, when designing free running counters.
For this usages, saturation can be disabled.

    >>> Sfix(0.9, left=0, right=-17, overflow_style=fixed_wrap)
    0.9000015258789062 [0:-17]

    >>> Sfix(0.9 + 0.1, left=0, right=-17, overflow_style=fixed_wrap)
    -1.0 [0:-17]


Rounding
~~~~~~~~

Pyha support rounding on arithmetic, basically it should be turned off as it costs alot.

.. :todo::
    ref https://www.embeddedrelated.com/showarticle/1015.php


Fixed-point arithmetic and sizing rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Arithmetic operations can be run on fixed point variables as usual. Division is not defined as it is almost always
unneccesary in hardware.

Library comes with sizing rules in order to guarantee that fixed point operations never overflow.

For example consider an fixed point number with format that can represent numbers between [-1, 1):
    >>> Sfix(0.9, 0, -17)
    0.9000015258789062 [0:-17]

Now adding two such numbers:
    >>> Sfix(0.9, 0, -17) + Sfix(0.9, 0, -17)
    1.8000030517578125 [1:-17]

While this operation should overflow, it did not. Because fixed point library always resizes the output for
the worst case. In case of addition it always adds one integer bit to accumulate possible overflows.

But note that this system is not very smart, if we would add up such numbers 100 times, it would add 100 bits to the
integer portion of the number.

The philosophy of fixed point library is to guarantee no precision loss happens during arithmetic operations, in order
to do this it has to extend the output format. It is designers job to resize numbers back into optimal format after
operations.


Resizing
~~~~~~~~

Fixed point number can be forced to whatever size by using the resize functionality.

    >>> a = Sfix(0.89, left=0, right=-17)
    >>> a
    0.8899993896484375 [0:-17]
    >>> b = resize(a, 0, -6)
    >>> b
    0.890625 [0:-6]

    >>> c = resize(a, size_res=b)
    >>> c
    0.890625 [0:-6]

Pyha support automatic resizing for registers. All assignments to registers will be automatically resized to the
original type of the definition.

.. :todo:: Autoresize should be mentioned somwhere else maybe?


Conversion to VHDL
~~~~~~~~~~~~~~~~~~
VHDL comes with a strong support for fixed-point types by providing and fixed point package in the standard library.
More information is about this package is given in :cite:`vhdlfixed`.

In general Sfix type is built in such a way that all the functions map to the VHDL library, so no conversion
is neccesary.

Another option would have been to implement fixed point compiler on my own, it would provide more flexibility but
it would take many time + it has t be kept in mind that the VHDL library is already production-tested. Ths mapping to
VHDL library seemed like the best option.

It limits the conversion to VHDL only, for example Verilog has no fixed point package in standard library.

Complex fixed-point
-------------------
Objective of this tool was to simplify model based design and verification of DSP to FPGA models.
One frequent problem with DSP models was that they commonly want to use complex numbers.
In order to unify the interface of the model and hardware model, Pyha supports complex numbers for interfacing means,
arithmetic operations are not defined. That means complex values can be passed arond and registered but arithmetics must
be done on :code:`.real` and :code:`.imag` elements, that are just Sfix objects.


    >>> a = ComplexSfix(0.45 + 0.88j, left=0, right=-17)
    >>> a
    0.45+0.88j [0:-17]
    >>> a.real
    0.4499969482421875 [0:-17]
    >>> a.imag
    0.8799972534179688 [0:-17]

    Another way to construct it:

    >>> a = Sfix(-0.5, 0, -17)
    >>> b = Sfix(0.5, 0, -17)
    >>> ComplexSfix(a, b)
    -0.50+0.50j [0:-17]


