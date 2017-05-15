import doctest
import json
import os
import unittest
import sys

sys.path.insert(0, "../lib")
import configr
sys.path.pop(0)


class Test_AppDir(unittest.TestCase):

  def tests_metadata(_):
    _.assertTrue(hasattr(configr, "__version__"))
    _.assertTrue(hasattr(configr, "__version_info__"))

  def test_details(_):
    c = configr.Configr("myapp")
    _.assertEqual("myapp", c.__name)
    _.assertEqual("myapp", c["__name"])
    c.a = "a"
    c["b"] = "b"
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    c.saveSettings(location = os.getcwd(), clientCodeLocation = __file__)
    _.assertIsNotNone(c.__savedTo)  # ensure no exception during saving
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    _.assertEqual("myapp", c.__name)
    with open(c.__savedTo[0], "r") as fd: a = contents = json.loads(fd.read())
    _.assertEqual({"a": "a", "b": "b"}, contents)


def load_tests(loader, tests, ignore):
  ''' The function suffix of "_tests" is the conventional way of telling unittest about a test case. '''
  tests.addTests(doctest.DocTestSuite(configr))
  return tests

if __name__ == "__main__":
  unittest.main()
