
# <module> ____________________________________________
# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py

# <module>.where ____________________________________________
# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py
if _CACERT_PATH is None:
    _CACERT_CTX = get_path('certifi', 'cacert.pem')
    _CACERT_PATH = str(_CACERT_CTX.__enter__())
return _CACERT_PATH
# global _CACERT_CTX ## Warning: Unused global
# global _CACERT_PATH ## Warning: Unused global
# <module>.read_text ____________________________________________
# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py
with open((where()), 'r', encoding=encoding) as (data):
    return data.read()
# <module>.where ____________________________________________
# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py
f = os.path.dirname(__file__)
return os.path.join(f, 'cacert.pem')
# <module>.contents ____________________________________________
# uncompyle6 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: certifi\core.py
return read_text('certifi', 'cacert.pem', encoding='ascii')