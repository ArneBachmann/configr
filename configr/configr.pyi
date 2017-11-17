from typing import *

EXTENSION:str
BACKUP:str

home:Optional[str]


def bites(s:str) -> str: ...

def determineHomeFolder(name:str) -> str: ...

class Configr(object):
  exports:Set[str]
  internals:Set[str]

  def __init__(_, name:Optional[str] = None, data:Dict[str,Any] = {}, defaults:Dict[str,Any] = {}) -> None: ...
  def __getitem__(_, key:Any) -> Any: ...
  def __setitem__(_, key:Any, value:Any) -> None: ...
  def __delitem__(_, key:Any) -> None: ...
  def __getattribute__(_, key:Any) -> Any: ...
  def __setattr__(_, key:Any, value:Any) -> None: ...
  def __delattr__(_, key:Any) -> None: ...
  def __repr__(_) -> str: ...
  def __str__(_) -> str: ...
  def loadSettings(_, data:Dict[str,Any] = {}, location:Optional[str] = None, ignores:List[str] = [], clientCodeLocation:str = 'undefined') -> Tuple[Optional[str],Optional[Exception]]: ...
  def saveSettings(_, keys:Optional[List[str]] = None, location:Optional[str] = None, ignores:List[str] = [], clientCodeLocation:str = 'undefined') -> Tuple[Optional[str],Optional[Exception]]: ...
  def keys(_) -> List[str]: ...
  def values(_) -> List[Any]: ...
  def items(_) -> List[Tuple[str,Any]]: ...
