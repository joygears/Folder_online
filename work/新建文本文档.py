# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: settings\audible.py
import os, json, xmlrpc.client, platform, subprocess, string
from struct import unpack, pack
import re, shutil, tempfile
from PyQt5.QtCore import QProcess
from settings.functions import os_sep, getExeDirectory, mkdir, choosename, getmd5, get_cover_from_aa, get_cover_from_aax
from ui.dlgOption import AudibleMeta
from settings.settings import res
SERVER = xmlrpc.client.ServerProxy('http://45.79.165.199:9766')
SERVER_PROXY1 = xmlrpc.client.ServerProxy('http://47.52.109.97:9766')
TMPDIR = tempfile.gettempdir()

class AudibleConvert:

    def __init__(self, settingsPath):
        self.settingsPath = settingsPath
        self.EXE = 'plugins/win' if os.sep == '\\' else 'plugins/mac'
        self.EXE = os_sep(os.path.join(getExeDirectory(), self.EXE))
        self.CFGFILE = os.path.join(self.settingsPath, 'audible.cfg')
        if not os.path.isfile(self.CFGFILE):
            json.dump({}, open(self.CFGFILE, 'w'))
        self.d = {}

    def setSettings(self, outputPath, isRegister=False):
        self.outputPath = outputPath
        self.isRegister = isRegister

    @staticmethod
    def check_type(filepath):
        bs = open(filepath, 'rb').read(12)
        if bs[4:8] == b'W\x90u6':
            return 'aa'
        else:
            if bs[3:] == b'$ftypaax ':
                return 'aax'
            return ''

    @staticmethod
    def is_aaxc(filepath):
        bs = open(filepath, 'rb').read(12)
        if bs[3:] == b'$ftypaaxc':
            return True
        else:
            return False

    def compute(self, checksum):
        if os.sep == '\\':
            process = QProcess()
            process.start('bin\\win_rcrack.exe', ['bin\\tables', '-h', checksum])
            process.waitForStarted()
            process.waitForFinished(-1)
            output = process.readAllStandardOutput().data().decode().strip()
            code = output[-8:]
            if self.verify_code(code):
                return code
            return ''
        else:
            process = QProcess()
            process.start('bin/mac_rcrack', [
             'bin/tables/audible_byte#4-4_0_10000x1362345_0.rt',
             'bin/tables/audible_byte#4-4_1_10000x1362345_0.rt',
             'bin/tables/audible_byte#4-4_2_10000x1362345_0.rt',
             'bin/tables/audible_byte#4-4_3_10000x1362345_0.rt',
             '-h', checksum])
            process.waitForStarted()
            process.waitForFinished(-1)
            output = process.readAllStandardOutput().data().decode().strip()
            code = output[-8:]
            if self.verify_code(code):
                return code
            return ''

    @staticmethod
    def get_key_from_server(checksum):
        for server in (SERVER, SERVER_PROXY1):
            try:
                code = server.query(checksum)
                if code:
                    print('code from', server, code)
                    return code
            except:
                continue

        return ''

    @staticmethod
    def verify_code(code):
        return all(c in string.hexdigits.lower() for c in code)

    def seek_code(self, checksum):
        if not self.d:
            self.d = json.load(open(self.CFGFILE))
        else:
            if checksum in self.d:
                if self.d[checksum]:
                    if self.verify_code(self.d[checksum]):
                        return self.d[checksum]
                code = self.get_key_from_server(checksum)
                if code or '64bit' in platform.architecture():
                    code = self.compute(checksum)
            else:
                code = ''
        if code:
            self.d[checksum] = code
            json.dump(self.d, open(self.CFGFILE, 'w'))
            return code
        else:
            return ''

    def getMeta(self, filepath):
        """
        获取aa/aax的元数据相关信息
        需要：title, artist, album, copyright, comment, date, genre, cover
        param: audible file path
        return: AudibleMeta instance
        """
        meta = AudibleMeta()

        def get_meta_one(info, meta, endstr='\n'):
            if info.find(meta) >= 0:
                start = info.find(meta) + len(meta)
                end = info.find(endstr, start)
                if end > start:
                    if info[(end - 1)] == '\r':
                        end -= 1
                    return info[start:end]
            return ''

        process = QProcess()
        process.start(self.EXE, ['-i', filepath, '-hide_banner'])
        process.waitForStarted()
        process.waitForFinished(-1)
        output = process.readAllStandardError().data().decode(encoding='utf8', errors='ignore')
        title = get_meta_one(output, 'title           : ')
        meta.title = title
        album = get_meta_one(output, 'album           : ')
        if album:
            meta.album = album
        else:
            author = get_meta_one(output, 'author          : ')
            if author:
                meta.artist = author
            else:
                meta.artist = get_meta_one(output, 'artist          : ')
        cpright = get_meta_one(output, 'copyright       : ')
        if cpright:
            meta.copyright = cpright
        date = get_meta_one(output, 'date            : ')
        if date:
            meta.year = date
        pubdate = get_meta_one(output, 'pubdate         : ')
        if pubdate:
            meta.year = pubdate
        else:
            meta.genre = 'Audiobook'
            comment = get_meta_one(output, 'comment         : ')
            if comment:
                meta.comments = comment
            coverpath = os.path.join(res.coverpath, getmd5(filepath) + '.jpg')
            typ = self.check_type(filepath)
            if typ == 'aax':
                cover_data = get_cover_from_aax(filepath)
            else:
                cover_data = get_cover_from_aa(filepath)
        if cover_data:
            open(coverpath, 'wb').write(cover_data)
            meta.cover = coverpath
        duration = get_meta_one(output, 'Duration: ', ',')
        meta.duration = duration
        checksum = get_meta_one(output, 'checksum == ')
        meta.checksum = checksum
        return meta

    def process(self,item,ext,signalRate):
 # L. 204         0  LOAD_CONST               0
 #                2  STORE_FAST               'progress'
        progress = 0
 # L. 206         4  LOAD_FAST                'item'
 #                6  LOAD_ATTR                audibleMeta
 #                8  STORE_FAST               'a_meta'
        a_meta = item.audibleMeta
 # L. 208        10  LOAD_FAST                'item'
 #               12  LOAD_ATTR                filepath
 #               14  STORE_FAST               'filepath'
        filepath = item.filepath
 # L. 210        16  LOAD_FAST                'a_meta'
 #               18  LOAD_ATTR                duration
 #               20  STORE_FAST               'duration'
        duration = a_meta.duration
 # L. 211        22  LOAD_FAST                'duration'
 #               24  LOAD_CONST               None
 #               26  LOAD_CONST               -3
 #               28  BUILD_SLICE_2         2
 #               30  BINARY_SUBSCR
 #               32  LOAD_ATTR                split
 #               34  LOAD_STR                 ':'
 #               36  CALL_FUNCTION_1       1  '1 positional argument'
 #               38  UNPACK_SEQUENCE_3     3
 #               40  STORE_FAST               'hours'
 #               42  STORE_FAST               'mins'
 #               44  STORE_FAST               'secs'
        hours,mins,secs = duration[:-3].split(':')
 # L. 212        46  LOAD_GLOBAL              int
 #               48  LOAD_FAST                'hours'
 #               50  CALL_FUNCTION_1       1  '1 positional argument'
 #               52  LOAD_CONST               3600
 #               54  BINARY_MULTIPLY
 #               56  LOAD_GLOBAL              int
 #               58  LOAD_FAST                'mins'
 #               60  CALL_FUNCTION_1       1  '1 positional argument'
 #               62  LOAD_CONST               60
 #               64  BINARY_MULTIPLY
 #               66  BINARY_ADD
 #               68  LOAD_GLOBAL              int
 #               70  LOAD_FAST                'secs'
 #               72  CALL_FUNCTION_1       1  '1 positional argument'
 #               74  BINARY_ADD
 #               76  STORE_FAST               'duration'
        duration = int(secs) + 60 * int(mins) + 3600 * int(hours)
 # L. 214        78  LOAD_FAST                'item'
 #               80  LOAD_ATTR                convertParam
 #               82  STORE_FAST               'convparam'
        convparam = item.convertParam
 # L. 216        84  BUILD_LIST_0          0
 #               86  STORE_FAST               'split_points'
        split_points = []
 # L. 218        88  LOAD_FAST                'convparam'
 #               90  LOAD_CONST               0
 #               92  BINARY_SUBSCR
 #               94  LOAD_CONST               0
 #               96  COMPARE_OP               ==
 #               98  POP_JUMP_IF_FALSE   112  'to 112'
        if  0 == convparam[0]:
            pass
             # L. 219       100  LOAD_CONST               0
             #              102  LOAD_FAST                'duration'
             #              104  BUILD_LIST_2          2
             #              106  BUILD_LIST_1          1
             #              108  STORE_FAST               'split_points'
            split_points = [[0,duration]]
             #              110  JUMP_FORWARD        350  'to 350'
             #              112  ELSE                     '350'
        else:
            pass
             # L. 220       112  LOAD_FAST                'convparam'
             #              114  LOAD_CONST               0
             #              116  BINARY_SUBSCR
             #              118  LOAD_CONST               1
             #              120  COMPARE_OP               ==
             #              122  POP_JUMP_IF_FALSE   218  'to 218'
            if convparam[0] == 1:
                 # L. 221       124  LOAD_FAST                'convparam'
                 #              126  LOAD_CONST               1
                 #              128  BINARY_SUBSCR
                 #              130  LOAD_CONST               60
                 #              132  BINARY_MULTIPLY
                 #              134  STORE_FAST               'dur_per_one'
                 dur_per_one = convparam[1] * 60
                 # L. 222       136  LOAD_GLOBAL              divmod
                 #              138  LOAD_FAST                'duration'
                 #              140  LOAD_FAST                'dur_per_one'
                 #              142  CALL_FUNCTION_2       2  '2 positional arguments'
                 #              144  UNPACK_SEQUENCE_2     2
                 #              146  STORE_FAST               'm'
                 #              148  STORE_FAST               'n'
                 m,n = divmod(duration,dur_per_one)
                 # L. 223       150  SETUP_LOOP          194  'to 194'
                 #              152  LOAD_GLOBAL              range
                 #              154  LOAD_FAST                'm'
                 #              156  CALL_FUNCTION_1       1  '1 positional argument'
                 #              158  GET_ITER
                 #              160  FOR_ITER            192  'to 192'
                 #              162  STORE_FAST               'i'
                 for i in range(m):
                     # L. 224       164  LOAD_FAST                'split_points'
                     #              166  LOAD_ATTR                append
                     #              168  LOAD_FAST                'dur_per_one'
                     #              170  LOAD_FAST                'i'
                     #              172  BINARY_MULTIPLY
                     #              174  LOAD_FAST                'dur_per_one'
                     #              176  LOAD_FAST                'i'
                     #              178  LOAD_CONST               1
                     #              180  BINARY_ADD
                     #              182  BINARY_MULTIPLY
                     #              184  BUILD_LIST_2          2
                     #              186  CALL_FUNCTION_1       1  '1 positional argument'
                     #              188  POP_TOP
                     #              190  JUMP_BACK           160  'to 160'
                     #              192  POP_BLOCK
                     #            194_0  COME_FROM_LOOP      150  '150'
                     split_points.append([i * dur_per_one, (1 + i) * dur_per_one])

                 # L. 225       194  LOAD_FAST                'n'
                 #              196  POP_JUMP_IF_FALSE   216  'to 216'
                 if n is True:
                     # L. 226       198  LOAD_FAST                'split_points'
                     #              200  LOAD_ATTR                append
                     #              202  LOAD_FAST                'duration'
                     #              204  LOAD_FAST                'n'
                     #              206  BINARY_SUBTRACT
                     #              208  LOAD_FAST                'duration'
                     #              210  BUILD_LIST_2          2
                     #              212  CALL_FUNCTION_1       1  '1 positional argument'
                     #              214  POP_TOP
                     #            216_0  COME_FROM           196  '196'
                     #              216  JUMP_FORWARD        350  'to 350'
                     #              218  ELSE                     '350'
                     split_points.append([duration-n,duration])
            else:
                 # L. 227       218  LOAD_FAST                'convparam'
                 #              220  LOAD_CONST               0
                 #              222  BINARY_SUBSCR
                 #              224  LOAD_CONST               2
                 #              226  COMPARE_OP               ==
                 #              228  POP_JUMP_IF_FALSE   326  'to 326'
                if convparam[0] == 2:
                     # L. 228       232  LOAD_FAST                'convparam'
                     #              234  LOAD_CONST               1
                     #              236  BINARY_SUBSCR
                     #              238  STORE_FAST               'file_num'
                    file_num = convparam[1]
                     # L. 229       240  LOAD_GLOBAL              int
                     #              242  LOAD_FAST                'duration'
                     #              244  LOAD_FAST                'file_num'
                     #              246  BINARY_TRUE_DIVIDE
                     #              248  CALL_FUNCTION_1       1  '1 positional argument'
                     #              250  STORE_FAST               'dur_per_one'
                    dur_per_one = int(duration / file_num)
                     # L. 230       252  SETUP_LOOP          302  'to 302'
                     #              254  LOAD_GLOBAL              range
                     #              256  LOAD_FAST                'file_num'
                     #              258  LOAD_CONST               1
                     #              260  BINARY_SUBTRACT
                     #              262  CALL_FUNCTION_1       1  '1 positional argument'
                     #              264  GET_ITER
                     #              266  FOR_ITER            300  'to 300'
                     #              268  STORE_FAST               'i'
                    for i in range(file_num - 1):
                         # L. 231       270  LOAD_FAST                'split_points'
                         #              272  LOAD_ATTR                append
                         #              274  LOAD_FAST                'dur_per_one'
                         #              276  LOAD_FAST                'i'
                         #              278  BINARY_MULTIPLY
                         #              280  LOAD_FAST                'dur_per_one'
                         #              282  LOAD_FAST                'i'
                         #              284  LOAD_CONST               1
                         #              286  BINARY_ADD
                         #              288  BINARY_MULTIPLY
                         #              290  BUILD_LIST_2          2
                         #              292  CALL_FUNCTION_1       1  '1 positional argument'
                         #              294  POP_TOP
                         #              296  JUMP_BACK           266  'to 266'
                         #              300  POP_BLOCK
                         #            302_0  COME_FROM_LOOP      252  '252'
                        split_points.append([dur_per_one * i,dur_per_one * (i + 1)])
                     # L. 232       302  LOAD_FAST                'split_points'
                     #              304  LOAD_ATTR                append
                     #              306  LOAD_FAST                'dur_per_one'
                     #              308  LOAD_FAST                'file_num'
                     #              310  LOAD_CONST               1
                     #              312  BINARY_SUBTRACT
                     #              314  BINARY_MULTIPLY
                     #              316  LOAD_FAST                'duration'
                     #              318  BUILD_LIST_2          2
                     #              320  CALL_FUNCTION_1       1  '1 positional argument'
                     #              322  POP_TOP
                     #              324  JUMP_FORWARD        350  'to 350'
                     #              326  ELSE                     '350'
                    split_points.append([dur_per_one * (file_num - 1), duration])
                else:
                    pass
                     #
                     # L. 233       326  LOAD_FAST                'convparam'
                     #              328  LOAD_CONST               0
                     #              330  BINARY_SUBSCR
                     #              332  LOAD_CONST               3
                     #              334  COMPARE_OP               ==
                     #              336  POP_JUMP_IF_FALSE   350  'to 350'
                    if convparam[0] == 3:
                         # L. 234       340  LOAD_FAST                'self'
                         #              342  LOAD_ATTR                get_chapters
                         #              344  LOAD_FAST                'filepath'
                         #              346  CALL_FUNCTION_1       1  '1 positional argument'
                         #              348  STORE_FAST               'split_points'
                         #            350_0  COME_FROM           336  '336'
                         #            350_1  COME_FROM           324  '324'
                         #            350_2  COME_FROM           216  '216'
                         #            350_3  COME_FROM           110  '110'
                        split_points = self.get_chapters(filepath)
 # L. 236       350  LOAD_FAST                'item'
 #              352  LOAD_ATTR                filetype
 #              354  STORE_FAST               'mime'
        mime = item.filetype
 # L. 238       356  LOAD_CONST               None
 #              358  STORE_FAST               'startupinfo'
        startupinfo = None
 # L. 240       360  LOAD_GLOBAL              os
 #              362  LOAD_ATTR                sep
 #              364  LOAD_STR                 '\\'
 #              366  COMPARE_OP               ==
 #              368  POP_JUMP_IF_FALSE   396  'to 396'
        if os.sep == "\\":
             # L. 241       372  LOAD_GLOBAL              subprocess
             #              374  LOAD_ATTR                STARTUPINFO
             #              376  CALL_FUNCTION_0       0  '0 positional arguments'
             #              378  STORE_FAST               'startupinfo'
            startupinfo = subprocess.STARTUPINFO()
             # L. 242       380  LOAD_FAST                'startupinfo'
             #              382  DUP_TOP
             #              384  LOAD_ATTR                dwFlags
             #              386  LOAD_GLOBAL              subprocess
             #              388  LOAD_ATTR                STARTF_USESHOWWINDOW
             #              390  INPLACE_OR
             #              392  ROT_TWO
             #              394  STORE_ATTR               dwFlags
             #            396_0  COME_FROM           368  '368'
            startupinfo.dwFlags = startupinfo.dwFlags | subprocess.STARTF_USESHOWWINDOW
 # L. 244       396  LOAD_FAST                'self'
 #              398  LOAD_ATTR                isRegister
 #              400  POP_JUMP_IF_TRUE    772  'to 772'
            if self.isRegister is False:

                 # L. 245       404  LOAD_FAST                'self'
                 #              406  LOAD_ATTR                validate_title
                 #              408  LOAD_FAST                'a_meta'
                 #              410  LOAD_ATTR                title
                 #              412  CALL_FUNCTION_1       1  '1 positional argument'
                 #              414  LOAD_FAST                'ext'
                 #              416  BINARY_ADD
                 #              418  STORE_FAST               'outname'
                outname = self.validate_title(a_meta.title) + ext
                 # L. 246       420  LOAD_GLOBAL              os
                 #              422  LOAD_ATTR                path
                 #              424  LOAD_ATTR                join
                 #              426  LOAD_FAST                'self'
                 #              428  LOAD_ATTR                outputPath
                 #              430  LOAD_FAST                'outname'
                 #              432  CALL_FUNCTION_2       2  '2 positional arguments'
                 #              434  STORE_FAST               'outpath'
                outpath = os.path.join(self.outputPath,outname)
                 # L. 247       436  LOAD_GLOBAL              len
                 #              438  LOAD_FAST                'outpath'
                 #              440  CALL_FUNCTION_1       1  '1 positional argument'
                 #              442  LOAD_CONST               245
                 #              444  COMPARE_OP               >
                 #              446  POP_JUMP_IF_FALSE   466  'to 466'
                if len(outpath) > 245:
                     # L. 248       450  LOAD_FAST                'outpath'
                     #              452  LOAD_CONST               None
                     #              454  LOAD_CONST               240
                     #              456  BUILD_SLICE_2         2
                     #              458  BINARY_SUBSCR
                     #              460  LOAD_FAST                'ext'
                     #              462  BINARY_ADD
                     #              464  STORE_FAST               'outpath'
                     #            466_0  COME_FROM           446  '446'
                    outpath = outpath[None:240] + ext 
                 # L. 249       466  LOAD_GLOBAL              choosename
                 #              468  LOAD_FAST                'outpath'
                 #              470  CALL_FUNCTION_1       1  '1 positional argument'
                 #              472  STORE_FAST               'outpath'
                outpath = choosename(outpath)
                 # L. 250       474  LOAD_FAST                'mime'
                 #              476  LOAD_STR                 'aa'
                 #              478  COMPARE_OP               ==
                 #              480  POP_JUMP_IF_FALSE   506  'to 506'
                if mime == 'aa':
                     # L. 251       484  LOAD_STR                 '-y'
                     #              486  LOAD_STR                 '-i'
                     #              488  LOAD_FAST                'filepath'
                     #              490  LOAD_STR                 '-ss'
                     #              492  LOAD_STR                 '0'
                     #              494  LOAD_STR                 '-t'
                     #              496  LOAD_STR                 '600'
                     #              498  LOAD_FAST                'outpath'
                     #              500  BUILD_LIST_8          8
                     #              502  STORE_FAST               'args'
                     #              504  JUMP_FORWARD        554  'to 554'
                     #              506  ELSE                     '554'
                    args = ['-y','-i',filepath,'-ss','0','-t','600',outpath]
                else:
                     #
                     # L. 253       506  LOAD_FAST                'self'
                     #              508  LOAD_ATTR                seek_code
                     #              510  LOAD_FAST                'a_meta'
                     #              512  LOAD_ATTR                checksum
                     #              514  CALL_FUNCTION_1       1  '1 positional argument'
                     #              516  STORE_FAST               'act_code'
                    act_code = self.seek_code(a_meta.checksum)
                     # L. 254       518  LOAD_FAST                'act_code'
                     #              520  POP_JUMP_IF_TRUE    528  'to 528'
                    if act_code is False:
                         # L. 255       524  LOAD_STR                 ''
                         #              526  RETURN_END_IF
                         #            528_0  COME_FROM           520  '520'
                        act_code = ""
                        
                     # L. 256       528  LOAD_STR                 '-y'
                     #              530  LOAD_STR                 '-activation_bytes'
                     #              532  LOAD_FAST                'act_code'
                     #              534  LOAD_STR                 '-i'
                     #              536  LOAD_FAST                'filepath'
                     #              538  LOAD_STR                 '-ss'
                     #              540  LOAD_STR                 '0'
                     #              542  LOAD_STR                 '-t'
                     #              544  LOAD_STR                 '600'
                     #              546  LOAD_STR                 '-vn'
                     #              548  LOAD_FAST                'outpath'
                     #              550  BUILD_LIST_11        11
                     #              552  STORE_FAST               'args'
                     #            554_0  COME_FROM           504  '504'
                    args = ['-y','-activation_bytes',act_code,'-i',filepath,'-ss','0','-t','600','-vn',outpath]
                 #
                 # L. 258       554  LOAD_GLOBAL              subprocess
                 #              556  LOAD_ATTR                Popen
                 #              558  LOAD_FAST                'self'
                 #              560  LOAD_ATTR                EXE
                 #              562  BUILD_LIST_1          1
                 #              564  LOAD_FAST                'args'
                 #              566  BINARY_ADD
                 #              568  LOAD_GLOBAL              subprocess
                 #              570  LOAD_ATTR                PIPE
                 #              572  LOAD_CONST               True
                 #
                 # L. 259       574  LOAD_FAST                'startupinfo'
                 #              576  LOAD_CONST               ('stderr', 'universal_newlines', 'startupinfo')
                 #              578  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
                 #              580  STORE_FAST               'proc'
                proc = subprocess.Popen([self.EXE] + args,stderr=subprocess.PIPE,universal_newlines=True,startupinfo=startupinfo)
                 # L. 260       582  SETUP_LOOP          712  'to 712'
                 #              584  LOAD_FAST                'proc'
                 #              586  LOAD_ATTR                poll
                 #              588  CALL_FUNCTION_0       0  '0 positional arguments'
                 #              590  LOAD_CONST               None
                 #              592  COMPARE_OP               is
                 #              594  POP_JUMP_IF_FALSE   710  'to 710'
                while proc.poll() is not None:
                     # L. 261       598  SETUP_EXCEPT        614  'to 614'
                    try:
                         # L. 262       600  LOAD_FAST                'proc'
                         #              602  LOAD_ATTR                stderr
                         #              604  LOAD_ATTR                readline
                         #              606  CALL_FUNCTION_0       0  '0 positional arguments'
                         #              608  STORE_FAST               'content'
                         #              610  POP_BLOCK
                         #              612  JUMP_FORWARD        640  'to 640'
                         #            614_0  COME_FROM_EXCEPT    598  '598'
                         content = proc.stderr.readline()
                         # L. 263       614  DUP_TOP
                         #              616  LOAD_GLOBAL              UnicodeDecodeError
                         #              618  COMPARE_OP               exception-match
                         #              620  POP_JUMP_IF_FALSE   638  'to 638'
                         #              624  POP_TOP
                         #              626  POP_TOP
                         #              628  POP_TOP
                    except UnicodeDecodeError:
                         # L. 264       630  LOAD_STR                 ''
                         #              632  STORE_FAST               'content'
                         #              634  POP_EXCEPT
                         #              636  JUMP_FORWARD        640  'to 640'
                         #              638  END_FINALLY
                         #            640_0  COME_FROM           636  '636'
                         #            640_1  COME_FROM           612  '612'
                        content = ""
                     # L. 265       640  LOAD_STR                 'size='
                     #              642  LOAD_FAST                'content'
                     #              644  COMPARE_OP               in
                     #              646  POP_JUMP_IF_FALSE   584  'to 584'
                     if 'size=' not in content:
                        continue
                     # L. 266       650  LOAD_GLOBAL              int
                     #              652  LOAD_FAST                'self'
                     #              654  LOAD_ATTR                timestamp
                     #              656  LOAD_FAST                'content'
                     #              658  CALL_FUNCTION_1       1  '1 positional argument'
                     #              660  LOAD_CONST               600
                     #              662  BINARY_TRUE_DIVIDE
                     #              664  LOAD_CONST               100
                     #              666  BINARY_MULTIPLY
                     #              668  CALL_FUNCTION_1       1  '1 positional argument'
                     #              670  DUP_TOP
                     #              672  STORE_FAST               '_progress'
                     #              674  STORE_FAST               '_progress'
                     #
                     # L. 267       676  LOAD_FAST                '_progress'
                     #              678  LOAD_FAST                'progress'
                     #              680  COMPARE_OP               >
                     #              682  POP_JUMP_IF_FALSE   584  'to 584'
                     #
                     # L. 268       686  LOAD_FAST                '_progress'
                     #              688  STORE_FAST               'progress'
                     #
                     # L. 269       690  LOAD_FAST                'progress'
                     #              692  LOAD_FAST                'item'
                     #              694  STORE_ATTR               rate
                     #
                     # L. 270       696  LOAD_FAST                'signal'
                     #              698  LOAD_ATTR                emit
                     #              700  LOAD_FAST                'item'
                     #              702  CALL_FUNCTION_1       1  '1 positional argument'
                     #              704  POP_TOP
                     #              706  JUMP_BACK           584  'to 584'
                     #            710_0  COME_FROM           594  '594'
                     #              710  POP_BLOCK
                     #            712_0  COME_FROM_LOOP      582  '582'
                
                 # L. 272       712  LOAD_FAST                'proc'
                 #              714  LOAD_ATTR                returncode
                 #              716  LOAD_CONST               0
                 #              718  COMPARE_OP               !=
                 #              720  POP_JUMP_IF_FALSE   728  'to 728'
                 #
                 # L. 273       724  LOAD_STR                 ''
                 #              726  RETURN_END_IF
                 #            728_0  COME_FROM           720  '720'
                 #
                 # L. 275       728  LOAD_FAST                'ext'
                 #              730  LOAD_STR                 '.mp3'
                 #              732  COMPARE_OP               ==
                 #              734  POP_JUMP_IF_FALSE   754  'to 754'
                 #
                 # L. 276       738  LOAD_FAST                'self'
                 #              740  LOAD_ATTR                set_mp3_cover
                 #              742  LOAD_FAST                'outpath'
                 #              744  LOAD_FAST                'a_meta'
                 #              746  LOAD_ATTR                cover
                 #              748  CALL_FUNCTION_2       2  '2 positional arguments'
                 #              750  POP_TOP
                 #              752  JUMP_FORWARD        768  'to 768'
                 #              754  ELSE                     '768'
                 #
                 # L. 278       754  LOAD_FAST                'self'
                 #              756  LOAD_ATTR                set_m4b_cover
                 #              758  LOAD_FAST                'outpath'
                 #              760  LOAD_FAST                'a_meta'
                 #              762  LOAD_ATTR                cover
                 #              764  CALL_FUNCTION_2       2  '2 positional arguments'
                 #              766  POP_TOP
                 #            768_0  COME_FROM           752  '752'
                 #
                 # L. 280       768  LOAD_FAST                'outpath'
                 #              770  RETURN_END_IF
                 #            772_0  COME_FROM           400  '400'
 #
 # L. 282       772  LOAD_GLOBAL              len
 #              774  LOAD_FAST                'split_points'
 #              776  CALL_FUNCTION_1       1  '1 positional argument'
 #              778  LOAD_CONST               1
 #              780  COMPARE_OP               ==
 #              782  POP_JUMP_IF_FALSE  1200  'to 1200'
 #
 # L. 283       786  LOAD_FAST                'self'
 #              788  LOAD_ATTR                validate_title
 #              790  LOAD_FAST                'a_meta'
 #              792  LOAD_ATTR                title
 #              794  CALL_FUNCTION_1       1  '1 positional argument'
 #              796  LOAD_FAST                'ext'
 #              798  BINARY_ADD
 #              800  STORE_FAST               'outname'
 #
 # L. 284       802  LOAD_GLOBAL              os
 #              804  LOAD_ATTR                path
 #              806  LOAD_ATTR                join
 #              808  LOAD_FAST                'self'
 #              810  LOAD_ATTR                outputPath
 #              812  LOAD_FAST                'outname'
 #              814  CALL_FUNCTION_2       2  '2 positional arguments'
 #              816  STORE_FAST               'outpath'
 #
 # L. 285       818  LOAD_GLOBAL              len
 #              820  LOAD_FAST                'outpath'
 #              822  CALL_FUNCTION_1       1  '1 positional argument'
 #              824  LOAD_CONST               245
 #              826  COMPARE_OP               >
 #              828  POP_JUMP_IF_FALSE   848  'to 848'
 #
 # L. 286       832  LOAD_FAST                'outpath'
 #              834  LOAD_CONST               None
 #              836  LOAD_CONST               240
 #              838  BUILD_SLICE_2         2
 #              840  BINARY_SUBSCR
 #              842  LOAD_FAST                'ext'
 #              844  BINARY_ADD
 #              846  STORE_FAST               'outpath'
 #            848_0  COME_FROM           828  '828'
 #
 # L. 287       848  LOAD_GLOBAL              choosename
 #              850  LOAD_FAST                'outpath'
 #              852  CALL_FUNCTION_1       1  '1 positional argument'
 #              854  STORE_FAST               'outpath'
 #
 # L. 288       856  LOAD_FAST                'mime'
 #              858  LOAD_STR                 'aa'
 #              860  COMPARE_OP               ==
 #              862  POP_JUMP_IF_FALSE   880  'to 880'
 #
 # L. 289       866  LOAD_STR                 '-y'
 #              868  LOAD_STR                 '-i'
 #              870  LOAD_FAST                'filepath'
 #              872  LOAD_FAST                'outpath'
 #              874  BUILD_LIST_4          4
 #              876  STORE_FAST               'args'
 #              878  JUMP_FORWARD        958  'to 958'
 #              880  ELSE                     '958'
 #
 # L. 291       880  LOAD_FAST                'self'
 #              882  LOAD_ATTR                seek_code
 #              884  LOAD_FAST                'a_meta'
 #              886  LOAD_ATTR                checksum
 #              888  CALL_FUNCTION_1       1  '1 positional argument'
 #              890  STORE_FAST               'act_code'
 #
 # L. 292       892  LOAD_FAST                'act_code'
 #              894  POP_JUMP_IF_TRUE    902  'to 902'
 #
 # L. 293       898  LOAD_STR                 ''
 #              900  RETURN_END_IF
 #            902_0  COME_FROM           894  '894'
 #
 # L. 294       902  LOAD_FAST                'ext'
 #              904  LOAD_ATTR                lower
 #              906  CALL_FUNCTION_0       0  '0 positional arguments'
 #              908  LOAD_STR                 '.m4b'
 #              910  COMPARE_OP               ==
 #              912  POP_JUMP_IF_FALSE   940  'to 940'
 #
 # L. 295       916  LOAD_STR                 '-y'
 #              918  LOAD_STR                 '-activation_bytes'
 #              920  LOAD_FAST                'act_code'
 #              922  LOAD_STR                 '-i'
 #              924  LOAD_FAST                'filepath'
 #              926  LOAD_STR                 '-vn'
 #              928  LOAD_STR                 '-c:a'
 #              930  LOAD_STR                 'copy'
 #              932  LOAD_FAST                'outpath'
 #              934  BUILD_LIST_9          9
 #              936  STORE_FAST               'args'
 #              938  JUMP_FORWARD        958  'to 958'
 #              940  ELSE                     '958'
 #
 # L. 297       940  LOAD_STR                 '-y'
 #              942  LOAD_STR                 '-activation_bytes'
 #              944  LOAD_FAST                'act_code'
 #              946  LOAD_STR                 '-i'
 #              948  LOAD_FAST                'filepath'
 #              950  LOAD_STR                 '-vn'
 #              952  LOAD_FAST                'outpath'
 #              954  BUILD_LIST_7          7
 #              956  STORE_FAST               'args'
 #            958_0  COME_FROM           938  '938'
 #            958_1  COME_FROM           878  '878'
 #
 # L. 299       958  LOAD_GLOBAL              subprocess
 #              960  LOAD_ATTR                Popen
 #              962  LOAD_FAST                'self'
 #              964  LOAD_ATTR                EXE
 #              966  BUILD_LIST_1          1
 #              968  LOAD_FAST                'args'
 #              970  BINARY_ADD
 #              972  LOAD_GLOBAL              subprocess
 #              974  LOAD_ATTR                PIPE
 #              976  LOAD_CONST               True
 #
 # L. 300       978  LOAD_FAST                'startupinfo'
 #              980  LOAD_CONST               ('stderr', 'universal_newlines', 'startupinfo')
 #              982  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
 #              984  STORE_FAST               'proc'
 #
 # L. 301       986  SETUP_LOOP         1116  'to 1116'
 #              988  LOAD_FAST                'proc'
 #              990  LOAD_ATTR                poll
 #              992  CALL_FUNCTION_0       0  '0 positional arguments'
 #              994  LOAD_CONST               None
 #              996  COMPARE_OP               is
 #              998  POP_JUMP_IF_FALSE  1114  'to 1114'
 #
 # L. 302      1002  SETUP_EXCEPT       1018  'to 1018'
 #
 # L. 303      1004  LOAD_FAST                'proc'
 #             1006  LOAD_ATTR                stderr
 #             1008  LOAD_ATTR                readline
 #             1010  CALL_FUNCTION_0       0  '0 positional arguments'
 #             1012  STORE_FAST               'content'
 #             1014  POP_BLOCK
 #             1016  JUMP_FORWARD       1044  'to 1044'
 #           1018_0  COME_FROM_EXCEPT   1002  '1002'
 #
 # L. 304      1018  DUP_TOP
 #             1020  LOAD_GLOBAL              UnicodeDecodeError
 #             1022  COMPARE_OP               exception-match
 #             1024  POP_JUMP_IF_FALSE  1042  'to 1042'
 #             1028  POP_TOP
 #             1030  POP_TOP
 #             1032  POP_TOP
 #
 # L. 305      1034  LOAD_STR                 ''
 #             1036  STORE_FAST               'content'
 #             1038  POP_EXCEPT
 #             1040  JUMP_FORWARD       1044  'to 1044'
 #             1042  END_FINALLY
 #           1044_0  COME_FROM          1040  '1040'
 #           1044_1  COME_FROM          1016  '1016'
 #
 # L. 306      1044  LOAD_STR                 'size='
 #             1046  LOAD_FAST                'content'
 #             1048  COMPARE_OP               in
 #             1050  POP_JUMP_IF_FALSE   988  'to 988'
 #
 # L. 307      1054  LOAD_GLOBAL              int
 #             1056  LOAD_FAST                'self'
 #             1058  LOAD_ATTR                timestamp
 #             1060  LOAD_FAST                'content'
 #             1062  CALL_FUNCTION_1       1  '1 positional argument'
 #             1064  LOAD_FAST                'duration'
 #             1066  BINARY_TRUE_DIVIDE
 #             1068  LOAD_CONST               100
 #             1070  BINARY_MULTIPLY
 #             1072  CALL_FUNCTION_1       1  '1 positional argument'
 #             1074  DUP_TOP
 #             1076  STORE_FAST               '_progress'
 #             1078  STORE_FAST               '_progress'
 #
 # L. 308      1080  LOAD_FAST                '_progress'
 #             1082  LOAD_FAST                'progress'
 #             1084  COMPARE_OP               >
 #             1086  POP_JUMP_IF_FALSE   988  'to 988'
 #
 # L. 309      1090  LOAD_FAST                '_progress'
 #             1092  STORE_FAST               'progress'
 #
 # L. 310      1094  LOAD_FAST                'progress'
 #             1096  LOAD_FAST                'item'
 #             1098  STORE_ATTR               rate
 #
 # L. 311      1100  LOAD_FAST                'signal'
 #             1102  LOAD_ATTR                emit
 #             1104  LOAD_FAST                'item'
 #             1106  CALL_FUNCTION_1       1  '1 positional argument'
 #             1108  POP_TOP
 #             1110  JUMP_BACK           988  'to 988'
 #           1114_0  COME_FROM           998  '998'
 #             1114  POP_BLOCK
 #           1116_0  COME_FROM_LOOP      986  '986'
 #
 # L. 313      1116  LOAD_FAST                'proc'
 #             1118  LOAD_ATTR                returncode
 #             1120  LOAD_CONST               0
 #             1122  COMPARE_OP               !=
 #             1124  POP_JUMP_IF_FALSE  1132  'to 1132'
 #
 # L. 314      1128  LOAD_STR                 ''
 #             1130  RETURN_END_IF
 #           1132_0  COME_FROM          1124  '1124'
 #
 # L. 316      1132  LOAD_FAST                'ext'
 #             1134  LOAD_STR                 '.mp3'
 #             1136  COMPARE_OP               ==
 #             1138  POP_JUMP_IF_FALSE  1170  'to 1170'
 #
 # L. 317      1142  LOAD_FAST                'self'
 #             1144  LOAD_ATTR                set_mp3_meta
 #             1146  LOAD_FAST                'outpath'
 #             1148  LOAD_FAST                'a_meta'
 #             1150  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1152  POP_TOP
 #
 # L. 318      1154  LOAD_FAST                'self'
 #             1156  LOAD_ATTR                set_mp3_cover
 #             1158  LOAD_FAST                'outpath'
 #             1160  LOAD_FAST                'a_meta'
 #             1162  LOAD_ATTR                cover
 #             1164  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1166  POP_TOP
 #             1168  JUMP_FORWARD       1196  'to 1196'
 #             1170  ELSE                     '1196'
 #
 # L. 320      1170  LOAD_FAST                'self'
 #             1172  LOAD_ATTR                set_m4b_meta
 #             1174  LOAD_FAST                'outpath'
 #             1176  LOAD_FAST                'a_meta'
 #             1178  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1180  POP_TOP
 #
 # L. 321      1182  LOAD_FAST                'self'
 #             1184  LOAD_ATTR                set_m4b_cover
 #             1186  LOAD_FAST                'outpath'
 #             1188  LOAD_FAST                'a_meta'
 #             1190  LOAD_ATTR                cover
 #             1192  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1194  POP_TOP
 #           1196_0  COME_FROM          1168  '1168'
 #
 # L. 322      1196  LOAD_FAST                'outpath'
 #             1198  RETURN_END_IF
 #           1200_0  COME_FROM           782  '782'
 #
 # L. 324      1200  LOAD_FAST                'self'
 #             1202  LOAD_ATTR                validate_title
 #             1204  LOAD_FAST                'a_meta'
 #             1206  LOAD_ATTR                title
 #             1208  CALL_FUNCTION_1       1  '1 positional argument'
 #             1210  STORE_FAST               'name'
 #
 # L. 325      1212  LOAD_GLOBAL              os
 #             1214  LOAD_ATTR                path
 #             1216  LOAD_ATTR                join
 #             1218  LOAD_FAST                'self'
 #             1220  LOAD_ATTR                outputPath
 #             1222  LOAD_FAST                'name'
 #             1224  LOAD_CONST               None
 #             1226  LOAD_CONST               20
 #             1228  BUILD_SLICE_2         2
 #             1230  BINARY_SUBSCR
 #             1232  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1234  STORE_DEREF              'outdir'
 #
 # L. 326      1236  LOAD_GLOBAL              mkdir
 #             1238  LOAD_DEREF               'outdir'
 #             1240  CALL_FUNCTION_1       1  '1 positional argument'
 #             1242  STORE_DEREF              'outdir'
 #
 # L. 328      1244  BUILD_LIST_0          0
 #             1246  STORE_FAST               'cmds'
 #
 # L. 329      1248  LOAD_FAST                'mime'
 #             1250  LOAD_STR                 'aa'
 #             1252  COMPARE_OP               ==
 #             1254  POP_JUMP_IF_FALSE  1456  'to 1456'
 #
 # L. 330      1258  SETUP_LOOP         1452  'to 1452'
 #             1260  LOAD_GLOBAL              enumerate
 #             1262  LOAD_FAST                'split_points'
 #             1264  CALL_FUNCTION_1       1  '1 positional argument'
 #             1266  GET_ITER
 #             1268  FOR_ITER           1450  'to 1450'
 #             1270  UNPACK_SEQUENCE_2     2
 #             1272  STORE_FAST               'idx'
 #             1274  STORE_FAST               'item_'
 #
 # L. 331      1276  LOAD_GLOBAL              os
 #             1278  LOAD_ATTR                path
 #             1280  LOAD_ATTR                join
 #             1282  LOAD_DEREF               'outdir'
 #             1284  LOAD_FAST                'name'
 #             1286  LOAD_STR                 '--%04d'
 #             1288  LOAD_FAST                'idx'
 #             1290  LOAD_CONST               1
 #             1292  BINARY_ADD
 #             1294  BINARY_MODULO
 #             1296  BINARY_ADD
 #             1298  LOAD_FAST                'ext'
 #             1300  BINARY_ADD
 #             1302  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1304  STORE_FAST               'secure_outpath'
 #
 # L. 332      1306  LOAD_FAST                'a_meta'
 #             1308  LOAD_ATTR                title
 #             1310  LOAD_STR                 '--%04d'
 #             1312  LOAD_FAST                'idx'
 #             1314  LOAD_CONST               1
 #             1316  BINARY_ADD
 #             1318  BINARY_MODULO
 #             1320  BINARY_ADD
 #             1322  LOAD_STR                 '"'
 #             1324  BINARY_ADD
 #             1326  STORE_FAST               'title'
 #
 # L. 333      1328  LOAD_GLOBAL              len
 #             1330  LOAD_FAST                'secure_outpath'
 #             1332  CALL_FUNCTION_1       1  '1 positional argument'
 #             1334  STORE_FAST               'path_length'
 #
 # L. 334      1336  LOAD_FAST                'path_length'
 #             1338  LOAD_CONST               245
 #             1340  COMPARE_OP               >
 #             1342  POP_JUMP_IF_FALSE  1388  'to 1388'
 #
 # L. 335      1346  LOAD_GLOBAL              os
 #             1348  LOAD_ATTR                path
 #             1350  LOAD_ATTR                join
 #             1352  LOAD_DEREF               'outdir'
 #             1354  LOAD_FAST                'name'
 #             1356  LOAD_CONST               None
 #             1358  LOAD_CONST               245
 #             1360  LOAD_FAST                'path_length'
 #             1362  BINARY_SUBTRACT
 #             1364  BUILD_SLICE_2         2
 #             1366  BINARY_SUBSCR
 #             1368  LOAD_STR                 '--%04d'
 #             1370  LOAD_FAST                'idx'
 #             1372  LOAD_CONST               1
 #             1374  BINARY_ADD
 #             1376  BINARY_MODULO
 #             1378  BINARY_ADD
 #             1380  LOAD_FAST                'ext'
 #             1382  BINARY_ADD
 #             1384  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1386  STORE_FAST               'secure_outpath'
 #           1388_0  COME_FROM          1342  '1342'
 #
 # L. 336      1388  LOAD_FAST                'cmds'
 #             1390  LOAD_ATTR                append
 #
 # L. 337      1392  LOAD_STR                 '-y'
 #             1394  LOAD_STR                 '-i'
 #             1396  LOAD_FAST                'filepath'
 #             1398  LOAD_STR                 '-ss'
 #             1400  LOAD_GLOBAL              str
 #             1402  LOAD_FAST                'item_'
 #             1404  LOAD_CONST               0
 #             1406  BINARY_SUBSCR
 #             1408  CALL_FUNCTION_1       1  '1 positional argument'
 #             1410  LOAD_STR                 '-t'
 #             1412  LOAD_GLOBAL              str
 #             1414  LOAD_FAST                'item_'
 #             1416  LOAD_CONST               1
 #             1418  BINARY_SUBSCR
 #             1420  LOAD_FAST                'item_'
 #             1422  LOAD_CONST               0
 #             1424  BINARY_SUBSCR
 #             1426  BINARY_SUBTRACT
 #             1428  CALL_FUNCTION_1       1  '1 positional argument'
 #             1430  LOAD_STR                 '-metadata'
 #
 # L. 338      1432  LOAD_STR                 'title=%s'
 #             1434  LOAD_FAST                'title'
 #             1436  BINARY_MODULO
 #
 # L. 339      1438  LOAD_FAST                'secure_outpath'
 #             1440  BUILD_LIST_10        10
 #             1442  CALL_FUNCTION_1       1  '1 positional argument'
 #             1444  POP_TOP
 #             1446  JUMP_BACK          1268  'to 1268'
 #             1450  POP_BLOCK
 #           1452_0  COME_FROM_LOOP     1258  '1258'
 #             1452  JUMP_FORWARD       2014  'to 2014'
 #             1456  ELSE                     '2014'
 #
 # L. 341      1456  LOAD_FAST                'self'
 #             1458  LOAD_ATTR                seek_code
 #             1460  LOAD_FAST                'a_meta'
 #             1462  LOAD_ATTR                checksum
 #             1464  CALL_FUNCTION_1       1  '1 positional argument'
 #             1466  STORE_FAST               'act_code'
 #
 # L. 342      1468  LOAD_FAST                'ext'
 #             1470  LOAD_ATTR                lower
 #             1472  CALL_FUNCTION_0       0  '0 positional arguments'
 #             1474  LOAD_STR                 '.m4b'
 #             1476  COMPARE_OP               ==
 #             1478  POP_JUMP_IF_FALSE  1750  'to 1750'
 #
 # L. 343      1482  SETUP_LOOP         2014  'to 2014'
 #             1486  LOAD_GLOBAL              enumerate
 #             1488  LOAD_FAST                'split_points'
 #             1490  CALL_FUNCTION_1       1  '1 positional argument'
 #             1492  GET_ITER
 #             1494  FOR_ITER           1744  'to 1744'
 #             1496  UNPACK_SEQUENCE_2     2
 #             1498  STORE_FAST               'idx'
 #             1500  STORE_FAST               'item_'
 #
 # L. 344      1502  LOAD_GLOBAL              os
 #             1504  LOAD_ATTR                path
 #             1506  LOAD_ATTR                join
 #             1508  LOAD_DEREF               'outdir'
 #             1510  LOAD_FAST                'name'
 #             1512  LOAD_STR                 '--%04d'
 #             1514  LOAD_FAST                'idx'
 #             1516  LOAD_CONST               1
 #             1518  BINARY_ADD
 #             1520  BINARY_MODULO
 #             1522  BINARY_ADD
 #             1524  LOAD_FAST                'ext'
 #             1526  BINARY_ADD
 #             1528  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1530  STORE_FAST               'secure_outpath'
 #
 # L. 345      1532  LOAD_STR                 'title="'
 #             1534  LOAD_FAST                'name'
 #             1536  BINARY_ADD
 #             1538  LOAD_STR                 '--%04d'
 #             1540  LOAD_FAST                'idx'
 #             1542  LOAD_CONST               1
 #             1544  BINARY_ADD
 #             1546  BINARY_MODULO
 #             1548  BINARY_ADD
 #             1550  LOAD_STR                 '"'
 #             1552  BINARY_ADD
 #             1554  STORE_FAST               'title'
 #
 # L. 346      1556  LOAD_GLOBAL              len
 #             1558  LOAD_FAST                'secure_outpath'
 #             1560  CALL_FUNCTION_1       1  '1 positional argument'
 #             1562  STORE_FAST               'path_length'
 #
 # L. 347      1564  LOAD_FAST                'path_length'
 #             1566  LOAD_CONST               245
 #             1568  COMPARE_OP               >
 #             1570  POP_JUMP_IF_FALSE  1616  'to 1616'
 #
 # L. 348      1574  LOAD_GLOBAL              os
 #             1576  LOAD_ATTR                path
 #             1578  LOAD_ATTR                join
 #             1580  LOAD_DEREF               'outdir'
 #
 # L. 349      1582  LOAD_FAST                'name'
 #             1584  LOAD_CONST               None
 #             1586  LOAD_CONST               245
 #             1588  LOAD_FAST                'path_length'
 #             1590  BINARY_SUBTRACT
 #             1592  BUILD_SLICE_2         2
 #             1594  BINARY_SUBSCR
 #             1596  LOAD_STR                 '--%04d'
 #             1598  LOAD_FAST                'idx'
 #             1600  LOAD_CONST               1
 #             1602  BINARY_ADD
 #             1604  BINARY_MODULO
 #             1606  BINARY_ADD
 #             1608  LOAD_FAST                'ext'
 #             1610  BINARY_ADD
 #             1612  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1614  STORE_FAST               'secure_outpath'
 #           1616_0  COME_FROM          1570  '1570'
 #
 # L. 350      1616  LOAD_FAST                'cmds'
 #             1618  LOAD_ATTR                append
 #             1620  LOAD_STR                 '-y'
 #             1622  LOAD_STR                 '-activation_bytes'
 #             1624  LOAD_FAST                'act_code'
 #
 # L. 351      1626  LOAD_STR                 '-i'
 #
 # L. 352      1628  LOAD_FAST                'filepath'
 #
 # L. 353      1630  LOAD_STR                 '-ss'
 #             1632  LOAD_GLOBAL              str
 #             1634  LOAD_FAST                'item_'
 #             1636  LOAD_CONST               0
 #             1638  BINARY_SUBSCR
 #             1640  CALL_FUNCTION_1       1  '1 positional argument'
 #             1642  LOAD_STR                 '-t'
 #             1644  LOAD_GLOBAL              str
 #             1646  LOAD_FAST                'item_'
 #             1648  LOAD_CONST               1
 #             1650  BINARY_SUBSCR
 #             1652  LOAD_FAST                'item_'
 #             1654  LOAD_CONST               0
 #             1656  BINARY_SUBSCR
 #             1658  BINARY_SUBTRACT
 #             1660  CALL_FUNCTION_1       1  '1 positional argument'
 #
 # L. 354      1662  LOAD_STR                 '-vn'
 #             1664  LOAD_STR                 '-c:a'
 #             1666  LOAD_STR                 'copy'
 #
 # L. 355      1668  LOAD_STR                 '-metadata'
 #
 # L. 356      1670  LOAD_FAST                'title'
 #
 # L. 357      1672  LOAD_STR                 '-metadata'
 #             1674  LOAD_STR                 'album=%s'
 #             1676  LOAD_FAST                'a_meta'
 #             1678  LOAD_ATTR                album
 #             1680  BINARY_MODULO
 #
 # L. 358      1682  LOAD_STR                 '-metadata'
 #             1684  LOAD_STR                 'artist=%s'
 #             1686  LOAD_FAST                'a_meta'
 #             1688  LOAD_ATTR                artist
 #             1690  BINARY_MODULO
 #
 # L. 359      1692  LOAD_STR                 '-metadata'
 #             1694  LOAD_STR                 'copyright=%s'
 #             1696  LOAD_FAST                'a_meta'
 #             1698  LOAD_ATTR                copyright
 #             1700  BINARY_MODULO
 #
 # L. 360      1702  LOAD_STR                 '-metadata'
 #             1704  LOAD_STR                 'date=%s'
 #             1706  LOAD_FAST                'a_meta'
 #             1708  LOAD_ATTR                year
 #             1710  BINARY_MODULO
 #
 # L. 361      1712  LOAD_STR                 '-metadata'
 #             1714  LOAD_STR                 'genre=%s'
 #             1716  LOAD_FAST                'a_meta'
 #             1718  LOAD_ATTR                genre
 #             1720  BINARY_MODULO
 #
 # L. 362      1722  LOAD_STR                 '-metadata'
 #             1724  LOAD_STR                 'comment=%s'
 #             1726  LOAD_FAST                'a_meta'
 #             1728  LOAD_ATTR                comments
 #             1730  BINARY_MODULO
 #
 # L. 363      1732  LOAD_FAST                'secure_outpath'
 #             1734  BUILD_LIST_27        27
 #             1736  CALL_FUNCTION_1       1  '1 positional argument'
 #             1738  POP_TOP
 #             1740  JUMP_BACK          1494  'to 1494'
 #             1744  POP_BLOCK
 #             1746  JUMP_FORWARD       2014  'to 2014'
 #             1750  ELSE                     '2014'
 #
 # L. 365      1750  SETUP_LOOP         2014  'to 2014'
 #             1754  LOAD_GLOBAL              enumerate
 #             1756  LOAD_FAST                'split_points'
 #             1758  CALL_FUNCTION_1       1  '1 positional argument'
 #             1760  GET_ITER
 #             1762  FOR_ITER           2012  'to 2012'
 #             1764  UNPACK_SEQUENCE_2     2
 #             1766  STORE_FAST               'idx'
 #             1768  STORE_FAST               'item_'
 #
 # L. 366      1770  LOAD_GLOBAL              os
 #             1772  LOAD_ATTR                path
 #             1774  LOAD_ATTR                join
 #             1776  LOAD_DEREF               'outdir'
 #             1778  LOAD_FAST                'name'
 #             1780  LOAD_STR                 '--%04d'
 #             1782  LOAD_FAST                'idx'
 #             1784  LOAD_CONST               1
 #             1786  BINARY_ADD
 #             1788  BINARY_MODULO
 #             1790  BINARY_ADD
 #             1792  LOAD_FAST                'ext'
 #             1794  BINARY_ADD
 #             1796  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1798  STORE_FAST               'secure_outpath'
 #
 # L. 367      1800  LOAD_STR                 'title="'
 #             1802  LOAD_FAST                'name'
 #             1804  BINARY_ADD
 #             1806  LOAD_STR                 '--%04d'
 #             1808  LOAD_FAST                'idx'
 #             1810  LOAD_CONST               1
 #             1812  BINARY_ADD
 #             1814  BINARY_MODULO
 #             1816  BINARY_ADD
 #             1818  LOAD_STR                 '"'
 #             1820  BINARY_ADD
 #             1822  STORE_FAST               'title'
 #
 # L. 368      1824  LOAD_GLOBAL              len
 #             1826  LOAD_FAST                'secure_outpath'
 #             1828  CALL_FUNCTION_1       1  '1 positional argument'
 #             1830  STORE_FAST               'path_length'
 #
 # L. 369      1832  LOAD_FAST                'path_length'
 #             1834  LOAD_CONST               245
 #             1836  COMPARE_OP               >
 #             1838  POP_JUMP_IF_FALSE  1884  'to 1884'
 #
 # L. 370      1842  LOAD_GLOBAL              os
 #             1844  LOAD_ATTR                path
 #             1846  LOAD_ATTR                join
 #             1848  LOAD_DEREF               'outdir'
 #
 # L. 371      1850  LOAD_FAST                'name'
 #             1852  LOAD_CONST               None
 #             1854  LOAD_CONST               245
 #             1856  LOAD_FAST                'path_length'
 #             1858  BINARY_SUBTRACT
 #             1860  BUILD_SLICE_2         2
 #             1862  BINARY_SUBSCR
 #             1864  LOAD_STR                 '--%04d'
 #             1866  LOAD_FAST                'idx'
 #             1868  LOAD_CONST               1
 #             1870  BINARY_ADD
 #             1872  BINARY_MODULO
 #             1874  BINARY_ADD
 #             1876  LOAD_FAST                'ext'
 #             1878  BINARY_ADD
 #             1880  CALL_FUNCTION_2       2  '2 positional arguments'
 #             1882  STORE_FAST               'secure_outpath'
 #           1884_0  COME_FROM          1838  '1838'
 #
 # L. 372      1884  LOAD_FAST                'cmds'
 #             1886  LOAD_ATTR                append
 #             1888  LOAD_STR                 '-y'
 #             1890  LOAD_STR                 '-activation_bytes'
 #             1892  LOAD_FAST                'act_code'
 #
 # L. 373      1894  LOAD_STR                 '-i'
 #
 # L. 374      1896  LOAD_FAST                'filepath'
 #
 # L. 375      1898  LOAD_STR                 '-ss'
 #             1900  LOAD_GLOBAL              str
 #             1902  LOAD_FAST                'item_'
 #             1904  LOAD_CONST               0
 #             1906  BINARY_SUBSCR
 #             1908  CALL_FUNCTION_1       1  '1 positional argument'
 #             1910  LOAD_STR                 '-t'
 #             1912  LOAD_GLOBAL              str
 #             1914  LOAD_FAST                'item_'
 #             1916  LOAD_CONST               1
 #             1918  BINARY_SUBSCR
 #             1920  LOAD_FAST                'item_'
 #             1922  LOAD_CONST               0
 #             1924  BINARY_SUBSCR
 #             1926  BINARY_SUBTRACT
 #             1928  CALL_FUNCTION_1       1  '1 positional argument'
 #
 # L. 376      1930  LOAD_STR                 '-vn'
 #
 # L. 377      1932  LOAD_STR                 '-id3v2_version'
 #             1934  LOAD_STR                 '3'
 #
 # L. 378      1936  LOAD_STR                 '-metadata'
 #
 # L. 379      1938  LOAD_FAST                'title'
 #
 # L. 380      1940  LOAD_STR                 '-metadata'
 #             1942  LOAD_STR                 'album=%s'
 #             1944  LOAD_FAST                'a_meta'
 #             1946  LOAD_ATTR                album
 #             1948  BINARY_MODULO
 #
 # L. 381      1950  LOAD_STR                 '-metadata'
 #             1952  LOAD_STR                 'artist=%s'
 #             1954  LOAD_FAST                'a_meta'
 #             1956  LOAD_ATTR                artist
 #             1958  BINARY_MODULO
 #
 # L. 382      1960  LOAD_STR                 '-metadata'
 #             1962  LOAD_STR                 'copyright=%s'
 #             1964  LOAD_FAST                'a_meta'
 #             1966  LOAD_ATTR                copyright
 #             1968  BINARY_MODULO
 #
 # L. 383      1970  LOAD_STR                 '-metadata'
 #             1972  LOAD_STR                 'date=%s'
 #             1974  LOAD_FAST                'a_meta'
 #             1976  LOAD_ATTR                year
 #             1978  BINARY_MODULO
 #
 # L. 384      1980  LOAD_STR                 '-metadata'
 #             1982  LOAD_STR                 'genre=%s'
 #             1984  LOAD_FAST                'a_meta'
 #             1986  LOAD_ATTR                genre
 #             1988  BINARY_MODULO
 #
 # L. 385      1990  LOAD_STR                 '-metadata'
 #             1992  LOAD_STR                 'comment=%s'
 #             1994  LOAD_FAST                'a_meta'
 #             1996  LOAD_ATTR                comments
 #             1998  BINARY_MODULO
 #
 # L. 386      2000  LOAD_FAST                'secure_outpath'
 #             2002  BUILD_LIST_27        27
 #             2004  CALL_FUNCTION_1       1  '1 positional argument'
 #             2006  POP_TOP
 #             2008  JUMP_BACK          1762  'to 1762'
 #             2012  POP_BLOCK
 #           2014_0  COME_FROM_LOOP     1750  '1750'
 #           2014_1  COME_FROM          1746  '1746'
 #           2014_2  COME_FROM          1452  '1452'
 #
 # L. 387      2014  SETUP_LOOP         2224  'to 2224'
 #             2016  LOAD_GLOBAL              enumerate
 #             2018  LOAD_FAST                'cmds'
 #             2020  CALL_FUNCTION_1       1  '1 positional argument'
 #             2022  GET_ITER
 #             2024  FOR_ITER           2222  'to 2222'
 #             2026  UNPACK_SEQUENCE_2     2
 #             2028  STORE_FAST               'idx'
 #             2030  STORE_FAST               'cmd'
 #
 # L. 388      2032  LOAD_GLOBAL              subprocess
 #             2034  LOAD_ATTR                Popen
 #             2036  LOAD_FAST                'self'
 #             2038  LOAD_ATTR                EXE
 #             2040  BUILD_LIST_1          1
 #             2042  LOAD_FAST                'cmd'
 #             2044  BINARY_ADD
 #             2046  LOAD_GLOBAL              subprocess
 #             2048  LOAD_ATTR                PIPE
 #             2050  LOAD_CONST               True
 #
 # L. 389      2052  LOAD_FAST                'startupinfo'
 #             2054  LOAD_CONST               ('stderr', 'universal_newlines', 'startupinfo')
 #             2056  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
 #             2058  STORE_FAST               'proc'
 #
 # L. 390      2060  SETUP_LOOP         2202  'to 2202'
 #             2062  LOAD_FAST                'proc'
 #             2064  LOAD_ATTR                poll
 #             2066  CALL_FUNCTION_0       0  '0 positional arguments'
 #             2068  LOAD_CONST               None
 #             2070  COMPARE_OP               is
 #             2072  POP_JUMP_IF_FALSE  2200  'to 2200'
 #
 # L. 391      2076  SETUP_EXCEPT       2092  'to 2092'
 #
 # L. 392      2078  LOAD_FAST                'proc'
 #             2080  LOAD_ATTR                stderr
 #             2082  LOAD_ATTR                readline
 #             2084  CALL_FUNCTION_0       0  '0 positional arguments'
 #             2086  STORE_FAST               'content'
 #             2088  POP_BLOCK
 #             2090  JUMP_FORWARD       2118  'to 2118'
 #           2092_0  COME_FROM_EXCEPT   2076  '2076'
 #
 # L. 393      2092  DUP_TOP
 #             2094  LOAD_GLOBAL              UnicodeDecodeError
 #             2096  COMPARE_OP               exception-match
 #             2098  POP_JUMP_IF_FALSE  2116  'to 2116'
 #             2102  POP_TOP
 #             2104  POP_TOP
 #             2106  POP_TOP
 #
 # L. 394      2108  LOAD_STR                 ''
 #             2110  STORE_FAST               'content'
 #             2112  POP_EXCEPT
 #             2114  JUMP_FORWARD       2118  'to 2118'
 #             2116  END_FINALLY
 #           2118_0  COME_FROM          2114  '2114'
 #           2118_1  COME_FROM          2090  '2090'
 #
 # L. 395      2118  LOAD_STR                 'size='
 #             2120  LOAD_FAST                'content'
 #             2122  COMPARE_OP               in
 #             2124  POP_JUMP_IF_FALSE  2062  'to 2062'
 #
 # L. 396      2128  LOAD_GLOBAL              int
 #
 # L. 397      2130  LOAD_FAST                'self'
 #             2132  LOAD_ATTR                timestamp
 #             2134  LOAD_FAST                'content'
 #             2136  CALL_FUNCTION_1       1  '1 positional argument'
 #             2138  LOAD_FAST                'split_points'
 #             2140  LOAD_FAST                'idx'
 #             2142  BINARY_SUBSCR
 #             2144  LOAD_CONST               0
 #             2146  BINARY_SUBSCR
 #             2148  BINARY_ADD
 #             2150  LOAD_FAST                'duration'
 #             2152  BINARY_TRUE_DIVIDE
 #             2154  LOAD_CONST               100
 #             2156  BINARY_MULTIPLY
 #             2158  CALL_FUNCTION_1       1  '1 positional argument'
 #             2160  DUP_TOP
 #             2162  STORE_FAST               '_progress'
 #             2164  STORE_FAST               '_progress'
 #
 # L. 398      2166  LOAD_FAST                '_progress'
 #             2168  LOAD_FAST                'progress'
 #             2170  COMPARE_OP               >
 #             2172  POP_JUMP_IF_FALSE  2062  'to 2062'
 #
 # L. 399      2176  LOAD_FAST                '_progress'
 #             2178  STORE_FAST               'progress'
 #
 # L. 400      2180  LOAD_FAST                'progress'
 #             2182  LOAD_FAST                'item'
 #             2184  STORE_ATTR               rate
 #
 # L. 401      2186  LOAD_FAST                'signal'
 #             2188  LOAD_ATTR                emit
 #             2190  LOAD_FAST                'item'
 #             2192  CALL_FUNCTION_1       1  '1 positional argument'
 #             2194  POP_TOP
 #             2196  JUMP_BACK          2062  'to 2062'
 #           2200_0  COME_FROM          2072  '2072'
 #             2200  POP_BLOCK
 #           2202_0  COME_FROM_LOOP     2060  '2060'
 #
 # L. 402      2202  LOAD_FAST                'proc'
 #             2204  LOAD_ATTR                returncode
 #             2206  LOAD_CONST               0
 #             2208  COMPARE_OP               !=
 #             2210  POP_JUMP_IF_FALSE  2024  'to 2024'
 #
 # L. 403      2214  LOAD_STR                 ''
 #             2216  RETURN_VALUE
 #             2218  JUMP_BACK          2024  'to 2024'
 #             2222  POP_BLOCK
 #           2224_0  COME_FROM_LOOP     2014  '2014'
 #
 # L. 405      2224  LOAD_GLOBAL              os
 #             2226  LOAD_ATTR                listdir
 #             2228  LOAD_DEREF               'outdir'
 #             2230  CALL_FUNCTION_1       1  '1 positional argument'
 #             2232  STORE_FAST               'files'
 #
 # L. 406      2234  LOAD_CLOSURE             'outdir'
 #             2236  BUILD_TUPLE_1         1
 #             2238  LOAD_LISTCOMP            '<code_object <listcomp>>'
 #             2240  LOAD_STR                 'AudibleConvert.process.<locals>.<listcomp>'
 #             2242  MAKE_FUNCTION_8          'closure'
 #             2244  LOAD_FAST                'files'
 #             2246  GET_ITER
 #             2248  CALL_FUNCTION_1       1  '1 positional argument'
 #             2250  STORE_FAST               'files'
 #
 # L. 407      2252  SETUP_LOOP         2308  'to 2308'
 #             2254  LOAD_FAST                'files'
 #             2256  GET_ITER
 #             2258  FOR_ITER           2306  'to 2306'
 #             2260  STORE_FAST               'f'
 #
 # L. 408      2262  LOAD_FAST                'ext'
 #             2264  LOAD_STR                 '.mp3'
 #             2266  COMPARE_OP               ==
 #             2268  POP_JUMP_IF_FALSE  2288  'to 2288'
 #
 # L. 409      2272  LOAD_FAST                'self'
 #             2274  LOAD_ATTR                set_mp3_cover
 #             2276  LOAD_FAST                'f'
 #             2278  LOAD_FAST                'a_meta'
 #             2280  LOAD_ATTR                cover
 #             2282  CALL_FUNCTION_2       2  '2 positional arguments'
 #             2284  POP_TOP
 #             2286  JUMP_FORWARD       2302  'to 2302'
 #             2288  ELSE                     '2302'
 #
 # L. 411      2288  LOAD_FAST                'self'
 #             2290  LOAD_ATTR                set_m4b_cover
 #             2292  LOAD_FAST                'f'
 #             2294  LOAD_FAST                'a_meta'
 #             2296  LOAD_ATTR                cover
 #             2298  CALL_FUNCTION_2       2  '2 positional arguments'
 #             2300  POP_TOP
 #           2302_0  COME_FROM          2286  '2286'
 #             2302  JUMP_BACK          2258  'to 2258'
 #             2306  POP_BLOCK
 #           2308_0  COME_FROM_LOOP     2252  '2252'
 #
 # L. 413      2308  LOAD_DEREF               'outdir'
 #             2310  RETURN_VALUE



    def get_chapters(self, filepath):
        typ = self.check_type(filepath)
        if typ == 'aa':
            one_k = 1000
            pattern = 'bitrate: (\\d{2,3})'
            process = QProcess()
            process.start(self.EXE, ['-i', filepath])
            process.waitForFinished(-1)
            output = process.readAllStandardError().data().decode(errors='ignore')
            bitrate = re.search(pattern, output).group(1)
            bytes_per_second = int(bitrate) / 8 * one_k
            MAGIC = b'\xff\xff\xff\xff\xff\xff\xff\xff'
            fp = open(filepath, 'rb')
            contents = fp.read()
            idxs = [i.start() for i in re.finditer(MAGIC, contents)]
            points = []
            for idx in idxs:
                fp.seek(idx + len(MAGIC))
                packed_data = fp.read(4)
                point = unpack('>i', packed_data)[0]
                points.append(point)

            points = [p / bytes_per_second for p in points]
            result = []
            for i in range(len(points)):
                result.append([sum(points[:i]), sum(points[:i + 1]) + 1])

            return result
        else:
            pattern = '(\\d+\\.\\d{6})'
            process = QProcess()
            process.start(self.EXE, ['-i', filepath])
            process.waitForFinished(-1)
            output = process.readAllStandardError().data().decode(errors='ignore')
            rs = []
            for line in output.split('\n'):
                if line.strip().startswith('Chapter #'):
                    r = re.findall(pattern, line)
                    rs.append(r)

            rs = [[float(i[0]), float(i[1])] for i in rs]
            return rs

    @staticmethod
    def timestamp(output):
        pattern = 'time=(\\d{2,}):(\\d{2})+:(\\d{2})+\\.'
        r = re.findall(pattern, output)
        stamp = int(r[0][0]) * 3600 + int(r[0][1]) * 60 + int(r[0][2])
        return stamp

    def set_mp3_meta(self, filepath, meta):
        _, name = os.path.split(filepath)
        tmpfile = os.path.join(TMPDIR, name)
        process = QProcess()
        process.start(self.EXE, ['-i', filepath, '-c', 'copy', '-id3v2_version', '3',
         '-metadata', 'title=%s' % meta.title,
         '-metadata', 'album=%s' % meta.album,
         '-metadata', 'artist=%s' % meta.artist,
         '-metadata', 'copyright=%s' % meta.copyright,
         '-metadata', 'date=%s' % meta.year,
         '-metadata', 'genre=%s' % meta.genre,
         '-metadata', 'comment=%s' % meta.comments,
         tmpfile])
        process.waitForStarted()
        process.waitForFinished(-1)
        shutil.move(tmpfile, filepath)

    def set_m4b_meta(self, filepath, meta):
        _, name = os.path.split(filepath)
        tmpfile = os.path.join(TMPDIR, name)
        process = QProcess()
        process.start(self.EXE, ['-i', filepath, '-c:a', 'copy',
         '-metadata', 'title=%s' % meta.title,
         '-metadata', 'album=%s' % meta.album,
         '-metadata', 'artist=%s' % meta.artist,
         '-metadata', 'copyright=%s' % meta.copyright,
         '-metadata', 'date=%s' % meta.year,
         '-metadata', 'genre=%s' % meta.genre,
         '-metadata', 'comment=%s' % meta.comments,
         tmpfile])
        process.waitForStarted()
        process.waitForFinished(-1)
        shutil.move(tmpfile, filepath)

    def set_mp3_cover(self, filepath, cover):
        _, name = os.path.split(filepath)
        tmpfile = os.path.join(TMPDIR, name)
        process = QProcess()
        process.start(self.EXE, [
         '-i', filepath, '-i', cover, '-map', '0:0', '-map', '1:0', '-c', 'copy', '-id3v2_version', '3',
         tmpfile])
        process.waitForStarted()
        process.waitForFinished(-1)
        shutil.move(tmpfile, filepath)

    @staticmethod
    def set_m4b_cover(filepath, cover):
        _, name = os.path.split(filepath)
        tmpfile = os.path.join(TMPDIR, name)
        out = open(filepath, 'rb').read()
        cov = open(cover, 'rb').read()
        cov_len = len(cov)
        idx_moov = out.rfind(b'moov')
        old_moov_bytes = out[idx_moov - 4:idx_moov]
        old_moov_size = unpack('>i', old_moov_bytes)[0]
        new_moov_size = old_moov_size + cov_len + 24
        new_moov_bytes = pack('>i', new_moov_size)
        out = out[:idx_moov - 4] + new_moov_bytes + out[idx_moov:]
        idx_meta = out.find(b'meta', idx_moov)
        old_meta_bytes = out[idx_meta - 4:idx_meta]
        old_meta_size = unpack('>i', old_meta_bytes)[0]
        new_meta_size = old_meta_size + cov_len + 24
        new_meta_bytes = pack('>i', new_meta_size)
        out = out[:idx_meta - 4] + new_meta_bytes + out[idx_meta:]
        idx_udta = out.find(b'udta', idx_moov)
        old_udta_bytes = out[idx_udta - 4:idx_udta]
        old_udta_size = unpack('>i', old_udta_bytes)[0]
        new_udta_size = old_udta_size + cov_len + 24
        new_udta_bytes = pack('>i', new_udta_size)
        out = out[:idx_udta - 4] + new_udta_bytes + out[idx_udta:]
        idx_ilst = out.find(b'ilst', idx_udta)
        old_ilst_bytes = out[idx_ilst - 4:idx_ilst]
        old_ilst_size = unpack('>i', old_ilst_bytes)[0]
        new_ilst_size = old_ilst_size + cov_len + 24
        new_ilst_bytes = pack('>i', new_ilst_size)
        out = out[:idx_ilst - 4] + new_ilst_bytes + out[idx_ilst:]
        idx_chpl = out.find(b'chpl', idx_ilst)
        covr_len_bytes = pack('>i', cov_len + 24)
        data_len_bytes = pack('>i', cov_len + 24 - 8)
        covr_box_bytes = covr_len_bytes + b'covr' + data_len_bytes + b'data' + b'\x00\x00\x00\r\x00\x00\x00\x00' + cov
        out = out[:idx_chpl - 4] + covr_box_bytes + out[idx_chpl - 4:]
        open(tmpfile, 'wb').write(out)
        shutil.move(tmpfile, filepath)

    @staticmethod
    def validate_title(title):
        rstr = '[\\/\\\\\\:\\*\\?\\"\\<\\>\\|]'
        new_title = re.sub(rstr, '_', title)
        return new_title


if __name__ == '__main__':
    audible = AudibleConvert(os.path.join(os.environ['APPDATA'], '.EpuborAudible'))
    audible.getMeta('./x.aa')