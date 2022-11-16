# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: settings\settings.py
import sys, os, locale, subprocess
from ctypes import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QCommonStyle, QStyle
from module.logger import logger
preferred_encoding = locale.getpreferredencoding()
plat = sys.platform.lower()
iswindows = plat.startswith('win')
isosx = plat.startswith('darwin')
islinux = plat.startswith('linux')
isxp = iswindows and sys.getwindowsversion().major < 6
if iswindows:
    confpath = os.environ['APPDATA']
    homepath = os.path.expanduser('~')
elif isosx:
    homepath = confpath = os.path.expanduser('~')
RELEASE = True
try:
    if iswindows:
        os.environ['PATH'] = 'plugins;' + os.environ['PATH']
    else:
        if isosx:
            if RELEASE:
                CWD = os.path.dirname(sys.executable)
                os.chdir(CWD)
                os.environ['PATH'] = 'plugins:' + os.environ['PATH']
except Exception as e:
    print('Failed with init dll or exe for ecore, drm module', e)

res = None
apps = None
isblind = False
MP3_CHAPTER = False
MultiLanguage = {}

def getMultiLang():
    MultiLanguage['language_cn'] = '简体中文 (Simplified Chinese)'
    MultiLanguage['language_en'] = 'English'
    MultiLanguage['language_ja'] = '日本語 (Japanese)'
    MultiLanguage['language_fr'] = 'Français (French)'
    MultiLanguage['language_italian'] = 'Italiano (Italian)'
    MultiLanguage['language_de'] = 'German'


def sysLanguage():
    language = 'language_en'
    lan = None
    if iswindows:
        try:
            dll = windll.kernel32
            lan = locale.windows_locale[dll.GetUserDefaultUILanguage()]
        except Exception as e:
            print('Failed with getting system language', e)
            lan = None

    else:
        if isosx:
            try:
                cmd = 'defaults read .GlobalPreferences AppleLanguages'
                arglist = cmd.split(' ')
                ret = subprocess.Popen(arglist, stdout=(subprocess.PIPE),
                  stderr=(subprocess.PIPE),
                  startupinfo=None)
                lang = ret.stdout.read().decode(preferred_encoding).replace('\r', '').replace('\n', '').replace(' ', '')
                lang = lang[1:5]
                lan = lang
            except Exception as e:
                print('Failed getting system language', e)
                lan = None

        if lan:
            lan = lan.lower()
            if 'zh' in lan:
                language = 'language_cn'
            else:
                if 'ja' in lan:
                    language = 'language_ja'
                elif 'en' in lan:
                    language = 'language_en'
        return language


STYLE_SCROLLBAR = 'QScrollBar{background:transparent; width: 10px;}QScrollBar::handle::vertical{min-height: 20px;}QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}QScrollBar::handle:hover{background:gray;}QScrollBar::sub-line{background:transparent;}QScrollBar::add-line{background:transparent;}'

class Styled(QCommonStyle):

    def __init__(self):
        QCommonStyle.__init__(self)

    def drawPrimitive(self, element, option, painter, widget):
        if element == QStyle.PE_FrameFocusRect:
            return
        QCommonStyle.drawPrimitive(self, element, option, painter, widget)


def tr(msg):
    global apps
    if not apps or apps['app_language'] == 'language_en':
        return msg
    else:
        tMsg = QCoreApplication.translate('@default', msg)
        if tMsg != '@_NOT_TRANSLATE_@':
            return tMsg
        return ''


def tr_ui(context, msg):
    return tr(msg)


def docpath():
    if iswindows:
        import winreg
        try:
            keyvalue = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders')
            r = winreg.QueryValueEx(keyvalue, 'Personal')
            s = r[0]
            winreg.CloseKey(keyvalue)
            return s
        except Exception as e:
            print('Get doc path from regedit err', e)

    else:
        if isosx:
            return os.path.join(homepath, 'Documents')
        return ''


def join_strs(item_0, item_1, item_2, item_3, item_4, item_5=''):
    strs = '<html><head/><body><p><h3>' + tr('Benefits of ') + item_0 + '</h3></p><p style="font-weight:normal;color:#666666; line-height:20px;">>>' + item_1 + '<br/>>>' + item_2 + '<br/>>>' + item_3 + '<br/>>>' + item_4 + '<br/></p>' + '<p style="font-size:14px;color:red; line-height:20px;">>>' + item_5 + '</p></body></html>'
    return strs


class Settings:

    def __init__(self):
        global res
        from settings.functions import getmac
        self.__dict__ = {'app_language':'', 
         'email':'', 
         'id':getmac(), 
         'ui_size':[],  'is_max_size':False, 
         'output_formated':'.mp3', 
         'outputpath':res.outputpath, 
         'downloadpath':res.downloadpath}
        if os.path.isfile(self.pathOld):
            if os.path.isfile(self.path):
                os.remove(self.pathOld)
            else:
                os.rename(self.pathOld, self.path)
        else:
            oldAudibleCfg = os.path.join(res.usrpath[:-7], 'audible.cfg')
            if os.path.isfile(oldAudibleCfg):
                os.remove(oldAudibleCfg)
            if os.path.isfile(self.path):
                self.get()
                needSave = False
                if not os.path.isdir(self.__dict__['downloadpath']):
                    self.__dict__['downloadpath'] = docpath()
                    needSave = True
                if not os.path.isdir(self.__dict__['outputpath']):
                    self.__dict__['outputpath'] = res.outputpath
                    needSave = True
                if needSave:
                    self.save()
            else:
                self.save()

    @property
    def path(self):
        return os.path.join(res.usrpath, 'audible_setting')

    @property
    def pathOld(self):
        return os.path.join(res.usrpath[:-7], 'audible_setting')

    def __getitem__(self, key):
        self.get()
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value
        self.save()

    def get(self):
        try:
            fdict = eval(open((self.path), encoding='utf8').read())
            for key in fdict:
                self.__dict__[key] = fdict[key]

        except Exception as e:
            logger.error('Failed with reading settings file: ' + str(e))

    def save(self):
        try:
            open((self.path), 'w', encoding='utf8').write(str(self.__dict__))
        except Exception as e:
            logger.error('Failed with writing settings file: ' + str(e))


class BaseProduct:

    class RegInfo:

        def __init__(self):
            self.email = ''
            self.licenseCode = ''
            self.isRegister = False
            self.isExpired = False

    icon = ':/imgs/product.ico'
    regInfo = RegInfo()
    styled = Styled()
    filter_add = 'Audible Books(*.aax *.aa);;Aax Books(*.aax);;Aa Books(*.aa);;All Files(*.*)'

    def __init__(self):
        try:
            if os.path.isfile(self.outputpath[:-1]):
                os.remove(self.outputpath[:-1])
            elif os.path.isfile(self.coverpath[:-1]):
                os.remove(self.coverpath[:-1])
            elif not os.path.exists(self.outputpath):
                os.makedirs(self.outputpath)
            else:
                if not os.path.exists(self.usrpath):
                    os.makedirs(self.usrpath)
                if not os.path.exists(self.coverpath):
                    os.makedirs(self.coverpath)
                if iswindows:
                    self.downloadpath = os.path.join(os.environ['PUBLIC'], 'Documents\\Audible\\Downloads')
                    if not os.path.exists(self.downloadpath):
                        self.downloadpath = os.path.join(docpath(), 'Audible\\Downloads')
                elif isosx:
                    self.downloadpath = docpath()
        except Exception as e:
            print('Failed with creating default path', e)

    @property
    def usrpath(self):
        return os.path.join(confpath, '.' + self.__class__.__name__)

    @property
    def updatejson(self):
        return 'http://download.epubor.com/upgrade.aspx?productid=%s' % self.product_id

    @property
    def outputpath(self):
        return os.path.join(homepath, self.__class__.__name__)

    @property
    def coverpath(self):
        if iswindows:
            return (confpath + '\\%s\\cover\\') % self.__class__.__name__
        if isosx:
            return (confpath + '/.%s/cover/') % self.__class__.__name__

    @property
    def defaultcover(self):
        return os.path.join(self.coverpath, 'defaultcover.png')

    @property
    def ordertag(self):
        if iswindows:
            return '#os_Win'
        else:
            if isosx:
                return '#os_Mac'
            return '#os_Linux'

    @property
    def tag_utm_medium(self):
        return 'soft'

    @property
    def tag_utm_campaign(self):
        return 'register'

    @property
    def tag_utm_affiliate(self):
        return ''

    @property
    def descryption(self):
        return join_strs(self.titleMsg, tr('Convert AA, AAX audiobooks to MP3, M4B'), tr('Support batch conversion'), tr('Decrypt & convert purchased Audible books with only 1 click'), tr('Convert Audible audiobooks at the fastest speed'), tr('Trial version is limited to converting 10 minutes of each Audible book. And splitting audible into chapter is not available for trial version.'))

    @property
    def newVersion(self):
        try:
            import encodings.idna, requests, json
            ret = requests.get(res.updatejson)
            content = ret.content.decode('utf8').replace('\r', '').replace('\n', '')
            jsondict = ''
            if iswindows:
                jsondict = json.loads(content)['WinAudible']
            else:
                if isosx:
                    jsondict = json.loads(content)['MacAudible']
            if jsondict:
                curVersion = jsondict[0]['ver']
                if self.cmpVersion(curVersion, self.version):
                    return curVersion
        except Exception as e:
            print('Failed with get update information', e)

    def cmpVersion(self, server, local):
        pServer = server.split('.')
        pLocal = local.split('.')
        try:
            for i in range(len(pServer)):
                if i > len(pLocal) - 1:
                    return True
                if int(pServer[i]) > int(pLocal[i]):
                    return True
                if int(pServer[i]) < int(pLocal[i]):
                    return False

        except:
            return True
        else:
            return False


class EpuborAudible(BaseProduct):
    version = '1.0.10.295'
    versionReg = '1.0'
    titleMsg = 'Epubor Audible Converter'
    title = titleMsg + ' v' + version
    copyright = 'https://www.epubor.com/'
    author = 'support@epubor.com'
    isEpubor = True

    @property
    def product_id(self):
        if iswindows:
            return '36498-45'
        else:
            if isosx:
                return '36498-46'
            if islinux:
                return '36498-304'

    @property
    def price(self):
        if iswindows:
            return '22.99'
        else:
            if isosx:
                return '22.99'
            if islinux:
                return '22.99'

    @property
    def help(self):
        return 'https://www.epubor.com/audible-converter.html'

    @property
    def guideText(self):
        return 'https://www.epubor.com/audible-converter-user-guide.html'

    @property
    def guideLink(self):
        return 'https://www.epubor.com/epubor-audible-converter-user-guide.html'

    @property
    def ticket(self):
        return 'http://ticket.epubor.com'

    @property
    def AboutURL(self):
        return 'https://www.epubor.com/about.html?utm_medium=soft&utm_source=license-manage&utm_campaign=no-order-1&utm_content=' + res.version

    @property
    def UpgradeURL(self):
        return 'https://www.epubor.com/software-upgrade-policy.html?utm_medium=soft&utm_source=license-manage&utm_campaign=wrong-version-3&utm_content=' + res.version


class imElfinAudible(BaseProduct):
    version = '1.0.10.295'
    versionReg = '1.0'
    titleMsg = 'imElfin Audible Converter'
    title = titleMsg + ' v' + version
    copyright = 'http://www.imelfin.com/'
    author = 'support@imelfin.com'
    isEpubor = False

    @property
    def product_id(self):
        if iswindows:
            return '36498-450'
        else:
            if isosx:
                return '36498-460'
            if islinux:
                return '36498-304'

    @property
    def price(self):
        if iswindows:
            return '22.99'
        else:
            if isosx:
                return '22.99'
            if islinux:
                return '22.99'

    @property
    def help(self):
        if iswindows:
            return 'http://www.imelfin.com/audible-converter.html'
        if isosx:
            return 'http://www.imelfin.com/mac-audible-converter.html'

    @property
    def guideText(self):
        return self.help

    @property
    def guideLink(self):
        return self.help

    @property
    def ticket(self):
        return 'http://ticket.imelfin.com'

    @property
    def AboutURL(self):
        return self.copyright

    @property
    def UpgradeURL(self):
        return self.copyright


def initProduct(product=None):
    global apps
    global res
    if product == 'Epubor':
        res = EpuborAudible()
    else:
        if product == 'imElfin':
            res = imElfinAudible()
    apps = Settings()