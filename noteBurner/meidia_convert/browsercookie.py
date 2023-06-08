from urllib.parse import urlparse
def get_cookie(url):

    parsed_uri = urlparse(url)
    domain = parsed_uri.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    if domain.find('youtu.be') != -1:
        domain += ';youtube.com'
    if domain.find('spotify.com') != -1:
        domain += ';youtube.com'
    cookies = load_cookies(domain)
    return cookies
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.4 (tags/v3.7.4:e09359112e, Jul  8 2019, 20:34:20) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: browsercookie.py
import logging

import keyring

from Cookies.BrowserCookie import  createInstance
import os, os.path, sys, time, glob, tempfile, lz4.block, datetime, configparser, base64
from Crypto.Cipher import AES
try:
    import json
except ImportError:
    import simplejson as json

try:
    from pysqlite2 import dbapi2 as sqlite3
except ImportError:
    import sqlite3

import pyaes
from pbkdf2 import PBKDF2
if sys.platform == 'darwin':
    from struct import unpack
    try:
        from StringIO import StringIO
    except ImportError:
        from io import BytesIO as StringIO

class BrowserCookieError(Exception):
    pass


def create_local_copy(cookie_file):
    """Make a local copy of the sqlite cookie database and return the new filename.
    This is necessary in case this database is still being written to while the user browses
    to avoid sqlite locking errors.
    """
    if os.path.exists(cookie_file):
        tmp_cookie_file = tempfile.NamedTemporaryFile(suffix='.sqlite').name
        open(tmp_cookie_file, 'wb').write(open(cookie_file, 'rb').read())
        return tmp_cookie_file
    raise BrowserCookieError('Can not find cookie file at: ' + cookie_file)


def windows_group_policy_path():
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKeyEx, QueryValueEx, REG_EXPAND_SZ, REG_SZ
    try:
        root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        policy_key = OpenKeyEx(root, 'SOFTWARE\\Policies\\Google\\Chrome')
        user_data_dir, type_ = QueryValueEx(policy_key, 'UserDataDir')
        if type_ == REG_EXPAND_SZ:
            user_data_dir = os.path.expandvars(user_data_dir)
        else:
            if type_ != REG_SZ:
                return
    except OSError:
        return
    else:
        return os.path.join(user_data_dir, 'Default', 'Cookies')


def crypt_unprotect_data(cipher_text=b'', entropy=b'', reserved=None, prompt_struct=None, is_key=False):
    import ctypes, ctypes.wintypes

    class DataBlob(ctypes.Structure):
        _fields_ = [
         (
          'cbData', ctypes.wintypes.DWORD),
         (
          'pbData', ctypes.POINTER(ctypes.c_char))]

    blob_in, blob_entropy, blob_out = map(lambda x: DataBlob(len(x), ctypes.create_string_buffer(x)), [
     cipher_text, entropy, b''])
    desc = ctypes.c_wchar_p()
    CRYPTPROTECT_UI_FORBIDDEN = 1
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), ctypes.byref(desc), ctypes.byref(blob_entropy), reserved, prompt_struct, CRYPTPROTECT_UI_FORBIDDEN, ctypes.byref(blob_out)):
        raise RuntimeError('Failed to decrypt the cipher text with DPAPI')
    description = desc.value
    buffer_out = ctypes.create_string_buffer(int(blob_out.cbData))
    ctypes.memmove(buffer_out, blob_out.pbData, blob_out.cbData)
    map(ctypes.windll.kernel32.LocalFree, [desc, blob_out.pbData])
    if is_key:
        return (
         description, buffer_out.raw)
    return (description, buffer_out.value)

def create_local_copy(cookie_file):
    """Make a local copy of the sqlite cookie database and return the new filename.
    This is necessary in case this database is still being written to while the user browses
    to avoid sqlite locking errors.
    """
    # check if cookie file exists
    if os.path.exists(cookie_file):
        # copy to random name in tmp folder
        tmp_cookie_file = tempfile.NamedTemporaryFile(suffix='.sqlite').name
        open(tmp_cookie_file, 'wb').write(open(cookie_file, 'rb').read())
        return tmp_cookie_file
    else:
        raise BrowserCookieError('Can not find cookie file at: ' + cookie_file)
class Chrome:

    def __init__(self, cookie_file=None, domain_name=''):
        self.cookies = ''
        self.salt = b'saltysalt'
        self.iv = b'                '
        self.length = 16
        self.domain_name = domain_name

        if sys.platform == 'darwin':
            # self.chrome = ChromeHD(domain_name=domain_name)
            self.browser = "chrome"
            self.cookie_file = None
            osx_cookies = '~/Library/Application Support/Google/Chrome/Default/Cookies'
            os_crypt_name= 'chrome'
            osx_key_service = 'Chrome Safe Storage'
            osx_key_user =  'Chrome'
            my_pass = keyring.get_password(osx_key_service, osx_key_user)
            # try default peanuts password, probably won't work
            if not my_pass:
                my_pass = 'peanuts'
            my_pass = my_pass.encode('utf-8')

            iterations = 1003  # number of pbkdf2 iterations on mac
            self.key = PBKDF2(my_pass, self.salt,
                              iterations=iterations).read(self.length)
            paths = [osx_cookies]
            paths = map(os.path.expanduser, paths)
            paths = next(filter(os.path.exists, paths), None)
            cookie_file = self.cookie_file or paths
            if not cookie_file:
                raise BrowserCookieError('Failed to find {} cookie'.format(self.browser))
            self.tmp_cookie_file = create_local_copy(cookie_file)
            return
        else:
            if sys.platform.startswith('linux'):
                my_pass = 'peanuts'.encode('utf8')
                iterations = 1
                self.key = PBKDF2(my_pass, (self.salt), iterations=iterations).read(self.length)
                paths = map(os.path.expanduser, [
                 '~/.config/google-chrome/Default/Cookies',
                 '~/.config/chromium/Default/Cookies',
                 '~/.config/google-chrome-beta/Default/Cookies'])
                cookie_file = cookie_file or next(filter(os.path.exists, paths), None)
            else:
                if sys.platform == 'win32':
                    key_file = glob.glob(os.path.join(os.getenv('APPDATA', ''), '..\\Local\\Google\\Chrome\\User Data\\Local State')) or glob.glob(os.path.join(os.getenv('LOCALAPPDATA', ''), 'Google\\Chrome\\User Data\\Local State')) or glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Google\\Chrome\\User Data\\Local State'))
                    if isinstance(key_file, list):
                        if key_file:
                            key_file = key_file[0]
                    if key_file:
                        logging.info("开始打开chrome浏览器文件")
                        f = open(key_file, 'rb')
                        key_file_json = json.load(f)
                        logging.info("结束打开chrome浏览器文件")
                        key64 = key_file_json['os_crypt']['encrypted_key'].encode('utf-8')
                        keydpapi = base64.standard_b64decode(key64)[5:]
                        _, self.key = crypt_unprotect_data(keydpapi, is_key=True)
                    cookie_file = cookie_file or windows_group_policy_path() or glob.glob(os.path.join(os.getenv('APPDATA', ''), '..\\Local\\Google\\Chrome\\User Data\\Default\\Cookies')) or glob.glob(os.path.join(os.getenv('LOCALAPPDATA', ''), 'Google\\Chrome\\User Data\\Default\\Cookies')) or glob.glob(os.path.join(os.getenv('APPDATA', ''), 'Google\\Chrome\\User Data\\Default\\Cookies'))
                else:
                    raise BrowserCookieError('OS not recognized. Works on Chrome for OSX, Windows, and Linux.')
        if isinstance(cookie_file, list):
            if not cookie_file:
                raise BrowserCookieError('Failed to find Chrome cookie')
            cookie_file = cookie_file[0]
        self.tmp_cookie_file = create_local_copy(cookie_file)

    def __del__(self):
        if hasattr(self, 'tmp_cookie_file'):
            os.remove(self.tmp_cookie_file)

    def __str__(self):
        return 'chrome'

    def load(self):
        # if sys.platform == 'darwin':
        #     return self.chrome.load()
        con = sqlite3.connect(self.tmp_cookie_file)
        cur = con.cursor()
        try:
            cur.execute('SELECT host_key, path, secure, expires_utc, name, value, encrypted_value FROM cookies WHERE host_key like %s;' % self.domain_name)
        except sqlite3.OperationalError:
            cur.execute('SELECT host_key, path, is_secure, expires_utc, name, value, encrypted_value FROM cookies WHERE host_key like %s;' % self.domain_name)

        epoch_start = datetime.datetime(1601, 1, 1)
        for item in cur.fetchall():
            host, path, secure, expires, name = item[:5]
            if item[3] != 0:
                try:
                    offset = min(int(item[3]), 265000000000000000)
                    delta = datetime.timedelta(microseconds=offset)
                    expires = epoch_start + delta
                    expires = expires.timestamp()
                except OSError:
                    offset = min(int(item[3]), 32536799999000000)
                    delta = datetime.timedelta(microseconds=offset)
                    expires = epoch_start + delta
                    expires = expires.timestamp()

            if int(expires) == 0:
                expires = time.time() + 3600
            value = self._decrypt(item[5], item[6])
            securestr = 'FALSE' if secure == 0 else 'TRUE'
            domain_specified = 'TRUE' if host.startswith('.') else 'FALSE'
            self.cookies += host + '\t' + domain_specified + '\t' + path + '\t' + securestr + '\t' + str(int(expires)) + '\t' + name + '\t' + value + '\n'

        con.close()
        return self.cookies

    @staticmethod
    def _decrypt_windows_chrome(value, encrypted_value):
        if len(value) != 0:
            return value
        if encrypted_value == '':
            return ''
        _, data = crypt_unprotect_data(encrypted_value)
        assert isinstance(data, bytes)
        return data.decode()

    def _decrypt(self, value, encrypted_value):
        """Decrypt encoded cookies
        """
        if sys.platform == 'win32':
            try:
                return self._decrypt_windows_chrome(value, encrypted_value)
            except RuntimeError:
                if not self.key:
                    raise RuntimeError('Failed to decrypt the cipher text with DPAPI and no AES key.')
                encrypted_value = encrypted_value[3:]
                nonce, tag = encrypted_value[:12], encrypted_value[-16:]
                aes = AES.new((self.key), (AES.MODE_GCM), nonce=nonce)
                data = aes.decrypt_and_verify(encrypted_value[12:-16], tag)
                return data.decode()

        if value or encrypted_value[:3] != b'v10':
            return value
        encrypted_value = encrypted_value[3:]
        encrypted_value_half_len = int(len(encrypted_value) / 2)
        cipher = pyaes.Decrypter(pyaes.AESModeOfOperationCBC(self.key, self.iv))
        decrypted = cipher.feed(encrypted_value[:encrypted_value_half_len])
        decrypted += cipher.feed(encrypted_value[encrypted_value_half_len:])
        decrypted += cipher.feed()
        return decrypted.decode('utf-8')


class Firefox:

    def __init__(self, cookie_file=None, domain_name=''):
        self.cookies = ''
        self.tmp_cookie_file = None
        cookie_file = cookie_file or self.find_cookie_file()
        self.tmp_cookie_file = create_local_copy(cookie_file)
        self.session_file = os.path.join(os.path.dirname(cookie_file), 'sessionstore.js')
        self.session_file_lz4 = os.path.join(os.path.dirname(cookie_file), 'sessionstore-backups', 'recovery.jsonlz4')
        self.domain_name = domain_name

    def __del__(self):
        if self.tmp_cookie_file:
            os.remove(self.tmp_cookie_file)

    def __str__(self):
        return 'firefox'

    @staticmethod
    def get_default_profile(user_data_path):
        config = configparser.ConfigParser()
        profiles_ini_path = glob.glob(os.path.join(user_data_path + '**', 'profiles.ini'))
        fallback_path = user_data_path + '**'
        if not profiles_ini_path:
            return fallback_path
        profiles_ini_path = profiles_ini_path[0]
        config.read(profiles_ini_path)
        profile_path = None
        for section in config.sections():
            if section.startswith('Install'):
                profile_path = config[section].get('Default')
                break

        for section in config.sections():
            if config[section].get('Path') == profile_path:
                absolute = config[section].get('IsRelative') == '0'
                if absolute:
                    return profile_path
                return os.path.join(os.path.dirname(profiles_ini_path), profile_path)

        return fallback_path

    @staticmethod
    def find_cookie_file():
        cookie_files = []
        if sys.platform == 'darwin':
            user_data_path = os.path.expanduser('~/Library/Application Support/Firefox')
        else:
            if sys.platform.startswith('linux'):
                user_data_path = os.path.expanduser('~/.mozilla/firefox')
            else:
                if sys.platform == 'win32':
                    user_data_path = os.path.join(os.environ.get('APPDATA'), 'Mozilla', 'Firefox')
                    cookie_files = glob.glob(os.path.join(os.environ.get('PROGRAMFILES'), 'Mozilla Firefox', 'profile', 'cookies.sqlite')) or glob.glob(os.path.join(os.environ.get('PROGRAMFILES(X86)'), 'Mozilla Firefox', 'profile', 'cookies.sqlite'))
                else:
                    raise BrowserCookieError('Unsupported operating system: ' + sys.platform)
        cookie_files = glob.glob(os.path.join(Firefox.get_default_profile(user_data_path), 'cookies.sqlite')) or cookie_files
        if cookie_files:
            return cookie_files[0]
        raise BrowserCookieError('Failed to find Firefox cookie')

    def __create_session_cookie(self, cookie_json):
        host = cookie_json.get('host', '')
        path = cookie_json.get('path', '')
        expires = str(int(time.time()) + 604800)
        name = cookie_json.get('name', '')
        value = cookie_json.get('value', '')
        domain_specified = 'TRUE' if host.startswith('.') else 'FALSE'
        self.cookies += host + '\t' + domain_specified + '\t' + path + '\t' + 'FALSE' + '\t' + expires + '\t' + name + '\t' + value + '\n'

    def __add_session_cookies(self):
        if not os.path.exists(self.session_file):
            return
        try:
            json_data = json.loads(open(self.session_file, 'rb').read().decode())
        except ValueError as e:
            try:
                print('Error parsing firefox session JSON:', str(e))
            finally:
                e = None
                del e

        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    self._create_session_cookie(cookie)

    def __add_session_cookies_lz4(self):
        if not os.path.exists(self.session_file_lz4):
            return
        try:
            file_obj = open(self.session_file_lz4, 'rb')
            file_obj.read(8)
            json_data = json.loads(lz4.block.decompress(file_obj.read()))
        except ValueError as e:
            try:
                print('Error parsing firefox session JSON LZ4:', str(e))
            finally:
                e = None
                del e

        else:
            for cookie in json_data.get('cookies', []):
                self._Firefox__create_session_cookie(cookie)

    def load(self):
        con = sqlite3.connect(self.tmp_cookie_file)
        cur = con.cursor()
        cur.execute('select host, path, isSecure, expiry, name, value from moz_cookies where host like "%{}%"'.format(self.domain_name))
        for item in cur.fetchall():
            host, path, secure, expires, name, value = item[:6]
            securestr = 'FALSE' if secure == 0 else 'TRUE'
            domain_specified = 'TRUE' if host.startswith('.') else 'FALSE'
            self.cookies += host + '\t' + domain_specified + '\t' + path + '\t' + securestr + '\t' + str(int(expires)) + '\t' + name + '\t' + value + '\n'

        con.close()
        self._Firefox__add_session_cookies()
        self._Firefox__add_session_cookies_lz4()
        return self.cookies


class Safari:

    def __init__(self, cookie_file=None, domain_name=''):
        self.cookies = ''
        self.domain_name = domain_name
        if sys.platform != 'darwin':
            raise BrowserCookieError('Safari only work on OSX')

    def load(self):
        if sys.platform != 'darwin':
            return self.cookies
        FilePath = os.path.expanduser('~/Library/Cookies/Cookies.binarycookies')
        try:
            binary_file = open(FilePath, 'rb')
        except IOError:
            return self.cookies
        else:
            binary_file.read(4)
            num_pages = unpack('>i', binary_file.read(4))[0]
            page_sizes = []
            for _ in range(num_pages):
                page_sizes.append(unpack('>i', binary_file.read(4))[0])

            pages = []
            for ps in page_sizes:
                pages.append(binary_file.read(ps))

            for page in pages:
                page = StringIO(page)
                page.read(4)
                num_cookies = unpack('<i', page.read(4))[0]
                cookie_offsets = []
                for _ in range(num_cookies):
                    cookie_offsets.append(unpack('<i', page.read(4))[0])

                page.read(4)
                cookie = ''
                for offset in cookie_offsets:
                    page.seek(offset)
                    cookiesize = unpack('<i', page.read(4))[0]
                    cookie = StringIO(page.read(cookiesize))
                    cookie.read(4)
                    flags = unpack('<i', cookie.read(4))[0]
                    cookie_flags = ''
                    if flags == 0:
                        cookie_flags = False
                    elif flags == 1:
                        cookie_flags = True
                    else:
                        if flags == 4:
                            cookie_flags = False
                        else:
                            if flags == 5:
                                cookie_flags = True
                            else:
                                cookie_flags = False
                    cookie.read(4)
                    urloffset = unpack('<i', cookie.read(4))[0]
                    nameoffset = unpack('<i', cookie.read(4))[0]
                    pathoffset = unpack('<i', cookie.read(4))[0]
                    valueoffset = unpack('<i', cookie.read(4))[0]
                    expiry_date = str(int(unpack('<d', cookie.read(8))[0] + 978307200))
                    cookie.seek(urloffset - 4)
                    host = ''
                    u = cookie.read(1)
                    while unpack('<b', u)[0] != 0:
                        host = host + u.decode('utf-8')
                        u = cookie.read(1)

                    cookie.seek(nameoffset - 4)
                    name = ''
                    n = cookie.read(1)
                    while unpack('<b', n)[0] != 0:
                        name = name + n.decode('utf-8')
                        n = cookie.read(1)

                    cookie.seek(pathoffset - 4)
                    path = ''
                    pa = cookie.read(1)
                    while unpack('<b', pa)[0] != 0:
                        path = path + pa.decode('utf-8')
                        pa = cookie.read(1)

                    cookie.seek(valueoffset - 4)
                    value = ''
                    va = cookie.read(1)
                    while unpack('<b', va)[0] != 0:
                        value = value + va.decode('utf-8')
                        va = cookie.read(1)

                    if self.domain_name not in host:
                        continue
                    securestr = 'TRUE' if cookie_flags else 'FALSE'
                    domain_specified = 'TRUE' if host.startswith('.') else 'FALSE'
                    self.cookies += host + '\t' + domain_specified + '\t' + path + '\t' + securestr + '\t' + str(int(expiry_date)) + '\t' + name + '\t' + value + '\n'

            binary_file.close()
            return self.cookies


def chrome(cookie_file=None, domain_name=''):
    """Returns the cookies used by Chrome. Optionally pass in a
    domain name to only load cookies from the specified domain
    """
    #return Chrome(cookie_file, domain_name).load()
    return createInstance('CookiesJar').getCookies("."+domain_name, 'chrome')


def firefox(cookie_file=None, domain_name=''):
    """Returns the cookies and sessions used by Firefox. Optionally
    pass in a domain name to only load cookies from the specified domain
    """
    # return Firefox(cookie_file, domain_name).load()
    return createInstance('CookiesJar').getCookies("."+domain_name, 'firefox')


def safari(cookie_file=None, domain_name=''):
    """Returns the cookies and sessions used by Safari. Optionally
    pass in a domain name to only load cookies from the specified domain
    """
    # return Safari(cookie_file, domain_name).load()
    return createInstance('CookiesJar').getCookies("."+domain_name, 'safari')
def IE(cookie_file=None, domain_name=''):
    """Returns the cookies and sessions used by Safari. Optionally
    pass in a domain name to only load cookies from the specified domain
    """
    # return Safari(cookie_file, domain_name).load()
    return createInstance('CookiesJar').getCookies("."+domain_name, 'IE')


def load_cookies(domain_names=''):
    cookies = []
    for cookie_fn in [chrome, safari, firefox,IE]:
        try:
            domains = domain_names.split(';')
            cookie = None
            for domain_name in domains:
                cookie = cookie_fn(domain_name=domain_name)

            if cookie != '':
                cookies.append(cookie)
        except Exception as e:
            try:
                continue
            finally:
                e = None
                del e

    return cookies