# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: xml\sax\expatreader.py
"""
SAX driver for the pyexpat C module.  This driver works with
pyexpat.__version__ == '2.22'.
"""
version = '0.20'
from xml.sax._exceptions import *
from xml.sax.handler import feature_validation, feature_namespaces
from xml.sax.handler import feature_namespace_prefixes
from xml.sax.handler import feature_external_ges, feature_external_pes
from xml.sax.handler import feature_string_interning
from xml.sax.handler import property_xml_string, property_interning_dict
import sys
if sys.platform[:4] == 'java':
    raise SAXReaderNotAvailable('expat not available in Java', None)
del sys
try:
    from xml.parsers import expat
except ImportError:
    raise SAXReaderNotAvailable('expat not supported', None)
else:
    if not hasattr(expat, 'ParserCreate'):
        raise SAXReaderNotAvailable('expat not supported', None)
    from xml.sax import xmlreader, saxutils, handler
    AttributesImpl = xmlreader.AttributesImpl
    AttributesNSImpl = xmlreader.AttributesNSImpl
    try:
        import _weakref
    except ImportError:

        def _mkproxy(o):
            return o


    else:
        import weakref
        _mkproxy = weakref.proxy
        del weakref
        del _weakref

    class _ClosedParser:
        pass


    class ExpatLocator(xmlreader.Locator):
        __doc__ = 'Locator for use with the ExpatParser class.\n\n    This uses a weak reference to the parser object to avoid creating\n    a circular reference between the parser and the content handler.\n    '

        def __init__(self, parser):
            self._ref = _mkproxy(parser)

        def getColumnNumber(self):
            parser = self._ref
            if parser._parser is None:
                return
            else:
                return parser._parser.ErrorColumnNumber

        def getLineNumber(self):
            parser = self._ref
            if parser._parser is None:
                return 1
            else:
                return parser._parser.ErrorLineNumber

        def getPublicId(self):
            parser = self._ref
            if parser is None:
                return
            else:
                return parser._source.getPublicId()

        def getSystemId(self):
            parser = self._ref
            if parser is None:
                return
            else:
                return parser._source.getSystemId()


    class ExpatParser(xmlreader.IncrementalParser, xmlreader.Locator):
        __doc__ = 'SAX driver for the pyexpat C module.'

        def __init__(self, namespaceHandling=0, bufsize=65516):
            xmlreader.IncrementalParser.__init__(self, bufsize)
            self._source = xmlreader.InputSource()
            self._parser = None
            self._namespaces = namespaceHandling
            self._lex_handler_prop = None
            self._parsing = 0
            self._entity_stack = []
            self._external_ges = 0
            self._interning = None

        def parse(self, source):
            """Parse an XML document from a URL or an InputSource."""
            source = saxutils.prepare_input_source(source)
            self._source = source
            try:
                self.reset()
                self._cont_handler.setDocumentLocator(ExpatLocator(self))
                xmlreader.IncrementalParser.parse(self, source)
            except:
                self._close_source()
                raise

        def prepareParser(self, source):
            if source.getSystemId() is not None:
                self._parser.SetBase(source.getSystemId())

        def setContentHandler(self, handler):
            xmlreader.IncrementalParser.setContentHandler(self, handler)
            if self._parsing:
                self._reset_cont_handler()

        def getFeature(self, name):
            if name == feature_namespaces:
                return self._namespaces
            else:
                if name == feature_string_interning:
                    return self._interning is not None
                if name in (feature_validation, feature_external_pes,
                 feature_namespace_prefixes):
                    return 0
                if name == feature_external_ges:
                    return self._external_ges
            raise SAXNotRecognizedException("Feature '%s' not recognized" % name)

        def setFeature--- This code section failed: ---

 L. 143         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _parsing
                4  POP_JUMP_IF_FALSE    14  'to 14'

 L. 144         6  LOAD_GLOBAL              SAXNotSupportedException
                8  LOAD_STR                 'Cannot set features while parsing'
               10  CALL_FUNCTION_1       1  '1 positional argument'
               12  RAISE_VARARGS_1       1  'exception'
             14_0  COME_FROM             4  '4'

 L. 146        14  LOAD_FAST                'name'
               16  LOAD_GLOBAL              feature_namespaces
               18  COMPARE_OP               ==
               20  POP_JUMP_IF_FALSE    30  'to 30'

 L. 147        22  LOAD_FAST                'state'
               24  LOAD_FAST                'self'
               26  STORE_ATTR               _namespaces
               28  JUMP_FORWARD        162  'to 162'
               30  ELSE                     '162'

 L. 148        30  LOAD_FAST                'name'
               32  LOAD_GLOBAL              feature_external_ges
               34  COMPARE_OP               ==
               36  POP_JUMP_IF_FALSE    46  'to 46'

 L. 149        38  LOAD_FAST                'state'
               40  LOAD_FAST                'self'
               42  STORE_ATTR               _external_ges
               44  JUMP_FORWARD        162  'to 162'
               46  ELSE                     '162'

 L. 150        46  LOAD_FAST                'name'
               48  LOAD_GLOBAL              feature_string_interning
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    84  'to 84'

 L. 151        54  LOAD_FAST                'state'
               56  POP_JUMP_IF_FALSE    76  'to 76'

 L. 152        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _interning
               62  LOAD_CONST               None
               64  COMPARE_OP               is
               66  POP_JUMP_IF_FALSE    82  'to 82'

 L. 153        68  BUILD_MAP_0           0 
               70  LOAD_FAST                'self'
               72  STORE_ATTR               _interning
               74  JUMP_ABSOLUTE       162  'to 162'
               76  ELSE                     '82'

 L. 155        76  LOAD_CONST               None
               78  LOAD_FAST                'self'
               80  STORE_ATTR               _interning
             82_0  COME_FROM            66  '66'
               82  JUMP_FORWARD        162  'to 162'
               84  ELSE                     '162'

 L. 156        84  LOAD_FAST                'name'
               86  LOAD_GLOBAL              feature_validation
               88  COMPARE_OP               ==
               90  POP_JUMP_IF_FALSE   106  'to 106'

 L. 157        92  LOAD_FAST                'state'
               94  POP_JUMP_IF_FALSE   162  'to 162'

 L. 158        96  LOAD_GLOBAL              SAXNotSupportedException

 L. 159        98  LOAD_STR                 'expat does not support validation'
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  RAISE_VARARGS_1       1  'exception'
              104  JUMP_FORWARD        162  'to 162'
              106  ELSE                     '162'

 L. 160       106  LOAD_FAST                'name'
              108  LOAD_GLOBAL              feature_external_pes
              110  COMPARE_OP               ==
              112  POP_JUMP_IF_FALSE   128  'to 128'

 L. 161       114  LOAD_FAST                'state'
              116  POP_JUMP_IF_FALSE   162  'to 162'

 L. 162       118  LOAD_GLOBAL              SAXNotSupportedException

 L. 163       120  LOAD_STR                 'expat does not read external parameter entities'
              122  CALL_FUNCTION_1       1  '1 positional argument'
              124  RAISE_VARARGS_1       1  'exception'
              126  JUMP_FORWARD        162  'to 162'
              128  ELSE                     '162'

 L. 164       128  LOAD_FAST                'name'
              130  LOAD_GLOBAL              feature_namespace_prefixes
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   150  'to 150'

 L. 165       136  LOAD_FAST                'state'
              138  POP_JUMP_IF_FALSE   162  'to 162'

 L. 166       140  LOAD_GLOBAL              SAXNotSupportedException

 L. 167       142  LOAD_STR                 'expat does not report namespace prefixes'
              144  CALL_FUNCTION_1       1  '1 positional argument'
              146  RAISE_VARARGS_1       1  'exception'
              148  JUMP_FORWARD        162  'to 162'
              150  ELSE                     '162'

 L. 169       150  LOAD_GLOBAL              SAXNotRecognizedException

 L. 170       152  LOAD_STR                 "Feature '%s' not recognized"
              154  LOAD_FAST                'name'
              156  BINARY_MODULO    
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  RAISE_VARARGS_1       1  'exception'
            162_0  COME_FROM           148  '148'
            162_1  COME_FROM           138  '138'
            162_2  COME_FROM           126  '126'
            162_3  COME_FROM           116  '116'
            162_4  COME_FROM           104  '104'
            162_5  COME_FROM            94  '94'
            162_6  COME_FROM            82  '82'
            162_7  COME_FROM            44  '44'
            162_8  COME_FROM            28  '28'

Parse error at or near `COME_FROM' instruction at offset 162_7

        def getProperty(self, name):
            if name == handler.property_lexical_handler:
                return self._lex_handler_prop
            else:
                if name == property_interning_dict:
                    return self._interning
                if name == property_xml_string:
                    if self._parser:
                        if hasattr(self._parser, 'GetInputContext'):
                            return self._parser.GetInputContext()
                        raise SAXNotRecognizedException('This version of expat does not support getting the XML string')
                    else:
                        raise SAXNotSupportedException('XML string cannot be returned when not parsing')
            raise SAXNotRecognizedException("Property '%s' not recognized" % name)

        def setProperty(self, name, value):
            if name == handler.property_lexical_handler:
                self._lex_handler_prop = value
                if self._parsing:
                    self._reset_lex_handler_prop()
            else:
                if name == property_interning_dict:
                    self._interning = value
                else:
                    if name == property_xml_string:
                        raise SAXNotSupportedException("Property '%s' cannot be set" % name)
                    else:
                        raise SAXNotRecognizedException("Property '%s' not recognized" % name)

        def feed(self, data, isFinal=0):
            if not self._parsing:
                self.reset()
                self._parsing = 1
                self._cont_handler.startDocument()
            try:
                self._parser.Parse(data, isFinal)
            except expat.error as e:
                exc = SAXParseException(expat.ErrorString(e.code), e, self)
                self._err_handler.fatalError(exc)

        def _close_source(self):
            source = self._source
            try:
                file = source.getCharacterStream()
                if file is not None:
                    file.close()
            finally:
                file = source.getByteStream()
                if file is not None:
                    file.close()

        def close(self):
            if self._entity_stack or self._parser is None or isinstance(self._parser, _ClosedParser):
                return
            try:
                self.feed('', isFinal=1)
                self._cont_handler.endDocument()
                self._parsing = 0
                self._parser = None
            finally:
                self._parsing = 0
                if self._parser is not None:
                    parser = _ClosedParser()
                    parser.ErrorColumnNumber = self._parser.ErrorColumnNumber
                    parser.ErrorLineNumber = self._parser.ErrorLineNumber
                    self._parser = parser
                self._close_source()

        def _reset_cont_handler(self):
            self._parser.ProcessingInstructionHandler = self._cont_handler.processingInstruction
            self._parser.CharacterDataHandler = self._cont_handler.characters

        def _reset_lex_handler_prop(self):
            lex = self._lex_handler_prop
            parser = self._parser
            if lex is None:
                parser.CommentHandler = None
                parser.StartCdataSectionHandler = None
                parser.EndCdataSectionHandler = None
                parser.StartDoctypeDeclHandler = None
                parser.EndDoctypeDeclHandler = None
            else:
                parser.CommentHandler = lex.comment
                parser.StartCdataSectionHandler = lex.startCDATA
                parser.EndCdataSectionHandler = lex.endCDATA
                parser.StartDoctypeDeclHandler = self.start_doctype_decl
                parser.EndDoctypeDeclHandler = lex.endDTD

        def reset(self):
            if self._namespaces:
                self._parser = expat.ParserCreate((self._source.getEncoding()), ' ', intern=(self._interning))
                self._parser.namespace_prefixes = 1
                self._parser.StartElementHandler = self.start_element_ns
                self._parser.EndElementHandler = self.end_element_ns
            else:
                self._parser = expat.ParserCreate((self._source.getEncoding()), intern=(self._interning))
                self._parser.StartElementHandler = self.start_element
                self._parser.EndElementHandler = self.end_element
            self._reset_cont_handler()
            self._parser.UnparsedEntityDeclHandler = self.unparsed_entity_decl
            self._parser.NotationDeclHandler = self.notation_decl
            self._parser.StartNamespaceDeclHandler = self.start_namespace_decl
            self._parser.EndNamespaceDeclHandler = self.end_namespace_decl
            self._decl_handler_prop = None
            if self._lex_handler_prop:
                self._reset_lex_handler_prop()
            self._parser.ExternalEntityRefHandler = self.external_entity_ref
            try:
                self._parser.SkippedEntityHandler = self.skipped_entity_handler
            except AttributeError:
                pass

            self._parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE)
            self._parsing = 0
            self._entity_stack = []

        def getColumnNumber(self):
            if self._parser is None:
                return
            else:
                return self._parser.ErrorColumnNumber

        def getLineNumber(self):
            if self._parser is None:
                return 1
            else:
                return self._parser.ErrorLineNumber

        def getPublicId(self):
            return self._source.getPublicId()

        def getSystemId(self):
            return self._source.getSystemId()

        def start_element(self, name, attrs):
            self._cont_handler.startElement(name, AttributesImpl(attrs))

        def end_element(self, name):
            self._cont_handler.endElement(name)

        def start_element_ns(self, name, attrs):
            pair = name.split()
            if len(pair) == 1:
                pair = (None, name)
            else:
                if len(pair) == 3:
                    pair = (
                     pair[0], pair[1])
                else:
                    pair = tuple(pair)
            newattrs = {}
            qnames = {}
            for aname, value in attrs.items():
                parts = aname.split()
                length = len(parts)
                if length == 1:
                    qname = aname
                    apair = (None, aname)
                else:
                    if length == 3:
                        qname = '%s:%s' % (parts[2], parts[1])
                        apair = (parts[0], parts[1])
                    else:
                        qname = parts[1]
                        apair = tuple(parts)
                newattrs[apair] = value
                qnames[apair] = qname

            self._cont_handler.startElementNS(pair, None, AttributesNSImpl(newattrs, qnames))

        def end_element_ns(self, name):
            pair = name.split()
            if len(pair) == 1:
                pair = (
                 None, name)
            else:
                if len(pair) == 3:
                    pair = (
                     pair[0], pair[1])
                else:
                    pair = tuple(pair)
            self._cont_handler.endElementNS(pair, None)

        def processing_instruction(self, target, data):
            self._cont_handler.processingInstruction(target, data)

        def character_data(self, data):
            self._cont_handler.characters(data)

        def start_namespace_decl(self, prefix, uri):
            self._cont_handler.startPrefixMapping(prefix, uri)

        def end_namespace_decl(self, prefix):
            self._cont_handler.endPrefixMapping(prefix)

        def start_doctype_decl(self, name, sysid, pubid, has_internal_subset):
            self._lex_handler_prop.startDTD(name, pubid, sysid)

        def unparsed_entity_decl(self, name, base, sysid, pubid, notation_name):
            self._dtd_handler.unparsedEntityDecl(name, pubid, sysid, notation_name)

        def notation_decl(self, name, base, sysid, pubid):
            self._dtd_handler.notationDecl(name, pubid, sysid)

        def external_entity_ref(self, context, base, sysid, pubid):
            if not self._external_ges:
                return 1
            else:
                source = self._ent_handler.resolveEntity(pubid, sysid)
                source = saxutils.prepare_input_source(source, self._source.getSystemId() or '')
                self._entity_stack.append((self._parser, self._source))
                self._parser = self._parser.ExternalEntityParserCreate(context)
                self._source = source
                try:
                    xmlreader.IncrementalParser.parse(self, source)
                except:
                    return 0
                else:
                    self._parser, self._source = self._entity_stack[(-1)]
                    del self._entity_stack[-1]
                return 1

        def skipped_entity_handler(self, name, is_pe):
            if is_pe:
                name = '%' + name
            self._cont_handler.skippedEntity(name)


    def create_parser(*args, **kwargs):
        return ExpatParser(*args, **kwargs)


    if __name__ == '__main__':
        import xml.sax.saxutils
        p = create_parser()
        p.setContentHandler(xml.sax.saxutils.XMLGenerator())
        p.setErrorHandler(xml.sax.ErrorHandler())
        p.parse('http://www.ibiblio.org/xml/examples/shakespeare/hamlet.xml')