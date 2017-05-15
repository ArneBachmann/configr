'''
A practical configuration library for your Python apps.
- https://pypi.python.org/pypi/configr/
- https://github.com/ArneBachmann/configr

Optional external dependencies:  appdirs
Optional standard modules:       pwd, win32com
'''

from version import __version_info__, __version__  # used by setup.py

# Standard modules
import hashlib
import json
import os


bites = lambda s: s.encode('utf-8')  # name derived from "bytes" which would have been an alternative implementation

class Configr(object):
  ''' Main configuration object. Property access directly on attributes or dict-style access. '''

  exports = ["loadSettings", "saveSettings"]  # list of functions to accept calling

  def __init__(_, name, data = {}, defaults = {}):
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
    _.__name = name
    _.__defaults = {str(k): v for k, v in defaults.items()}
    _.__map = {str(k): v for k, v in data.items()}  # create shallow copy
    try:
      import appdirs  # optional dependency which already solves some some problems for us
      home = appdirs.user_data_dir(name, name)  # app/author
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
          if home is None:
            home = os.expanduser("~")  # recommended cross-platform solution, but could refer to a mapped network drive on Windows
    if home is None: raise Exception("Cannot reliably determine user's home directory, please file a bug report at https://github.com/ArneBachmann/configr")
    _.__home = home  # keep reference on object

  def __getitem__(_, key):
    ''' Query a configuration value via dictionary access. '''
    key = str(key)
    if key.startswith('__'): return _.__getattribute__(key)
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setitem__(_, key, value):
    ''' Define a configuration value via dictionary access. '''
    _.__map[str(key)] = value

  def __getattribute__(_, key):
    ''' Query a configuration value via attribute access. '''
    key = str(key)
    if key == '__name': return object.__getattribute__(_, "__name")
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    if key.startswith("_Test_AppDir"): key = key[len("_Test_AppDir"):]  # for unit testing
    if key.startswith('__') or key in Configr.exports: return object.__getattribute__(_, key)
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setattr__(_, key, value):
    ''' Define a configuration value via attribute access. '''
    key = str(key)
    if key.startswith("_Configr"): key = key[len("_Configr"):]  # strange hack necessary
    if key.startswith("_Test_AppDir"): key = key[len("_Test_AppDir"):]  # for unit testing
    if key.startswith('__'): object.__setattr__(_, key, value)
    else: _.__map[key] = value

  def loadSettings(_, data = {}, location = None, ignores = [], clientCodeLocation = 'undefined'):
    ''' Load settings from file system and store on self object.
        data: settings to use only for keys missing in the file
        location: load from a fixed path, e.g. system-wide global settings like app dir
        clientCodeLocation: should be a call to os.__file__ from the caller's script to separate configuration for different tools
        ignores: list of keys to ignore and not load from file
        returns: None
    '''
    config = os.path.join(_.__home if location is None else location, "%s-%s-%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation)))).hexdigest()[:4]))  # always use current (installed or local) library's location and caller's location to separate configs
    try:
      with open(config, "r") as fd:
        tmp = json.loads(fd.read())
        for k, v in data.items(): _[k] = v  # preset data
        for k, v in [(K, V) for K, V in tmp.items() if K not in ignores]: _[k] = v
      _.__loadedFrom = (config, None)  # memorize file location loaded from
    except Exception as E:
      _.__loadedFrom = (None, E)  # callers can detect errors by checking this flag

  def saveSettings(_, keys = None, location = None, clientCodeLocation = 'undefined'):
    ''' Save settings stored onself object to file system.
        keys: if defined, a list of keys to write
        location: save to a fixed path, e.g. system-wide global settings like app dir
        clientCodeLocation: should be a call to os.__file__ from the caller's script to separate configuration for different tools
        returns: None
    '''
    config = os.path.join(_.__home if location is None else location, "%s-%s-%s" % (
        _.__name,
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(os.__file__)))).hexdigest()[:4],
        hashlib.sha1(bites(os.path.dirname(os.path.abspath(clientCodeLocation)))).hexdigest()[:4]))  # always use current (installed or local) library's location and caller's location to separate configs
    try: os.makedirs(_.__home)
    except: pass  # already exists
    try:
      with open(config, "w") as fd:
        to_write = [K for K in _.__map.keys() if not K.startswith("_") and K not in ["__savedTo", "__loadedFrom"]] if keys is None else keys
        tmp = {k: _[k] for k in to_write}
        fd.write(json.dumps(tmp))
      _.__savedTo = (config, None)
    except Exception as E:
      _.__savedTo = (None, E)


if __name__ == '__main__':
  import doctest
  doctest.testmod()
