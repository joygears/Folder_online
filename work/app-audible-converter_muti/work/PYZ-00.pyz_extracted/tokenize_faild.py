# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: tokenize.py
"""Tokenization help for Python programs.

tokenize(readline) is a generator that breaks a stream of bytes into
Python tokens.  It decodes the bytes according to PEP-0263 for
determining source file encoding.

It accepts a readline-like method which is called repeatedly to get the
next line of input (or b"" for EOF).  It generates 5-tuples with these
members:

    the token type (see token.py)
    the token (a string)
    the starting (row, column) indices of the token (a 2-tuple of ints)
    the ending (row, column) indices of the token (a 2-tuple of ints)
    the original line (string)

It is designed to match the working of the Python tokenizer exactly, except
that it produces COMMENT tokens for comments and gives type OP for all
operators.  Additionally, all token lists start with an ENCODING token
which tells you which encoding was used to decode the bytes stream.
"""
__author__ = 'Ka-Ping Yee <ping@lfw.org>'
__credits__ = 'GvR, ESR, Tim Peters, Thomas Wouters, Fred Drake, Skip Montanaro, Raymond Hettinger, Trent Nelson, Michael Foord'
from builtins import open as _builtin_open
from codecs import lookup, BOM_UTF8
import collections
from io import TextIOWrapper
from itertools import chain
import itertools as _itertools, re, sys
from token import *
cookie_re = re.compile('^[ \\t\\f]*#.*?coding[:=][ \\t]*([-\\w.]+)', re.ASCII)
blank_re = re.compile(b'^[ \\t\\f]*(?:[#\\r\\n]|$)', re.ASCII)
import token
__all__ = token.__all__ + ['COMMENT', 'tokenize', 'detect_encoding',
 'NL', 'untokenize', 'ENCODING', 'TokenInfo']
del token
COMMENT = N_TOKENS
tok_name[COMMENT] = 'COMMENT'
NL = N_TOKENS + 1
tok_name[NL] = 'NL'
ENCODING = N_TOKENS + 2
tok_name[ENCODING] = 'ENCODING'
N_TOKENS += 3
EXACT_TOKEN_TYPES = {'(':LPAR, 
 ')':RPAR, 
 '[':LSQB, 
 ']':RSQB, 
 ':':COLON, 
 ',':COMMA, 
 ';':SEMI, 
 '+':PLUS, 
 '-':MINUS, 
 '*':STAR, 
 '/':SLASH, 
 '|':VBAR, 
 '&':AMPER, 
 '<':LESS, 
 '>':GREATER, 
 '=':EQUAL, 
 '.':DOT, 
 '%':PERCENT, 
 '{':LBRACE, 
 '}':RBRACE, 
 '==':EQEQUAL, 
 '!=':NOTEQUAL, 
 '<=':LESSEQUAL, 
 '>=':GREATEREQUAL, 
 '~':TILDE, 
 '^':CIRCUMFLEX, 
 '<<':LEFTSHIFT, 
 '>>':RIGHTSHIFT, 
 '**':DOUBLESTAR, 
 '+=':PLUSEQUAL, 
 '-=':MINEQUAL, 
 '*=':STAREQUAL, 
 '/=':SLASHEQUAL, 
 '%=':PERCENTEQUAL, 
 '&=':AMPEREQUAL, 
 '|=':VBAREQUAL, 
 '^=':CIRCUMFLEXEQUAL, 
 '<<=':LEFTSHIFTEQUAL, 
 '>>=':RIGHTSHIFTEQUAL, 
 '**=':DOUBLESTAREQUAL, 
 '//':DOUBLESLASH, 
 '//=':DOUBLESLASHEQUAL, 
 '@':AT, 
 '@=':ATEQUAL}

class TokenInfo(collections.namedtuple('TokenInfo', 'type string start end line')):

    def __repr__(self):
        annotated_type = '%d (%s)' % (self.type, tok_name[self.type])
        return 'TokenInfo(type=%s, string=%r, start=%r, end=%r, line=%r)' % self._replace(type=annotated_type)

    @property
    def exact_type(self):
        if self.type == OP:
            if self.string in EXACT_TOKEN_TYPES:
                return EXACT_TOKEN_TYPES[self.string]
        return self.type


def group(*choices):
    return '(' + '|'.join(choices) + ')'


def any(*choices):
    return group(*choices) + '*'


def maybe(*choices):
    return group(*choices) + '?'


Whitespace = '[ \\f\\t]*'
Comment = '#[^\\r\\n]*'
Ignore = Whitespace + any('\\\\\\r?\\n' + Whitespace) + maybe(Comment)
Name = '\\w+'
Hexnumber = '0[xX](?:_?[0-9a-fA-F])+'
Binnumber = '0[bB](?:_?[01])+'
Octnumber = '0[oO](?:_?[0-7])+'
Decnumber = '(?:0(?:_?0)*|[1-9](?:_?[0-9])*)'
Intnumber = group(Hexnumber, Binnumber, Octnumber, Decnumber)
Exponent = '[eE][-+]?[0-9](?:_?[0-9])*'
Pointfloat = group('[0-9](?:_?[0-9])*\\.(?:[0-9](?:_?[0-9])*)?', '\\.[0-9](?:_?[0-9])*') + maybe(Exponent)
Expfloat = '[0-9](?:_?[0-9])*' + Exponent
Floatnumber = group(Pointfloat, Expfloat)
Imagnumber = group('[0-9](?:_?[0-9])*[jJ]', Floatnumber + '[jJ]')
Number = group(Imagnumber, Floatnumber, Intnumber)

def _all_string_prefixes():
    _valid_string_prefixes = [
     'b', 'r', 'u', 'f', 'br', 'fr']
    result = set([''])
    for prefix in _valid_string_prefixes:
        for t in _itertools.permutations(prefix):
            for u in (_itertools.product)(*[(c, c.upper()) for c in t]):
                result.add(''.join(u))

    return result


def _compile(expr):
    return re.compile(expr, re.UNICODE)


StringPrefix = group(*_all_string_prefixes())
Single = "[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"
Double = '[^"\\\\]*(?:\\\\.[^"\\\\]*)*"'
Single3 = "[^'\\\\]*(?:(?:\\\\.|'(?!''))[^'\\\\]*)*'''"
Double3 = '[^"\\\\]*(?:(?:\\\\.|"(?!""))[^"\\\\]*)*"""'
Triple = group(StringPrefix + "'''", StringPrefix + '"""')
String = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*'", StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*"')
Operator = group('\\*\\*=?', '>>=?', '<<=?', '!=', '//=?', '->', '[+\\-*/%&@|^=<>]=?', '~')
Bracket = '[][(){}]'
Special = group('\\r?\\n', '\\.\\.\\.', '[:;.,@]')
Funny = group(Operator, Bracket, Special)
PlainToken = group(Number, Funny, String, Name)
Token = Ignore + PlainToken
ContStr = group(StringPrefix + "'[^\\n'\\\\]*(?:\\\\.[^\\n'\\\\]*)*" + group("'", '\\\\\\r?\\n'), StringPrefix + '"[^\\n"\\\\]*(?:\\\\.[^\\n"\\\\]*)*' + group('"', '\\\\\\r?\\n'))
PseudoExtras = group('\\\\\\r?\\n|\\Z', Comment, Triple)
PseudoToken = Whitespace + group(PseudoExtras, Number, Funny, ContStr, Name)
endpats = {}
for _prefix in _all_string_prefixes():
    endpats[_prefix + "'"] = Single
    endpats[_prefix + '"'] = Double
    endpats[_prefix + "'''"] = Single3
    endpats[_prefix + '"""'] = Double3

single_quoted = set()
triple_quoted = set()
for t in _all_string_prefixes():
    for u in (t + '"', t + "'"):
        single_quoted.add(u)

    for u in (t + '"""', t + "'''"):
        triple_quoted.add(u)

tabsize = 8

class TokenError(Exception):
    pass


class StopTokenizing(Exception):
    pass


class Untokenizer:

    def __init__(self):
        self.tokens = []
        self.prev_row = 1
        self.prev_col = 0
        self.encoding = None

    def add_whitespace(self, start):
        row, col = start
        if row < self.prev_row or row == self.prev_row and col < self.prev_col:
            raise ValueError('start ({},{}) precedes previous end ({},{})'.format(row, col, self.prev_row, self.prev_col))
        row_offset = row - self.prev_row
        if row_offset:
            self.tokens.append('\\\n' * row_offset)
            self.prev_col = 0
        col_offset = col - self.prev_col
        if col_offset:
            self.tokens.append(' ' * col_offset)

    def untokenize(self, iterable):
        it = iter(iterable)
        indents = []
        startline = False
        for t in it:
            if len(t) == 2:
                self.compat(t, it)
                break
            tok_type, token, start, end, line = t
            if tok_type == ENCODING:
                self.encoding = token
            else:
                if tok_type == ENDMARKER:
                    break
                else:
                    if tok_type == INDENT:
                        indents.append(token)
                        continue
                    else:
                        if tok_type == DEDENT:
                            indents.pop()
                            self.prev_row, self.prev_col = end
                            continue
                        else:
                            if tok_type in (NEWLINE, NL):
                                startline = True
                            elif startline:
                                if indents:
                                    indent = indents[(-1)]
                                    if start[1] >= len(indent):
                                        self.tokens.append(indent)
                                        self.prev_col = len(indent)
                                    startline = False
                self.add_whitespace(start)
                self.tokens.append(token)
                self.prev_row, self.prev_col = end
                if tok_type in (NEWLINE, NL):
                    self.prev_row += 1
                    self.prev_col = 0

        return ''.join(self.tokens)

    def compat(self, token, iterable):
        indents = []
        toks_append = self.tokens.append
        startline = token[0] in (NEWLINE, NL)
        prevstring = False
        for tok in chain([token], iterable):
            toknum, tokval = tok[:2]
            if toknum == ENCODING:
                self.encoding = tokval
            else:
                if toknum in (NAME, NUMBER, ASYNC, AWAIT):
                    tokval += ' '
                else:
                    if toknum == STRING:
                        if prevstring:
                            tokval = ' ' + tokval
                        prevstring = True
                    else:
                        prevstring = False
                if toknum == INDENT:
                    indents.append(tokval)
                    continue
                else:
                    if toknum == DEDENT:
                        indents.pop()
                        continue
                    else:
                        if toknum in (NEWLINE, NL):
                            startline = True
                        else:
                            if startline:
                                if indents:
                                    toks_append(indents[(-1)])
                                    startline = False
                toks_append(tokval)


def untokenize(iterable):
    """Transform tokens back into Python source code.
    It returns a bytes object, encoded using the ENCODING
    token, which is the first token sequence output by tokenize.

    Each element returned by the iterable must be a token sequence
    with at least two elements, a token number and token value.  If
    only two tokens are passed, the resulting output is poor.

    Round-trip invariant for full input:
        Untokenized source will match input source exactly

    Round-trip invariant for limited input:
        # Output bytes will tokenize back to the input
        t1 = [tok[:2] for tok in tokenize(f.readline)]
        newcode = untokenize(t1)
        readline = BytesIO(newcode).readline
        t2 = [tok[:2] for tok in tokenize(readline)]
        assert t1 == t2
    """
    ut = Untokenizer()
    out = ut.untokenize(iterable)
    if ut.encoding is not None:
        out = out.encode(ut.encoding)
    return out


def _get_normal_name(orig_enc):
    """Imitates get_normal_name in tokenizer.c."""
    enc = orig_enc[:12].lower().replace('_', '-')
    if enc == 'utf-8' or enc.startswith('utf-8-'):
        return 'utf-8'
    else:
        if enc in ('latin-1', 'iso-8859-1', 'iso-latin-1') or enc.startswith(('latin-1-',
                                                                              'iso-8859-1-',
                                                                              'iso-latin-1-')):
            return 'iso-8859-1'
        return orig_enc


def detect_encoding(readline):
    """
    The detect_encoding() function is used to detect the encoding that should
    be used to decode a Python source file.  It requires one argument, readline,
    in the same way as the tokenize() generator.

    It will call readline a maximum of twice, and return the encoding used
    (as a string) and a list of any lines (left as bytes) it has read in.

    It detects the encoding from the presence of a utf-8 bom or an encoding
    cookie as specified in pep-0263.  If both a bom and a cookie are present,
    but disagree, a SyntaxError will be raised.  If the encoding cookie is an
    invalid charset, raise a SyntaxError.  Note that if a utf-8 bom is found,
    'utf-8-sig' is returned.

    If no encoding is specified, then the default of 'utf-8' will be returned.
    """
    try:
        filename = readline.__self__.name
    except AttributeError:
        filename = None

    bom_found = False
    encoding = None
    default = 'utf-8'

    def read_or_stop():
        try:
            return readline()
        except StopIteration:
            return b''

    def find_cookie(line):
        try:
            line_string = line.decode('utf-8')
        except UnicodeDecodeError:
            msg = 'invalid or missing encoding declaration'
            if filename is not None:
                msg = '{} for {!r}'.format(msg, filename)
            raise SyntaxError(msg)

        match = cookie_re.match(line_string)
        if not match:
            return
        else:
            encoding = _get_normal_name(match.group(1))
            try:
                codec = lookup(encoding)
            except LookupError:
                if filename is None:
                    msg = 'unknown encoding: ' + encoding
                else:
                    msg = 'unknown encoding for {!r}: {}'.format(filename, encoding)
                raise SyntaxError(msg)

            if bom_found:
                if encoding != 'utf-8':
                    if filename is None:
                        msg = 'encoding problem: utf-8'
                    else:
                        msg = 'encoding problem for {!r}: utf-8'.format(filename)
                    raise SyntaxError(msg)
                encoding += '-sig'
            return encoding

    first = read_or_stop()
    if first.startswith(BOM_UTF8):
        bom_found = True
        first = first[3:]
        default = 'utf-8-sig'
    if not first:
        return (
         default, [])
    encoding = find_cookie(first)
    if encoding:
        return (
         encoding, [first])
    if not blank_re.match(first):
        return (
         default, [first])
    second = read_or_stop()
    if not second:
        return (default, [first])
    else:
        encoding = find_cookie(second)
        if encoding:
            return (
             encoding, [first, second])
        return (default, [first, second])


def open(filename):
    """Open a file in read only mode using the encoding detected by
    detect_encoding().
    """
    buffer = _builtin_open(filename, 'rb')
    try:
        encoding, lines = detect_encoding(buffer.readline)
        buffer.seek(0)
        text = TextIOWrapper(buffer, encoding, line_buffering=True)
        text.mode = 'r'
        return text
    except:
        buffer.close()
        raise


def tokenize(readline):
    """
    The tokenize() generator requires one argument, readline, which
    must be a callable object which provides the same interface as the
    readline() method of built-in file objects.  Each call to the function
    should return one line of input as bytes.  Alternatively, readline
    can be a callable function terminating with StopIteration:
        readline = open(myfile, 'rb').__next__  # Example of alternate readline

    The generator produces 5-tuples with these members: the token type; the
    token string; a 2-tuple (srow, scol) of ints specifying the row and
    column where the token begins in the source; a 2-tuple (erow, ecol) of
    ints specifying the row and column where the token ends in the source;
    and the line on which the token was found.  The line passed is the
    logical line; continuation lines are included.

    The first token sequence will always be an ENCODING token
    which tells you which encoding was used to decode the bytes stream.
    """
    from itertools import chain, repeat
    encoding, consumed = detect_encoding(readline)
    rl_gen = iter(readline, b'')
    empty = repeat(b'')
    return _tokenize(chain(consumed, rl_gen, empty).__next__, encoding)


def _tokenize--- This code section failed: ---

 L. 493         0  LOAD_CONST               0
                2  DUP_TOP          
                4  STORE_FAST               'lnum'
                6  DUP_TOP          
                8  STORE_FAST               'parenlev'
               10  STORE_FAST               'continued'

 L. 494        12  LOAD_STR                 '0123456789'
               14  STORE_FAST               'numchars'

 L. 495        16  LOAD_CONST               ('', 0)
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'contstr'
               22  STORE_FAST               'needcont'

 L. 496        24  LOAD_CONST               None
               26  STORE_FAST               'contline'

 L. 497        28  LOAD_CONST               0
               30  BUILD_LIST_1          1 
               32  STORE_FAST               'indents'

 L. 500        34  LOAD_CONST               None
               36  STORE_FAST               'stashed'

 L. 501        38  LOAD_CONST               False
               40  STORE_FAST               'async_def'

 L. 502        42  LOAD_CONST               0
               44  STORE_FAST               'async_def_indent'

 L. 503        46  LOAD_CONST               False
               48  STORE_FAST               'async_def_nl'

 L. 505        50  LOAD_FAST                'encoding'
               52  LOAD_CONST               None
               54  COMPARE_OP               is-not
               56  POP_JUMP_IF_FALSE    88  'to 88'

 L. 506        58  LOAD_FAST                'encoding'
               60  LOAD_STR                 'utf-8-sig'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_FALSE    70  'to 70'

 L. 508        66  LOAD_STR                 'utf-8'
               68  STORE_FAST               'encoding'
             70_0  COME_FROM            64  '64'

 L. 509        70  LOAD_GLOBAL              TokenInfo
               72  LOAD_GLOBAL              ENCODING
               74  LOAD_FAST                'encoding'
               76  LOAD_CONST               (0, 0)
               78  LOAD_CONST               (0, 0)
               80  LOAD_STR                 ''
               82  CALL_FUNCTION_5       5  '5 positional arguments'
               84  YIELD_VALUE      
               86  POP_TOP          
             88_0  COME_FROM            56  '56'

 L. 510        88  LOAD_CONST               b''
               90  STORE_FAST               'last_line'

 L. 511        92  LOAD_CONST               b''
               94  STORE_FAST               'line'

 L. 512        96  SETUP_LOOP         1920  'to 1920'

 L. 513       100  SETUP_EXCEPT        116  'to 116'

 L. 518       102  LOAD_FAST                'line'
              104  STORE_FAST               'last_line'

 L. 519       106  LOAD_FAST                'readline'
              108  CALL_FUNCTION_0       0  '0 positional arguments'
              110  STORE_FAST               'line'
              112  POP_BLOCK        
              114  JUMP_FORWARD        140  'to 140'
            116_0  COME_FROM_EXCEPT    100  '100'

 L. 520       116  DUP_TOP          
              118  LOAD_GLOBAL              StopIteration
              120  COMPARE_OP               exception-match
              122  POP_JUMP_IF_FALSE   138  'to 138'
              124  POP_TOP          
              126  POP_TOP          
              128  POP_TOP          

 L. 521       130  LOAD_CONST               b''
              132  STORE_FAST               'line'
              134  POP_EXCEPT       
              136  JUMP_FORWARD        140  'to 140'
              138  END_FINALLY      
            140_0  COME_FROM           136  '136'
            140_1  COME_FROM           114  '114'

 L. 523       140  LOAD_FAST                'encoding'
              142  LOAD_CONST               None
              144  COMPARE_OP               is-not
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L. 524       148  LOAD_FAST                'line'
              150  LOAD_ATTR                decode
              152  LOAD_FAST                'encoding'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  STORE_FAST               'line'
            158_0  COME_FROM           146  '146'

 L. 525       158  LOAD_FAST                'lnum'
              160  LOAD_CONST               1
              162  INPLACE_ADD      
              164  STORE_FAST               'lnum'

 L. 526       166  LOAD_CONST               0
              168  LOAD_GLOBAL              len
              170  LOAD_FAST                'line'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  ROT_TWO          
              176  STORE_FAST               'pos'
              178  STORE_FAST               'max'

 L. 528       180  LOAD_FAST                'contstr'
              182  POP_JUMP_IF_FALSE   388  'to 388'

 L. 529       186  LOAD_FAST                'line'
              188  POP_JUMP_IF_TRUE    200  'to 200'

 L. 530       190  LOAD_GLOBAL              TokenError
              192  LOAD_STR                 'EOF in multi-line string'
              194  LOAD_FAST                'strstart'
              196  CALL_FUNCTION_2       2  '2 positional arguments'
              198  RAISE_VARARGS_1       1  'exception'
            200_0  COME_FROM           188  '188'

 L. 531       200  LOAD_FAST                'endprog'
              202  LOAD_ATTR                match
              204  LOAD_FAST                'line'
              206  CALL_FUNCTION_1       1  '1 positional argument'
              208  STORE_FAST               'endmatch'

 L. 532       210  LOAD_FAST                'endmatch'
              212  POP_JUMP_IF_FALSE   282  'to 282'

 L. 533       216  LOAD_FAST                'endmatch'
              218  LOAD_ATTR                end
              220  LOAD_CONST               0
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  DUP_TOP          
              226  STORE_FAST               'pos'
              228  STORE_FAST               'end'

 L. 534       230  LOAD_GLOBAL              TokenInfo
              232  LOAD_GLOBAL              STRING
              234  LOAD_FAST                'contstr'
              236  LOAD_FAST                'line'
              238  LOAD_CONST               None
              240  LOAD_FAST                'end'
              242  BUILD_SLICE_2         2 
              244  BINARY_SUBSCR    
              246  BINARY_ADD       

 L. 535       248  LOAD_FAST                'strstart'
              250  LOAD_FAST                'lnum'
              252  LOAD_FAST                'end'
              254  BUILD_TUPLE_2         2 
              256  LOAD_FAST                'contline'
              258  LOAD_FAST                'line'
              260  BINARY_ADD       
              262  CALL_FUNCTION_5       5  '5 positional arguments'
              264  YIELD_VALUE      
              266  POP_TOP          

 L. 536       268  LOAD_CONST               ('', 0)
              270  UNPACK_SEQUENCE_2     2 
              272  STORE_FAST               'contstr'
              274  STORE_FAST               'needcont'

 L. 537       276  LOAD_CONST               None
              278  STORE_FAST               'contline'
              280  JUMP_FORWARD        384  'to 384'
              282  ELSE                     '384'

 L. 538       282  LOAD_FAST                'needcont'
              284  POP_JUMP_IF_FALSE   366  'to 366'
              288  LOAD_FAST                'line'
              290  LOAD_CONST               -2
              292  LOAD_CONST               None
              294  BUILD_SLICE_2         2 
              296  BINARY_SUBSCR    
              298  LOAD_STR                 '\\\n'
              300  COMPARE_OP               !=
              302  POP_JUMP_IF_FALSE   366  'to 366'
              306  LOAD_FAST                'line'
              308  LOAD_CONST               -3
              310  LOAD_CONST               None
              312  BUILD_SLICE_2         2 
              314  BINARY_SUBSCR    
              316  LOAD_STR                 '\\\r\n'
              318  COMPARE_OP               !=
              320  POP_JUMP_IF_FALSE   366  'to 366'

 L. 539       324  LOAD_GLOBAL              TokenInfo
              326  LOAD_GLOBAL              ERRORTOKEN
              328  LOAD_FAST                'contstr'
              330  LOAD_FAST                'line'
              332  BINARY_ADD       

 L. 540       334  LOAD_FAST                'strstart'
              336  LOAD_FAST                'lnum'
              338  LOAD_GLOBAL              len
              340  LOAD_FAST                'line'
              342  CALL_FUNCTION_1       1  '1 positional argument'
              344  BUILD_TUPLE_2         2 
              346  LOAD_FAST                'contline'
              348  CALL_FUNCTION_5       5  '5 positional arguments'
              350  YIELD_VALUE      
              352  POP_TOP          

 L. 541       354  LOAD_STR                 ''
              356  STORE_FAST               'contstr'

 L. 542       358  LOAD_CONST               None
              360  STORE_FAST               'contline'

 L. 543       362  CONTINUE            100  'to 100'
              364  JUMP_FORWARD        384  'to 384'
            366_0  COME_FROM           302  '302'
            366_1  COME_FROM           284  '284'

 L. 545       366  LOAD_FAST                'contstr'
              368  LOAD_FAST                'line'
              370  BINARY_ADD       
              372  STORE_FAST               'contstr'

 L. 546       374  LOAD_FAST                'contline'
              376  LOAD_FAST                'line'
              378  BINARY_ADD       
              380  STORE_FAST               'contline'

 L. 547       382  CONTINUE            100  'to 100'
            384_0  COME_FROM           364  '364'
            384_1  COME_FROM           280  '280'
              384  JUMP_FORWARD        964  'to 964'
              388  ELSE                     '964'

 L. 549       388  LOAD_FAST                'parenlev'
              390  LOAD_CONST               0
              392  COMPARE_OP               ==
              394  POP_JUMP_IF_FALSE   940  'to 940'
              398  LOAD_FAST                'continued'
              400  UNARY_NOT        
              402  POP_JUMP_IF_FALSE   940  'to 940'

 L. 550       406  LOAD_FAST                'line'
              408  POP_JUMP_IF_TRUE    414  'to 414'

 L. 550       412  BREAK_LOOP       
            414_0  COME_FROM           408  '408'

 L. 551       414  LOAD_CONST               0
              416  STORE_FAST               'column'

 L. 552       418  SETUP_LOOP          522  'to 522'
              420  LOAD_FAST                'pos'
              422  LOAD_FAST                'max'
              424  COMPARE_OP               <
              426  POP_JUMP_IF_FALSE   520  'to 520'

 L. 553       430  LOAD_FAST                'line'
              432  LOAD_FAST                'pos'
              434  BINARY_SUBSCR    
              436  LOAD_STR                 ' '
              438  COMPARE_OP               ==
              440  POP_JUMP_IF_FALSE   454  'to 454'

 L. 554       444  LOAD_FAST                'column'
              446  LOAD_CONST               1
              448  INPLACE_ADD      
              450  STORE_FAST               'column'
              452  JUMP_FORWARD        508  'to 508'
              454  ELSE                     '508'

 L. 555       454  LOAD_FAST                'line'
              456  LOAD_FAST                'pos'
              458  BINARY_SUBSCR    
              460  LOAD_STR                 '\t'
              462  COMPARE_OP               ==
              464  POP_JUMP_IF_FALSE   486  'to 486'

 L. 556       468  LOAD_FAST                'column'
              470  LOAD_GLOBAL              tabsize
              472  BINARY_FLOOR_DIVIDE
              474  LOAD_CONST               1
              476  BINARY_ADD       
              478  LOAD_GLOBAL              tabsize
              480  BINARY_MULTIPLY  
              482  STORE_FAST               'column'
              484  JUMP_FORWARD        508  'to 508'
              486  ELSE                     '508'

 L. 557       486  LOAD_FAST                'line'
              488  LOAD_FAST                'pos'
              490  BINARY_SUBSCR    
              492  LOAD_STR                 '\x0c'
              494  COMPARE_OP               ==
              496  POP_JUMP_IF_FALSE   506  'to 506'

 L. 558       500  LOAD_CONST               0
              502  STORE_FAST               'column'
              504  JUMP_FORWARD        508  'to 508'
              506  ELSE                     '508'

 L. 560       506  BREAK_LOOP       
            508_0  COME_FROM           504  '504'
            508_1  COME_FROM           484  '484'
            508_2  COME_FROM           452  '452'

 L. 561       508  LOAD_FAST                'pos'
              510  LOAD_CONST               1
              512  INPLACE_ADD      
              514  STORE_FAST               'pos'
              516  JUMP_BACK           420  'to 420'
            520_0  COME_FROM           426  '426'
              520  POP_BLOCK        
            522_0  COME_FROM_LOOP      418  '418'

 L. 562       522  LOAD_FAST                'pos'
              524  LOAD_FAST                'max'
              526  COMPARE_OP               ==
              528  POP_JUMP_IF_FALSE   534  'to 534'

 L. 563       532  BREAK_LOOP       
            534_0  COME_FROM           528  '528'

 L. 565       534  LOAD_FAST                'line'
              536  LOAD_FAST                'pos'
              538  BINARY_SUBSCR    
              540  LOAD_STR                 '#\r\n'
              542  COMPARE_OP               in
              544  POP_JUMP_IF_FALSE   722  'to 722'

 L. 566       548  LOAD_FAST                'line'
              550  LOAD_FAST                'pos'
              552  BINARY_SUBSCR    
              554  LOAD_STR                 '#'
              556  COMPARE_OP               ==
              558  POP_JUMP_IF_FALSE   666  'to 666'

 L. 567       562  LOAD_FAST                'line'
              564  LOAD_FAST                'pos'
              566  LOAD_CONST               None
              568  BUILD_SLICE_2         2 
              570  BINARY_SUBSCR    
              572  LOAD_ATTR                rstrip
              574  LOAD_STR                 '\r\n'
              576  CALL_FUNCTION_1       1  '1 positional argument'
              578  STORE_FAST               'comment_token'

 L. 568       580  LOAD_FAST                'pos'
              582  LOAD_GLOBAL              len
              584  LOAD_FAST                'comment_token'
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  BINARY_ADD       
              590  STORE_FAST               'nl_pos'

 L. 569       592  LOAD_GLOBAL              TokenInfo
              594  LOAD_GLOBAL              COMMENT
              596  LOAD_FAST                'comment_token'

 L. 570       598  LOAD_FAST                'lnum'
              600  LOAD_FAST                'pos'
              602  BUILD_TUPLE_2         2 
              604  LOAD_FAST                'lnum'
              606  LOAD_FAST                'pos'
              608  LOAD_GLOBAL              len
              610  LOAD_FAST                'comment_token'
              612  CALL_FUNCTION_1       1  '1 positional argument'
              614  BINARY_ADD       
              616  BUILD_TUPLE_2         2 
              618  LOAD_FAST                'line'
              620  CALL_FUNCTION_5       5  '5 positional arguments'
              622  YIELD_VALUE      
              624  POP_TOP          

 L. 571       626  LOAD_GLOBAL              TokenInfo
              628  LOAD_GLOBAL              NL
              630  LOAD_FAST                'line'
              632  LOAD_FAST                'nl_pos'
              634  LOAD_CONST               None
              636  BUILD_SLICE_2         2 
              638  BINARY_SUBSCR    

 L. 572       640  LOAD_FAST                'lnum'
              642  LOAD_FAST                'nl_pos'
              644  BUILD_TUPLE_2         2 
              646  LOAD_FAST                'lnum'
              648  LOAD_GLOBAL              len
              650  LOAD_FAST                'line'
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  BUILD_TUPLE_2         2 
              656  LOAD_FAST                'line'
              658  CALL_FUNCTION_5       5  '5 positional arguments'
              660  YIELD_VALUE      
              662  POP_TOP          
              664  JUMP_BACK           100  'to 100'
              666  ELSE                     '720'

 L. 574       666  LOAD_GLOBAL              TokenInfo
              668  LOAD_GLOBAL              NL
              670  LOAD_GLOBAL              COMMENT
              672  BUILD_TUPLE_2         2 
              674  LOAD_FAST                'line'
              676  LOAD_FAST                'pos'
              678  BINARY_SUBSCR    
              680  LOAD_STR                 '#'
              682  COMPARE_OP               ==
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'line'
              688  LOAD_FAST                'pos'
              690  LOAD_CONST               None
              692  BUILD_SLICE_2         2 
              694  BINARY_SUBSCR    

 L. 575       696  LOAD_FAST                'lnum'
              698  LOAD_FAST                'pos'
              700  BUILD_TUPLE_2         2 
              702  LOAD_FAST                'lnum'
              704  LOAD_GLOBAL              len
              706  LOAD_FAST                'line'
              708  CALL_FUNCTION_1       1  '1 positional argument'
              710  BUILD_TUPLE_2         2 
              712  LOAD_FAST                'line'
              714  CALL_FUNCTION_5       5  '5 positional arguments'
              716  YIELD_VALUE      
              718  POP_TOP          

 L. 576       720  CONTINUE            100  'to 100'

 L. 578       722  LOAD_FAST                'column'
              724  LOAD_FAST                'indents'
              726  LOAD_CONST               -1
              728  BINARY_SUBSCR    
              730  COMPARE_OP               >
              732  POP_JUMP_IF_FALSE   780  'to 780'

 L. 579       736  LOAD_FAST                'indents'
              738  LOAD_ATTR                append
              740  LOAD_FAST                'column'
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  POP_TOP          

 L. 580       746  LOAD_GLOBAL              TokenInfo
              748  LOAD_GLOBAL              INDENT
              750  LOAD_FAST                'line'
              752  LOAD_CONST               None
              754  LOAD_FAST                'pos'
              756  BUILD_SLICE_2         2 
              758  BINARY_SUBSCR    
              760  LOAD_FAST                'lnum'
              762  LOAD_CONST               0
              764  BUILD_TUPLE_2         2 
              766  LOAD_FAST                'lnum'
              768  LOAD_FAST                'pos'
              770  BUILD_TUPLE_2         2 
              772  LOAD_FAST                'line'
              774  CALL_FUNCTION_5       5  '5 positional arguments'
              776  YIELD_VALUE      
              778  POP_TOP          
            780_0  COME_FROM           732  '732'

 L. 581       780  SETUP_LOOP          900  'to 900'
              782  LOAD_FAST                'column'
              784  LOAD_FAST                'indents'
              786  LOAD_CONST               -1
              788  BINARY_SUBSCR    
              790  COMPARE_OP               <
              792  POP_JUMP_IF_FALSE   898  'to 898'

 L. 582       796  LOAD_FAST                'column'
              798  LOAD_FAST                'indents'
              800  COMPARE_OP               not-in
              802  POP_JUMP_IF_FALSE   824  'to 824'

 L. 583       806  LOAD_GLOBAL              IndentationError

 L. 584       808  LOAD_STR                 'unindent does not match any outer indentation level'

 L. 585       810  LOAD_STR                 '<tokenize>'
              812  LOAD_FAST                'lnum'
              814  LOAD_FAST                'pos'
              816  LOAD_FAST                'line'
              818  BUILD_TUPLE_4         4 
              820  CALL_FUNCTION_2       2  '2 positional arguments'
              822  RAISE_VARARGS_1       1  'exception'
            824_0  COME_FROM           802  '802'

 L. 586       824  LOAD_FAST                'indents'
              826  LOAD_CONST               None
              828  LOAD_CONST               -1
              830  BUILD_SLICE_2         2 
              832  BINARY_SUBSCR    
              834  STORE_FAST               'indents'

 L. 588       836  LOAD_FAST                'async_def'
              838  POP_JUMP_IF_FALSE   868  'to 868'
              842  LOAD_FAST                'async_def_indent'
              844  LOAD_FAST                'indents'
              846  LOAD_CONST               -1
              848  BINARY_SUBSCR    
              850  COMPARE_OP               >=
              852  POP_JUMP_IF_FALSE   868  'to 868'

 L. 589       856  LOAD_CONST               False
              858  STORE_FAST               'async_def'

 L. 590       860  LOAD_CONST               False
              862  STORE_FAST               'async_def_nl'

 L. 591       864  LOAD_CONST               0
              866  STORE_FAST               'async_def_indent'
            868_0  COME_FROM           852  '852'
            868_1  COME_FROM           838  '838'

 L. 593       868  LOAD_GLOBAL              TokenInfo
              870  LOAD_GLOBAL              DEDENT
              872  LOAD_STR                 ''
              874  LOAD_FAST                'lnum'
              876  LOAD_FAST                'pos'
              878  BUILD_TUPLE_2         2 
              880  LOAD_FAST                'lnum'
              882  LOAD_FAST                'pos'
              884  BUILD_TUPLE_2         2 
              886  LOAD_FAST                'line'
              888  CALL_FUNCTION_5       5  '5 positional arguments'
              890  YIELD_VALUE      
              892  POP_TOP          
              894  JUMP_BACK           782  'to 782'
            898_0  COME_FROM           792  '792'
              898  POP_BLOCK        
            900_0  COME_FROM_LOOP      780  '780'

 L. 595       900  LOAD_FAST                'async_def'
              902  POP_JUMP_IF_FALSE   964  'to 964'
              906  LOAD_FAST                'async_def_nl'
              908  POP_JUMP_IF_FALSE   964  'to 964'
              912  LOAD_FAST                'async_def_indent'
              914  LOAD_FAST                'indents'
              916  LOAD_CONST               -1
              918  BINARY_SUBSCR    
              920  COMPARE_OP               >=
              922  POP_JUMP_IF_FALSE   964  'to 964'

 L. 596       926  LOAD_CONST               False
              928  STORE_FAST               'async_def'

 L. 597       930  LOAD_CONST               False
              932  STORE_FAST               'async_def_nl'

 L. 598       934  LOAD_CONST               0
              936  STORE_FAST               'async_def_indent'
              938  JUMP_FORWARD        964  'to 964'
            940_0  COME_FROM           394  '394'

 L. 601       940  LOAD_FAST                'line'
              942  POP_JUMP_IF_TRUE    960  'to 960'

 L. 602       946  LOAD_GLOBAL              TokenError
              948  LOAD_STR                 'EOF in multi-line statement'
              950  LOAD_FAST                'lnum'
              952  LOAD_CONST               0
              954  BUILD_TUPLE_2         2 
              956  CALL_FUNCTION_2       2  '2 positional arguments'
              958  RAISE_VARARGS_1       1  'exception'
            960_0  COME_FROM           942  '942'

 L. 603       960  LOAD_CONST               0
              962  STORE_FAST               'continued'
            964_0  COME_FROM           938  '938'
            964_1  COME_FROM           922  '922'
            964_2  COME_FROM           908  '908'
            964_3  COME_FROM           902  '902'
            964_4  COME_FROM           384  '384'

 L. 605       964  SETUP_LOOP         1916  'to 1916'
              968  LOAD_FAST                'pos'
              970  LOAD_FAST                'max'
              972  COMPARE_OP               <
              974  POP_JUMP_IF_FALSE  1914  'to 1914'

 L. 606       978  LOAD_GLOBAL              _compile
              980  LOAD_GLOBAL              PseudoToken
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  LOAD_ATTR                match
              986  LOAD_FAST                'line'
              988  LOAD_FAST                'pos'
              990  CALL_FUNCTION_2       2  '2 positional arguments'
              992  STORE_FAST               'pseudomatch'

 L. 607       994  LOAD_FAST                'pseudomatch'
              996  POP_JUMP_IF_FALSE  1868  'to 1868'

 L. 608      1000  LOAD_FAST                'pseudomatch'
             1002  LOAD_ATTR                span
             1004  LOAD_CONST               1
             1006  CALL_FUNCTION_1       1  '1 positional argument'
             1008  UNPACK_SEQUENCE_2     2 
             1010  STORE_FAST               'start'
             1012  STORE_FAST               'end'

 L. 609      1014  LOAD_FAST                'lnum'
             1016  LOAD_FAST                'start'
             1018  BUILD_TUPLE_2         2 
             1020  LOAD_FAST                'lnum'
             1022  LOAD_FAST                'end'
             1024  BUILD_TUPLE_2         2 
             1026  LOAD_FAST                'end'
             1028  ROT_THREE        
             1030  ROT_TWO          
             1032  STORE_FAST               'spos'
             1034  STORE_FAST               'epos'
             1036  STORE_FAST               'pos'

 L. 610      1038  LOAD_FAST                'start'
             1040  LOAD_FAST                'end'
             1042  COMPARE_OP               ==
             1044  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 611      1048  CONTINUE            968  'to 968'
             1052  ELSE                     '1866'

 L. 612      1052  LOAD_FAST                'line'
             1054  LOAD_FAST                'start'
             1056  LOAD_FAST                'end'
             1058  BUILD_SLICE_2         2 
             1060  BINARY_SUBSCR    
             1062  LOAD_FAST                'line'
             1064  LOAD_FAST                'start'
             1066  BINARY_SUBSCR    
             1068  ROT_TWO          
             1070  STORE_FAST               'token'
             1072  STORE_FAST               'initial'

 L. 614      1074  LOAD_FAST                'initial'
             1076  LOAD_FAST                'numchars'
             1078  COMPARE_OP               in
             1080  POP_JUMP_IF_TRUE   1114  'to 1114'

 L. 615      1084  LOAD_FAST                'initial'
             1086  LOAD_STR                 '.'
             1088  COMPARE_OP               ==
             1090  POP_JUMP_IF_FALSE  1136  'to 1136'
             1094  LOAD_FAST                'token'
             1096  LOAD_STR                 '.'
             1098  COMPARE_OP               !=
             1100  POP_JUMP_IF_FALSE  1136  'to 1136'
             1104  LOAD_FAST                'token'
             1106  LOAD_STR                 '...'
             1108  COMPARE_OP               !=
           1110_0  COME_FROM          1100  '1100'
           1110_1  COME_FROM          1090  '1090'
           1110_2  COME_FROM          1080  '1080'
             1110  POP_JUMP_IF_FALSE  1136  'to 1136'

 L. 616      1114  LOAD_GLOBAL              TokenInfo
             1116  LOAD_GLOBAL              NUMBER
             1118  LOAD_FAST                'token'
             1120  LOAD_FAST                'spos'
             1122  LOAD_FAST                'epos'
             1124  LOAD_FAST                'line'
             1126  CALL_FUNCTION_5       5  '5 positional arguments'
             1128  YIELD_VALUE      
             1130  POP_TOP          
             1132  JUMP_ABSOLUTE      1910  'to 1910'
             1136  ELSE                     '1866'

 L. 617      1136  LOAD_FAST                'initial'
             1138  LOAD_STR                 '\r\n'
             1140  COMPARE_OP               in
             1142  POP_JUMP_IF_FALSE  1224  'to 1224'

 L. 618      1146  LOAD_FAST                'stashed'
             1148  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 619      1152  LOAD_FAST                'stashed'
             1154  YIELD_VALUE      
             1156  POP_TOP          

 L. 620      1158  LOAD_CONST               None
             1160  STORE_FAST               'stashed'
           1162_0  COME_FROM          1148  '1148'

 L. 621      1162  LOAD_FAST                'parenlev'
             1164  LOAD_CONST               0
             1166  COMPARE_OP               >
             1168  POP_JUMP_IF_FALSE  1192  'to 1192'

 L. 622      1172  LOAD_GLOBAL              TokenInfo
             1174  LOAD_GLOBAL              NL
             1176  LOAD_FAST                'token'
             1178  LOAD_FAST                'spos'
             1180  LOAD_FAST                'epos'
             1182  LOAD_FAST                'line'
             1184  CALL_FUNCTION_5       5  '5 positional arguments'
             1186  YIELD_VALUE      
             1188  POP_TOP          
             1190  JUMP_FORWARD       1220  'to 1220'
             1192  ELSE                     '1220'

 L. 624      1192  LOAD_GLOBAL              TokenInfo
             1194  LOAD_GLOBAL              NEWLINE
             1196  LOAD_FAST                'token'
             1198  LOAD_FAST                'spos'
             1200  LOAD_FAST                'epos'
             1202  LOAD_FAST                'line'
             1204  CALL_FUNCTION_5       5  '5 positional arguments'
             1206  YIELD_VALUE      
             1208  POP_TOP          

 L. 625      1210  LOAD_FAST                'async_def'
             1212  POP_JUMP_IF_FALSE  1866  'to 1866'

 L. 626      1216  LOAD_CONST               True
             1218  STORE_FAST               'async_def_nl'
           1220_0  COME_FROM          1190  '1190'
             1220  JUMP_ABSOLUTE      1910  'to 1910'
             1224  ELSE                     '1866'

 L. 628      1224  LOAD_FAST                'initial'
             1226  LOAD_STR                 '#'
             1228  COMPARE_OP               ==
             1230  POP_JUMP_IF_FALSE  1290  'to 1290'

 L. 629      1234  LOAD_FAST                'token'
             1236  LOAD_ATTR                endswith
             1238  LOAD_STR                 '\n'
             1240  CALL_FUNCTION_1       1  '1 positional argument'
             1242  UNARY_NOT        
             1244  POP_JUMP_IF_TRUE   1252  'to 1252'
             1248  LOAD_ASSERT              AssertionError
             1250  RAISE_VARARGS_1       1  'exception'
           1252_0  COME_FROM          1244  '1244'

 L. 630      1252  LOAD_FAST                'stashed'
             1254  POP_JUMP_IF_FALSE  1268  'to 1268'

 L. 631      1258  LOAD_FAST                'stashed'
             1260  YIELD_VALUE      
             1262  POP_TOP          

 L. 632      1264  LOAD_CONST               None
             1266  STORE_FAST               'stashed'
           1268_0  COME_FROM          1254  '1254'

 L. 633      1268  LOAD_GLOBAL              TokenInfo
             1270  LOAD_GLOBAL              COMMENT
             1272  LOAD_FAST                'token'
             1274  LOAD_FAST                'spos'
             1276  LOAD_FAST                'epos'
             1278  LOAD_FAST                'line'
             1280  CALL_FUNCTION_5       5  '5 positional arguments'
             1282  YIELD_VALUE      
             1284  POP_TOP          
             1286  JUMP_ABSOLUTE      1910  'to 1910'
             1290  ELSE                     '1866'

 L. 635      1290  LOAD_FAST                'token'
             1292  LOAD_GLOBAL              triple_quoted
             1294  COMPARE_OP               in
             1296  POP_JUMP_IF_FALSE  1406  'to 1406'

 L. 636      1300  LOAD_GLOBAL              _compile
             1302  LOAD_GLOBAL              endpats
             1304  LOAD_FAST                'token'
             1306  BINARY_SUBSCR    
             1308  CALL_FUNCTION_1       1  '1 positional argument'
             1310  STORE_FAST               'endprog'

 L. 637      1312  LOAD_FAST                'endprog'
             1314  LOAD_ATTR                match
             1316  LOAD_FAST                'line'
             1318  LOAD_FAST                'pos'
             1320  CALL_FUNCTION_2       2  '2 positional arguments'
             1322  STORE_FAST               'endmatch'

 L. 638      1324  LOAD_FAST                'endmatch'
             1326  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 639      1330  LOAD_FAST                'endmatch'
             1332  LOAD_ATTR                end
             1334  LOAD_CONST               0
             1336  CALL_FUNCTION_1       1  '1 positional argument'
             1338  STORE_FAST               'pos'

 L. 640      1340  LOAD_FAST                'line'
             1342  LOAD_FAST                'start'
             1344  LOAD_FAST                'pos'
             1346  BUILD_SLICE_2         2 
             1348  BINARY_SUBSCR    
             1350  STORE_FAST               'token'

 L. 641      1352  LOAD_GLOBAL              TokenInfo
             1354  LOAD_GLOBAL              STRING
             1356  LOAD_FAST                'token'
             1358  LOAD_FAST                'spos'
             1360  LOAD_FAST                'lnum'
             1362  LOAD_FAST                'pos'
             1364  BUILD_TUPLE_2         2 
             1366  LOAD_FAST                'line'
             1368  CALL_FUNCTION_5       5  '5 positional arguments'
             1370  YIELD_VALUE      
             1372  POP_TOP          
             1374  JUMP_FORWARD       1402  'to 1402'
             1376  ELSE                     '1402'

 L. 643      1376  LOAD_FAST                'lnum'
             1378  LOAD_FAST                'start'
             1380  BUILD_TUPLE_2         2 
             1382  STORE_FAST               'strstart'

 L. 644      1384  LOAD_FAST                'line'
             1386  LOAD_FAST                'start'
             1388  LOAD_CONST               None
             1390  BUILD_SLICE_2         2 
             1392  BINARY_SUBSCR    
             1394  STORE_FAST               'contstr'

 L. 645      1396  LOAD_FAST                'line'
             1398  STORE_FAST               'contline'

 L. 646      1400  BREAK_LOOP       
           1402_0  COME_FROM          1374  '1374'
             1402  JUMP_ABSOLUTE      1910  'to 1910'
             1406  ELSE                     '1866'

 L. 658      1406  LOAD_FAST                'initial'
             1408  LOAD_GLOBAL              single_quoted
             1410  COMPARE_OP               in
             1412  POP_JUMP_IF_TRUE   1452  'to 1452'

 L. 659      1416  LOAD_FAST                'token'
             1418  LOAD_CONST               None
             1420  LOAD_CONST               2
             1422  BUILD_SLICE_2         2 
             1424  BINARY_SUBSCR    
             1426  LOAD_GLOBAL              single_quoted
             1428  COMPARE_OP               in
             1430  POP_JUMP_IF_TRUE   1452  'to 1452'

 L. 660      1434  LOAD_FAST                'token'
             1436  LOAD_CONST               None
             1438  LOAD_CONST               3
             1440  BUILD_SLICE_2         2 
             1442  BINARY_SUBSCR    
             1444  LOAD_GLOBAL              single_quoted
             1446  COMPARE_OP               in
           1448_0  COME_FROM          1430  '1430'
           1448_1  COME_FROM          1412  '1412'
             1448  POP_JUMP_IF_FALSE  1568  'to 1568'

 L. 661      1452  LOAD_FAST                'token'
             1454  LOAD_CONST               -1
             1456  BINARY_SUBSCR    
             1458  LOAD_STR                 '\n'
             1460  COMPARE_OP               ==
             1462  POP_JUMP_IF_FALSE  1546  'to 1546'

 L. 662      1466  LOAD_FAST                'lnum'
             1468  LOAD_FAST                'start'
             1470  BUILD_TUPLE_2         2 
             1472  STORE_FAST               'strstart'

 L. 669      1474  LOAD_GLOBAL              _compile
             1476  LOAD_GLOBAL              endpats
             1478  LOAD_ATTR                get
             1480  LOAD_FAST                'initial'
             1482  CALL_FUNCTION_1       1  '1 positional argument'
             1484  JUMP_IF_TRUE_OR_POP  1516  'to 1516'

 L. 670      1488  LOAD_GLOBAL              endpats
             1490  LOAD_ATTR                get
             1492  LOAD_FAST                'token'
             1494  LOAD_CONST               1
             1496  BINARY_SUBSCR    
             1498  CALL_FUNCTION_1       1  '1 positional argument'
             1500  JUMP_IF_TRUE_OR_POP  1516  'to 1516'

 L. 671      1504  LOAD_GLOBAL              endpats
             1506  LOAD_ATTR                get
             1508  LOAD_FAST                'token'
             1510  LOAD_CONST               2
             1512  BINARY_SUBSCR    
             1514  CALL_FUNCTION_1       1  '1 positional argument'
           1516_0  COME_FROM          1500  '1500'
           1516_1  COME_FROM          1484  '1484'
             1516  CALL_FUNCTION_1       1  '1 positional argument'
             1518  STORE_FAST               'endprog'

 L. 672      1520  LOAD_FAST                'line'
             1522  LOAD_FAST                'start'
             1524  LOAD_CONST               None
             1526  BUILD_SLICE_2         2 
             1528  BINARY_SUBSCR    
             1530  LOAD_CONST               1
             1532  ROT_TWO          
             1534  STORE_FAST               'contstr'
             1536  STORE_FAST               'needcont'

 L. 673      1538  LOAD_FAST                'line'
             1540  STORE_FAST               'contline'

 L. 674      1542  BREAK_LOOP       
             1544  JUMP_FORWARD       1564  'to 1564'
             1546  ELSE                     '1564'

 L. 676      1546  LOAD_GLOBAL              TokenInfo
             1548  LOAD_GLOBAL              STRING
             1550  LOAD_FAST                'token'
             1552  LOAD_FAST                'spos'
             1554  LOAD_FAST                'epos'
             1556  LOAD_FAST                'line'
             1558  CALL_FUNCTION_5       5  '5 positional arguments'
             1560  YIELD_VALUE      
             1562  POP_TOP          
           1564_0  COME_FROM          1544  '1544'
             1564  JUMP_ABSOLUTE      1910  'to 1910'
             1568  ELSE                     '1866'

 L. 678      1568  LOAD_FAST                'initial'
             1570  LOAD_ATTR                isidentifier
             1572  CALL_FUNCTION_0       0  '0 positional arguments'
             1574  POP_JUMP_IF_FALSE  1778  'to 1778'

 L. 679      1578  LOAD_FAST                'token'
             1580  LOAD_CONST               ('async', 'await')
             1582  COMPARE_OP               in
             1584  POP_JUMP_IF_FALSE  1630  'to 1630'

 L. 680      1588  LOAD_FAST                'async_def'
             1590  POP_JUMP_IF_FALSE  1630  'to 1630'

 L. 681      1594  LOAD_GLOBAL              TokenInfo

 L. 682      1596  LOAD_FAST                'token'
             1598  LOAD_STR                 'async'
             1600  COMPARE_OP               ==
             1602  POP_JUMP_IF_FALSE  1610  'to 1610'
             1606  LOAD_GLOBAL              ASYNC
             1608  JUMP_FORWARD       1612  'to 1612'
             1610  ELSE                     '1612'
             1610  LOAD_GLOBAL              AWAIT
           1612_0  COME_FROM          1608  '1608'

 L. 683      1612  LOAD_FAST                'token'
             1614  LOAD_FAST                'spos'
             1616  LOAD_FAST                'epos'
             1618  LOAD_FAST                'line'
             1620  CALL_FUNCTION_5       5  '5 positional arguments'
             1622  YIELD_VALUE      
             1624  POP_TOP          

 L. 684      1626  CONTINUE            968  'to 968'
           1630_0  COME_FROM          1584  '1584'

 L. 686      1630  LOAD_GLOBAL              TokenInfo
             1632  LOAD_GLOBAL              NAME
             1634  LOAD_FAST                'token'
             1636  LOAD_FAST                'spos'
             1638  LOAD_FAST                'epos'
             1640  LOAD_FAST                'line'
             1642  CALL_FUNCTION_5       5  '5 positional arguments'
             1644  STORE_FAST               'tok'

 L. 687      1646  LOAD_FAST                'token'
             1648  LOAD_STR                 'async'
             1650  COMPARE_OP               ==
             1652  POP_JUMP_IF_FALSE  1672  'to 1672'
             1656  LOAD_FAST                'stashed'
             1658  UNARY_NOT        
             1660  POP_JUMP_IF_FALSE  1672  'to 1672'

 L. 688      1664  LOAD_FAST                'tok'
             1666  STORE_FAST               'stashed'

 L. 689      1668  CONTINUE            968  'to 968'
           1672_0  COME_FROM          1652  '1652'

 L. 691      1672  LOAD_FAST                'token'
             1674  LOAD_STR                 'def'
             1676  COMPARE_OP               ==
             1678  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 692      1682  LOAD_FAST                'stashed'
             1684  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 693      1688  LOAD_FAST                'stashed'
             1690  LOAD_ATTR                type
             1692  LOAD_GLOBAL              NAME
             1694  COMPARE_OP               ==
             1696  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 694      1700  LOAD_FAST                'stashed'
             1702  LOAD_ATTR                string
             1704  LOAD_STR                 'async'
             1706  COMPARE_OP               ==
             1708  POP_JUMP_IF_FALSE  1754  'to 1754'

 L. 696      1712  LOAD_CONST               True
             1714  STORE_FAST               'async_def'

 L. 697      1716  LOAD_FAST                'indents'
             1718  LOAD_CONST               -1
             1720  BINARY_SUBSCR    
             1722  STORE_FAST               'async_def_indent'

 L. 699      1724  LOAD_GLOBAL              TokenInfo
             1726  LOAD_GLOBAL              ASYNC
             1728  LOAD_FAST                'stashed'
             1730  LOAD_ATTR                string

 L. 700      1732  LOAD_FAST                'stashed'
             1734  LOAD_ATTR                start
             1736  LOAD_FAST                'stashed'
             1738  LOAD_ATTR                end

 L. 701      1740  LOAD_FAST                'stashed'
             1742  LOAD_ATTR                line
             1744  CALL_FUNCTION_5       5  '5 positional arguments'
             1746  YIELD_VALUE      
             1748  POP_TOP          

 L. 702      1750  LOAD_CONST               None
             1752  STORE_FAST               'stashed'
           1754_0  COME_FROM          1708  '1708'
           1754_1  COME_FROM          1696  '1696'
           1754_2  COME_FROM          1684  '1684'
           1754_3  COME_FROM          1678  '1678'

 L. 704      1754  LOAD_FAST                'stashed'
             1756  POP_JUMP_IF_FALSE  1770  'to 1770'

 L. 705      1760  LOAD_FAST                'stashed'
             1762  YIELD_VALUE      
             1764  POP_TOP          

 L. 706      1766  LOAD_CONST               None
             1768  STORE_FAST               'stashed'
           1770_0  COME_FROM          1756  '1756'

 L. 708      1770  LOAD_FAST                'tok'
             1772  YIELD_VALUE      
             1774  POP_TOP          
             1776  JUMP_FORWARD       1866  'to 1866'
             1778  ELSE                     '1866'

 L. 709      1778  LOAD_FAST                'initial'
             1780  LOAD_STR                 '\\'
             1782  COMPARE_OP               ==
             1784  POP_JUMP_IF_FALSE  1794  'to 1794'

 L. 710      1788  LOAD_CONST               1
             1790  STORE_FAST               'continued'
             1792  JUMP_FORWARD       1866  'to 1866'
             1794  ELSE                     '1866'

 L. 712      1794  LOAD_FAST                'initial'
             1796  LOAD_STR                 '([{'
             1798  COMPARE_OP               in
             1800  POP_JUMP_IF_FALSE  1814  'to 1814'

 L. 713      1804  LOAD_FAST                'parenlev'
             1806  LOAD_CONST               1
             1808  INPLACE_ADD      
             1810  STORE_FAST               'parenlev'
             1812  JUMP_FORWARD       1832  'to 1832'
             1814  ELSE                     '1832'

 L. 714      1814  LOAD_FAST                'initial'
             1816  LOAD_STR                 ')]}'
             1818  COMPARE_OP               in
             1820  POP_JUMP_IF_FALSE  1832  'to 1832'

 L. 715      1824  LOAD_FAST                'parenlev'
             1826  LOAD_CONST               1
             1828  INPLACE_SUBTRACT 
             1830  STORE_FAST               'parenlev'
           1832_0  COME_FROM          1820  '1820'
           1832_1  COME_FROM          1812  '1812'

 L. 716      1832  LOAD_FAST                'stashed'
             1834  POP_JUMP_IF_FALSE  1848  'to 1848'

 L. 717      1838  LOAD_FAST                'stashed'
             1840  YIELD_VALUE      
             1842  POP_TOP          

 L. 718      1844  LOAD_CONST               None
             1846  STORE_FAST               'stashed'
           1848_0  COME_FROM          1834  '1834'

 L. 719      1848  LOAD_GLOBAL              TokenInfo
             1850  LOAD_GLOBAL              OP
             1852  LOAD_FAST                'token'
             1854  LOAD_FAST                'spos'
             1856  LOAD_FAST                'epos'
             1858  LOAD_FAST                'line'
             1860  CALL_FUNCTION_5       5  '5 positional arguments'
             1862  YIELD_VALUE      
             1864  POP_TOP          
           1866_0  COME_FROM          1792  '1792'
           1866_1  COME_FROM          1776  '1776'
           1866_2  COME_FROM          1212  '1212'
             1866  JUMP_FORWARD       1910  'to 1910'
             1868  ELSE                     '1910'

 L. 721      1868  LOAD_GLOBAL              TokenInfo
             1870  LOAD_GLOBAL              ERRORTOKEN
             1872  LOAD_FAST                'line'
             1874  LOAD_FAST                'pos'
             1876  BINARY_SUBSCR    

 L. 722      1878  LOAD_FAST                'lnum'
             1880  LOAD_FAST                'pos'
             1882  BUILD_TUPLE_2         2 
             1884  LOAD_FAST                'lnum'
             1886  LOAD_FAST                'pos'
             1888  LOAD_CONST               1
             1890  BINARY_ADD       
             1892  BUILD_TUPLE_2         2 
             1894  LOAD_FAST                'line'
             1896  CALL_FUNCTION_5       5  '5 positional arguments'
             1898  YIELD_VALUE      
             1900  POP_TOP          

 L. 723      1902  LOAD_FAST                'pos'
             1904  LOAD_CONST               1
             1906  INPLACE_ADD      
             1908  STORE_FAST               'pos'
           1910_0  COME_FROM          1866  '1866'
             1910  JUMP_BACK           968  'to 968'
           1914_0  COME_FROM           974  '974'
             1914  POP_BLOCK        
           1916_0  COME_FROM_LOOP      964  '964'
             1916  JUMP_BACK           100  'to 100'
             1918  POP_BLOCK        
           1920_0  COME_FROM_LOOP       96  '96'

 L. 725      1920  LOAD_FAST                'stashed'
             1922  POP_JUMP_IF_FALSE  1936  'to 1936'

 L. 726      1926  LOAD_FAST                'stashed'
             1928  YIELD_VALUE      
             1930  POP_TOP          

 L. 727      1932  LOAD_CONST               None
             1934  STORE_FAST               'stashed'
           1936_0  COME_FROM          1922  '1922'

 L. 730      1936  LOAD_FAST                'last_line'
             1938  POP_JUMP_IF_FALSE  2002  'to 2002'
             1942  LOAD_FAST                'last_line'
             1944  LOAD_CONST               -1
             1946  BINARY_SUBSCR    
             1948  LOAD_STR                 '\r\n'
             1950  COMPARE_OP               not-in
             1952  POP_JUMP_IF_FALSE  2002  'to 2002'

 L. 731      1956  LOAD_GLOBAL              TokenInfo
             1958  LOAD_GLOBAL              NEWLINE
             1960  LOAD_STR                 ''
             1962  LOAD_FAST                'lnum'
             1964  LOAD_CONST               1
             1966  BINARY_SUBTRACT  
             1968  LOAD_GLOBAL              len
             1970  LOAD_FAST                'last_line'
             1972  CALL_FUNCTION_1       1  '1 positional argument'
             1974  BUILD_TUPLE_2         2 
             1976  LOAD_FAST                'lnum'
             1978  LOAD_CONST               1
             1980  BINARY_SUBTRACT  
             1982  LOAD_GLOBAL              len
             1984  LOAD_FAST                'last_line'
             1986  CALL_FUNCTION_1       1  '1 positional argument'
             1988  LOAD_CONST               1
             1990  BINARY_ADD       
             1992  BUILD_TUPLE_2         2 
             1994  LOAD_STR                 ''
             1996  CALL_FUNCTION_5       5  '5 positional arguments'
             1998  YIELD_VALUE      
             2000  POP_TOP          
           2002_0  COME_FROM          1952  '1952'
           2002_1  COME_FROM          1938  '1938'

 L. 732      2002  SETUP_LOOP         2052  'to 2052'
             2004  LOAD_FAST                'indents'
             2006  LOAD_CONST               1
             2008  LOAD_CONST               None
             2010  BUILD_SLICE_2         2 
             2012  BINARY_SUBSCR    
             2014  GET_ITER         
             2016  FOR_ITER           2050  'to 2050'
             2018  STORE_FAST               'indent'

 L. 733      2020  LOAD_GLOBAL              TokenInfo
             2022  LOAD_GLOBAL              DEDENT
             2024  LOAD_STR                 ''
             2026  LOAD_FAST                'lnum'
             2028  LOAD_CONST               0
             2030  BUILD_TUPLE_2         2 
             2032  LOAD_FAST                'lnum'
             2034  LOAD_CONST               0
             2036  BUILD_TUPLE_2         2 
             2038  LOAD_STR                 ''
             2040  CALL_FUNCTION_5       5  '5 positional arguments'
             2042  YIELD_VALUE      
             2044  POP_TOP          
             2046  JUMP_BACK          2016  'to 2016'
             2050  POP_BLOCK        
           2052_0  COME_FROM_LOOP     2002  '2002'

 L. 734      2052  LOAD_GLOBAL              TokenInfo
             2054  LOAD_GLOBAL              ENDMARKER
             2056  LOAD_STR                 ''
             2058  LOAD_FAST                'lnum'
             2060  LOAD_CONST               0
             2062  BUILD_TUPLE_2         2 
             2064  LOAD_FAST                'lnum'
             2066  LOAD_CONST               0
             2068  BUILD_TUPLE_2         2 
             2070  LOAD_STR                 ''
             2072  CALL_FUNCTION_5       5  '5 positional arguments'
             2074  YIELD_VALUE      
             2076  POP_TOP          

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 1220


def generate_tokens(readline):
    return _tokenize(readline, None)


def main():
    import argparse

    def perror(message):
        print(message, file=(sys.stderr))

    def error(message, filename=None, location=None):
        if location:
            args = (
             filename,) + location + (message,)
            perror('%s:%d:%d: error: %s' % args)
        else:
            if filename:
                perror('%s: error: %s' % (filename, message))
            else:
                perror('error: %s' % message)
        sys.exit(1)

    parser = argparse.ArgumentParser(prog='python -m tokenize')
    parser.add_argument(dest='filename', nargs='?', metavar='filename.py',
      help='the file to tokenize; defaults to stdin')
    parser.add_argument('-e', '--exact', dest='exact', action='store_true', help='display token names using the exact type')
    args = parser.parse_args()
    try:
        if args.filename:
            filename = args.filename
            with _builtin_open(filename, 'rb') as (f):
                tokens = list(tokenize(f.readline))
        else:
            filename = '<stdin>'
            tokens = _tokenize(sys.stdin.readline, None)
        for token in tokens:
            token_type = token.type
            if args.exact:
                token_type = token.exact_type
            token_range = '%d,%d-%d,%d:' % (token.start + token.end)
            print('%-20s%-15s%-15r' % (
             token_range, tok_name[token_type], token.string))

    except IndentationError as err:
        line, column = err.args[1][1:3]
        error(err.args[0], filename, (line, column))
    except TokenError as err:
        line, column = err.args[1]
        error(err.args[0], filename, (line, column))
    except SyntaxError as err:
        error(err, filename)
    except OSError as err:
        error(err)
    except KeyboardInterrupt:
        print('interrupted\n')
    except Exception as err:
        perror('unexpected error: %s' % err)
        raise


if __name__ == '__main__':
    main()