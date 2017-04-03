Design flow
===========

This chapter aims to investigate how modern software development techniques coulde be used
in design of hardware.

While MyHDL brings development to the Python world, it still requires the make of testbenches
and stuff. Pyha aimst to simplify this by providing higl level simulation functions.

Convetional design flow
-----------------------

VHDL uuendused? VUNIT VUEM?

Test-driven development / unit-tests
------------------------------------

.. http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=1034&context=csse_fac

Model based development
-----------------------

How MyHDl and other stuffs contribute here?



Pyha support
------------

Since Pyha brings the development into Python domain, it opens this whole ecosystem for writing
testing code.

Python ships with many unit-test libraries, for example PyTest, that is the main one used for
Pyha.

As far as what goes for model writing, Python comes with extensive schinetific stuff. For example
Scipy and Numpy. In addition all the GNURadio blocks have Python mappings.


Simplifying testing
~~~~~~~~~~~~~~~~~~~

One problem for model based designs is that the model is generally written in some higher
level language and so testing the model needs to have different tests than HDL testing. That
is one ov the problems with CocoTB.

Pyha simplifies this by providing an one function that can repeat the test on model, hardware-model, RTL
and GATE level simulations.


Ipython notebook
~~~~~~~~~~~~~~~~

It is interactive environment for python.
Show how this can be used.







