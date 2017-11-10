'''
Configr
=======

A practical configuration library for your Python apps.

https://pypi.python.org/pypi/configr/
https://github.com/ArneBachmann/configr

Optional external dependencies:  appdirs (automatically installed when using pip)
Optional standard modules:       pwd, win32com (used on Linux or Windows, respectively)
'''


# Standard modules
import collections
import hashlib
import json
import logging
import os
import shutil
import uuid


try: import configr.version as version  # created and used by setup.py
except: import version  # Python 2 logic


_log = logging.getLogger(__name__); debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error

EXTENSION = ".cfg"
BACKUP = ".bak"

ReturnValue = collections.namedtuple("ReturnValue", "path error")  # what load and save returns

home = None  # user's home folder


def bites(s): return s.encode('utf-8')  # name derived from "bytes" which would have been an alternative implementation

def determineHomeFolder(name):
  ''' Determine process's user's home directory.
      No need to run on every Configr object creation, as it is assumed to be static throughout one configuration state lifetime.
      If any of the environment variables have been modified by the same process, call the function again.
      name: application name to use
      returns: None
      Side effect: sets module-global "home" variable
  '''
  global home
  try:
    import appdirs  # optional dependency which already solves some some problems for us
    home = appdirs.user_data_dir(name, "configr")  # app/author
  except:
    try:  # get user home regardless of currently set environment variables
      from win32com.shell import shell, shellcon
      home = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
    except:
      try:  # unix-like native solution ignoring environment variables
        from pwd import getpwuid
        home = getpwuid(os.getuid()).pw_dir
      except:  # now try standard approaches
        home = os.getenv("USERPROFILE")  # for windows only
        if home is None: home = os.expanduser("~")  # recommended cross-platform solution, but could refer to a mapped network drive on Windows
  if home is None: raise Exception("Cannot reliably determine user's home directory, please file a bug report at https://github.com/ArneBachmann/configr")
  return home


class Configr(object):
  ''' Main configuration object. Property access directly on attributes or dict-style access. '''

  exports = {"loadSettings", "saveSettings", "keys", "values", "items", "__repr__", "__str__"}  # set of function names to accept calling
  internals = {"__name", "__map", "__defaults", "__savedTo", "__loadedFrom"}  # app name, dict, fallbacks, hints

  def __init__(_, name = None, data = {}, defaults = {}):
    ''' Create config object for interaction with settings.
        name: file name, usually corresponding with main app name
        data: configuration objects to store initially
        defaults: a fallback map to use when querying undefined values

    >>> c = Configr("a", data = {1:1, 2:2, "c":"c"}, defaults = {"d": "d"})
    >>> print(c.__name) # test meta access
    a
    >>> print(c[1]) # test dictionary access
    1
    >>> print(c["c"])
    c
    >>> print(c.c) # test attribute access
    c
    >>> print(c["d"]) # test default
    d
    >>> print(c.d) # same for attribute access
    d
    '''
    if name is None: name = uuid.uuid4()
    _.__name = name
    _.__defaults = {str(k): v for k, v in defaults.items()}
    _.__map = {str(k): v for k, v in data.items()}  # create shallow copy
    if home is None: determineHomeFolder(name)  # determine only once

  def __getitem__(_, key):
    ''' Query a configuration value via dictionary access, e.g. value = obj[name]. '''
    key = str(key)  # always convert keys to strings
    if key in Configr.internals: return getattr(_, key)  # e.g. __map attribute
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setitem__(_, key, value):
    ''' Define a configuration value via dictionary access, e.g. obj[name] = value. '''
    _.__map[str(key)] = value  # always convert keys to strings

  def __delitem__(_, key):
    ''' Remove a configuration entry via dictionary access, e.g. del obj[name]. '''
    del _.__map[str(key)]

  def __getattribute__(_, key):
    ''' Query a configuration value via attribute access, e.g. value = obj.name. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary to remove object name key prefix
    elif key.startswith("_Test_AppDir"): key = key[len("_Test_AppDir"):]  # for unit testing
    if key in Configr.internals or key in Configr.exports: return object.__getattribute__(_, key)
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setattr__(_, key, value):
    ''' Define a configuration value via attribute access, e.g. obj.name = value. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    elif key.startswith("_Test_AppDir"): key = key[len("_Test_AppDir"):]  # for unit testing
    if key in Configr.internals: object.__setattr__(_, key, value)
    else: _.__map[key] = value

  def __delattr__(_, key):
    ''' Remove an configuration entry via attribute access, e.g. del obj.name. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    elif key.startswith("_Test_AppDir"): key = key[len("_Test_AppDir"):]  # for unit testing
    if key in Configr.internals or key in Configr.exports: return
    del _.__map[key]  # delegate to dictionary style

  def __repr__(_):
    return "Configr(%s)" % ", ".join(["%s: %s" % (k, repr(v)) for k, v in _.__map.items()])

  def __str__(_):
    return "Configr(%s)" % ", ".join(["%s: %s" % (k, str(v)) for k, v in _.__map.items()])

  def loadSettings(_, data = {}, location = None, ignores = [], clientCodeLocation = 'undefined'):
    ''' Load settings from file system and store on self object.
        data: settings to use only for keys missing in the file
        location: load from a fixed path, e.g. system-wide global settings like app dir
        clientCodeLocation: should be a call to os.path.abspath(__file__) from the caller's script to separate configuration for different tool installation locations
        ignores: list of keys to ignore and not load from file
        returns: ReturnValue 2-tuple(config-file or None, None or Exception)
    '''
    config = os.path.join(home if location is None else location, "%s-%s-%s%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation)))).hexdigest()[:4],
        EXTENSION))  # always use current (installed or local) library's location and caller's location to separate configs
    debug("Loading configuration %r" % config)
    try:
      with open(config, "r") as fd:
        loaded = json.loads(fd.read())
        for k, v in data.items(): _[k] = v  # preset data
        for k, v in [(K, V) for K, V in loaded.items() if K not in ignores]: _[k] = v
      _.__loadedFrom = ReturnValue(config, None)  # memorize file location loaded from
    except Exception as E:
      debug(str(E))
      _.__loadedFrom = ReturnValue(None, E)  # callers can detect errors by checking this flag
    return _.__loadedFrom

  def saveSettings(_, keys = None, location = None, clientCodeLocation = 'undefined'):
    ''' Save settings stored onself object to file system.
        keys: if defined, a list of keys to write
        location: save to a fixed path, e.g. system-wide global settings like app dir
        clientCodeLocation: should be a call to os.__file__ from the caller's script to separate configuration for different tools
        returns: ReturnValue 2-tuple(config-file or None, None or Exception)
    '''
    config = os.path.join(home if location is None else location, "%s-%s-%s%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation)))).hexdigest()[:4],
        EXTENSION))  # always use current (installed or local) library's location and caller's location to separate configs
    debug("Storing configuration %r" % config)
    try: os.makedirs(home)
    except: pass  # already exists
    try: shutil.copy2(config, config + BACKUP)
    except: pass
    try:
      with open(config, "w") as fd:
        toWrite = [K for K in _.__map.keys() if K not in internals] if keys is None else keys
        tmp = {k: _[k] for k in toWrite}
        fd.write(json.dumps(tmp))
      _.__savedTo = ReturnValue(config, None)
    except Exception as E:
      debug(str(E))
      _.__savedTo = ReturnValue(None, E)
    return _.__savedTo

  def keys(_):
    ''' Return configuration's keys.
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"})
    >>> print(sorted(c.keys()))
    ['1', '2', 'c']
    '''
    return _.__map.keys()

  def values(_):
    ''' Return configuration's values.
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"})
    >>> print(sorted([str(v) for v in c.values()]))
    ['1', '2', 'c']
    '''
    return _.__map.values()

  def items(_):
    ''' Return (unsorted) list or dict_items object for all configuration's key-value pairs.
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"})
    >>> print(sorted(c.items()))
    [('1', 1), ('2', 2), ('c', 'c')]
    '''
    return _.__map.items()


if __name__ == '__main__':
  ''' Running this library module as a main file will invoke the test suite instead to avoid side-effects. '''
  import doctest
  doctest.testmod()
