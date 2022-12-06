from __future__ import unicode_literals
import  re
import xml.etree.ElementTree
from ..extractor.common import  InfoExtractor
from ..extractor.bbc import BBCCoUkIE, BBCIE, BBCCoUkArticleIE
from ..utils import ExtractorError, float_or_none, int_or_none, parse_duration, parse_iso8601, remove_end, unescapeHTML
from ..compat import compat_HTTPError, compat_urllib_parse_urlparse
class BBCCoUkIE(InfoExtractor):

    IE_NAME = 'bbc.co.uk'
    IE_DESC = 'BBC iPlayer'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/(?:(?:programmes/(?!articles/)|iplayer(?:/[^/]+)?/(?:episode/|playlist/))|music/clips[/#])(?P<id>[\\da-z]{8})'
    _MEDIASELECTOR_URLS = [
        'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/%s',
        'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/%s'
    ]
    _MEDIASELECTION_NS = 'http://bbc.co.uk/2008/mp/mediaselection'
    _EMP_PLAYLIST_NS = 'http://bbc.co.uk/2008/emp/playlist'
    _USP_RE = '/([^/]+?)\\.ism(?:\\.hlsv2\\.ism)?/[^/]+\\.m3u8'
    _NAMESPACES = [_MEDIASELECTION_NS,
                   _EMP_PLAYLIST_NS]
    class MediaSelectionError(Exception):
        def __init__(self,id):
            self.id = id
    def _extract_asx_playlist(self,connection,programme_id):
        asx = self._download_xml(connection.get('href'), programme_id, 'Downloading ASX playlist')
        return [ref.get('href') for ref in asx.findall('./Entry/ref')]




    #  61          72 LOAD_CONST              13 (<code object _extract_connection at 0x000002AA88847D20, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 61>)
    #              74 LOAD_CONST              14 ('BBCCoUkIE._extract_connection')
    #              76 MAKE_FUNCTION            0
    #              78 STORE_NAME              14 (_extract_connection)
    def _extract_connection(self,connection, programme_id):
        # 62           0 BUILD_LIST               0
        #               2 STORE_FAST               3 (formats)
        formats = []
        #  63           4 LOAD_FAST                1 (connection)
        #               6 LOAD_METHOD              0 (get)
        #               8 LOAD_CONST               1 ('kind')
        #              10 CALL_METHOD              1
        #              12 STORE_FAST               4 (kind)
        kind = connection.get('kind')
        # 64          14 LOAD_FAST                1 (connection)
        #              16 LOAD_METHOD              0 (get)
        #              18 LOAD_CONST               2 ('protocol')
        #              20 CALL_METHOD              1
        #              22 STORE_FAST               5 (protocol)
        protocol = connection.get('protocol')
        # 65          24 LOAD_FAST                1 (connection)
        #              26 LOAD_METHOD              0 (get)
        #              28 LOAD_CONST               3 ('supplier')
        #              30 CALL_METHOD              1
        #              32 STORE_FAST               6 (supplier)
        supplier = connection.get('supplier')
        #  66          34 LOAD_FAST                5 (protocol)
        #              36 LOAD_CONST               4 ('http')
        #              38 COMPARE_OP               2 (==)
        #              40 EXTENDED_ARG             1
        #              42 POP_JUMP_IF_FALSE      374
        if protocol == 'http':
            # 67          44 LOAD_FAST                1 (connection)
            #              46 LOAD_METHOD              0 (get)
            #              48 LOAD_CONST               5 ('href')
            #              50 CALL_METHOD              1
            #              52 STORE_FAST               7 (href)
            href = connection.get('href')
            #  68          54 LOAD_FAST                1 (connection)
            #              56 LOAD_METHOD              0 (get)
            #              58 LOAD_CONST               6 ('transferFormat')
            #              60 CALL_METHOD              1
            #              62 STORE_FAST               8 (transfer_format)
            transfer_format = connection.get("transferFormat")
            # 70          64 LOAD_FAST                6 (supplier)
            #              66 LOAD_CONST               7 ('asx')
            #              68 COMPARE_OP               2 (==)
            #              70 POP_JUMP_IF_FALSE      128
            if supplier == 'asx':
                #  71          72 SETUP_LOOP              52 (to 126)
                #              74 LOAD_GLOBAL              1 (enumerate)
                #              76 LOAD_FAST                0 (self)
                #              78 LOAD_METHOD              2 (_extract_asx_playlist)
                #              80 LOAD_FAST                1 (connection)
                #              82 LOAD_FAST                2 (programme_id)
                #              84 CALL_METHOD              2
                #              86 CALL_FUNCTION            1
                #              88 GET_ITER
                #         >>   90 FOR_ITER                32 (to 124)
                #              92 UNPACK_SEQUENCE          2
                #              94 STORE_FAST               9 (i)
                #              96 STORE_FAST              10 (ref)
                for i,ref in enumerate(self._extract_asx_playlist(connection,programme_id)):
                    #  72          98 LOAD_FAST                3 (formats)
                    #             100 LOAD_METHOD              3 (append)
                    #
                    #  73         102 LOAD_FAST               10 (ref)
                    formats.append(ref)
                    #  74         104 LOAD_CONST               8 ('ref%s_%s')
                    #             106 LOAD_FAST                9 (i)
                    #             108 LOAD_FAST                6 (supplier)
                    #             110 BUILD_TUPLE              2
                    #             112 BINARY_MODULO
                    #             114 LOAD_CONST               9 (('url', 'format_id'))
                    #             116 BUILD_CONST_KEY_MAP      2
                    #             118 CALL_METHOD              1
                    #             120 POP_TOP
                    #             122 JUMP_ABSOLUTE           90
                    #         >>  124 POP_BLOCK
                    #         >>  126 JUMP_FORWARD           244 (to 372)
                    formats.append({"url":ref,'format_id':'ref%s_%s'% (i,supplier)})
            #  77     >>  128 LOAD_FAST                8 (transfer_format)
            #             130 LOAD_CONST              10 ('dash')
            #             132 COMPARE_OP               2 (==)
            #             134 POP_JUMP_IF_FALSE      162
            if transfer_format == 'dash':
                # 78         136 LOAD_FAST                3 (formats)
                #             138 LOAD_METHOD              4 (extend)
                #             140 LOAD_FAST                0 (self)
                #             142 LOAD_ATTR                5 (_extract_mpd_formats)
                #             144 LOAD_FAST                7 (href)
                #             146 LOAD_FAST                2 (programme_id)
                #             148 LOAD_CONST              10 ('dash')
                #             150 LOAD_CONST              11 (False)
                #             152 LOAD_CONST              12 (('mpd_id', 'fatal'))
                #             154 CALL_FUNCTION_KW         4
                #             156 CALL_METHOD              1
                #             158 POP_TOP
                #             160 JUMP_FORWARD           210 (to 372)
                formats.extend(self._extract_mpd_formats(href, programme_id, hrefpd_id='dash', fatal=False))
            #  79     >>  162 LOAD_FAST                8 (transfer_format)
            #             164 LOAD_CONST              13 ('hls')
            #             166 COMPARE_OP               2 (==)
            #             168 EXTENDED_ARG             1
            #             170 POP_JUMP_IF_FALSE      344
            if transfer_format == 'hls':
                # 80         172 LOAD_FAST                3 (formats)
                #             174 LOAD_METHOD              4 (extend)
                #             176 LOAD_FAST                0 (self)
                #             178 LOAD_ATTR                6 (_extract_m3u8_formats)
                #
                #  81         180 LOAD_FAST                7 (href)
                #             182 LOAD_FAST                2 (programme_id)
                #             184 LOAD_CONST              14 ('mp4')
                #             186 LOAD_CONST              15 ('m3u8_native')
                #
                #  82         188 LOAD_FAST                2 (programme_id)
                #             190 LOAD_CONST              11 (False)
                #             192 LOAD_CONST              16 (('ext', 'entry_protocol', 'm3u8_id', 'fatal'))
                #             194 CALL_FUNCTION_KW         6
                #             196 CALL_METHOD              1
                #             198 POP_TOP
                self._extract_m3u8_formats(href,programme_id,ext='mp4',entry_protocol='m3u8_native',m3u8_id=programme_id,fatal=False)
                #  83         200 LOAD_GLOBAL              7 (re)
                #             202 LOAD_METHOD              8 (search)
                #             204 LOAD_FAST                0 (self)
                #             206 LOAD_ATTR                9 (_USP_RE)
                #             208 LOAD_FAST                7 (href)
                #             210 CALL_METHOD              2
                #             212 EXTENDED_ARG             1
                #             214 POP_JUMP_IF_FALSE      308
                if re.search(self._USP_RE,href):
                    # 84         216 LOAD_FAST                0 (self)
                    #             218 LOAD_ATTR                6 (_extract_m3u8_formats)
                    #
                    #  85         220 LOAD_GLOBAL              7 (re)
                    #             222 LOAD_METHOD             10 (sub)
                    #             224 LOAD_FAST                0 (self)
                    #             226 LOAD_ATTR                9 (_USP_RE)
                    #             228 LOAD_CONST              17 ('/\\1.ism/\\1.m3u8')
                    #             230 LOAD_FAST                7 (href)
                    #             232 CALL_METHOD              3
                    # 86         234 LOAD_FAST                2 (programme_id)
                    #             236 LOAD_CONST              14 ('mp4')
                    #             238 LOAD_CONST              15 ('m3u8_native')
                    #
                    #  87         240 LOAD_FAST                2 (programme_id)
                    #             242 LOAD_CONST              11 (False)
                    #             244 LOAD_CONST              16 (('ext', 'entry_protocol', 'm3u8_id', 'fatal'))
                    #             246 CALL_FUNCTION_KW         6
                    #             248 STORE_FAST              11 (usp_formats)
                    usp_formats =self._extract_m3u8_formats(re.sub(self._USP_RE,'/\\1.ism/\\1.m3u8',href),programme_id,ext='mp4',entry_protocol='m3u8_native',m3u8_id=programme_id,fatal=False)
                    #  88         250 SETUP_LOOP              90 (to 342)
                    #             252 LOAD_FAST               11 (usp_formats)
                    #             254 GET_ITER
                    #         >>  256 FOR_ITER                46 (to 304)
                    #             258 STORE_FAST              12 (f)
                    for f in usp_formats:
                        #  89         260 LOAD_FAST               12 (f)
                        #             262 LOAD_METHOD              0 (get)
                        #             264 LOAD_CONST              18 ('height')
                        #             266 CALL_METHOD              1
                        #             268 EXTENDED_ARG             1
                        #             270 POP_JUMP_IF_FALSE      290
                        #             272 LOAD_FAST               12 (f)
                        #             274 LOAD_CONST              18 ('height')
                        #             276 BINARY_SUBSCR
                        #             278 LOAD_CONST              19 (720)
                        #             280 COMPARE_OP               4 (>)
                        #             282 EXTENDED_ARG             1
                        #             284 POP_JUMP_IF_FALSE      290
                        #  90         286 EXTENDED_ARG             1
                        #             288 JUMP_ABSOLUTE          256
                        if f.get('height') and f['height'] > 720:
                            continue

                        # 91     >>  290 LOAD_FAST                3 (formats)
                        #             292 LOAD_METHOD              3 (append)
                        #             294 LOAD_FAST               12 (f)
                        #             296 CALL_METHOD              1
                        #             298 POP_TOP
                        #             300 EXTENDED_ARG             1
                        #             302 JUMP_ABSOLUTE          256
                        #         >>  304 POP_BLOCK
                        #             306 JUMP_FORWARD            34 (to 342)
                        formats.append(f)
            #  92     >>  308 LOAD_FAST                8 (transfer_format)
            #             310 LOAD_CONST              20 ('hds')
            #             312 COMPARE_OP               2 (==)
            #             314 EXTENDED_ARG             1
            #             316 POP_JUMP_IF_FALSE      372
            if transfer_format == 'hds':
                #  93         318 LOAD_FAST                3 (formats)
                #             320 LOAD_METHOD              4 (extend)
                #             322 LOAD_FAST                0 (self)
                #             324 LOAD_ATTR               11 (_extract_f4m_formats)
                #
                #  94         326 LOAD_FAST                7 (href)
                #             328 LOAD_FAST                2 (programme_id)
                #             330 LOAD_FAST                2 (programme_id)
                #             332 LOAD_CONST              11 (False)
                #             334 LOAD_CONST              21 (('f4m_id', 'fatal'))
                #             336 CALL_FUNCTION_KW         4
                #             338 CALL_METHOD              1
                #             340 POP_TOP
                #         >>  342 JUMP_FORWARD            28 (to 372)
                formats.extend(self._extract_f4m_formatshref(href,programme_id,f4m_id=programme_id,fatal=False))
                # 97     >>  344 LOAD_FAST                3 (formats)
                #             346 LOAD_METHOD              3 (append)
                #
                #  98         348 LOAD_FAST                7 (href)
                #
                #  99         350 LOAD_FAST                6 (supplier)
                #             352 EXTENDED_ARG             1
                #             354 JUMP_IF_TRUE_OR_POP    364
                #             356 LOAD_FAST                4 (kind)
                #             358 EXTENDED_ARG             1
                #             360 JUMP_IF_TRUE_OR_POP    364
                #             362 LOAD_FAST                5 (protocol)
                #         >>  364 LOAD_CONST               9 (('url', 'format_id'))
                #             366 BUILD_CONST_KEY_MAP      2
                #             368 CALL_METHOD              1
                #             370 POP_TOP
                #         >>  372 JUMP_FORWARD           100 (to 474)
                formats.append({'url':href, 'format_id':supplier if supplier else kind if  kind else protocol})
        # 374 LOAD_FAST                5 (protocol)
        # 376 LOAD_CONST              22 ('rtmp')
        # 378 COMPARE_OP               2 (==)
        # 380 EXTENDED_ARG             1
        # 382 POP_JUMP_IF_FALSE      474
        if protocol == 'rtmp':
            # 102         384 LOAD_FAST                1 (connection)
            #             386 LOAD_METHOD              0 (get)
            #             388 LOAD_CONST              23 ('application')
            #             390 LOAD_CONST              24 ('ondemand')
            #             392 CALL_METHOD              2
            #             394 STORE_FAST              13 (application)
            application = connection.get("application",'ondemand')
            # 103         396 LOAD_FAST                1 (connection)
            #             398 LOAD_METHOD              0 (get)
            #             400 LOAD_CONST              25 ('authString')
            #             402 CALL_METHOD              1
            #             404 STORE_FAST              14 (auth_string)
            auth_string = connection.get('authString')
            # 104         406 LOAD_FAST                1 (connection)
            #             408 LOAD_METHOD              0 (get)
            #             410 LOAD_CONST              26 ('identifier')
            #             412 CALL_METHOD              1
            #             414 STORE_FAST              15 (identifier)
            identifier = connection.get('identifier')
            # 105         416 LOAD_FAST                1 (connection)
            #             418 LOAD_METHOD              0 (get)
            #             420 LOAD_CONST              27 ('server')
            #             422 CALL_METHOD              1
            #             424 STORE_FAST              16 (server)
            server = connection.get('server')
            # 106         426 LOAD_FAST                3 (formats)
            #             428 LOAD_METHOD              3 (append)
            #
            # 107         430 LOAD_CONST              28 ('%s://%s/%s?%s')
            #             432 LOAD_FAST                5 (protocol)
            #             434 LOAD_FAST               16 (server)
            #             436 LOAD_FAST               13 (application)
            #             438 LOAD_FAST               14 (auth_string)
            #             440 BUILD_TUPLE              4
            #             442 BINARY_MODULO
            #
            # 108         444 LOAD_FAST               15 (identifier)
            #
            # 109         446 LOAD_CONST              29 ('%s?%s')
            #             448 LOAD_FAST               13 (application)
            #             450 LOAD_FAST               14 (auth_string)
            #             452 BUILD_TUPLE              2
            #             454 BINARY_MODULO
            #
            # 110         456 LOAD_CONST              30 ('http://www.bbc.co.uk')
            #
            # 111         458 LOAD_CONST              31 ('http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf')
            #
            # 112         460 LOAD_CONST              11 (False)
            #
            # 113         462 LOAD_CONST              32 ('flv')
            #
            # 114         464 LOAD_FAST                6 (supplier)
            #             466 LOAD_CONST              33 (('url', 'play_path', 'app', 'page_url', 'player_url', 'rtmp_live', 'ext', 'format_id'))
            #             468 BUILD_CONST_KEY_MAP      8
            #             470 CALL_METHOD              1
            #             472 POP_TOP
            formats.append({'url':'%s://%s/%s?%s'%(protocol,server,application,auth_string), 'play_path':identifier, 'app':'%s?%s'%(application,auth_string), 'page_url':'http://www.bbc.co.uk', 'player_url':'http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf', 'rtmp_live':False, 'ext':'flv', 'format_id':supplier})
            # 116     >>  474 LOAD_FAST                3 (formats)
            #             476 RETURN_VALUE
            return formats
    # 118          80 LOAD_CONST              15 (<code object _extract_items at 0x000002AA88847DB0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 118>)
    #              82 LOAD_CONST              16 ('BBCCoUkIE._extract_items')
    #              84 MAKE_FUNCTION            0
    #              86 STORE_NAME              15 (_extract_items)
    def _extract_items(self,playlist):
        return playlist.findall('./{%s}item' % self._EMP_PLAYLIST_NS)
    # 121          88 LOAD_CONST              17 (<code object _findall_ns at 0x000002AA88847E40, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 121>)
    #              90 LOAD_CONST              18 ('BBCCoUkIE._findall_ns')
    #              92 MAKE_FUNCTION            0
    #              94 STORE_NAME              16 (_findall_ns)
    def _findall_ns(self,element,xpath):
        elements = []
        for ns in self._NAMESPACES:
            elements.extend(element.findall(xpath % ns))
    # 127          96 LOAD_CONST              19 (<code object _extract_medias at 0x000002AA88847ED0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 127>)
    #              98 LOAD_CONST              20 ('BBCCoUkIE._extract_medias')
    #             100 MAKE_FUNCTION            0
    #             102 STORE_NAME              17 (_extract_medias)
    def _extract_medias(self,media_selection):
        error = media_selection.find('./{%s}error' % self._MEDIASELECTION_NS)
        if error is None:
            media_selection.find('./{%s}error' % self._EMP_PLAYLIST_NS)
        if error is not None:
            raise BBCCoUkIE.MediaSelectionError(error.get('id'))
        return self._findall_ns(media_selection, './{%s}media')
    # 135         104 LOAD_CONST              21 (<code object _extract_connections at 0x000002AA88847F60, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 135>)
    #             106 LOAD_CONST              22 ('BBCCoUkIE._extract_connections')
    #             108 MAKE_FUNCTION            0
    #             110 STORE_NAME              18 (_extract_connections)
    def _extract_connections(self,media):
        return self._findall_ns(media, './{%s}connection')

    def _extract_video(self,media,programme_id):
        formats = []
        vbr = int_or_none(media.get('bitrate'))
        vcodec = media.get('encoding')
        service = media.get('service')
        width = int_or_none(media.get('width'))
        height = int_or_none(media.get('height'))
        file_size = int_or_none(media.get('media_file_size'))
        for connection in self._extract_connections(media):
            conn_formats = self._extract_connection(connection, programme_id)
            for format in conn_formats:
                format.update({'width': width,
                               'height': height,
                               'vbr': vbr,
                               'vcodec': vcodec,
                               'filesize': file_size})
                if service:
                    format['format_id'] = '%s_%s' % (service, format['format_id'])

            formats.extend(conn_formats)

        return formats

    # 161         120 LOAD_CONST              25 (<code object _extract_audio at 0x000002AA888490C0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 161>)
    #             122 LOAD_CONST              26 ('BBCCoUkIE._extract_audio')
    #             124 MAKE_FUNCTION            0
    #             126 STORE_NAME              20 (_extract_audio)
    def _extract_audio(self,media,programme_id):
        formats = []
        abr = int_or_none(media.get('bitrate'))
        acodec = media.get('encoding')
        service = media.get('service')
        for connection in self._extract_connections(media):
            conn_formats = self._extract_connection(connection, programme_id)
            for format in conn_formats:
                format.update({'format_id': '%s_%s' % (service, format['format_id']),
                               'abr': abr,
                               'acodec': acodec})

            formats.extend(conn_formats)

        return formats

    # 177         128 LOAD_CONST              27 (<code object _get_subtitles at 0x000002AA888491E0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 177>)
    #             130 LOAD_CONST              28 ('BBCCoUkIE._get_subtitles')
    #             132 MAKE_FUNCTION            0
    #             134 STORE_NAME              21 (_get_subtitles)
    def _get_subtitles(self,media,programme_id):
        subtitles = {}
        for connection in self._extract_connections(media):
            try:
                captions = self._download_xml(connection.get('href'), programme_id, 'Downloading captions')
                lang = captions.get('{http://www.w3.org/XML/1998/namespace}lang', 'en')
                subtitles[lang] = [
                    {'url': connection.get('href'),
                     'ext': 'ttml'}]
            except:
                pass

        return subtitles

    # 193         136 LOAD_CONST              29 (<code object _raise_extractor_error at 0x000002AA88849270, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 193>)
    #             138 LOAD_CONST              30 ('BBCCoUkIE._raise_extractor_error')
    #             140 MAKE_FUNCTION            0
    #             142 STORE_NAME              22 (_raise_extractor_error)
    def _raise_extractor_error(self,media_selection_error):
        raise ExtractorError(('%s returned error: %s' % (self.IE_NAME, media_selection_error.id)),
                             expected=True)
    # 198         144 LOAD_CONST              31 (<code object _getNewMediaSelection at 0x000002AA88849390, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 198>)
    #             146 LOAD_CONST              32 ('BBCCoUkIE._getNewMediaSelection')
    #             148 MAKE_FUNCTION            0
    #             150 STORE_NAME              23 (_getNewMediaSelection)
    def _getNewMediaSelection(self,vpid):
        str = 'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/pc/vpid/%s/'
        import hashlib
        key = '7dff7671d0c697fedb1d905d9a121719938b92bf'
        data = key + vpid
        import sys
        if sys.version_info >= (3, 0):
            data = data.encode('utf-8')
        hashValue = hashlib.sha1(data).hexdigest()
        return str + 'atk/%s/asn/1/' % hashValue
    # 212         152 LOAD_CONST              33 (<code object _download_media_selector at 0x000002AA888494B0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 212>)
    #             154 LOAD_CONST              34 ('BBCCoUkIE._download_media_selector')
    #             156 MAKE_FUNCTION            0
    #             158 STORE_NAME              24 (_download_media_selector)
    def _download_media_selector(self,programme_id):
        last_exception = None
        for mediaselector_url in self._MEDIASELECTOR_URLS:
            try:
                mediaselector_url = mediaselector_url % programme_id
                formats, subtitles = self._download_media_selector_url(mediaselector_url, programme_id)
                formats = [item for item in formats if re.search('rtmp://|rtmpe://', formats[0]['url']) is None]
                self._check_formats(formats, video_id='123')
                if len(formats) > 0:
                    return (
                        formats, subtitles)
                continue
            except BBCCoUkIE.MediaSelectionError as e:
                try:
                    if e.id in ('notukerror', 'geolocation'):
                        last_exception = e
                        continue
                    self._raise_extractor_error(e)
                finally:
                    e = None
                    del e

            except Exception as e:
                try:
                    continue
                finally:
                    e = None
                    del e

        self._raise_extractor_error(last_exception)
    # 233         160 LOAD_CONST              56 ((None,))
    #             162 LOAD_CONST              36 (<code object _download_media_selector_url at 0x000002AA88849540, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 233>)
    #             164 LOAD_CONST              37 ('BBCCoUkIE._download_media_selector_url')
    #             166 MAKE_FUNCTION            1
    #             168 STORE_NAME              25 (_download_media_selector_url)
    def _download_media_selector_url(self,url,programme_id):
        try:
            media_selection = self._download_xml(url, programme_id, 'Downloading media selection XML')
        except ExtractorError as ee:
            try:
                if isinstance(ee.cause, compat_HTTPError) and ee.cause.code == 403:
                    media_selection = xml.etree.ElementTree.fromstring(ee.cause.read().decode('utf-8'))
                else:
                    raise
            finally:
                ee = None
                del ee

        return self._process_media_selector(media_selection, programme_id)
    # 244         170 LOAD_CONST              38 (<code object _process_media_selector at 0x000002AA888495D0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 244>)
    #             172 LOAD_CONST              39 ('BBCCoUkIE._process_media_selector')
    #             174 MAKE_FUNCTION            0
    #             176 STORE_NAME              26 (_process_media_selector)
    def _process_media_selector(self,media_selection,programme_id):
        formats = []
        subtitles = None
        for media in self._extract_medias(media_selection):
            kind = media.get('kind')
            if kind == 'audio':
                formats.extend(self._extract_audio(media, programme_id))
            elif kind == 'video':
                formats.extend(self._extract_video(media, programme_id))
            elif kind == 'captions':
                try:
                    subtitles = self.extract_subtitles(media, programme_id)
                except:
                    pass

        return (formats, subtitles)
    # 261         178 LOAD_CONST              40 (<code object _download_playlist at 0x000002AA88849660, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 261>)
    #             180 LOAD_CONST              41 ('BBCCoUkIE._download_playlist')
    #             182 MAKE_FUNCTION            0
    #             184 STORE_NAME              27 (_download_playlist)
    def _download_playlist(self,playlist_id):
        try:
            playlist = {}
            try:
                playlist = self._download_json('http://www.bbc.co.uk/programmes/%s/playlist.json' % playlist_id,
                                               playlist_id, 'Downloading playlist JSON')
            except Exception as ex:
                try:
                    if ex.message.find('400') > -1:
                        playlist = self._download_json(
                            ('http://www.bbc.co.uk/programmes/%s/playlist.json' % playlist_id),
                            playlist_id,
                            'Downloading playlist JSON', headers={'Cookies': ''})
                finally:
                    ex = None
                    del ex

            version = playlist.get('defaultAvailableVersion')
            if version:
                smp_config = version['smpConfig']
                title = smp_config['title']
                description = smp_config['summary']
                for item in smp_config['items']:
                    kind = item['kind']
                    if kind != 'programme':
                        if kind != 'radioProgramme':
                            continue
                    programme_id = item.get('vpid')
                    duration = int_or_none(item.get('duration'))
                    self._MEDIASELECTOR_URLS.insert(0, self._getNewMediaSelection(programme_id))
                    formats, subtitles = self._download_media_selector(programme_id)

                return (programme_id, title, description, duration, formats, subtitles)
        except ExtractorError as ee:
            try:
                if not (isinstance(ee.cause, compat_HTTPError) and ee.cause.code == 404):
                    raise
            finally:
                ee = None
                del ee

        return self._process_legacy_playlist(playlist_id)

    # 297         186 LOAD_CONST              42 (<code object _process_legacy_playlist_url at 0x000002AA888496F0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 297>)
    #             188 LOAD_CONST              43 ('BBCCoUkIE._process_legacy_playlist_url')
    #             190 MAKE_FUNCTION            0
    #             192 STORE_NAME              28 (_process_legacy_playlist_url)
    def _process_legacy_playlist_url(self,url,display_id):
        playlist = self._download_legacy_playlist_url(url, display_id)
        return self._extract_from_legacy_playlist(playlist, display_id)
    # 301         194 LOAD_CONST              44 (<code object _process_legacy_playlist at 0x000002AA88849780, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 301>)
    #             196 LOAD_CONST              45 ('BBCCoUkIE._process_legacy_playlist')
    #             198 MAKE_FUNCTION            0
    #             200 STORE_NAME              29 (_process_legacy_playlist)
    def _process_legacy_playlist(self,playlist_id):
        return self._process_legacy_playlist_url('http://www.bbc.co.uk/iplayer/playlist/%s' % playlist_id, playlist_id)
    # 305         202 LOAD_CONST              57 ((None,))
    #             204 LOAD_CONST              46 (<code object _download_legacy_playlist_url at 0x000002AA88849810, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 305>)
    #             206 LOAD_CONST              47 ('BBCCoUkIE._download_legacy_playlist_url')
    #             208 MAKE_FUNCTION            1
    #             210 STORE_NAME              30 (_download_legacy_playlist_url)
    def _download_legacy_playlist_url(self,url,playlist_id):
        return self._download_xml(url, playlist_id, 'Downloading legacy playlist XML')
    # 309         212 LOAD_CONST              48 (<code object _extract_from_legacy_playlist at 0x000002AA88849A50, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 309>)
    #             214 LOAD_CONST              49 ('BBCCoUkIE._extract_from_legacy_playlist')
    #             216 MAKE_FUNCTION            0
    #             218 STORE_NAME              31 (_extract_from_legacy_playlist)
    def _extract_from_legacy_playlist(self,playlist,playlist_id):
        no_items = playlist.find('./{%s}noItems' % self._EMP_PLAYLIST_NS)
        if no_items is not None:
            reason = no_items.get('reason')
            if reason == 'preAvailability':
                msg = 'Episode %s is not yet available' % playlist_id
            else:
                if reason == 'postAvailability':
                    msg = 'Episode %s is no longer available' % playlist_id
                else:
                    if reason == 'noMedia':
                        msg = 'Episode %s is not currently available' % playlist_id
                    else:
                        msg = 'Episode %s is not available: %s' % (playlist_id, reason)
            raise ExtractorError(msg, expected=True)
        for item in self._extract_items(playlist):
            kind = item.get('kind')
            if kind != 'programme':
                if kind != 'radioProgramme':
                    continue
            title = playlist.find('./{%s}title' % self._EMP_PLAYLIST_NS).text
            description_el = playlist.find('./{%s}summary' % self._EMP_PLAYLIST_NS)
            description = description_el.text if description_el is not None else None

            def get_programme_id(item):

                def get_from_attributes(item):
                    for p in ('identifier', 'group'):
                        value = item.get(p)
                        if value and re.match('^[pb][\\da-z]{7}$', value):
                            return value

                get_from_attributes(item)
                mediator = item.find('./{%s}mediator' % self._EMP_PLAYLIST_NS)
                if mediator is not None:
                    return get_from_attributes(mediator)

            programme_id = get_programme_id(item)
            duration = int_or_none(item.get('duration'))
            if programme_id:
                formats, subtitles = self._download_media_selector(programme_id)
            else:
                formats, subtitles = self._process_media_selector(item, playlist_id)
                programme_id = playlist_id

        return (programme_id, title, description, duration, formats, subtitles)
    # 353         220 LOAD_CONST              50 (<code object _sort_formats at 0x000002AA88849B70, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 353>)
    #             222 LOAD_CONST              51 ('BBCCoUkIE._sort_formats')
    #             224 MAKE_FUNCTION            0
    #             226 STORE_NAME              32 (_sort_formats)
    def _sort_formats(self,formats):
        if not formats:
            raise ExtractorError('No video formats found')

        def _formats_key(f):
            from ..utils import determine_ext
            if not f.get('ext'):
                if 'url' in f:
                    f['ext'] = determine_ext(f['url'])
            preference = f.get('preference')
            if preference is None:
                proto = f.get('protocol')
                if proto is None:
                    proto = compat_urllib_parse_urlparse(f.get('url', '')).scheme
                preference = 0 if proto in ('http', 'https') else -0.1
                preference = preference - 50 if proto in ('rtmp', 'rtmpe') else preference
                if f.get('ext') in ('f4f', 'f4m'):
                    preference -= 0.5
            if f.get('vcodec') == 'none':
                if self._downloader.params.get('prefer_free_formats'):
                    ORDER = [
                        'aac', 'mp3', 'm4a', 'webm', 'ogg', 'opus']
                else:
                    ORDER = [
                        'webm', 'opus', 'ogg', 'mp3', 'aac', 'm4a']
                ext_preference = 0
                try:
                    audio_ext_preference = ORDER.index(f['ext'])
                except ValueError:
                    audio_ext_preference = -1

            else:
                if self._downloader.params.get('prefer_free_formats'):
                    ORDER = [
                        'flv', 'mp4', 'webm']
                else:
                    ORDER = [
                        'webm', 'flv', 'mp4']
                try:
                    ext_preference = ORDER.index(f['ext'])
                except ValueError:
                    ext_preference = -1

                audio_ext_preference = 0
            return (
                preference,
                f.get('language_preference') if f.get('language_preference') is not None else -1,
                f.get('quality') if f.get('quality') is not None else -1,
                f.get('tbr') if f.get('tbr') is not None else -1,
                f.get('filesize') if f.get('filesize') is not None else -1,
                f.get('vbr') if f.get('vbr') is not None else -1,
                f.get('height') if f.get('height') is not None else -1,
                f.get('width') if f.get('width') is not None else -1,
                ext_preference,
                f.get('abr') if f.get('abr') is not None else -1,
                audio_ext_preference,
                f.get('fps') if f.get('fps') is not None else -1,
                f.get('filesize_approx') if f.get('filesize_approx') is not None else -1,
                f.get('source_preference') if f.get('source_preference') is not None else -1,
                f.get('format_id'))

        formats.sort(key=_formats_key)
    # 415         228 LOAD_CONST              52 (<code object _real_extract at 0x000002AA88849C00, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 415>)
    #             230 LOAD_CONST              53 ('BBCCoUkIE._real_extract')
    #             232 MAKE_FUNCTION            0
    #             234 STORE_NAME              33 (_real_extract)
    def _real_extract(self,url):
        for i in range(2):
            self._downloader.params['listsubtitles'] = 1
            try:
                try:
                    result = self.do_real_extract(url)
                    if result:
                        if len(result.get('formats', [])) > 0:
                            return result
                    if i == 1:
                        try:
                            self._downloader.cookiejar.clear('.co.uk')
                        except:
                            pass

                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

            finally:
                if 'listsubtitles' in self._downloader.params:
                    self._downloader.params.pop('listsubtitles')
    # 435         236 LOAD_CONST              54 (<code object do_real_extract at 0x000002AA88849C90, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 435>)
    #             238 LOAD_CONST              55 ('BBCCoUkIE.do_real_extract')
    #             240 MAKE_FUNCTION            0
    #             242 STORE_NAME              34 (do_real_extract)
    #             244 LOAD_CONST              35 (None)
    #             246 RETURN_VALUE
    def do_real_extract(self,url):
        oldBBC = OldBBCCoUkIE()
        oldBBC.set_downloader(self._downloader)
        try:
            result = oldBBC._real_extract(url)
        except Exception as ex:
            try:
                result = None
            finally:
                ex = None
                del ex

        if result:
            return result
        group_id = self._match_id(url)
        webpage = self._download_webpage(url, group_id, 'Downloading video page')
        programme_id = None
        tviplayer = self._search_regex('mediator\\.bind\\(({.+?})\\s*,\\s*document\\.getElementById',
                                       webpage,
                                       'player', default=None)
        if tviplayer:
            player = self._parse_json(tviplayer, group_id).get('player', {})
            duration = int_or_none(player.get('duration'))
            programme_id = player.get('vpid')
        else:
            if not programme_id:
                programme_id = self._search_regex('"vpid"\\s*:\\s*"([\\da-z]{8})"',
                                                  webpage, 'vpid', fatal=False, default=None)
            if programme_id:
                self._MEDIASELECTOR_URLS.insert(0, self._getNewMediaSelection(programme_id))
                formats, subtitles = self._download_media_selector(programme_id)
                title = self._og_search_title(webpage)
                description = self._search_regex('<p class="[^"]*medium-description[^"]*">([^<]+)</p>',
                                                 webpage,
                                                 'description', fatal=False, default='')
                duration = self._search_regex('"duration":(\\d*)', webpage, 'duration', default=0)
            else:
                programme_id, title, description, duration, formats, subtitles = self._download_playlist(group_id)
        self._sort_formats(formats)
        return {'id': programme_id,
                'title': title,
                'description': description,
                'thumbnail': self._og_search_thumbnail(webpage, default=None),
                'duration': duration,
                'formats': formats,
                'subtitles': subtitles}
#485         128 LOAD_BUILD_CLASS
            # 130 LOAD_CONST              10 (<code object BBCIE at 0x000002AA8884E780, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 485>)
            # 132 LOAD_CONST              11 ('BBCIE')
            # 134 MAKE_FUNCTION            0
            # 136 LOAD_CONST              11 ('BBCIE')
            # 138 LOAD_NAME                8 (BBCCoUkIE)
            # 140 CALL_FUNCTION            3
            # 142 STORE_NAME              10 (BBCIE)

class BBCIE(BBCCoUkIE):
    IE_NAME = 'bbc'
    IE_DESC = 'BBC'
    _VALID_URL = 'https?://(?:www\\.)?bbc\\.(?:com|co\\.uk)/(?:[^/]+/)+(?P<id>[^/#?]+)'
    _MEDIASELECTOR_URLS = [
        'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/iptv-all/vpid/%s',
        'http://open.live.bbc.co.uk/mediaselector/4/mtis/stream/%s',
        'http://open.live.bbc.co.uk/mediaselector/5/select/version/2.0/mediaset/journalism-pc/vpid/%s']
    _TESTS = [
        {'url': 'http://www.bbc.com/news/world-europe-32668511',
         'info_dict': {'id': 'world-europe-32668511',
                       'title': 'Russia stages massive WW2 parade despite Western boycott',
                       'description': 'md5:00ff61976f6081841f759a08bf78cc9c'},
         'playlist_count': 2},
        {'url': 'http://www.bbc.com/news/business-28299555',
         'info_dict': {'id': 'business-28299555',
                       'title': 'Farnborough Airshow: Video highlights',
                       'description': 'BBC reports and video highlights at the Farnborough Airshow.'},
         'playlist_count': 9,
         'skip': 'Save time'},
        {'url': 'http://www.bbc.co.uk/blogs/adamcurtis/entries/3662a707-0af9-3149-963f-47bea720b460',
         'info_dict': {'id': '3662a707-0af9-3149-963f-47bea720b460',
                       'title': 'BBC Blogs - Adam Curtis - BUGGER'},
         'playlist_count': 18},
        {'url': 'http://www.bbc.com/news/world-europe-32041533',
         'info_dict': {'id': 'p02mprgb',
                       'ext': 'mp4',
                       'title': 'Aerial footage showed the site of the crash in the Alps - courtesy BFM TV',
                       'description': 'md5:2868290467291b37feda7863f7a83f54',
                       'duration': 47,
                       'timestamp': 1427219242,
                       'upload_date': '20150324'},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/turkce/haberler/2015/06/150615_telabyad_kentin_cogu',
         'info_dict': {'id': '150615_telabyad_kentin_cogu',
                       'ext': 'mp4',
                       'title': "YPG: Tel Abyad'ın tamamı kontrolümüzde",
                       'timestamp': 1434397334,
                       'upload_date': '20150615'},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/mundo/video_fotos/2015/06/150619_video_honduras_militares_hospitales_corrupcion_aw',
         'info_dict': {'id': '150619_video_honduras_militares_hospitales_corrupcion_aw',
                       'ext': 'mp4',
                       'title': 'Honduras militariza sus hospitales por nuevo escándalo de corrupción',
                       'timestamp': 1434713142,
                       'upload_date': '20150619'},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/news/video_and_audio/must_see/33376376',
         'info_dict': {'id': 'p02w6qjc',
                       'ext': 'mp4',
                       'title': 'Judge Mindy Glazer: "I\'m sorry to see you here... I always wondered what happened to you"',
                       'duration': 56},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/travel/story/20150625-sri-lankas-spicy-secret',
         'info_dict': {'id': 'p02q6gc4',
                       'ext': 'flv',
                       'title': 'Sri Lanka’s spicy secret',
                       'description': 'As a new train line to Jaffna opens up the country’s north, travellers can experience a truly distinct slice of Tamil culture.',
                       'timestamp': 1437674293,
                       'upload_date': '20150723'},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/autos/story/20130513-hyundais-rock-star',
         'info_dict': {'id': 'p018zqqg',
                       'ext': 'mp4',
                       'title': 'Hyundai Santa Fe Sport: Rock star',
                       'description': 'md5:b042a26142c4154a6e472933cf20793d',
                       'timestamp': 1415867444,
                       'upload_date': '20141113'},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/sport/0/football/33653409',
         'info_dict': {'id': 'p02xycnp',
                       'ext': 'mp4',
                       'title': 'Transfers: Cristiano Ronaldo to Man Utd, Arsenal to spend?',
                       'description': "BBC Sport's David Ornstein has the latest transfer gossip, including rumours of a Manchester United return for Cristiano Ronaldo.",
                       'duration': 140},
         'params': {'skip_download': True}},
        {'url': 'http://www.bbc.com/sport/0/football/34475836',
         'info_dict': {'id': '34475836',
                       'title': 'What Liverpool can expect from Klopp'},
         'playlist_count': 3},
        {'url': 'http://www.bbc.com/weather/features/33601775',
         'only_matching': True},
        {'url': 'http://www.bbc.co.uk/news/science-environment-33661876',
         'only_matching': True}]

    @classmethod
    def suitable(cls, url):
        if BBCCoUkIE.suitable(url) or BBCCoUkArticleIE.suitable(url):
            return False
        return super(BBCIE, cls).suitable(url)

    def _extract_from_media_meta(self, media_meta, video_id):
        source_files = media_meta.get('sourceFiles')
        if source_files:
            return (
                [{'url': f['url'], 'format_id': format_id, 'ext': f.get('encoding'),
                  'tbr': float_or_none(f.get('bitrate'), 1000), 'filesize': int_or_none(f.get('filesize'))} for
                 format_id, f in source_files.items() if f.get('url')], [])
        programme_id = media_meta.get('externalId')
        if programme_id:
            return self._download_media_selector(programme_id)
        href = media_meta.get('href')
        if href:
            playlist = self._download_legacy_playlist_url(href)
            _, _, _, _, formats, subtitles = self._extract_from_legacy_playlist(playlist, video_id)
            return (formats, subtitles)
        return ([], [])

    def _extract_from_playlist_sxml(self, url, playlist_id, timestamp):
        programme_id, title, description, duration, formats, subtitles = self._process_legacy_playlist_url(url,
                                                                                                           playlist_id)
        self._sort_formats(formats)
        return {'id': programme_id,
                'title': title,
                'description': description,
                'duration': duration,
                'timestamp': timestamp,
                'formats': formats,
                'subtitles': subtitles}

    def _real_extract(self, url):
        try:
            playlist_id = self._match_id(url)
            webpage = self._download_webpage(url, playlist_id)
            timestamp = None
            playlist_title = None
            playlist_description = None
            ld = self._parse_json(self._search_regex('(?s)<script type="application/ld\\+json">(.+?)</script>',
                                                     webpage,
                                                     'ld json', default='{}'),
                                  playlist_id,
                                  fatal=False)
            if ld:
                timestamp = parse_iso8601(ld.get('datePublished'))
                playlist_title = ld.get('headline')
                playlist_description = ld.get('articleBody')
            if not timestamp:
                timestamp = parse_iso8601(self._search_regex([
                    '<meta[^>]+property="article:published_time"[^>]+content="([^"]+)"',
                    'itemprop="datePublished"[^>]+datetime="([^"]+)"',
                    '"datePublished":\\s*"([^"]+)'],
                    webpage,
                    'date', default=None))
            entries = []
            playlists = re.findall('<param[^>]+name="playlist"[^>]+value="([^"]+)"', webpage)
            if playlists:
                entries = [self._extract_from_playlist_sxml(playlists[0], playlist_id, timestamp)]
            data_playables = re.findall('data-playable=(["\\\'])({.+?})\\1', webpage)
            if data_playables:
                for _, data_playable_json in data_playables:
                    data_playable = self._parse_json((unescapeHTML(data_playable_json)),
                                                     playlist_id, fatal=False)
                    if not data_playable:
                        continue
                    settings = data_playable.get('settings', {})
                    if settings:
                        playlist_object = settings.get('playlistObject', {})
                        if playlist_object:
                            items = playlist_object.get('items')
                            if items:
                                if isinstance(items, list):
                                    title = playlist_object['title']
                                    description = playlist_object.get('summary')
                                    duration = int_or_none(items[0].get('duration'))
                                    programme_id = items[0].get('vpid')
                                    formats, subtitles = self._download_media_selector(programme_id)
                                    self._sort_formats(formats)
                                    entries.append({'id': programme_id,
                                                    'title': title,
                                                    'description': description,
                                                    'timestamp': timestamp,
                                                    'duration': duration,
                                                    'formats': formats,
                                                    'subtitles': subtitles})
                                else:
                                    playlist = data_playable.get('otherSettings', {}).get('playlist', {})
                                    if playlist:
                                        entries.append(
                                            self._extract_from_playlist_sxml(playlist.get('progressiveDownloadUrl'),
                                                                             playlist_id, timestamp))

            if entries:
                playlist_title = playlist_title or remove_end(self._og_search_title(webpage), ' - BBC News')
                playlist_description = playlist_description or self._og_search_description(webpage, default=None)
                return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)
            programme_id = self._search_regex([
                'data-video-player-vpid="([\\da-z]{8})"',
                '<param[^>]+name="externalIdentifier"[^>]+value="([\\da-z]{8})"',
                '"vpid"\\s*:\\s*"([\\da-z]{8})"'],
                webpage,
                'vpid', default=None)
            if programme_id:
                formats, subtitles = self._download_media_selector(programme_id)
                self._sort_formats(formats)
                digital_data = self._parse_json(self._search_regex('var\\s+digitalData\\s*=\\s*({.+?});?\\n',
                                                                   webpage, 'digital data', default='{}'),
                                                programme_id,
                                                fatal=False)
                page_info = digital_data.get('page', {}).get('pageInfo', {})
                title = page_info.get('pageName') or self._og_search_title(webpage)
                description = page_info.get('description') or self._og_search_description(webpage)
                timestamp = parse_iso8601(page_info.get('publicationDate')) or timestamp
                return {'id': programme_id,
                        'title': title,
                        'description': description,
                        'timestamp': timestamp,
                        'formats': formats,
                        'subtitles': subtitles}
            playlist_title = self._html_search_regex('<title>(.*?)(?:\\s*-\\s*BBC [^ ]+)?</title>', webpage,
                                                     'playlist title')
            playlist_description = self._og_search_description(webpage, default=None)

            def extract_all(pattern):
                return list(filter(None, map(lambda s: self._parse_json(s, playlist_id, fatal=False),
                                             re.findall(pattern, webpage))))

            EMBED_URL = 'https?://(?:www\\.)?bbc\\.co\\.uk/(?:[^/]+/)+[\\da-z]{8}(?:\\b[^"]+)?'
            entries = []
            for match in extract_all('new\\s+SMP\\(({.+?})\\)'):
                embed_url = match.get('playerSettings', {}).get('externalEmbedUrl')
                if embed_url and re.match(EMBED_URL, embed_url):
                    entries.append(embed_url)

            entries.extend(re.findall('setPlaylist\\("(%s)"\\)' % EMBED_URL, webpage))
            if entries:
                return self.playlist_result([self.url_result(entry, 'BBCCoUk') for entry in entries], playlist_id,
                                            playlist_title, playlist_description)
            medias = extract_all("data-media-meta='({[^']+})'")
            media_asset = medias or self._search_regex('mediaAssetPage\\.init\\(\\s*({.+?}), "/',
                                                       webpage,
                                                       'media asset', default=None)
            if media_asset:
                media_asset_page = self._parse_json(media_asset, playlist_id, fatal=False)
                medias = []
                for video in media_asset_page.get('videos', {}).values():
                    medias.extend(video.values())

            vxp_playlist = medias or self._parse_json(self._search_regex(
                '<script[^>]+class="vxp-playlist-data"[^>]+type="application/json"[^>]*>([^<]+)</script>', webpage,
                'playlist data'), playlist_id)
            playlist_medias = []
            for item in vxp_playlist:
                media = item.get('media')
                if not media:
                    continue
                playlist_medias.append(media)
                if item.get('advert', {}).get('assetId') == playlist_id:
                    medias = [
                        media]
                    break

            if not medias:
                medias = playlist_medias
            entries = []
            for num, media_meta in enumerate(medias, start=1):
                formats, subtitles = self._extract_from_media_meta(media_meta, playlist_id)
                if not formats:
                    continue
                self._sort_formats(formats)
                video_id = media_meta.get('externalId')
                if not video_id:
                    video_id = playlist_id if len(medias) == 1 else '%s-%s' % (playlist_id, num)
                title = media_meta.get('caption')
                if not title:
                    title = playlist_title if len(medias) == 1 else '%s - Video %s' % (playlist_title, num)
                duration = int_or_none(media_meta.get('durationInSeconds')) or parse_duration(
                    media_meta.get('duration'))
                images = []
                for image in media_meta.get('images', {}).values():
                    images.extend(image.values())

                if 'image' in media_meta:
                    images.append(media_meta['image'])
                thumbnails = [{'url': image.get('href'), 'width': int_or_none(image.get('width')),
                               'height': int_or_none(image.get('height'))} for image in images]
                entries.append({'id': video_id,
                                'title': title,
                                'thumbnails': thumbnails,
                                'duration': duration,
                                'timestamp': timestamp,
                                'formats': formats,
                                'subtitles': subtitles})

            return self.playlist_result(entries, playlist_id, playlist_title, playlist_description)
        except:
            try:
                result = self._try_newVersion_extract(webpage)
            except:
                result = None

            if result:
                return result
            if OldBBCIE.suitable(url):
                old = OldBBCIE()
                old.set_downloader(self._downloader)
                return old._real_extract(url)

    def _try_newVersion_extract(self, webpage):
        programme_id = self._search_regex([
            '&quot;vpid&quot;:&quot;(.+?)&quot;,'],
            webpage,
            'vpid', default=None)
        if programme_id:
            formats, subtitles = self._download_media_selector(programme_id)
            self._sort_formats(formats)
            title = self._og_search_title(webpage)
            thumbnail = self._og_search_thumbnail(webpage)
            return {'id': programme_id,
                    'title': title,
                    'thumbnail': thumbnail,
                    'formats': formats,
                    'subtitles': subtitles}
        playlist_id = self._search_regex([
            '<div class="video" data-pid="([^"]+)'],
            webpage,
            'vpid', default=None)
        description = None
        duration = None
        if playlist_id:
            programme_id, title, description, duration, formats, subtitles = self._download_playlist(playlist_id)
        else:
            preload_state = self._parse_json(
                self._search_regex('window\\.__PRELOADED_STATE__\\s*=\\s*({.+?});', webpage, 'preload state',
                                   default='{}'),
                playlist_id, fatal=False)
            if preload_state:
                current_programme = preload_state.get('programmes', {}).get('current') or {}
                programme_id = current_programme.get('id')
                formats, subtitles = self._download_media_selector(programme_id)
                title = self._og_search_title(webpage)
                thumbnail = self._og_search_thumbnail(webpage)
        self._sort_formats(formats)
        return {'id': programme_id,
                'title': title,
                'description': description,
                'thumbnail': self._og_search_thumbnail(webpage, default=None),
                'duration': duration,
                'formats': formats,
                'subtitles': subtitles}



# 963         144 LOAD_BUILD_CLASS
  #             146 LOAD_CONST              12 (<code object BBCCoUkArticleIE at 0x000002AA8884E9C0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 963>)
  #             148 LOAD_CONST              13 ('BBCCoUkArticleIE')
  #             150 MAKE_FUNCTION            0
  #             152 LOAD_CONST              13 ('BBCCoUkArticleIE')
  #             154 LOAD_NAME                6 (InfoExtractor)
  #             156 CALL_FUNCTION            3
  #             158 STORE_NAME              12 (BBCCoUkArticleIE)
class BBCCoUkArticleIE(InfoExtractor):
    _VALID_URL = 'http://www.bbc.co.uk/programmes/articles/(?P<id>[a-zA-Z0-9]+)'
    IE_NAME = 'bbc.co.uk:article'
    IE_DESC = 'BBC articles'
    _TEST = {
        'url': 'http://www.bbc.co.uk/programmes/articles/3jNQLTMrPlYGTBn0WV6M2MS/not-your-typical-role-model-ada-lovelace-the-19th-century-programmer',
        'info_dict': {'id': '3jNQLTMrPlYGTBn0WV6M2MS',
                      'title': 'Calculating Ada: The Countess of Computing - Not your typical role model: Ada Lovelace the 19th century programmer - BBC Four',
                      'description': 'Hannah Fry reveals some of her surprising discoveries about Ada Lovelace during filming.'},
        'playlist_count': 4,
        'add_ie': [
            'BBCCoUk']}

    def _real_extract(self, url):
        if OldBBCCoUkArticleIE.suitable(url):
            old = OldBBCCoUkArticleIE()
            old.set_downloader(self._downloader)
            try:
                result = old._real_extract(url)
                return result
            except:
                pass

        playlist_id = self._match_id(url)
        webpage = self._download_webpage(url, playlist_id)
        title = self._og_search_title(webpage)
        description = self._og_search_description(webpage).strip()
        entries = [self.url_result(programme_url) for programme_url in
                   re.findall('<div[^>]+typeof="Clip"[^>]+resource="([^"]+)"', webpage)]
        return self.playlist_result(entries, playlist_id, title, description)

# 999         160 LOAD_BUILD_CLASS
#             162 LOAD_CONST              14 (<code object BBCCoUkReelVideoIE at 0x000002AA8884EAE0, file "C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py", line 999>)
#             164 LOAD_CONST              15 ('BBCCoUkReelVideoIE')
#             166 MAKE_FUNCTION            0
#             168 LOAD_CONST              15 ('BBCCoUkReelVideoIE')
#             170 LOAD_NAME                6 (InfoExtractor)
#             172 CALL_FUNCTION            3
#             174 STORE_NAME              25 (BBCCoUkReelVideoIE)
#             176 LOAD_CONST               2 (None)
#             178 RETURN_VALUE
class BBCCoUkReelVideoIE(InfoExtractor):
    _VALID_URL = 'https?://www\\.bbc\\.com/reel/'

    def _real_extract(self, url):
        programmesID = self._search_regex('video/([^/]+)', url, '', fatal=False, default=None)
        if not programmesID:
            programmesID = self._search_regex('playlist/.+?vpid=([^/]+)', url, '', fatal=False, default=None)
        if programmesID:
            return {'_type': 'url_transparent', 'url': 'https://www.bbc.co.uk/programmes/' + programmesID,
                    'id': programmesID}



