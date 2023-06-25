# decompyle3 version 3.8.0
# Python bytecode 3.7.0 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\ws\AppData\Local\Temp\tmphkf2lm_t\Cookies\BrowserCookie.py
# Compiled at: 2022-04-11 10:34:06
# Size of source mod 2**32: 26098 bytes
import getpass
import http.cookiejar
import os, sys, time, glob
import pickle

from http.cookiejar import *

import tempfile
from ctypes import *
import re

import keyring

needLogging = False
if needLogging:
    import logging
    log_file = '/Users/admin/Desktop/123/1.log'
    logging.basicConfig(filename=log_file, level=(logging.DEBUG))

def debugEx(obj):
    if needLogging:
        import logging
        logging.debug(obj)


debugEx(sys.path)
scriptPath = sys.path[0]
try:
    import json
except ImportError:
    import simplejson as json

if sys.platform == 'win32':
    debugEx('-------CDLL(sqlite3.dll)------------')
    debugEx(scriptPath)
    sys.path.insert(0, os.path.join(scriptPath, 'Cookies\\win32crypt'))
    sys.path.insert(0, os.path.join(scriptPath, 'Cookies'))
    filePath = os.path.join(scriptPath, 'Cookies\\sqlite\\sqlite3.dll')
    debugEx(filePath)
    if os.path.isfile(filePath):
        if sys.version_info < (3, 0):
            CDLL(filePath)
        debugEx('load success')
    else:
        debugEx('load fail')
    import sqlite3
    debugEx(sqlite3.sqlite_version)
else:
    import sqlite3
    debugEx(sqlite3.sqlite_version)
debugEx('--------------------------------------------------------------')
if sys.platform == 'win32':
    try:
        import win32crypt
    except ImportError:
        debugEx("Couldn't import module 'win32crypt'; cookie decryption on Windows disabled.\n")

    debugEx('win32 --------------------------------------------------------------')

class BrowserCookieError(Exception):
    pass
def _get_config_dir() -> str:
    if sys.platform == "win32":
        # on Windows, use %LOCALAPPDATA%\Instaloader
        localappdata = os.getenv("LOCALAPPDATA")
        if localappdata is not None:
            return os.path.join(localappdata, "cookie")
        # legacy fallback - store in temp dir if %LOCALAPPDATA% is not set
        return os.path.join(tempfile.gettempdir(), ".cookie-" + getpass.getuser())
    return os.path.join(os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config")), "instaloader")
def get_default_session_filename():
    """Returns default session filename for given username."""
    configdir = _get_config_dir()
    sessionfilename = "session-{}".format("key")
    return os.path.join(configdir, sessionfilename)
def savekey(cookies,saveFile):
    if not os.path.exists(os.path.dirname(saveFile)):
        os.makedirs(os.path.dirname(saveFile))
    f = open(saveFile,"wb")
    pickle.dump(cookies,f,0)
    f.close()

def loadkey(saveFile):
    try:
        f = open(saveFile, "rb")
        cookies =  pickle.load(f)
        f.close()
    except Exception as e:
        return
    return cookies
class Mackey:
    def __init__(self,keyvalue):
        self.key = keyvalue
        self.create_time = time.time()
    def get_key(self):
        return self.key
    def get_create_time(self):
        return self.create_time

def create_local_copy(cookie_file):
    """Make a local copy of the sqlite cookie database and return the new filename.
    This is necessary in case this database is still being written to while the user browses
    to avoid sqlite locking errors.
    """
    if os.path.exists(cookie_file):
        from shutil import copyfile
        tmp_file = tempfile.NamedTemporaryFile(suffix='.sqlite').name
        copyfile(cookie_file, tmp_file)
        return tmp_file
    raise BrowserCookieError('Can not find cookie file at: ' + cookie_file)


class Chrome:
    tmp_file = None

    def __init__(self, cookie_file=None):
        salt = b'saltysalt'
        length = 16
        my_pass = None
        if sys.platform == 'win32':
            appdata = os.getenv('APPDATA')
            chromeDefaultPath = '%s\\..\\Local\\Google\\Chrome\\User Data' % appdata
            Local_State = '%s%s' % (chromeDefaultPath, '\\Local State')
            if not os.path.isfile(Local_State):
                chromeDefaultPath =  '%s\\..\\Local\\Temp\\Google\\Chrome\\User Data' % appdata
                Local_State = '%s%s' % (chromeDefaultPath, '\\Local State')
            try:
                if os.path.isfile(Local_State):
                    with open(Local_State, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if 'profile' in data:
                            if 'last_userd' in data['profile']:
                                last_used = data['profile']['last_used']
                            elif 'last_active_profiles' in data['profile']:
                                if len(data['profile']['last_active_profiles']) > 0:
                                    last_used = data['profile']['last_active_profiles'][0]
                                else:
                                    last_used = "Default"
                            chromeDefaultPath = '%s\\%s' % (chromeDefaultPath, last_used)
                            cookie_file = '%s%s' % (chromeDefaultPath, '\\cookies')
                            if not os.path.isfile(cookie_file):
                                cookie_file = '%s%s' % (chromeDefaultPath, '\\network\\cookies')
            except Exception as ex:
                try:
                    print(ex)
                finally:
                    ex = None
                    del ex

            if not os.path.isfile(cookie_file):
                chromeDefaultPath = '%s\\..\\Local\\Google\\Chrome\\User Data\\Default' % appdata
                cookie_file = '%s%s' % (chromeDefaultPath, '\\cookies')
            if not os.path.isfile(cookie_file):
                chromeDefaultPath = '%s\\..\\Local\\Google\\Chrome\\User Data\\Profile 1' % appdata
                cookie_file = '%s%s' % (chromeDefaultPath, '\\cookies')
            if not os.path.isfile(cookie_file):
                chromeDefaultPath = '%s\\..\\Local\\Google\\Chrome\\User Data\\Profile 1\\network' % appdata
                cookie_file = '%s%s' % (chromeDefaultPath, '\\cookies')
        else:
            from keyring import get_password
            if sys.platform == 'darwin':
                cookie_file = None
                chromeDefaultPath = os.path.expanduser('~/Library/Application Support/Google/Chrome')
                Local_State = '%s%s' % (chromeDefaultPath, '/Local State')
                try:
                    if os.path.isfile(Local_State):
                        with open(Local_State, 'r') as f:
                            data = json.load(f)
                            if 'profile' in data:
                                if 'last_used' in data['profile']:
                                    last_used = data['profile']['last_used']
                                elif 'last_active_profiles' in data['profile']:
                                    last_used = data['profile']['last_active_profiles'][0]
                                chromeDefaultPath = '%s/%s' % (chromeDefaultPath, last_used)
                                cookie_file = '%s%s' % (chromeDefaultPath, '/Cookies')
                                if not os.path.isfile(cookie_file):
                                    cookie_file = '%s%s' % (chromeDefaultPath, '/network/Cookies')
                except Exception as ex:
                    try:
                        print(ex)
                    finally:
                        ex = None
                        del ex

                print(cookie_file)
                if not os.path.exists(cookie_file):
                    cookie_file = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/Cookies')
                    if not os.path.exists(cookie_file):
                        cookie_file = os.path.expanduser('~/Library/Application Support/Google/Chrome/Default/network/Cookies')
                        if not os.path.exists(cookie_file):
                            cookie_file = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/Cookies')
                            if not os.path.exists(cookie_file):
                                cookie_file = os.path.expanduser('~/Library/Application Support/Google/Chrome/Profile 1/network/Cookies')
                self.key = None

                if os.path.exists(cookie_file):
                    keyname = get_default_session_filename()
                    if os.path.exists(keyname):
                        key = loadkey(keyname)
                        if key is not None:
                            keyvalue = key.get_key()
                            create_time = key.get_create_time()
                            if time.time() - create_time < 60 * 60 * 24:
                                self.key = keyvalue
                    if self.key is None:
                        keyring.core.set_keyring(keyring.core.load_keyring('keyring.backends.macOS.Keyring'))
                        my_pass = get_password('Chrome Safe Storage', 'Chrome')
                        my_pass = my_pass.encode('utf8')
                        iterations = 1003
                else:
                    raise Exception('not install chrome')
            elif sys.platform.startswith('linux'):
                my_pass = 'peanuts'.encode('utf8')
                iterations = 1
                cookie_file = cookie_file or os.path.expanduser('~/.config/google-chrome/Default/Cookies') or os.path.expanduser('~/.config/chromium/Default/Cookies')
            if my_pass and self.key is None:
                from Crypto.Protocol.KDF import PBKDF2
                self.key = PBKDF2(my_pass, salt, length, iterations)
                savekey(Mackey(self.key), saveFile=keyname)
        debugEx(cookie_file)
        self.tmp_file = create_local_copy(cookie_file)

    def __del__(self):
        os.remove(self.tmp_file)

    def __str__(self):
        return 'chrome'
    def getCon(self,sq,chrome_database):
        return sq.connect(chrome_database)
    def load(self):
        """将数据的cookies加载到cookieJar
        """
        chrome_database = self.tmp_file
        con = self.getCon(sqlite3,chrome_database)
        con.text_factory = bytes
        cur = con.cursor()
        try:
            cur.execute('SELECT host_key, path, secure, expires_utc, name, value, encrypted_value FROM cookies;')
        except:
            cur.execute('SELECT host_key, path, is_secure, expires_utc, name, value, encrypted_value FROM cookies;')

        cj = CookieJar()
        for item in cur.fetchall():
            try:
                host, path, secure, expires, name = item[:5]
                value = self._decrypt(item[5], item[6])
                if not value:
                    continue
                else:
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')
                    c = create_cookie(host.decode(), path.decode(), secure, expires, name.decode(), value)
                    cj.set_cookie(c)
            except Exception as ex:
                try:
                    pass
                finally:
                    ex = None
                    del ex

        con.close()
        return cj

    def get_key_from_local_state(self):
        jsn = None
        Local_State = os.path.join(os.environ['LOCALAPPDATA'], 'Google\\Chrome\\User Data\\Local State')
        if not os.path.isfile(Local_State):
            Local_State = os.path.join(os.environ['LOCALAPPDATA'], 'Temp\\Google\\Chrome\\User Data\\Local State')
        with open((Local_State),
          encoding='utf-8', mode='r') as f:
            jsn = json.loads(str(f.readline()))
        return jsn['os_crypt']['encrypted_key']

    def aes_decrypt(self, encrypted_txt):
        if sys.platform != 'win32':
            return encrypted_txt
        from . import aesgcm
        import  base64
        encoded_key = self.get_key_from_local_state()
        encrypted_key = base64.b64decode(encoded_key.encode())
        encrypted_key = encrypted_key[5:]
        key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        nonce = encrypted_txt[3:15]
        cipher = aesgcm.get_cipher(key)
        return aesgcm.decrypt(cipher, encrypted_txt[15:], nonce)[:-16].decode()

    def chrome_decrypt(self, value, encrypted_value):
        from Crypto.Cipher import AES
        if value or (encrypted_value[:3] != b'v10'):
            return value
        encrypted_value = encrypted_value[3:]

        def clean(x):
            last = x[(-1)]
            if isinstance(last, int):
                return x[:-last].decode('utf-8')
            return x[:-ord(last)].decode('utf-8')

        iv = b'                '
        cipher = AES.new((self.key), (AES.MODE_CBC), IV=iv)
        decrypted = cipher.decrypt(encrypted_value)
        return clean(decrypted)

    def _decrypt(self, value, encrypted_value):
        if sys.platform == 'win32':
            try:
                if encrypted_value[:3] == b'v10':
                    return self.aes_decrypt(encrypted_value)
                return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1]
            except Exception as ex:
                try:
                    print('-----------------------------------------')
                    print(ex)
                    print('-----------------------------------------')
                    return '<encrypted>'
                finally:
                    ex = None
                    del ex

        else:
            return self.chrome_decrypt(value, encrypted_value)


class Firefox:
    tmp_file = None

    def __init__(self, cookie_file=None):
        cookie_file = cookie_file or self.find_cookie_file()
        self.tmp_file = create_local_copy(cookie_file)
        self.session_file = os.path.join(os.path.dirname(cookie_file), 'sessionstore.js')
        self.new_session_file = os.path.join(os.path.dirname(cookie_file), 'sessionstore-backups', 'recovery.jsonlz4')
        self.session_file2 = os.path.join(os.path.dirname(cookie_file), 'sessionstore.jsonlz4')

    def __del__(self):
        os.remove(self.tmp_file)

    def __str__(self):
        return 'firefox'

    def find_cookie_file(self):
        if sys.platform == 'darwin':
            cookie_files = glob.glob(os.path.expanduser('~/Library/Application Support/Firefox/Profiles/*.default*/cookies.sqlite'))
        elif sys.platform.startswith('linux'):
            cookie_files = glob.glob(os.path.expanduser('~/.mozilla/firefox/*.default*/cookies.sqlite'))
        else:
            pass
        if sys.platform == 'win32':
            cookie_files = glob.glob(os.path.join(os.getenv('PROGRAMFILES', ''), 'Mozilla Firefox/profile/cookies.sqlite')) or glob.glob(os.path.join(os.getenv('PROGRAMFILES(X86)', ''), 'Mozilla Firefox/profile/cookies.sqlite')) or glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Mozilla/Firefox/Profiles/*.default/cookies.sqlite'))
            print(os.path.join(os.getenv('APPDATA', '')))
            if len(cookie_files) > 1 or not cookie_files:
                config = glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Mozilla/Firefox/profiles.ini'))
                import configparser
                cf = configparser.ConfigParser()
                cf.read(config)
                sections = cf.sections()
                Profiles = [section for section in sections if section.find('Install') > -1]
                if Profiles:
                    cookie_files = glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Mozilla/Firefox/%s/cookies.sqlite' % cf.get(Profiles[0], 'Default')))
                if not (cookie_files and os.path.exists(cookie_files[0])):
                    Profiles = [section for section in sections if section.find('Profile') > -1]
                    print(Profiles)
                    for Profile in Profiles:
                        if cf.get(Profile, 'Default') == '1':
                            cookie_files = glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Mozilla/Firefox/%s/cookies.sqlite' % cf.get(Profile, 'Path')))
                            break

                    print(cookie_files)
            else:
                raise BrowserCookieError('Unsupported operating system: ' + sys.platform)
            if cookie_files:
                return cookie_files[0]
        raise BrowserCookieError('Failed to find Firefox cookie')

    def extreactSessionCookie(self, sessionFile, cj):
        try:
            import lz4.block
            in_file = open(sessionFile, 'rb')
            data = lz4.block.decompress(in_file.read()) if in_file.read(8) == b'mozLz40\x00' else b'{}'
            in_file.close()
            jsonData = json.loads(data.decode('utf-8'))
            cookies = jsonData.get('cookies', {})
            expires = str(int(time.time()) + 604800)
            for cookie in cookies:
                c = create_cookie(cookie.get('host', ''), cookie.get('path', ''), False, expires, cookie.get('name', ''), cookie.get('value', ''))
                cj.set_cookie(c)

        except Exception as ex:
            try:
                print(ex)
            finally:
                ex = None
                del ex

    def load(self):
        print('firefox', self.tmp_file)
        cj = CookieJar()
        try:
            con = sqlite3.connect(self.tmp_file)
            cur = con.cursor()
            cur.execute('select host, path, isSecure, expiry, name, value from moz_cookies')
            for item in cur.fetchall():
                c = create_cookie(*item)
                cj.set_cookie(c)

            con.close()
        except Exception as e:
            try:
                debugEx(e)
            finally:
                e = None
                del e

        if os.path.exists(self.session_file):
            try:
                json_data = json.loads(open(self.session_file, 'rb').read())
            except ValueError as e:
                try:
                    debugEx('Error parsing firefox session JSON: %s' % str(e))
                finally:
                    e = None
                    del e

            else:
                expires = str(int(time.time()) + 604800)
                for window in json_data.get('windows', []):
                    for cookie in window.get('cookies', []):
                        c = create_cookie(cookie.get('host', ''), cookie.get('path', ''), False, expires, cookie.get('name', ''), cookie.get('value', ''))
                        cj.set_cookie(c)

        elif os.path.exists(self.new_session_file):
            print(self.new_session_file)
            self.extreactSessionCookie(self.new_session_file, cj)
        elif os.path.exists(self.session_file2):
            print(self.session_file2)
            self.extreactSessionCookie(self.session_file2, cj)
        else:
            print('Firefox session filename does not exist: %s' % self.session_file)
        return cj


class Safari:

    def __init__(self, cookie_file=None):
        import logging
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.WARNING)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.log.addHandler(handler)
        if sys.platform == 'win32':
            self.cookie_file = cookie_file or os.path.join(os.getenv('APPDATA', ''), 'Apple Computer\\Safari\\Cookies\\Cookies.binarycookies')
        else:
            self.cookie_file = cookie_file or os.path.expanduser('~/Library/Cookies/Cookies.binarycookies')

    def load(self):
        from io import BytesIO
        from struct import pack, unpack
        cj = CookieJar()
        file = open(self.cookie_file, 'rb')
        try:
            cookies = []
            self.log.info('Parsing %s', file.name)
            magic = file.read(4)
            if magic != b'cook':
                self.log.exception('File is not a binary cookie valid format')
                return cookies
            num_pages = unpack('>i', file.read(4))[0]
            page_sizes = []
            for _ in range(num_pages):
                page_sizes.append(unpack('>i', file.read(4))[0])

            pages = []
            for ps in page_sizes:
                pages.append(file.read(ps))

            for page in pages:
                page = BytesIO(page)
                page.read(4)
                num_cookies = unpack('<i', page.read(4))[0]
                cookie_offsets = []
                for _ in range(num_cookies):
                    cookie_offsets.append(unpack('<i', page.read(4))[0])

                page.read(4)
                for offset in cookie_offsets:
                    content = {}
                    page.seek(offset)
                    content['size'] = unpack('<i', page.read(4))[0]
                    cookie = BytesIO(page.read(content['size']))
                    cookie.read(4)
                    content['flags'] = unpack('<i', cookie.read(4))[0]
                    cookie.read(4)
                    if sys.platform == 'win32':
                        keys = ('name', 'value', 'domain', 'path')
                    else:
                        keys = ('domain', 'name', 'path', 'value')
                    for key in keys:
                        content[key + '_offset'] = unpack('<i', cookie.read(4))[0]

                    cookie.read(8)
                    content['expiry_date'] = unpack('<d', cookie.read(8))[0]
                    content['creation_date'] = unpack('<d', cookie.read(8))[0]
                    for i in keys:
                        n = cookie.read(1)
                        value = []
                        while unpack('<b', n)[0] != 0:
                            value.append(n.decode('utf8'))
                            n = cookie.read(1)

                        content[i] = ''.join(value)

                    cookies.append(content)
                    cj.set_cookie(create_cookie(content['domain'], content['path'], content['flags'], content['expiry_date'], content['name'], content['value']))

            return cj
        finally:
            file.close()


class IE:

    def __init__(self, cookie_file=None):
        pass

    def load(self):

        def get_cookiedir():
            if sys.version_info >= (3, 0):
                import winreg
            else:
                import _winreg as winreg
            path = 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, path) as key:
                return winreg.QueryValueEx(key, 'Cookies')[0]

        cj = CookieJar()
        pattern = '*.txt'
        dirname = get_cookiedir()
        files = glob.glob(os.path.join(dirname, pattern))
        files += glob.glob(os.path.join(dirname, 'Low', pattern))
        for fname in files:
            with open(fname) as fp:
                for chunk in zip(*[fp] * 9):
                    name = chunk[0][:-1]
                    value = chunk[1][:-1]
                    host, path = chunk[2][:-1].split('/', 1)
                    path = '/' + path
                    flag = int(chunk[3])
                    secure = bool(flag & 1)
                    expires_nt = (int(chunk[5]) << 32) + int(chunk[4])
                    expires = expires_nt / 10000000 - 11644473600
                    c = create_cookie(host, path, secure, expires, name, value)
                    cj.set_cookie(c)

        return cj


def create_cookie(host, path, secure, expires, name, value):
    return Cookie(0, name, value, None, False, host, host.startswith('.'), host.startswith('.'), path, True, secure, expires, False, None, None, {})


class CookiesJar:

    def getCookies(self, domain, browser):

        def formatResult(cookies, domain):
            result = ''
            cj = http.cookiejar.CookieJar()
            for key in cookies:
                if re.search(domain, key):
                    c = cookies[key]
                    for sd in c:
                        for k in c[sd]:
                            try:

                                cj.set_cookie(c[sd][k])

                            except Exception as e:
                                try:
                                    pass
                                finally:
                                    e = None
                                    del e

            return cj

        result = ''
        try:
            if browser == 'chrome':
                c = Chrome()
            elif browser == 'firefox':
                c = Firefox()
            elif browser == 'IE':
                c = IE()
            else:
                c = Safari()
            cj = c.load()
            if cj:
                result = formatResult(cj._cookies, domain)
            else:
                result = ''
            return result
        except Exception as e:
            try:
                print(e)
                return ''
            finally:
                e = None
                del e


def createInstance(className):
    if className == 'CookiesJar':
        return CookiesJar()


if __name__ == '__main__':
    debugEx('--------------IE--------------------------')
    debugEx('--------------chrome--------------------------')
    debugEx('--------------firefox--------------------------')
    print(createInstance('CookiesJar').getCookies('https://www.bilibili.com/video/BV1XP411w71V/?spm_id_from=333.1007.tianma.1-1-1.click', 'chrome'))
    debugEx('--------------Safari-------------------------')