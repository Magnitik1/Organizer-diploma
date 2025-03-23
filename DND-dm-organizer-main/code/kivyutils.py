from kivy.lang.builder import Builder as _Builder
from pathlib import Path as _Path

def load_kv_for(pyfileSTR:str):
  """Given `pyfileSTR`, load a kv file with same filename but all lowercase.
  (This follows kivy convention for App kv autoloading, but maybe it shouldn't)

  :usage:
    `load_kv_for(__file__)`"""
  pyfile = _Path(pyfileSTR).resolve()
  directory = pyfile.parent
  kvfile=str(directory.joinpath(pyfile.stem.lower()+".kv"))
  _Builder.load_file(kvfile,rulesonly=True)

