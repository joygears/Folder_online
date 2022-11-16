# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: charset_normalizer\legacy.py
from charset_normalizer.api import from_bytes
from charset_normalizer.constant import CHARDET_CORRESPONDENCE
from typing import Dict, Optional, Union

def detect(byte_str: bytes) -> Dict[(str, Optional[Union[(str, float)]])]:
    """
    chardet legacy method
    Detect the encoding of the given byte string. It should be mostly backward-compatible.
    Encoding name will match Chardet own writing whenever possible. (Not on encoding name unsupported by it)
    This function is deprecated and should be used to migrate your project easily, consult the documentation for
    further information. Not planned for removal.

    :param byte_str:     The byte sequence to examine.
    """
    if not isinstance(byte_str, (bytearray, bytes)):
        raise TypeError('Expected object of type bytes or bytearray, got: {0}'.format(type(byte_str)))
    else:
        if isinstance(byte_str, bytearray):
            byte_str = bytes(byte_str)
        r = from_bytes(byte_str).best()
        encoding = r.encoding if r is not None else None
        language = r.language if (r is not None and r.language != 'Unknown') else ''
        confidence = 1.0 - r.chaos if r is not None else None
        if r is not None:
            if encoding == 'utf_8':
                if r.bom:
                    encoding += '_sig'
    return {'encoding':encoding if encoding not in CHARDET_CORRESPONDENCE else CHARDET_CORRESPONDENCE[encoding], 
     'language':language, 
     'confidence':confidence}