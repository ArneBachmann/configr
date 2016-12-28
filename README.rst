Configr
=======


|BuildStatus|_

.. |BuildStatus| image:: https://travis-ci.org/ArneBachmann/configr.svg?branch=master
.. _BuildStatus: https://travis-ci.org/ArneBachmann/configr


Synopsis
--------

This small utility library helps managing global or per-user configuration data for your apps.
Installation through pip will install the appdirs package, but the code may be used without any external dependencies as well.


Code Example
------------

Simple use::

    import configr
    cfg = configr.Configr("myapp")
    cfg.a = "Value of A"
    print cfg["a"]


Motivation
----------

This library helps solving a common problem found in many apps: simple configuration (file) handling.


Installation
------------

Using pip::

    pip install configr

Using setup.py (usually elevated rights are needed, e.g. via ``sudo`` (Linux) or ``runas`` (Windows))::

    python setup.py install


API reference
-------------

The Configr object has the following functions::

    __init__(_, name, data = {}, defaults = {})
    loadSettings(_, defaults = {}, location = None, ignores = [])
    SaveSettings(_, keys = None, location = None)

Additionally the object supports dictionary and attribute style access (the latter of couse only for keys that start with an alphabetic character or underscore).


Tests
-----

The tool provides unit tests through the doctest module and integration tests through the unittest module.


Contributors
------------

This library is currently developed by Arne Bachmann.


License
-------

Licensed under the terms of MIT license.

    MIT License

    Copyright (c) 2016 Arne Bachmann

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
