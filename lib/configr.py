''' A practical configuration library for your Python apps. '''

__version_info__ = (1, 0, 2)
__version__ = '.'.join(map(str, __version_info__))

# Standard modules
import json
import os

# Optional external dependencies: appdirs
# Optional standard modules: pwd, win32com


class Configr(dict):
  ''' Main configuration object. Property access directly on attributes or dict-style access. '''

  def __init__(_, name, data = {}, defaults = {}):
    ''' Create config object for interaction with settings.
        name: variable part for file name generation, usually corresponding with main app name.
        data: configuration objects
    '''
    _.name = name
    for k, v in data.items(): _[k] = v
    _.defaults = defaults
    try:
      import appdirs
      home = appdirs.user_data_dir(name, name) # app/author
    except:
      try: # get user home regardless of currently set environment variables
        from win32com.shell import shell, shellcon
        home = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
      except:
        try: # unix-like native solution ignoring envronment variables
          from pwd import getpwuid
          home = getpwuid(os.getuid()).pw_dir
        except: # now try standard approaches
          home = os.getenv("USERPROFILE") # for windows only
          if home is None:
            home = os.expanduser("~") # recommended cross-platform solution, but could refer to a mapped network drive on Windows
    assert home # if assertion fails, we cannot determine user's home directory in this environment
    _.home = home

  def __getattr__(_, key):
    ''' Simplified attribute access to dictionary.
    >>> c = Configr("a", {"b": 3})
    >>> c[1] = 1; print c[1]
    1
    >>> c.a2 = "a2"; print c.a2
    a2
    >>> print c["a2"]
    a2
    >>> print c.b
    3
    '''
    return _[key]

  def __setattr__(_, key, value):
    _[key] = value

  def loadSettings(_, defaults = {}, location = None, ignores = []):
    ''' Load settings from file system and store on self object.
        defaults: settings to use for missing keys
        ignores: map of keys to ignore (because loaded from another location by other load call)
        location: load from a fixed path, e.g. system-wide global settings like app dir
    '''
    for k, v in defaults.items(): _[k] = v
    try:
      config = os.path.join(_.home if location is None else location, _.name + ".cfg")
      with open(config, "r") as fd:
        tmp = json.loads(fd.read())
        for k, v in tmp.items():
          if k not in ignores: _[k] = v
        _.__loadedFrom__ = config
    except:
      _.__loadedFrom__ = None
      return tmp

  def saveSettings(_, keys = None, location = None):
    ''' Save settings stored onself object to file system.
        keys: if set, only write data contained in this list
        location: save to a fixed path, e.g. system-wide global settings like app dir
    '''
    config = os.path.join(_.home if location is None else location, _.name + ".cfg")
    try: os.makedirs(_.home)
    except: pass # already exists
    try:
      with open(config, "w") as fd:
        to_write = [K for K in _.keys() if not K.startswith("_") and K not in ["__savedTo__", "__loadedFrom__"]] if keys is None else keys
        tmp = {k: _[k] for k in to_write}
        fd.write(json.dumps(tmp))
        _.__savedTo__ = config
    except:
      _.__savedTo__ = None

if __name__ == '__main__':
  import doctest
  doctest.testmod()
