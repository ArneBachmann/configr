import doctest
import unittest

import configr


class Test_AppDir(unittest.TestCase):

  def tests_metadata(self):
    self.assertTrue(hasattr(configr, "__version__"))
    self.assertTrue(hasattr(configr, "__version_info__"))

def load_tests(loader, tests, ignore):
  ''' _tests is conventional way of telling unittest about a test case. '''
  tests.addTests(doctest.DocTestSuite(configr))
  return tests

if __name__ == "__main__":
  unittest.main()
