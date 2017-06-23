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
    c = configr.Configr("myapp", data = {"d": 2}, defaults = {"e": 1})
    _.assertEqual("myapp", c.__name)
    _.assertEqual("myapp", c["__name"])
    try: c["c"]; raise Exception("Should have crashed")  # not existing data via dictionary access case
    except: pass
    try: c.c; raise Exception("Should have crashed")  # not existing data via attribute access case
    except: pass
    _.assertEqual(2, c.d)  # pre-defined data case
    _.assertEqual(1, c["e"])  # default case
    c.a = "a"
    c["b"] = "b"
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    (path, excp) = c.saveSettings(location = os.getcwd(), keys = ["a", "b"], clientCodeLocation = __file__)  # CWD should be "tests" folder
    _.assertIsNotNone(path)
    _.assertIsNone(excp)
    _.assertEqual((path, excp), c.__savedTo)
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    with open(c.__savedTo[0], "r") as fd: contents = json.loads(fd.read())
    _.assertEqual({"a": "a", "b": "b"}, contents)
    c = configr.Configr("myapp")
    (path, excp) = c.loadSettings(location = os.getcwd(), data = {"c": 33})
    _.assertIsNotNone(path)
    _.assertIsNone(excp)
    _.assertEqual((path, excp), c.__loadedFrom)
    _.assertEqual(c.a, "a")
    _.assertEqual(c["b"], "b")
    _.assertEqual(c.c, 33)



def load_tests(loader, tests, ignore):
  ''' The function name suffix "_tests" tells the unittest module about a test case. '''
  tests.addTests(doctest.DocTestSuite(configr))
  return tests


if __name__ == "__main__":
  print(unittest.main())
