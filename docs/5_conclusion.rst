.. _5_conclusion:

Conclusion
==========

The task of implementing DSP systems on hardware is often carried out by using high level tools, such as MATLAB. However, these tools are costly, thus not available for everyone and unsuitable for open-source designs. Other high-level tools are mostly based on 'C', which is not reasonable for modeling purposes.
Given the limitations and drawbacks of existing solutions,
this thesis has proposed Pyha, a new Python based hardware description language aimed at simplifying DSP hardware
development in an open-source manner.

Overview of main features of Pyha have been given and shown that the proposed tool is usable for
describing hardware components. It was also demonstrated that Pyha supports
fixed-point types and semi-automatic conversion from floating point types.
Pyha also provides good support for unit test and enables debugging of hardware designs in Python ecosystem.

Two use cases presented in :numref:`4_examples` show that the developed solution is already usable on solving
real life problems. First, the moving average filter was implemented and demonstrated as a matched filter.
The second example showed how the object-oriented nature of Pyha can be used for simple design reuse by
developing linear phase DC removal filter.

The comparison to other similar tools (:numref:`4_comparison`) show that Pyha is an good alternative for commercial tools and provides increased abstraction level compared to other open source tools. Pyha may appeal to designers coming from software programming as it uses regular Python constructs and executes in sequential manner.


Contributions
~~~~~~~~~~~~~

The contributions of this thesis are:

    * Hardware description, simulation and debugging in Python - this is the main contribution of this thesis;
    * Sequential object-oriented VHDL model - the object-oriented VHDL model was developed to allow simple conversion from Python to VHDL;
    * Method for converting Python to X - this thesis developed an simple way to convert Python syntax to VHDL, this method could be used for other purposes as well;
    * Fixed-point arithmetic library for Python - fixed-point library was developed to support cycle-accurate simulation with the converted VHDL code, this library can be used to model fixed-point systems in Python domain;
    * Simplified simulation functions -  functions that can execute multiple layers of simulations (Python, RTL, GATE) without any boilerplate code, this contribution significantly improves the testability of hardware designs.

Future work
~~~~~~~~~~~

The technical part of Pyha has been developed by the author of this thesis during the period of one year; while the work is already usable, it could be definitely improved. For example, finishing the support of automatic conversion from floating-point to fixed-point. The current scope of the Python simulator has been limited to single clock domain, which is suitable for most DSP systems; lifting this limitation could make Pyha acceptable for wider community.

One of the most interesting enchantment would be the extension to the conversion process, to support some HLS backend (such as VivadoHLS). This would present the designer an choice between describing the RTL with VHDL backend or higher-level abstractions with HLS backend.

Long term work is to implement more DSP blocks in Pyha, so that complex systems could be built faster. In addition, the tool should also be supported on Windows based systems.

