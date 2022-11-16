# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: charset_normalizer\md.py
from functools import lru_cache
from typing import Optional, List
from charset_normalizer.constant import UNICODE_SECONDARY_RANGE_KEYWORD
from charset_normalizer.utils import is_punctuation, is_symbol, unicode_range, is_accentuated, is_latin, remove_accent, is_separator, is_cjk, is_case_variable, is_hangul, is_katakana, is_hiragana, is_ascii, is_thai

class MessDetectorPlugin:
    __doc__ = '\n    Base abstract class used for mess detection plugins.\n    All detectors MUST extend and implement given methods.\n    '

    def eligible(self, character: str) -> bool:
        """
        Determine if given character should be fed in.
        """
        raise NotImplementedError

    def feed(self, character: str) -> None:
        """
        The main routine to be executed upon character.
        Insert the logic in witch the text would be considered chaotic.
        """
        raise NotImplementedError

    def reset(self) -> None:
        """
        Permit to reset the plugin to the initial state.
        """
        raise NotImplementedError

    @property
    def ratio(self) -> float:
        """
        Compute the chaos ratio based on what your feed() has seen.
        Must NOT be lower than 0.; No restriction gt 0.
        """
        raise NotImplementedError


class TooManySymbolOrPunctuationPlugin(MessDetectorPlugin):

    def __init__(self):
        self._punctuation_count = 0
        self._symbol_count = 0
        self._character_count = 0
        self._last_printable_char = None
        self._frenzy_symbol_in_word = False

    def eligible(self, character: str) -> bool:
        return character.isprintable()

    def feed(self, character: str) -> None:
        self._character_count += 1
        if character != self._last_printable_char:
            if character not in ('<', '>', '=', ':', '/', '&', ';', '{', '}', '[',
                                 ']', ',', '|', '"'):
                if is_punctuation(character):
                    self._punctuation_count += 1
                elif character.isdigit() is False:
                    if is_symbol(character):
                        self._symbol_count += 2
        self._last_printable_char = character

    def reset(self) -> None:
        self._punctuation_count = 0
        self._character_count = 0
        self._symbol_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            ratio_of_punctuation = (self._punctuation_count + self._symbol_count) / self._character_count
            if ratio_of_punctuation >= 0.3:
                return ratio_of_punctuation
            return 0.0


class TooManyAccentuatedPlugin(MessDetectorPlugin):

    def __init__(self):
        self._character_count = 0
        self._accentuated_count = 0

    def eligible(self, character: str) -> bool:
        return character.isalpha()

    def feed(self, character: str) -> None:
        self._character_count += 1
        if is_accentuated(character):
            self._accentuated_count += 1

    def reset(self) -> None:
        self._character_count = 0
        self._accentuated_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            ratio_of_accentuation = self._accentuated_count / self._character_count
            if ratio_of_accentuation >= 0.35:
                return ratio_of_accentuation
            return 0.0


class UnprintablePlugin(MessDetectorPlugin):

    def __init__(self):
        self._unprintable_count = 0
        self._character_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed(self, character: str) -> None:
        if character not in frozenset({'\x0b', '\n', '\t', '\r'}):
            if character.isprintable() is False:
                self._unprintable_count += 1
        self._character_count += 1

    def reset(self) -> None:
        self._unprintable_count = 0

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            return self._unprintable_count * 8 / self._character_count


class SuspiciousDuplicateAccentPlugin(MessDetectorPlugin):

    def __init__(self):
        self._successive_count = 0
        self._character_count = 0
        self._last_latin_character = None

    def eligible(self, character: str) -> bool:
        return character.isalpha() and is_latin(character)

    def feed(self, character: str) -> None:
        self._character_count += 1
        if self._last_latin_character is not None:
            if is_accentuated(character):
                if is_accentuated(self._last_latin_character):
                    if character.isupper():
                        if self._last_latin_character.isupper():
                            self._successive_count += 1
                    if remove_accent(character) == remove_accent(self._last_latin_character):
                        self._successive_count += 1
        self._last_latin_character = character

    def reset(self) -> None:
        self._successive_count = 0
        self._character_count = 0
        self._last_latin_character = None

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            return self._successive_count * 2 / self._character_count


class SuspiciousRange(MessDetectorPlugin):

    def __init__(self):
        self._suspicious_successive_range_count = 0
        self._character_count = 0
        self._last_printable_seen = None

    def eligible(self, character: str) -> bool:
        return character.isprintable()

    def feed(self, character: str) -> None:
        self._character_count += 1
        if character.isspace() or is_punctuation(character):
            self._last_printable_seen = None
            return
        if self._last_printable_seen is None:
            self._last_printable_seen = character
            return
        unicode_range_a = unicode_range(self._last_printable_seen)
        unicode_range_b = unicode_range(character)
        if is_suspiciously_successive_range(unicode_range_a, unicode_range_b):
            self._suspicious_successive_range_count += 1
        self._last_printable_seen = character

    def reset(self) -> None:
        self._character_count = 0
        self._suspicious_successive_range_count = 0
        self._last_printable_seen = None

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            ratio_of_suspicious_range_usage = self._suspicious_successive_range_count * 2 / self._character_count
            if ratio_of_suspicious_range_usage < 0.1:
                return 0.0
            return ratio_of_suspicious_range_usage


class SuperWeirdWordPlugin(MessDetectorPlugin):

    def __init__(self):
        self._word_count = 0
        self._bad_word_count = 0
        self._is_current_word_bad = False
        self._foreign_long_watch = False
        self._character_count = 0
        self._bad_character_count = 0
        self._buffer = ''
        self._buffer_accent_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed(self, character: str) -> None:
        if character.isalpha():
            self._buffer = ''.join([self._buffer, character])
            if is_accentuated(character):
                self._buffer_accent_count += 1
            if self._foreign_long_watch is False:
                if is_latin(character) is False:
                    if is_cjk(character) is False:
                        if is_hangul(character) is False:
                            if is_katakana(character) is False:
                                if is_hiragana(character) is False:
                                    if is_thai(character) is False:
                                        self._foreign_long_watch = True
            return
        elif not self._buffer:
            return
        else:
            if (character.isspace() or is_punctuation(character) or is_separator(character)) and self._buffer:
                self._word_count += 1
                buffer_length = len(self._buffer)
                self._character_count += buffer_length
                if buffer_length >= 4:
                    if self._buffer_accent_count / buffer_length >= 0.3:
                        self._is_current_word_bad = True
                if buffer_length >= 24:
                    if self._foreign_long_watch:
                        self._is_current_word_bad = True
                if self._is_current_word_bad:
                    self._bad_word_count += 1
                    self._bad_character_count += len(self._buffer)
                    self._is_current_word_bad = False
                self._foreign_long_watch = False
                self._buffer = ''
                self._buffer_accent_count = 0
            else:
                if character not in frozenset({'=', '<', '>', '-'}):
                    if character.isdigit() is False:
                        if is_symbol(character):
                            self._is_current_word_bad = True
                            self._buffer += character

    def reset(self) -> None:
        self._buffer = ''
        self._is_current_word_bad = False
        self._foreign_long_watch = False
        self._bad_word_count = 0
        self._word_count = 0
        self._character_count = 0
        self._bad_character_count = 0

    @property
    def ratio(self) -> float:
        if self._word_count <= 10:
            return 0.0
        else:
            return self._bad_character_count / self._character_count


class CjkInvalidStopPlugin(MessDetectorPlugin):
    __doc__ = "\n    GB(Chinese) based encoding often render the stop incorrectly when the content does not fit and can be easily detected.\n    Searching for the overuse of '丅' and '丄'.\n    "

    def __init__(self):
        self._wrong_stop_count = 0
        self._cjk_character_count = 0

    def eligible(self, character: str) -> bool:
        return True

    def feed(self, character: str) -> None:
        if character in ('丅', '丄'):
            self._wrong_stop_count += 1
            return
        if is_cjk(character):
            self._cjk_character_count += 1

    def reset(self) -> None:
        self._wrong_stop_count = 0
        self._cjk_character_count = 0

    @property
    def ratio(self) -> float:
        if self._cjk_character_count < 16:
            return 0.0
        else:
            return self._wrong_stop_count / self._cjk_character_count


class ArchaicUpperLowerPlugin(MessDetectorPlugin):

    def __init__(self):
        self._buf = False
        self._character_count_since_last_sep = 0
        self._successive_upper_lower_count = 0
        self._successive_upper_lower_count_final = 0
        self._character_count = 0
        self._last_alpha_seen = None
        self._current_ascii_only = True

    def eligible(self, character: str) -> bool:
        return True

    def feed(self, character: str) -> None:
        is_concerned = character.isalpha() and is_case_variable(character)
        chunk_sep = is_concerned is False
        if chunk_sep:
            if self._character_count_since_last_sep > 0:
                if self._character_count_since_last_sep <= 64:
                    if character.isdigit() is False:
                        if self._current_ascii_only is False:
                            self._successive_upper_lower_count_final += self._successive_upper_lower_count
                self._successive_upper_lower_count = 0
                self._character_count_since_last_sep = 0
                self._last_alpha_seen = None
                self._buf = False
                self._character_count += 1
                self._current_ascii_only = True
                return
        if self._current_ascii_only is True:
            if is_ascii(character) is False:
                self._current_ascii_only = False
        if self._last_alpha_seen is not None:
            if character.isupper() and self._last_alpha_seen.islower() or character.islower() and self._last_alpha_seen.isupper():
                if self._buf is True:
                    self._successive_upper_lower_count += 2
                    self._buf = False
                else:
                    self._buf = True
            else:
                self._buf = False
        self._character_count += 1
        self._character_count_since_last_sep += 1
        self._last_alpha_seen = character

    def reset(self) -> None:
        self._character_count = 0
        self._character_count_since_last_sep = 0
        self._successive_upper_lower_count = 0
        self._successive_upper_lower_count_final = 0
        self._last_alpha_seen = None
        self._buf = False
        self._current_ascii_only = True

    @property
    def ratio(self) -> float:
        if self._character_count == 0:
            return 0.0
        else:
            return self._successive_upper_lower_count_final / self._character_count


def is_suspiciously_successive_range(unicode_range_a: Optional[str], unicode_range_b: Optional[str]) -> bool:
    """
    Determine if two Unicode range seen next to each other can be considered as suspicious.
    """
    if unicode_range_a is None or unicode_range_b is None:
        return True
    else:
        if unicode_range_a == unicode_range_b:
            return False
        elif 'Latin' in unicode_range_a:
            if 'Latin' in unicode_range_b:
                return False
            else:
                if 'Emoticons' in unicode_range_a or 'Emoticons' in unicode_range_b:
                    return False
                keywords_range_a, keywords_range_b = unicode_range_a.split(' '), unicode_range_b.split(' ')
                for el in keywords_range_a:
                    if el in UNICODE_SECONDARY_RANGE_KEYWORD:
                        pass
                    else:
                        if el in keywords_range_b:
                            return False

                if unicode_range_a in ('Katakana', 'Hiragana'):
                    if unicode_range_b in ('Katakana', 'Hiragana'):
                        return False
                if unicode_range_a in ('Katakana', 'Hiragana') or unicode_range_b in ('Katakana',
                                                                                      'Hiragana'):
                    if 'CJK' in unicode_range_a or 'CJK' in unicode_range_b:
                        return False
        else:
            if 'Hangul' in unicode_range_a or 'Hangul' in unicode_range_b:
                if 'CJK' in unicode_range_a or 'CJK' in unicode_range_b:
                    return False
                if unicode_range_a == 'Basic Latin' or unicode_range_b == 'Basic Latin':
                    return False
            if 'CJK' in unicode_range_a or 'CJK' in unicode_range_b or unicode_range_a in ('Katakana',
                                                                                           'Hiragana') and unicode_range_b in ('Katakana',
                                                                                                                               'Hiragana'):
                if 'Punctuation' in unicode_range_a or 'Punctuation' in unicode_range_b:
                    return False
                if 'Forms' in unicode_range_a or 'Forms' in unicode_range_b:
                    return False
        return True


@lru_cache(maxsize=2048)
def mess_ratio(decoded_sequence: str, maximum_threshold: float=0.2, debug: bool=False) -> float:
    """
    Compute a mess ratio given a decoded bytes sequence. The maximum threshold does stop the computation earlier.
    """
    detectors = []
    for md_class in MessDetectorPlugin.__subclasses__():
        detectors.append(md_class())

    length = len(decoded_sequence)
    mean_mess_ratio = 0.0
    if length < 512:
        intermediary_mean_mess_ratio_calc = 32
    else:
        if length <= 1024:
            intermediary_mean_mess_ratio_calc = 64
        else:
            intermediary_mean_mess_ratio_calc = 128
    for character, index in zip(decoded_sequence, range(0, length)):
        for detector in detectors:
            if detector.eligible(character):
                detector.feed(character)

        if index > 0 and index % intermediary_mean_mess_ratio_calc == 0 or index == length - 1:
            mean_mess_ratio = sum([dt.ratio for dt in detectors])
            if mean_mess_ratio >= maximum_threshold:
                break

    if debug:
        for dt in detectors:
            print(dt.__class__, dt.ratio)

    return round(mean_mess_ratio, 3)