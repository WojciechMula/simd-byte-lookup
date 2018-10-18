================================================================================
               SIMDized check which bytes are in a set 
================================================================================

Sample programs for `my article`__.

__ http://0x80.pl/articles/simd-byte-lookup.html

Software
--------------------------------------------------------------------------------

The main utility in is python script ``test.py``. It accepts:

* name of matching method,
* list of hexadecimal values that represent a set.

Please refer to ``Makefile`` for sample invocations.

The script generates a C++ program with implementation of function that checks
which bytes are present in the set. The program contains unit test which
validates the generated procedure.

Type ``make`` to build and run several sample programs.


Caveats
--------------------------------------------------------------------------------

Currently only SSE instructions are supported.
