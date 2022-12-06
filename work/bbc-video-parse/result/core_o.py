__doc__ = '\ncertifi.py\n~~~~~~~~~~\n\nThis module returns the installation location of cacert.pem or its contents.\n'
import os
try:
    from importlib.resources import path as get_path,read_text
    _CACERT_CTX = None
    _CACERT_PATH = None
    def where():
        global  _CACERT_PATH
        global _CACERT_CTX
        if _CACERT_PATH is None:
            _CACERT_CTX = get_path('certifi', 'cacert.pem')
            _CACERT_PATH = str(_CACERT_CTX.__enter__())
        return _CACERT_PATH
except ImportError:
    def read_text(encoding):
        with open((where()), 'r', encoding=encoding) as (data):
            return data.read()
    def where():
        f = os.path.dirname(__file__)
        return os.path.join(f, 'cacert.pem')
finally:
    def contents():
        return read_text('certifi', 'cacert.pem', encoding='ascii')
