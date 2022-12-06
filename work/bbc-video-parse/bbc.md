~~~
Name:              _extract_connection
Filename:          C:\Users\ws\AppData\Local\Temp\tmpbn0t4kab\youtube_dl\WS_Extractor\bbc.py
Argument count:    3
Kw-only arguments: 0
Number of locals:  17
Stack size:        11
Flags:             OPTIMIZED, NEWLOCALS, NOFREE
Constants:
   0: None
   1: 'kind'
   2: 'protocol'
   3: 'supplier'
   4: 'http'
   5: 'href'
   6: 'transferFormat'
   7: 'asx'
   8: 'ref%s_%s'
   9: ('url', 'format_id')
  10: 'dash'
  11: False
  12: ('mpd_id', 'fatal')
  13: 'hls'
  14: 'mp4'
  15: 'm3u8_native'
  16: ('ext', 'entry_protocol', 'm3u8_id', 'fatal')
  17: '/\\1.ism/\\1.m3u8'
  18: 'height'
  19: 720
  20: 'hds'
  21: ('f4m_id', 'fatal')
  22: 'rtmp'
  23: 'application'
  24: 'ondemand'
  25: 'authString'
  26: 'identifier'
  27: 'server'
  28: '%s://%s/%s?%s'
  29: '%s?%s'
  30: 'http://www.bbc.co.uk'
  31: 'http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf'
  32: 'flv'
  33: ('url', 'play_path', 'app', 'page_url', 'player_url', 'rtmp_live', 'ext', 'format_id')
Names:
   0: get
   1: enumerate
   2: _extract_asx_playlist
   3: append
   4: extend
   5: _extract_mpd_formats
   6: _extract_m3u8_formats
   7: re
   8: search
   9: _USP_RE
  10: sub
  11: _extract_f4m_formats
Variable names:
   0: self
   1: connection
   2: programme_id
   3: formats
   4: kind
   5: protocol
   6: supplier
   7: href
   8: transfer_format
   9: i
  10: ref
  11: usp_formats
  12: f
  13: application
  14: auth_string
  15: identifier
  16: server
~~~

~~~
62           0 BUILD_LIST               0
              2 STORE_FAST               3 (formats)

 63           4 LOAD_FAST                1 (connection)
              6 LOAD_METHOD              0 (get)
              8 LOAD_CONST               1 ('kind')
             10 CALL_METHOD              1
             12 STORE_FAST               4 (kind)

 64          14 LOAD_FAST                1 (connection)
             16 LOAD_METHOD              0 (get)
             18 LOAD_CONST               2 ('protocol')
             20 CALL_METHOD              1
             22 STORE_FAST               5 (protocol)

 65          24 LOAD_FAST                1 (connection)
             26 LOAD_METHOD              0 (get)
             28 LOAD_CONST               3 ('supplier')
             30 CALL_METHOD              1
             32 STORE_FAST               6 (supplier)

 66          34 LOAD_FAST                5 (protocol)
             36 LOAD_CONST               4 ('http')
             38 COMPARE_OP               2 (==)
             40 EXTENDED_ARG             1
             42 POP_JUMP_IF_FALSE      374

 67          44 LOAD_FAST                1 (connection)
             46 LOAD_METHOD              0 (get)
             48 LOAD_CONST               5 ('href')
             50 CALL_METHOD              1
             52 STORE_FAST               7 (href)

 68          54 LOAD_FAST                1 (connection)
             56 LOAD_METHOD              0 (get)
             58 LOAD_CONST               6 ('transferFormat')
             60 CALL_METHOD              1
             62 STORE_FAST               8 (transfer_format)

 70          64 LOAD_FAST                6 (supplier)
             66 LOAD_CONST               7 ('asx')
             68 COMPARE_OP               2 (==)
             70 POP_JUMP_IF_FALSE      128

 71          72 SETUP_LOOP              52 (to 126)
             74 LOAD_GLOBAL              1 (enumerate)
             76 LOAD_FAST                0 (self)
             78 LOAD_METHOD              2 (_extract_asx_playlist)
             80 LOAD_FAST                1 (connection)
             82 LOAD_FAST                2 (programme_id)
             84 CALL_METHOD              2
             86 CALL_FUNCTION            1
             88 GET_ITER
        >>   90 FOR_ITER                32 (to 124)
             92 UNPACK_SEQUENCE          2
             94 STORE_FAST               9 (i)
             96 STORE_FAST              10 (ref)

 72          98 LOAD_FAST                3 (formats)
            100 LOAD_METHOD              3 (append)

 73         102 LOAD_FAST               10 (ref)

 74         104 LOAD_CONST               8 ('ref%s_%s')
            106 LOAD_FAST                9 (i)
            108 LOAD_FAST                6 (supplier)
            110 BUILD_TUPLE              2
            112 BINARY_MODULO
            114 LOAD_CONST               9 (('url', 'format_id'))
            116 BUILD_CONST_KEY_MAP      2
            118 CALL_METHOD              1
            120 POP_TOP
            122 JUMP_ABSOLUTE           90
        >>  124 POP_BLOCK
        >>  126 JUMP_FORWARD           244 (to 372)

 77     >>  128 LOAD_FAST                8 (transfer_format)
            130 LOAD_CONST              10 ('dash')
            132 COMPARE_OP               2 (==)
            134 POP_JUMP_IF_FALSE      162

 78         136 LOAD_FAST                3 (formats)
            138 LOAD_METHOD              4 (extend)
            140 LOAD_FAST                0 (self)
            142 LOAD_ATTR                5 (_extract_mpd_formats)
            144 LOAD_FAST                7 (href)
            146 LOAD_FAST                2 (programme_id)
            148 LOAD_CONST              10 ('dash')
            150 LOAD_CONST              11 (False)
            152 LOAD_CONST              12 (('mpd_id', 'fatal'))
            154 CALL_FUNCTION_KW         4
            156 CALL_METHOD              1
            158 POP_TOP
            160 JUMP_FORWARD           210 (to 372)

 79     >>  162 LOAD_FAST                8 (transfer_format)
            164 LOAD_CONST              13 ('hls')
            166 COMPARE_OP               2 (==)
            168 EXTENDED_ARG             1
            170 POP_JUMP_IF_FALSE      344

 80         172 LOAD_FAST                3 (formats)
            174 LOAD_METHOD              4 (extend)
            176 LOAD_FAST                0 (self)
            178 LOAD_ATTR                6 (_extract_m3u8_formats)

 81         180 LOAD_FAST                7 (href)
            182 LOAD_FAST                2 (programme_id)
            184 LOAD_CONST              14 ('mp4')
            186 LOAD_CONST              15 ('m3u8_native')

 82         188 LOAD_FAST                2 (programme_id)
            190 LOAD_CONST              11 (False)
            192 LOAD_CONST              16 (('ext', 'entry_protocol', 'm3u8_id', 'fatal'))
            194 CALL_FUNCTION_KW         6
            196 CALL_METHOD              1
            198 POP_TOP

 83         200 LOAD_GLOBAL              7 (re)
            202 LOAD_METHOD              8 (search)
            204 LOAD_FAST                0 (self)
            206 LOAD_ATTR                9 (_USP_RE)
            208 LOAD_FAST                7 (href)
            210 CALL_METHOD              2
            212 EXTENDED_ARG             1
            214 POP_JUMP_IF_FALSE      308

 84         216 LOAD_FAST                0 (self)
            218 LOAD_ATTR                6 (_extract_m3u8_formats)

 85         220 LOAD_GLOBAL              7 (re)
            222 LOAD_METHOD             10 (sub)
            224 LOAD_FAST                0 (self)
            226 LOAD_ATTR                9 (_USP_RE)
            228 LOAD_CONST              17 ('/\\1.ism/\\1.m3u8')
            230 LOAD_FAST                7 (href)
            232 CALL_METHOD              3

 86         234 LOAD_FAST                2 (programme_id)
            236 LOAD_CONST              14 ('mp4')
            238 LOAD_CONST              15 ('m3u8_native')

 87         240 LOAD_FAST                2 (programme_id)
            242 LOAD_CONST              11 (False)
            244 LOAD_CONST              16 (('ext', 'entry_protocol', 'm3u8_id', 'fatal'))
            246 CALL_FUNCTION_KW         6
            248 STORE_FAST              11 (usp_formats)

 88         250 SETUP_LOOP              90 (to 342)
            252 LOAD_FAST               11 (usp_formats)
            254 GET_ITER
        >>  256 FOR_ITER                46 (to 304)
            258 STORE_FAST              12 (f)

 89         260 LOAD_FAST               12 (f)
            262 LOAD_METHOD              0 (get)
            264 LOAD_CONST              18 ('height')
            266 CALL_METHOD              1
            268 EXTENDED_ARG             1
            270 POP_JUMP_IF_FALSE      290
            272 LOAD_FAST               12 (f)
            274 LOAD_CONST              18 ('height')
            276 BINARY_SUBSCR
            278 LOAD_CONST              19 (720)
            280 COMPARE_OP               4 (>)
            282 EXTENDED_ARG             1
            284 POP_JUMP_IF_FALSE      290

 90         286 EXTENDED_ARG             1
            288 JUMP_ABSOLUTE          256

 91     >>  290 LOAD_FAST                3 (formats)
            292 LOAD_METHOD              3 (append)
            294 LOAD_FAST               12 (f)
            296 CALL_METHOD              1
            298 POP_TOP
            300 EXTENDED_ARG             1
            302 JUMP_ABSOLUTE          256
        >>  304 POP_BLOCK
            306 JUMP_FORWARD            34 (to 342)

 92     >>  308 LOAD_FAST                8 (transfer_format)
            310 LOAD_CONST              20 ('hds')
            312 COMPARE_OP               2 (==)
            314 EXTENDED_ARG             1
            316 POP_JUMP_IF_FALSE      372

 93         318 LOAD_FAST                3 (formats)
            320 LOAD_METHOD              4 (extend)
            322 LOAD_FAST                0 (self)
            324 LOAD_ATTR               11 (_extract_f4m_formats)

 94         326 LOAD_FAST                7 (href)
            328 LOAD_FAST                2 (programme_id)
            330 LOAD_FAST                2 (programme_id)
            332 LOAD_CONST              11 (False)
            334 LOAD_CONST              21 (('f4m_id', 'fatal'))
            336 CALL_FUNCTION_KW         4
            338 CALL_METHOD              1
            340 POP_TOP
        >>  342 JUMP_FORWARD            28 (to 372)

 97     >>  344 LOAD_FAST                3 (formats)
            346 LOAD_METHOD              3 (append)

 98         348 LOAD_FAST                7 (href)

 99         350 LOAD_FAST                6 (supplier)
            352 EXTENDED_ARG             1
            354 JUMP_IF_TRUE_OR_POP    364
            356 LOAD_FAST                4 (kind)
            358 EXTENDED_ARG             1
            360 JUMP_IF_TRUE_OR_POP    364
            362 LOAD_FAST                5 (protocol)
        >>  364 LOAD_CONST               9 (('url', 'format_id'))
            366 BUILD_CONST_KEY_MAP      2
            368 CALL_METHOD              1
            370 POP_TOP
        >>  372 JUMP_FORWARD           100 (to 474)

101     >>  374 LOAD_FAST                5 (protocol)
            376 LOAD_CONST              22 ('rtmp')
            378 COMPARE_OP               2 (==)
            380 EXTENDED_ARG             1
            382 POP_JUMP_IF_FALSE      474

102         384 LOAD_FAST                1 (connection)
            386 LOAD_METHOD              0 (get)
            388 LOAD_CONST              23 ('application')
            390 LOAD_CONST              24 ('ondemand')
            392 CALL_METHOD              2
            394 STORE_FAST              13 (application)

103         396 LOAD_FAST                1 (connection)
            398 LOAD_METHOD              0 (get)
            400 LOAD_CONST              25 ('authString')
            402 CALL_METHOD              1
            404 STORE_FAST              14 (auth_string)

104         406 LOAD_FAST                1 (connection)
            408 LOAD_METHOD              0 (get)
            410 LOAD_CONST              26 ('identifier')
            412 CALL_METHOD              1
            414 STORE_FAST              15 (identifier)

105         416 LOAD_FAST                1 (connection)
            418 LOAD_METHOD              0 (get)
            420 LOAD_CONST              27 ('server')
            422 CALL_METHOD              1
            424 STORE_FAST              16 (server)

106         426 LOAD_FAST                3 (formats)
            428 LOAD_METHOD              3 (append)

107         430 LOAD_CONST              28 ('%s://%s/%s?%s')
            432 LOAD_FAST                5 (protocol)
            434 LOAD_FAST               16 (server)
            436 LOAD_FAST               13 (application)
            438 LOAD_FAST               14 (auth_string)
            440 BUILD_TUPLE              4
            442 BINARY_MODULO

108         444 LOAD_FAST               15 (identifier)

109         446 LOAD_CONST              29 ('%s?%s')
            448 LOAD_FAST               13 (application)
            450 LOAD_FAST               14 (auth_string)
            452 BUILD_TUPLE              2
            454 BINARY_MODULO

110         456 LOAD_CONST              30 ('http://www.bbc.co.uk')

111         458 LOAD_CONST              31 ('http://www.bbc.co.uk/emp/releases/iplayer/revisions/617463_618125_4/617463_618125_4_emp.swf')

112         460 LOAD_CONST              11 (False)

113         462 LOAD_CONST              32 ('flv')

114         464 LOAD_FAST                6 (supplier)
            466 LOAD_CONST              33 (('url', 'play_path', 'app', 'page_url', 'player_url', 'rtmp_live', 'ext', 'format_id'))
            468 BUILD_CONST_KEY_MAP      8
            470 CALL_METHOD              1
            472 POP_TOP

116     >>  474 LOAD_FAST                3 (formats)
            476 RETURN_VALUE

~~~

