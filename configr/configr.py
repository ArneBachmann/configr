'''
Configr
=======

A practical configuration library for your Python apps.

https://pypi.python.org/pypi/configr/
https://github.com/ArneBachmann/configr

Optional external dependencies:  appdirs (automatically installed when using pip)
Optional standard modules:       pwd, win32com (used on Linux or Windows, respectively)
'''

import os, sys
__sut__ = __name__ == '__main__'
if __sut__: globals()['__name__'] = 'configr.' + os.path.basename(__file__); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import collections, hashlib, json, logging, shutil, uuid


from . import version


_log = logging.getLogger(__name__); debug, info, warn, error = _log.debug, _log.info, _log.warn, _log.error  # logging must be configured in caller app


# Constants
EXTENSION = ".cfg"
BACKUP = ".bak"


# Value type
ReturnValue = collections.namedtuple("ReturnValue", "path error")  # what load and save returns


# Global reference
home = {"value": None}  # user's home folder


def bites(s): return s.encode('utf-8')  # name derived from "bytes" which would have been an alternative implementation


def determineHomeFolder(name):
  ''' Determine process's user's home directory.
      No need to run on every Configr object creation, as it is assumed to be static throughout one configuration state lifetime.
      If any of the environment variables have been modified by the same process, call the function again.
      name: application name to use
      returns: None
      Side effect: sets module-global "home" variable
  '''
  try:
    import appdirs  # optional dependency which already solves some some problems for us
    home["value"] = appdirs.user_data_dir(name, "configr")  # app/author
  except ImportError:
    try:  # get user home regardless of currently set environment variables
      from win32com.shell import shell, shellcon
      home["value"] = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
    except ImportError:
      try:  # unix-like native solution ignoring environment variables
        from pwd import getpwuid
        home["value"] = getpwuid(os.getuid()).pw_dir
      except ImportError:  # now try standard approaches
        home["value"] = os.getenv("USERPROFILE")  # for windows only
        if home["value"] is None: home["value"] = os.expanduser("~")  # recommended cross-platform solution, but could refer to a mapped network drive on Windows
  if home["value"] is None: raise Exception("Cannot reliably determine user's home directory, please file a bug report at https://github.com/ArneBachmann/configr")
  debug("Determined home folder: %s" % home["value"])
  return home["value"]  # HINT this return is only for convenience and shouldn't be used by user code


class Configr(object):
  ''' Main configuration object. Property access directly on attributes or dict-style access. '''

  exports = {"loadSettings", "saveSettings", "keys", "values", "items", "__repr__", "__str__", "__contains__"}  # set of function names to accept calling
  internals = {"__class__", "__name", "__map", "__defaults", "__savedTo", "__loadedFrom"}  # app name, dict, fallbacks, hints

  def __init__(_, name = None, data = {}, defaults = {}):
    ''' Create config object for interaction with settings.
        name: file name, usually corresponding with main app name
        data: configuration objects to store initially
        defaults: a fallback map to use when querying undefined values, but won't be persisted on save

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
    if name is None: name = str(uuid.uuid4())
    _.__name = name
    _.__map = collections.ChainMap({str(k): v for k, v in data.items()}, *(defaults.__map.maps if defaults and isinstance(defaults, Configr) else [{str(k): v for k, v in (defaults.items() if defaults else {})}]))
    if home["value"] is None: determineHomeFolder(name)  # determine only once

  def __contains__(_, key): return key in _.__map

  def __getitem__(_, key):
    ''' Query a configuration value via dictionary access, e.g. value = obj[name]. '''
    key = str(key)  # always convert keys to strings
    if key in Configr.internals: return getattr(_, key)  # e.g. __map attribute
    return _.__map[key]

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
    elif key.startswith("_Tests"): key = key[len("_Tests"):]  # for unit testing
    if key in Configr.internals or key in Configr.exports: return object.__getattribute__(_, key)
    return _.__map[key]  # item access

  def __setattr__(_, key, value):
    ''' Define a configuration value via attribute access, e.g. obj.name = value. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    elif key.startswith("_Tests"): key = key[len("_Tests"):]  # for unit testing
    if key in Configr.internals: object.__setattr__(_, key, value)
    else: _.__map[key] = value

  def __delattr__(_, key):
    ''' Remove an configuration entry via attribute access, e.g. del obj.name. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    elif key.startswith("_Tests"): key = key[len("_Tests"):]  # for unit testing
    if key in Configr.internals or key in Configr.exports: return
    del _.__map[key]  # delegate to dictionary style

  def __repr__(_): return "<Configr %s>" % ", ".join(["%s: %s" % (k, repr(v)) for k, v in _.__map.items()])

  def __str__(_):  return "<Configr %s>" % ", ".join(["%s: %s" % (k, str(v))  for k, v in _.__map.items()])

  def loadSettings(_, data = {}, location = None, ignores = [], clientCodeLocation = None):
    ''' Load settings from file system and store on self object.
        data: settings to use only for keys missing in the file
        location: load from a fixed path, e.g. system-wide global settings like app dir
        ignores: a list of keys to exempt from reading (but not from the fallback values in data)
        clientCodeLocation: should be a call to os.path.abspath(__file__) from the caller's script to distinguish configuration of different tool installation locations
        ignores: list of keys to ignore and not load from file
        returns: ReturnValue 2-tuple(config-file-path or None, None or Exception)
    '''
    config = os.path.join(home["value"] if location is None else location, "%s-%s-%s%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation if clientCodeLocation is not None else 'undefined')))).hexdigest()[:4],
        EXTENSION))  # always use current (installed or local) library's location and caller's location to separate configs
    debug("Loading configuration %r" % config)
    for k, v in data.items(): _[k] = v  # preset data
    try:
      with open(config, "r") as fd:
        loaded = json.loads(fd.read())
        for k, v in loaded.items():
          if k not in ignores: _[k] = v
      _.__loadedFrom = ReturnValue(config, None)  # memorize file location loaded from
    except Exception as E: debug(str(E)); _.__loadedFrom = ReturnValue(None, E)  # callers can detect errors by checking this flag
    return _.__loadedFrom

  def saveSettings(_, keys = None, location = None, ignores = [], clientCodeLocation = None):
    ''' Save settings stored onself object to file system.
        keys: if defined, a list of keys to write, ignoring all others
        location: save to a fixed path instead of default user configuration folder, e.g. system-wide global settings like app dir
        ignores: a list of keys to exempt from writing
        clientCodeLocation: should be a call to os.path.abspath(__file__) from the caller's script to separate configuration for different tools
        returns: ReturnValue 2-tuple(config-file-path or None, None or Exception)
    '''
    path = home["value"] if location is None else location
    config = os.path.join(path, "%s-%s-%s%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],  # python library path
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation if clientCodeLocation is not None else 'undefined')))).hexdigest()[:4],  # caller location
        EXTENSION))  # always use current (installed or local) library's location and caller's location to separate configs
    debug("Storing configuration %r" % config)
    try: os.makedirs(path, exist_ok=True)
    except Exception: pass  # already exists
    try: shutil.copy2(config, config + BACKUP)
    except Exception: pass
    try:
      with open(config, "w") as fd:
        toWrite = [K for K in _.__map.keys() if K not in Configr.internals and K not in ignores] if keys is None else keys
        tmp = {k: _[k] for k in toWrite}
        fd.write(json.dumps(tmp))
      _.__savedTo = ReturnValue(config, None)
    except Exception as E: debug(str(E)); _.__savedTo = ReturnValue(None, E)
    return _.__savedTo

  def keys(_, with_nested = True, with_defaults = False):
    ''' Return configuration's keys.

    >>> from configr import Configr
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"}, defaults = Configr("Y", data = {3: 3}, defaults = {4: 4}))
    >>> print(sorted(c.keys(with_nested = False)))
    ['1', '2', 'c']
    >>> print(sorted(c.keys()))  # with nested keys except last default
    ['1', '2', '3', 'c']
    >>> print(sorted(c.keys(with_defaults = True)))
    ['1', '2', '3', '4', 'c']
    '''
    return _.__map.keys() if with_nested and with_defaults else (_.__map.maps[0].keys() if not with_defaults and not with_nested else (_.__map.parent.keys() if with_defaults else collections.ChainMap(*_.__map.maps[:-1]).keys()))

  def values(_, with_nested = True, with_defaults = False):
    ''' Return configuration's values.
    >>> from configr import Configr
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"}, defaults = Configr("Y", data = {3: 3}, defaults = {4: 4}))
    >>> print(sorted([str(v) for v in c.values(with_nested = False)]))
    ['1', '2', 'c']
    >>> print(sorted([str(v) for v in c.values(with_defaults = True)]))
    ['1', '2', '3', '4', 'c']
    '''
    return _.__map.values() if with_nested and with_defaults else (_.__map.maps[0].values() if not with_defaults and not with_nested else (_.__map.parent.values() if with_defaults else collections.ChainMap(*_.__map.maps[:-1]).values()))

  def items(_):
    ''' Return (unsorted) list or dict_items object for all configuration's key-value pairs.
    >>> from configr import Configr
    >>> c = Configr("X", data = {1: 1, 2: 2, "c": "c"})
    >>> print(sorted(c.items()))
    [('1', 1), ('2', 2), ('c', 'c')]
    '''
    return _.__map.items()


if __sut__: import doctest; doctest.testmod()
