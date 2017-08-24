import doctest
import json
import logging
import os
import unittest
import sys

sys.path.insert(0, "../configr")
import configr
sys.path.pop(0)



class Test_AppDir(unittest.TestCase):
  ''' Test suite. '''

  def tests_metadata(_):
    _.assertTrue(hasattr(configr, "version"))
    _.assertTrue(hasattr(configr.version, "__version__"))
    _.assertTrue(hasattr(configr.version, "__version_info__"))

  def test_details(_):
    try:
      for file in (f for f in os.listdir() if f.endswith(configr.EXTENSION + ".bak")):
        try: os.unlink(file)
        except: pass
    except: pass
    c = configr.Configr("myapp", data = {"d": 2}, defaults = {"e": 1})
    _.assertEqual("myapp", c.__name)
    _.assertEqual("myapp", c["__name"])
    try: c["c"]; raise Exception("Should have crashed")  # not existing data via dictionary access case
    except: pass
    try: c.c; raise Exception("Should have crashed")  # not existing data via attribute access case
    except: pass
    _.assertEqual(2, c.d)  # pre-defined data case
    _.assertEqual(1, c["e"])  # default case
    # Create some contents
    c.a = "a"
    c["b"] = "b"
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    # Save to file
    value = c.saveSettings(location = os.getcwd(), keys = ["a", "b"], clientCodeLocation = __file__)  # CWD should be "tests" folder
    _.assertIsNotNone(value.path)
    _.assertIsNone(value.error)
    _.assertEqual(value, c.__savedTo)
    _.assertEqual(os.getcwd(), os.path.dirname(c.__savedTo.path))
    _.assertEqual("a", c["a"])
    _.assertEqual("b", c.b)
    name = c.__savedTo.path
    with open(name, "r") as fd: contents = json.loads(fd.read())
    _.assertEqual({"a": "a", "b": "b"}, contents)
    # Now load and see if all is correct
    c = configr.Configr("myapp")
    value = c.loadSettings(location = os.getcwd(), data = {"c": 33}, clientCodeLocation = __file__)
    _.assertEqual(name, c.__loadedFrom.path)
    _.assertIsNotNone(value.path)
    _.assertIsNone(value.error)
    _.assertEqual(value, c.__loadedFrom)
    _.assertEqual(c.a, "a")
    _.assertEqual(c["b"], "b")
    _.assertEqual(c.c, 33)
    os.unlink(value.path)
    value = c.loadSettings(location = "bla", clientCodeLocation = __file__)  # provoke error
    _.assertIsNone(value.path)
    _.assertIsNotNone(value.error)
    # Now test removal
    del c["b"]
    del c.a
    _.assertEqual(1, len(c.keys()))
    _.assertIn("c", c.keys())
    # Now stringify
    _.assertEqual("Configr(c: 33)", str(c))
    _.assertEqual("Configr(c: 33)", repr(c))
    # Testing map functions: already done in doctest


def load_tests(loader, tests, ignore):
  ''' The function name suffix "_tests" tells the unittest module about a test case. '''
  tests.addTests(doctest.DocTestSuite(configr))
  return tests


if __name__ == "__main__":
  logging.basicConfig(level = logging.DEBUG, stream = sys.stderr, format = "%(asctime)-25s %(levelname)-8s %(name)-12s | %(message)s")
  print(unittest.main())
