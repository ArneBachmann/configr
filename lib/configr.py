'''
A practical configuration library for your Python apps.
https://pypi.python.org/pypi/configr/
'''

from version import __version_info__, __version__

# Standard modules
import json
import os

# Optional external dependencies:  appdirs
# Optional standard modules:       pwd, win32com


class Configr(object):
  ''' Main configuration object. Property access directly on attributes or dict-style access. '''

  exports = ["loadSettings", "saveSettings"]

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
    _.__defaults = defaults
    _.__map = { k: v for k, v in data.items()} # copy
    try:
      import appdirs # optional dependency
      home = appdirs.user_data_dir(name, name) # app/author
    except:
      try: # get user home regardless of currently set environment variables
        from win32com.shell import shell, shellcon
        home = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
      except:
        try: # unix-like native solution ignoring environment variables
          from pwd import getpwuid
          home = getpwuid(os.getuid()).pw_dir
        except: # now try standard approaches
          home = os.getenv("USERPROFILE") # for windows only
          if home is None:
            home = os.expanduser("~") # recommended cross-platform solution, but could refer to a mapped network drive on Windows
    assert home # if assertion fails, we cannot determine user's home directory in this environment
    _.__home = home

  def __getitem__(_, key):
    ''' Query a configuration value via dictionary access. '''
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setitem__(_, key, value):
    ''' Define a configuration value via dictionary access. '''
    _.__map[key] = value

  def __getattribute__(_, key):
    ''' Query a configuration value via attribute access. '''
    if key.startswith("_Configr"): key = key[len("_Configr"):] # strange hack necessary
    if key.startswith('__') or key in Configr.exports: return object.__getattribute__(_, key)
    try: return _.__map[key]
    except: return _.__defaults[key]

  def __setattr__(_, key, value):
    ''' Define a configuration value via attribute access. '''
    if key.startswith("_Configr"): key = key[len("_Configr"):] # strange hack necessary
    if key.startswith('__'): object.__setattr__(_, key, value)
    else: _.__map[key] = value

  def loadSettings(_, data = {}, location = None, ignores = []):
    ''' Load settings from file system and store on self object.
        data: settings to use only for keys missing in the file
        ignores: list of keys to ignore and not load from file
        location: load from a fixed path, e.g. system-wide global settings like app dir
    '''
    for k, v in data.items(): _[k] = v
    try:
      config = os.path.join(_.__home if location is None else location, _.__name)
      with open(config, "r") as fd:
        tmp = json.loads(fd.read())
        for k, v in [(K, V) for K, V in tmp.items() if K not in ignores]: _[k] = v
      _.__loadedFrom = config
    except:
      _.__loadedFrom = None

  def saveSettings(_, keys = None, location = None):
    ''' Save settings stored onself object to file system.
        keys: if set, only write data contained in this list
        location: save to a fixed path, e.g. system-wide global settings like app dir
    '''
    config = os.path.join(_.__home if location is None else location, _.__name)
    try: os.makedirs(_.__home)
    except: pass # already exists
    try:
      with open(config, "w") as fd:
        to_write = [K for K in _.keys() if not K.startswith("_") and K not in ["__savedTo", "__loadedFrom"]] if keys is None else keys
        tmp = {k: _[k] for k in to_write}
        fd.write(json.dumps(tmp))
      _.__savedTo = config
    except:
      _.__savedTo = None


if __name__ == '__main__':
  import doctest
  doctest.testmod()
