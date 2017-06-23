import sys
import os
import subprocess
import time
import unittest
from setuptools import setup

# Upload to PyPI by running setup.py clean build_py sdist bdist upload with a correctly set up ~/.pypirc (need HOME variable set correctly on Windows)

if os.path.exists(".git"):
  p = subprocess.Popen("git describe --always", shell = True, bufsize = 1, stdout = subprocess.PIPE)
  so, se = p.communicate()
  micro = so.strip() if sys.version_info.major < 3 else so.strip().decode('ascii')
else:
  micro = "svn"
md = time.localtime()
with open("configr" + os.sep + "version.py", "w") as fd:  # create version string at build time
  fd.write("__version_info__ = (%d, %d, %d)\n__version__ = '.'.join(map(str, __version_info__))\n" % (md.tm_year, (10 + md.tm_mon) * 100 + md.tm_mday, (10 + md.tm_hour) * 100 + md.tm_min))

_top_dir = os.path.dirname(os.path.abspath(__file__))
try: from configr import configr, test  # needed for version strings
except Exception as E: print(E)
finally: del sys.path[:2]  # clean sys.path after import
README = open(os.path.join(_top_dir, 'README.rst')).read()
# CHANGES = open(os.path.join(_top_dir, 'CHANGES.rst')).read()

try:
  testrun = unittest.defaultTestLoader.loadTestsFromModule(configr.test).run(unittest.TestResult())
  assert len(testrun.errors) == 0
  assert len(testrun.failures) == 0
except: pass  # pip install doesn't need it

setup(
  name = 'configr',
  version = configr.__version__,
  install_requires = ["appdirs >= 1.4.0"],
  test_suite = "tests",
  description = configr.__doc__,
  long_description = README,  # + '\n' + CHANGES,
  classifiers = [c.strip() for c in """
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.6
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
  keywords = 'application configuration management settings presets',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/configr',
  license = 'MIT',
  packages = ["configr"],
  package_dir = {"configr": "configr"},
  package_data = {"": ["LICENSE", "README.rst"]},
  include_package_data = True,
  zip_safe = False
)
