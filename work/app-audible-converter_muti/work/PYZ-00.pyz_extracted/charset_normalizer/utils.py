# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: charset_normalizer\utils.py
try:
    import unicodedata2 as unicodedata
except ImportError:
    import unicodedata

from codecs import IncrementalDecoder
from re import findall
from typing import Optional, Tuple, Union, List, Set
import importlib
from _multibytecodec import MultibyteIncrementalDecoder
from encodings.aliases import aliases
from functools import lru_cache
from charset_normalizer.constant import UNICODE_RANGES_COMBINED, UNICODE_SECONDARY_RANGE_KEYWORD, RE_POSSIBLE_ENCODING_INDICATION, ENCODING_MARKS, UTF8_MAXIMAL_ALLOCATION, IANA_SUPPORTED_SIMILAR

@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_accentuated(character: str) -> bool:
    try:
        description = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'WITH GRAVE' in description or 'WITH ACUTE' in description or 'WITH CEDILLA' in description or 'WITH DIAERESIS' in description or 'WITH CIRCUMFLEX' in description


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def remove_accent(character: str) -> str:
    decomposed = unicodedata.decomposition(character)
    if not decomposed:
        return character
    else:
        codes = decomposed.split(' ')
        return chr(int(codes[0], 16))


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def unicode_range(character: str) -> Optional[str]:
    """
    Retrieve the Unicode range official name from a single character.
    """
    character_ord = ord(character)
    for range_name, ord_range in UNICODE_RANGES_COMBINED.items():
        if character_ord in ord_range:
            return range_name


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_latin(character: str) -> bool:
    try:
        description = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'LATIN' in description


def is_ascii(character: str) -> bool:
    try:
        character.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_punctuation(character: str) -> bool:
    character_category = unicodedata.category(character)
    if 'P' in character_category:
        return True
    else:
        character_range = unicode_range(character)
        if character_range is None:
            return False
        return 'Punctuation' in character_range


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_symbol(character: str) -> bool:
    character_category = unicodedata.category(character)
    if 'S' in character_category or 'N' in character_category:
        return True
    else:
        character_range = unicode_range(character)
        if character_range is None:
            return False
        return 'Forms' in character_range


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_separator(character: str) -> bool:
    if character.isspace() or character in ('｜', '+', ',', ';', '<', '>'):
        return True
    else:
        character_category = unicodedata.category(character)
        return 'Z' in character_category


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_case_variable(character: str) -> bool:
    return character.islower() != character.isupper()


def is_private_use_only(character: str) -> bool:
    character_category = unicodedata.category(character)
    return 'Co' == character_category


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_cjk(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'CJK' in character_name


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_hiragana(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'HIRAGANA' in character_name


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_katakana(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'KATAKANA' in character_name


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_hangul(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'HANGUL' in character_name


@lru_cache(maxsize=UTF8_MAXIMAL_ALLOCATION)
def is_thai(character: str) -> bool:
    try:
        character_name = unicodedata.name(character)
    except ValueError:
        return False
    else:
        return 'THAI' in character_name


@lru_cache(maxsize=(len(UNICODE_RANGES_COMBINED)))
def is_unicode_range_secondary(range_name: str) -> bool:
    for keyword in UNICODE_SECONDARY_RANGE_KEYWORD:
        if keyword in range_name:
            return True

    return False


def any_specified_encoding(sequence: bytes, search_zone: int=4096) -> Optional[str]:
    """
    Extract using ASCII-only decoder any specified encoding in the first n-bytes.
    """
    if not isinstance(sequence, bytes):
        raise TypeError
    seq_len = len(sequence)
    results = findall(RE_POSSIBLE_ENCODING_INDICATION, sequence[:seq_len if seq_len <= search_zone else search_zone].decode('ascii', errors='ignore'))
    if len(results) == 0:
        return
    for specified_encoding in results:
        specified_encoding = specified_encoding.lower().replace('-', '_')
        for encoding_alias, encoding_iana in aliases.items():
            if encoding_alias == specified_encoding:
                return encoding_iana
            if encoding_iana == specified_encoding:
                return encoding_iana


@lru_cache(maxsize=128)
def is_multi_byte_encoding(name: str) -> bool:
    """
    Verify is a specific encoding is a multi byte one based on it IANA name
    """
    return name in frozenset({'utf_16', 'utf_16_le', 'utf_32', 'utf_8', 'utf_32_be', 'utf_7', 'utf_8_sig', 'utf_32_le', 'utf_16_be'}) or issubclass(importlib.import_module('encodings.{}'.format(name)).IncrementalDecoder, MultibyteIncrementalDecoder)


def identify_sig_or_bom(sequence: bytes) -> Tuple[(Optional[str], bytes)]:
    """
    Identify and extract SIG/BOM in given sequence.
    """
    for iana_encoding in ENCODING_MARKS:
        marks = ENCODING_MARKS[iana_encoding]
        if isinstance(marks, bytes):
            marks = [
             marks]
        for mark in marks:
            if sequence.startswith(mark):
                return (
                 iana_encoding, mark)

    return (None, b'')


def should_strip_sig_or_bom(iana_encoding: str) -> bool:
    return iana_encoding not in frozenset({'utf_16', 'utf_32'})


def iana_name(cp_name: str, strict: bool=True) -> str:
    cp_name = cp_name.lower().replace('-', '_')
    for encoding_alias, encoding_iana in aliases.items():
        if cp_name == encoding_alias or cp_name == encoding_iana:
            return encoding_iana

    if strict:
        raise ValueError("Unable to retrieve IANA for '{}'".format(cp_name))
    return cp_name


def range_scan(decoded_sequence: str) -> List[str]:
    ranges = set()
    for character in decoded_sequence:
        character_range = unicode_range(character)
        if character_range is None:
            pass
        else:
            ranges.add(character_range)

    return list(ranges)


def cp_similarity(iana_name_a: str, iana_name_b: str) -> float:
    if is_multi_byte_encoding(iana_name_a) or is_multi_byte_encoding(iana_name_b):
        return 0.0
    else:
        decoder_a = importlib.import_module('encodings.{}'.format(iana_name_a)).IncrementalDecoder
        decoder_b = importlib.import_module('encodings.{}'.format(iana_name_b)).IncrementalDecoder
        id_a = decoder_a(errors='ignore')
        id_b = decoder_b(errors='ignore')
        character_match_count = 0
        for i in range(0, 255):
            to_be_decoded = bytes([i])
            if id_a.decode(to_be_decoded) == id_b.decode(to_be_decoded):
                character_match_count += 1

        return character_match_count / 254


def is_cp_similar(iana_name_a: str, iana_name_b: str) -> bool:
    """
    Determine if two code page are at least 80% similar. IANA_SUPPORTED_SIMILAR dict was generated using
    the function cp_similarity.
    """
    return iana_name_a in IANA_SUPPORTED_SIMILAR and iana_name_b in IANA_SUPPORTED_SIMILAR[iana_name_a]