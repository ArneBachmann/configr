Configr
=======


.. image:: https://travis-ci.org/ArneBachmann/configr.svg?branch=master
   :target: https://travis-ci.org/ArneBachmann/configr

.. image:: https://badge.fury.io/py/configr.svg
   :target: https://badge.fury.io/py/configr

.. image:: https://coveralls.io/repos/github/ArneBachmann/configr/badge.svg?branch=master
   :target: https://coveralls.io/github/ArneBachmann/configr?branch=master



Synopsis
--------

This small utility library helps managing global or per-user configuration for your Python apps.
Installation through ``pip`` will install the ``appdirs`` package as a dependency, but the code may be used without any external dependencies as well.


Code Example
------------

Simple use::

    >>> import configr
    >>> cfg = configr.Configr("myapp")
    >>> cfg.a = "Value of A"
    >>> print cfg["a"]
    Value of A


Motivation
----------

This library helps solving a common problem found in many apps: simplified configuration/settings/preset handling.


Installation
------------

Using pip::

    pip install configr

Using setup.py (usually elevated rights are needed, e.g. via ``sudo`` (Linux) or ``runas`` (Windows))::

    python setup.py install


API reference
-------------

The Configr object has the following functions::

    __init__(_, name, data = {}, defaults = {})  # Constructor. "data" initializes the configuration, while "defaults" contains fallback values not explicity set on the configuration data.
    saveSettings(_, keys = None, location = None)  # Persist the configuration. "keys" limits the entries written. "location" is a file system path
    loadSettings(_, data = {}, location = None, ignores = [])  # load configuration. "data" is used if its key is not found in the file. "ignores" are keys to not load. location" is a file system path

Configr object supports dictionary and attribute style access to get or set entries.
Both "loadSettings" and "saveSettings" support an additional "clientCodeLocation" parameter to allow passing a path to further separated several installation locations of the same app on a single file system. This allows to separate settings for each installation, if they are placed in different directories.


Building, packaging and distribution
------------------------------------

Run ``python setup.py build sdist`` to package the module.
Run ``twine upload dist/*.tar.gz`` to upload the module to PyPI.


Todo
----

This library is supposed to be lightweight and gets the job done so far.
If you have ideas, please put them into the projec's issue tracker on Github.


Tests
-----

The tool provides unit tests through the doctest module and integration tests through the unittest module.


Contributors
------------

This library is currently developed and maintained by Arne Bachmann.


License
-------

Licensed under the terms of MIT license.

    MIT License

    Copyright (c) 2016-2017 Arne Bachmann

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
