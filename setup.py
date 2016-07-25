import sys
import os
from setuptools import setup


_top_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_top_dir, "lib"))
try:
  import configr
finally:
  del sys.path[0]
README = open(os.path.join(_top_dir, 'README.rst')).read()
#CHANGES = open(os.path.join(_top_dir, 'CHANGES.rst')).read()

setup(
  name='configr',
  version = configr.__version__,
  install_requires = ["appdirs >= 1.4.0"],
  test_suite = "tests",
  description = configr.__doc__,
  long_description = README,# + '\n' + CHANGES,
  classifiers = [c.strip() for c in """
        Development Status :: 4 - Beta
        Intended Audience :: Developers
        License :: OSI Approved :: MIT License
        Operating System :: OS Independent
        Programming Language :: Python :: 2
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Topic :: Software Development :: Libraries :: Python Modules
        """.split('\n') if c.strip()],
  keywords = 'application configuration settings presets',
  author = 'Arne Bachmann',
  author_email = 'arne.bachmann@web.de',
  maintainer = 'Arne Bachmann',
  maintainer_email = 'arne.bachmann@web.de',
  url = 'http://github.com/ArneBachmann/configr',
  license = 'MIT',
  py_modules = ["configr"],
  package_dir = {"": "lib"},
  include_package_data = True,
  zip_safe = False
)
