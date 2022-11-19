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
            exe = os.path.abspath('.\\bin\\win_rcrack.exe')
            tables = os.path.abspath('.\\bin\\tables')
            commands = [exe,tables, '-h', checksum]
            command  = " ".join(commands)
            process.start(exe,[tables, '-h', checksum])
            # process.start('cmd', ['echo hello world'])
            process.waitForStarted()
            process.waitForFinished(-1)
            output = process.readAllStandardOutput().data().decode().strip()
            r = os.popen(command)
            output = os.system(command)
            output = r.read()
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

        if checksum in self.d:
            if self.d[checksum]:
                if self.verify_code(self.d[checksum]):
                    return self.d[checksum]
        code = ''
        if code or '64bit' in platform.architecture():
            code = self.compute(checksum)
        else:
            code = self.get_key_from_server(checksum)
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

        progress = 0
        a_meta = item.audibleMeta
        filepath = item.filepath
        duration = a_meta.duration
        hours,mins,secs = duration[:-3].split(':')
        duration = int(secs) + 60 * int(mins) + 3600 * int(hours)
        convparam = item.convertParam
        split_points = []
        if 0 == convparam[0]:
            split_points = [[0,duration]]
        else:
            if convparam[0] == 1:
                 dur_per_one = convparam[1] * 60
                 m,n = divmod(duration,dur_per_one)
                 for i in range(m):
                     split_points.append([i * dur_per_one, (1 + i) * dur_per_one])
                 if n:
                     split_points.append([duration-n,duration])
            else:
                 if convparam[0] == 2:
                     file_num = convparam[1]
                     dur_per_one = int(duration / file_num)
                     for i in range(file_num - 1):
                         split_points.append([dur_per_one * i, dur_per_one * (i + 1)])
                     split_points.append([dur_per_one * (file_num - 1), duration])
            if convparam[0] == 3:
                split_points = self.get_chapters(filepath)
        mime = item.filetype
        startupinfo = None
        if os.sep == "\\":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags = startupinfo.dwFlags | subprocess.STARTF_USESHOWWINDOW
        if self.isRegister is False:
            outname = self.validate_title(a_meta.title) + ext
            outpath = os.path.join(self.outputPath, outname)
            if len(outpath) > 245:
                outpath = outpath[None:240] + ext
            outpath = choosename(outpath)
            if mime == 'aa':

                args = ['-y', '-i', filepath, '-ss', '0', '-t', '600', outpath]
            else:
                act_code = self.seek_code(a_meta.checksum)
                if act_code is False:
                    act_code = ""
                args = ['-y', '-activation_bytes', act_code, '-i', filepath, '-ss', '0', '-t', '600', '-vn', outpath]
            proc = subprocess.Popen([self.EXE] + args, stderr=subprocess.PIPE, universal_newlines=True,
                                    startupinfo=startupinfo)
            while proc.poll() is None:
                try:
                    content = proc.stderr.readline()
                except UnicodeDecodeError:
                    content = ""
                if 'size=' not in content:
                    continue
            

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