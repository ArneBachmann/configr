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
with open(os.path.join("configr", "version.py"), "w") as fd:  # create version string at build time
  fd.write("""\
__version_info__ = (%d, %d, %d)
__version__ = '.'.join(map(str, __version_info__))
""" % (md.tm_year, (10 + md.tm_mon) * 100 + md.tm_mday, (10 + md.tm_hour) * 100 + md.tm_min))

from configr import configr, test  # needed for version strings
README = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')).read()
# CHANGES = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CHANGES.rst')).read()

try:
  testrun = unittest.defaultTestLoader.loadTestsFromModule(configr.test).run(unittest.TestResult())
  assert len(testrun.errors) == 0
  assert len(testrun.failures) == 0
except: print("Warning: test suite failed")

# Clean old binaries
try:
  for file in os.listdir("dist"):
    try:
      if file.endswith(".tar.gz"): os.unlink(os.path.join("dist", file))
    except: print("Cannot remove " + file)
except: pass

print("Building configr version " + configr.__version__)
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
