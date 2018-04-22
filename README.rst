Configr 2018.1422.1940
======================


.. image:: https://travis-ci.org/ArneBachmann/configr.svg?branch=master
   :target: https://travis-ci.org/ArneBachmann/configr

.. image:: https://ci.appveyor.com/api/projects/status/lyidsj76smdyxd8v?svg=true
   :target: https://ci.appveyor.com/project/ArneBachmann/configr

.. image:: https://badge.fury.io/py/configr.svg
   :target: https://badge.fury.io/py/configr

.. image:: https://coveralls.io/repos/github/ArneBachmann/configr/badge.svg?branch=master
   :target: https://coveralls.io/github/ArneBachmann/configr?branch=master

.. image:: https://img.shields.io/pypi/pyversions/Django.svg
   :target: https://github.com/ArneBachmann/configr

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: https://github.com/ArneBachmann/configr

.. image:: https://bettercodehub.com/edge/badge/ArneBachmann/configr?branch=master
   :target: https://bettercodehub.com

Works with Python 2.7 and Python 3.3+


Synopsis
--------

This little utility library helps managing global or per-user configuration for your Python apps and therefore simplifies the common problem of configuration/settings/preset handling.

An installation through the ``pip`` command will also install the ``appdirs`` package as a dependency, but the code can be used without it as well.


Code Example
------------

Simple use::

    >>> import configr
    >>> cfg = configr.Configr("myapp")
    >>> cfg.a = "Value of A"
    >>> print cfg["a"]
    Value of A


Installation
------------

Using pip::

    pip install configr

Using setup.py (usually elevated rights are needed, e.g. via ``sudo`` (Linux) or ``runas`` (Windows))::

    python setup.py install

or

    python setup.py install -e .

for a development installation (pointing to the folder you checked the source code out in).


API reference
-------------

The ``configr.Configr`` object provides the following functions::

    __init__(_, name:Optional[str] = None, data:Dict[str,Any] = {}, defaults:Dict[str,Any] = {})  # "data" initializes the configuration, while "defaults" contains fallback values

    loadSettings(_, data:Dict[str,Any] = {}, location:Optional[str] = None, ignores:List[str] = [], clientCodeLocation:Optional[str] = None)  # load configuration. "data" is used for keys not in the file. "ignores" are keys to not load. "location" is a file system path, clientCodeLocation should be a call to os.path.abspath(__file__)

    saveSettings(_, keys:Optional[Dict[str,Any]] = None, location:Optional[str] = None, ignores:List[str] = [], clientCodeLocation:Optional[str] = None)  # save configuration. "keys" limits the entries written. "location" is a file system path, clientCodeLocation should be a call to os.path.abspath(__file__)

    keys(_)  # returns list of keys (Python 2) or an dict_keys object (Python 3)
    values(_)  # returns list of values (Python 2) or a dict_values object (Python 3)
    items(_)  # returns a list of (key, value) tuples (Python 2) or a dict_items object (Python 3)

Configr objects support dictionary and attribute style access to get or set entries, as well as the usual means to remove entries via ``del`` and ``remove()``.
Both ``loadSettings`` and ``saveSettings`` support an additional ``clientCodeLocation`` parameter to allow passing a unique file system path from the caller. This allows to separate settings for multiple installation locations of the same app on a single file system, cf. API comment above.

Both functions also return a named 2-tuple ``ReturnValue`` containing last loaded/saved file location in the first (``.path``), or an exception in the second (``.error``) position.

You may also nest Configr objects to have different levels of defaults (e.g. per-system, per-user, per-software, per-instance, ...), by passing Configr objects instead of the ``defaults`` dictionary.


Building, packaging and distribution
------------------------------------

- Run test suite under ``configr`` via ``python configr/test.py`` with Python 2 and Python 3. If there are no problems, continue:
- Run ``python setup.py clean build sdist`` to compile, raise the version number, and create the package archive.
- Run ``git commit`` and ``git push`` and let Travis CI run all tests. If the changes have no problems, continue:
- Run ``twine upload dist/*.tar.gz`` to upload the module to PyPI.


Todo
----

This library is supposed to be lightweight and gets the job done so far.
If you have ideas or discover bugs, please put them into the project's issue tracker on Github.


Tests
-----

The tool provides unit tests through the ``doctest`` module and integration tests through the ``unittest`` module.


Who uses it?
------------

The library is currently used by the `SOS project
<http://sos-vcs.net/>`_, developed by the author.
If you use ``configr`` for your Python apps, please let me know.


Contributors
------------

This library is currently developed and maintained by Arne Bachmann.


License
-------

Licensed under the terms of MIT license.

    MIT License

    Copyright (c) 2016-2018 Arne Bachmann

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
