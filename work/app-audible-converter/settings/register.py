# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: settings\register.py
import os, re, datetime, encodings.idna, requests
from ctypes import *
from urllib.parse import quote
from settings.settings import res, tr, iswindows, isosx
from PyQt5.QtWidgets import QMessageBox
from module.licenseBridge import online_license
RegAction_Register = 0
RegAction_Check = 1
RegAction_DeRegister = 2

class codeInfo(Structure):
    _fields_ = [
     (
      'czProductName', c_char * 255),
     (
      'nProductMajorVersion', c_ubyte),
     (
      'nProductMinorVersion', c_ubyte),
     (
      'czUserId', c_char * 254),
     (
      'nGenerateTime', c_int),
     (
      'czTime', c_char * 25),
     (
      'czTickcount', c_char * 10),
     (
      'nLimits', c_ubyte),
     (
      'cPlatform', c_char),
     (
      'nReserve', c_int)]


blackEmailList = [
 'NiOS@S.n.D']
blackLicenseCodeList = ['']

def checkEmailOrderId(data):
    pattern1 = re.compile('^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$')
    pattern2 = re.compile('(\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*)|(\\d{6,9})')
    return pattern1.match(data) or pattern2.match(data)


class Register:
    days_expired = 365
    info_expired = tr('License code can only be used to register in ') + str(days_expired) + tr('days after being generated.') + '<a href="' + res.help + '">' + tr('Get solution') + '</a>'
    reg_error = {-1: tr('Registration code is invalid.'), 
     -2: tr('Registration code is not compatible with this operating system.'), 
     -3: tr('Registration code is not compatible with your license email.'), 
     -4: tr('Registration code is not compatible with this software.'), 
     -5: tr('Registration code is not compatible with this software version.'), 
     -6: tr('Registration code has been expired.'), 
     -7: info_expired}

    def __init__(self, id, parent):
        self.id = id
        self.parent = parent
        if iswindows:
            dllPath = os.path.join('plugins', 'libauthdll.dll')
            self.Platform = 'W'
        else:
            if isosx:
                dllPath = os.path.join('plugins', 'libauthdll.dylib')
                self.Platform = 'M'
        try:
            dllhandle = CDLL(dllPath)
            self.verifySerial = dllhandle.VerifySerial
            self.decomposeSerial = dllhandle.DecomposeSerial
        except Exception:
            if iswindows:
                try:
                    dllhandle = WinDLL(dllPath)
                    self.verifySerial = dllhandle.VerifySerial_20
                    self.decomposeSerial = dllhandle.DecomposeSerial_8
                    return
                except Exception:
                    pass

            self.verifySerial = None
            self.decomposeSerial = None

    def verify(self, sn, email, isRegDialog=False):
        if not self.checkSn(sn):
            return -1
        else:
            id = email[:5]
            version = self.version()
            ret = self.verifySerial(c_char(self.Platform.encode('utf-8')), c_char_p(id.encode('utf-8')), c_char_p(res.product_id.encode('utf-8')), c_char_p(version.encode('utf-8')), c_char_p(sn.encode('utf-8')))
            if ret > 0:
                snInfo = self.decompose(sn)
                if not snInfo:
                    return -1
                ver = version.split('.')
                if snInfo.nProductMajorVersion != int(ver[0]) or snInfo.nProductMinorVersion != int(ver[1]):
                    return -5
                else:
                    if isRegDialog:
                        days = (datetime.datetime.now() - datetime.datetime.fromtimestamp(snInfo.nGenerateTime)).days
                        if days >= self.days_expired:
                            return -7
                    return 0
            if ret in self.reg_error:
                if ret == -6:
                    res.regInfo.isExpired = True
            else:
                ret = -9
            return ret

    def decompose(self, sn):
        regInfo = codeInfo()
        try:
            self.decomposeSerial(c_char_p(sn.encode('utf-8')), byref(regInfo))
        except Exception as e:
            print('decompose', e)
            return

        return regInfo

    def version(self):
        ret = res.version.split('.')
        return ret[0] + '.' + ret[1]

    def checkSn(self, sn):
        if len(sn) != 36:
            return False
        else:
            return sn[7] == '-' and sn[14] == '-' and sn[21] == '-' and sn[28] == '-'

    def getUrlContent(self, urlString):
        try:
            return requests.get(url=urlString, timeout=10).text
        except Exception as e:
            print('getUrlContent', e)

        return ''

    def register(self, email, licenseCode):
        tString = online_license(quote(email), res.product_id, res.versionReg, self.id, 'register')
        if tString:
            tList = tString.split(',')
            if len(tList) == 3:
                if tList[0] in [str(i) for i in range(8)]:
                    if tList[0] == '0':
                        if checkEmailOrderId(tList[2]):
                            if self.checkSn(tList[1]):
                                return (
                                 tList[2], tList[1], '0')
                    raise Exception('')
        else:
            if licenseCode:
                ret = self.verify(licenseCode, email, isRegDialog=True)
                if ret == 0:
                    return (
                     email, licenseCode, '0')
                raise Exception(ret)
            else:
                raise Exception(tr('Registration failed, please try to enter email to register.'))

    def check(self, email, licenseCode):
        ret = self.verify(licenseCode, email, isRegDialog=False)
        if ret == 0:
            return (
             email, licenseCode, '0')
        raise Exception(ret)

    def deregister(self, email):
        online_license(quote(email), res.product_id, res.versionReg, self.id, 'deregister')
        return ('der_OK', '', '0')

    def Register(self, email, action):
        if not email or not self.id:
            return ('', '', '')
        try:
            tList = email.split(';')
            email = tList[0]
            if email in blackEmailList:
                raise Exception('')
            licenseCode = ''
            if len(tList) == 2:
                licenseCode = tList[1]
                if licenseCode:
                    if licenseCode in blackLicenseCodeList:
                        raise Exception('')
            if not checkEmailOrderId(email):
                raise Exception(tr('Email format is incorrect!'))
            if action == RegAction_Register:
                return self.register(email, licenseCode)
            if action == RegAction_Check:
                return self.check(email, licenseCode)
            if action == RegAction_DeRegister:
                return self.deregister(email)
        except Exception as e:
            if action == RegAction_Register:
                result = e.args[0]
                if type(result) == str:
                    if result:
                        return (
                         '', result, 'NoQMessageBox')
                elif type(result) == int:
                    if result in self.reg_error:
                        return (
                         '', '', self.reg_error[result])
            return (
             '', '', tr('Registration failed!'))