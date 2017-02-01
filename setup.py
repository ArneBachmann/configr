import sys
import os
import time
import unittest
from setuptools import setup

# Upload to PyPI by running setup.py clean build_py sdist bdist upload with a correctly set up ~/.pypirc (need HOME variable set correctly on Windows)

with open("lib" + os.sep + "version.py", "w") as fd:  # create version string at build time
  fd.write(time.strftime("__version_info__ = tuple(int(_) for _ in ('%Y', '%m%d', '%H%M'))\n__version__ = '.'.join(map(str, __version_info__))\n"))

_top_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_top_dir, "tests"))  # temporary sys.path addition
sys.path.insert(0, os.path.join(_top_dir, "lib"))  # temporary sys.path addition
try: import configr, test  # needed for version strings
except Exception as E: print(E)
finally: del sys.path[:2]  # clean sys.path after import
README = open(os.path.join(_top_dir, 'README.rst')).read()
# CHANGES = open(os.path.join(_top_dir, 'CHANGES.rst')).read()

assert len(unittest.defaultTestLoader.loadTestsFromModule(test).run(unittest.TestResult()).errors) == 0
assert len(unittest.defaultTestLoader.loadTestsFromModule(test).run(unittest.TestResult()).failures) == 0

setup(
  name = 'configr',
  version = configr.__version__,
  install_requires = ["appdirs >= 1.4.0"],
  test_suite = "tests",
  description = configr.__doc__,
  long_description = README,  # + '\n' + CHANGES,
  classifiers = [c.strip() for c in """
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.5
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
  keywords = 'application configuration management settings presets',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/configr',
  license = 'MIT',
  py_modules = ["configr"],
  package_dir = {"": "lib"},
  package_data = {"": ["*.py"]},
  include_package_data = True,
  zip_safe = False
)
