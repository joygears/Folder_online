# uncompyle6 version 3.8.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.13 |Anaconda, Inc.| (default, Mar 16 2021, 11:37:27) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: module\licenseBridge.py
import requests
from module.logger import logger
LICENSE_LINKS = [
 'http://code.epubor.com/Post/soft_retrieve_code.aspx',
 'http://download.epubor.com:9932/',
 'http://47.89.15.221:9932/']

def online_license(email, productid, version, mac, action, sn=''):
    for link in LICENSE_LINKS:
        if sn:
            link += '?data=' + email + '&productid=' + productid + '&version=' + version + '&mac=' + mac + '&action=' + action + '&code=' + sn
        else:
            link += '?data=' + email + '&productid=' + productid + '&version=' + version + '&mac=' + mac + '&action=' + action
        try:
            logger.debug('Auth online license with link: ' + link)
            return requests.get(link, timeout=6).text
        except Exception as e:
            logger.error('Failed to get license from online server: ' + str(e))

    return ''