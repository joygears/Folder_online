# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: requests\packages.py
import sys
try:
    import chardet
except ImportError:
    import charset_normalizer as chardet, warnings
    warnings.filterwarnings('ignore', 'Trying to detect', module='charset_normalizer')

for package in ('urllib3', 'idna'):
    locals()[package] = __import__(package)
    for mod in list(sys.modules):
        if mod == package or mod.startswith(package + '.'):
            sys.modules['requests.packages.' + mod] = sys.modules[mod]

target = chardet.__name__
for mod in list(sys.modules):
    if mod == target or mod.startswith(target + '.'):
        sys.modules['requests.packages.' + target.replace(target, 'chardet')] = sys.modules[mod]