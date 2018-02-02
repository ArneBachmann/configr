import os
import sys
import subprocess
import time
import unittest
from setuptools import setup

if os.path.exists(".git"):
  try:
    p = subprocess.Popen("git describe --always", shell = sys.platform != 'win32', bufsize = 1, stdout = subprocess.PIPE)
    so, se = p.communicate()
    extra = (so.strip() if sys.version_info.major < 3 else so.strip().decode(sys.stdout.encoding)).replace("\n", "-")
    if "\x0d" in extra: extra = extra.split("\x0d")[1]
    print("Found Git hash %s" % extra)
  except: extra = "svn"
else:
  extra = "svn"
md = time.localtime()
version = (md.tm_year, (10 + md.tm_mon) * 100 + md.tm_mday, (10 + md.tm_hour) * 100 + md.tm_min)
versionString = '.'.join(map(str, version))
with open(os.path.join("configr", "version.py"), "w") as fd:  # create version string at build time
  fd.write("""\
__version_info__ = ({version[0]}, {version[1]}, {version[2]})
__version__ = r'{fullName}'
""".format(version = version, fullName = versionString + "-" + extra))

import configr
import configr.test
README = "\n".join(["Configr " + versionString] + open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.rst')).read().split("\n")[1:])
with open("README.rst", "w") as fd: fd.write(README)

# Ensure unit tests are fine
testrun = unittest.defaultTestLoader.loadTestsFromModule(configr.test).run(unittest.TestResult())
assert len(testrun.errors) == 0
assert len(testrun.failures) == 0

# Clean old binaries
if os.path.exists("dist"):
  rmFiles = list(sorted(os.listdir("dist")))
  try:
    for file in (f for f in (rmFiles if "build" in sys.argv and "sdist" in sys.argv else rmFiles[:-1]) if any([f.endswith(ext) for ext in (".tar.gz", "zip")])):
      print("Removing old sdist archive %s" % file)
      try: os.unlink(os.path.join("dist", file))
      except: print("Cannot remove old distribution file " + file)
  except: pass

print("Building configr version " + configr.version.__version__)
setup(
  name = 'configr',
  version = versionString,  # without extra
  install_requires = ["appdirs >= 1.4.0"],  # actually a optional dependency
  test_suite = "tests",  # is this executed automatically? Is also called above
  description = "configr: A practical configuration library for your Python apps.",
  long_description = README,  # + '\n' + CHANGES,
  classifiers = [c.strip() for c in """
        Development Status :: 5 - Production/Stable
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: 3
        Programming Language :: Python :: 3.3
        Programming Language :: Python :: 3.4
        Programming Language :: Python :: 3.5
        Programming Language :: Python :: 3.6
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],  # https://pypi.python.org/pypi?:action=list_classifiers
  keywords = 'application configuration management settings presets',
  author = 'Arne Bachmann',
  author_email = 'ArneBachmann@users.noreply.github.com',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'ArneBachmann@users.noreply.github.com',
  url = 'http://github.com/ArneBachmann/configr',
  license = 'MIT',
  packages = ["configr"],
  package_dir = {"configr": "configr"},
  package_data = {"": ["../LICENSE", "../README.rst", "../LICENSE"]},
  include_package_data = False,  # if True, will *NOT* package the data!
  zip_safe = False
)
