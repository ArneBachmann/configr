''' Package definition. '''
import sys
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
if sys.version_info.major >= 3:
  from configr.configr import *
  import configr.version
else:  # Python 2
  from configr import *
  import version
