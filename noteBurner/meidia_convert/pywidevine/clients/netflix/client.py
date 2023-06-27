import base64
from datetime import datetime
import gzip
import zlib
import json
import logging
from io import BytesIO
import random
import time
import os
import re
from itertools import islice


import requests
from Cryptodome.Cipher import AES
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.Hash import HMAC, SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util import Padding

import pywidevine.downloader.wvdownloaderconfig as wvdl_cfg
import pywidevine.clients.netflix.config as nf_cfg
import pywidevine.clients.netflix.subs as subs
#from netflix import parseCookieFile
from pywidevine.decrypt.wvdecrypt import WvDecrypt
from pywidevine.decrypt.wvdecryptconfig import WvDecryptConfig
from pywidevine.downloader.tracks import VideoTrack, AudioTrack, SubtitleTrack

# for operator sessions
from pywidevine.cdm import cdm, deviceconfig


from urllib3.exceptions import InsecureRequestWarning
import execjs
# Suppress only the single warning from urllib3 needed.
from utils import getSystemProxies

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

import urllib3

currentFile = __file__
realPath = os.path.realpath(currentFile)
realPath = realPath.replace('pywidevine\\clients\\netflix\\client.py', '')
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
wvDecrypterexe = dirPath + '/binaries/wvDecrypter/wvDecrypter.exe'
challengeBIN = dirPath + '/binaries/wvDecrypter/challenge.bin'
licenceBIN = dirPath + '/binaries/wvDecrypter/licence.bin'
mp4dump = dirPath + "/binaries/mp4dump.exe"
def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies

# keys are not padded properly
def base64key_decode(payload):
    l = len(payload) % 4
    if l == 2:
        payload += '=='
    elif l == 3:
        payload += '='
    elif l != 0:
        raise ValueError('Invalid base64 string')
    return base64.urlsafe_b64decode(payload.encode('utf-8'))


def find_str(s, char):
        index = 0
        if char in s:
            c = char[0]
            for ch in s:
                if ch == c and s[index:index + len(char)] == char:
                    return index
                index += 1

        return -1


class NetflixClient(object):
    def __init__(self, client_config):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("creating NetflixClient object")
        self.client_config = client_config
        self.session = requests.Session()
        self.current_message_id = 0
        self.rsa_key = None
        self.encryption_key = None
        self.sign_key = None
        self.sequence_number = None
        self.mastertoken = None
        self.useridtoken = None
        self.playbackContextId = None
        self.drmContextId = None
        self.playbackContextId_hpl = None
        self.drmContextId_hpl = None
        self.tokens = []
        self.rndm = random.SystemRandom()
        #self.cookies = self.cookie_login()

        # for operator sessions:
        if self.client_config.config['wv_keyexchange']:
            self.wv_keyexchange = True
            self.cdm = cdm.Cdm()
            self.cdm_session = None
        else:
            self.wv_keyexchange = False
            self.cdm = None
            self.cdm_session = None


    def login(self):
        self.logger.info("acquiring token & key for netflix api")
        config_dict = self.client_config.config

        #if self.cookies is None:
        #    self.cookies = self.cookie_login()

        if self.file_exists(wvdl_cfg.COOKIES_FOLDER, config_dict['msl_storage']):
            self.logger.info("old MSL data found, using")
            self.__load_msl_data()
        else:
            # could add support for other key exchanges here
            if not self.wv_keyexchange:
                if self.file_exists(wvdl_cfg.COOKIES_FOLDER, 'rsa_key.bin'):
                    self.logger.info('old RSA key found, using')
                    self.__load_rsa_keys()
                else:
                    self.logger.info('create new RSA Keys')
                    # Create new Key Pair and save
                    self.rsa_key = RSA.generate(2048)
                    self.__save_rsa_keys()
            # both RSA and wv key exchanges can be performed now
            self.__perform_key_handshake()

        if self.encryption_key:
            self.logger.info("negotiation successful, token & key acquired")
            return True
        else:
            self.logger.error("failed to perform key handshake")
            return False
    
    '''def cookie_login(self):
        """Logs into netflix"""
        config_dict = self.client_config.config
        post_data = {
            'email': config_dict['username'],
            'password': config_dict['password'],
            'rememberMe': 'true',
            'mode': 'login',
            'action': 'loginAction',
            'withFields': 'email,password,rememberMe,nextPage,showPassword',
            'nextPage': '',
            'showPassword': '',
        }
        req = self.session.post('https://www.netflix.com/login', post_data)
        return req.cookies'''

    def get_track_and_init_info(self,cookie,session_id="",challengeBase64=""):
        config_dict = self.client_config.config
        id = int(time.time() * 10000)
        xid = int(time.time() * 10000)
        manifest_request_data = {
                "id": id,
                "languages": [
                    "en-TW"
                ],
                "params": {
                    "clientVersion": "6.0035.231.911",
                    "contentPlaygraph": [
                        "start"
                    ],
                    "desiredSegmentVmaf": "plus_lts",
                    "desiredVmaf": "plus_lts",
                    "drmType": "widevine",
                    "drmVersion": 25,
                    "flavor": "STANDARD",
                    "imageSubtitleHeight": 1080,
                    "isBranching": False,
                    "isNonMember": False,
                    "isUIAutoPlay": False,
                    "licenseType": "standard",
                    "manifestVersion": "v2",
                    "preferAssistiveAudio": False,
                    "profileGroups": [
                        {
                            "name": "default",
                            "profiles": [
                                "webvtt-lssdh-ios8",
                                "webvtt-lssdh-ios8",
                                "heaac-2-dash",
                                "heaac-2hq-dash",
                                "playready-h264mpl30-dash",
                                "playready-h264mpl31-dash",
                                "playready-h264hpl30-dash",
                                "playready-h264hpl31-dash",
                                "vp9-profile0-L30-dash-cenc",
                                "vp9-profile0-L31-dash-cenc",
                                "av1-main-L30-dash-cbcs-prk",
                                "av1-main-L31-dash-cbcs-prk",
                                "dfxp-ls-sdh",
                                "simplesdh",
                                "nflx-cmisc",
                                "imsc1.1",
                                "BIF240",
                                "BIF320"
                            ]
                        }
                    ],
                    "profiles": [
                        "webvtt-lssdh-ios8",
                        "webvtt-lssdh-ios8",
                        "heaac-2-dash",
                        "heaac-2hq-dash",
                        "playready-h264mpl30-dash",
                        "playready-h264mpl31-dash",
                        "playready-h264hpl30-dash",
                        "playready-h264hpl31-dash",
                        "vp9-profile0-L30-dash-cenc",
                        "vp9-profile0-L31-dash-cenc",
                        "av1-main-L30-dash-cbcs-prk",
                        "av1-main-L31-dash-cbcs-prk",
                        "dfxp-ls-sdh",
                        "simplesdh",
                        "nflx-cmisc",
                        "imsc1.1",
                        "BIF240",
                        "BIF320"
                    ],
                    "requestSegmentVmaf": False,
                    "showAllSubDubTracks": True,
                    "supportsPartialHydration": False,
                    "supportsPreReleasePin": True,
                    "supportsUnequalizedDownloadables": True,
                    "supportsWatermark": True,
                    "titleSpecificData": {
                        str(self.client_config.viewable_id): {
                            "unletterboxed": False
                        }
                    },
                    "type": "standard",
                    "uiPlatform": "SHAKTI",
                    "uiVersion": "shakti-v0f92b626",
                    "useHttpsStreams": True,
                    "usePsshBox": True,
                    "videoOutputInfo": [
                        {
                            "isHdcpEngaged": False,
                            "outputType": "unknown",
                            "supportedHdcpVersions": [],
                            "type": "DigitalVideoOutputDescriptor"
                        }
                    ],
                    "viewableId": self.client_config.viewable_id,
                    "xid": xid
                },
                "url": "licensedManifest",
                "version": 2
            }
        if session_id!="" and challengeBase64!="":
            manifest_request_data = {
                "id": id,
                "languages": [
                    "en-TW"
                ],
                "params": {
                    "challenges": {
                        "default": [
                            {
                                "challengeBase64": challengeBase64,
                                "clientTime": int(id / 10000),
                                "drmSessionId": session_id
                            }
                        ]
                    },
                    "clientVersion": "6.0035.231.911",
                    "contentPlaygraph": [
                        "start"
                    ],
                    "desiredSegmentVmaf": "plus_lts",
                    "desiredVmaf": "plus_lts",
                    "drmType": "widevine",
                    "drmVersion": 25,
                    "flavor": "STANDARD",
                    "imageSubtitleHeight": 1080,
                    "isBranching": False,
                    "isNonMember": False,
                    "isUIAutoPlay": False,
                    "licenseType": "standard",
                    "manifestVersion": "v2",
                    "preferAssistiveAudio": False,
                    "profileGroups": [
                        {
                            "name": "default",
                            "profiles": [
                                "webvtt-lssdh-ios8",
                                "webvtt-lssdh-ios8",
                                "heaac-2-dash",
                                "heaac-2hq-dash",
                                "playready-h264mpl30-dash",
                                "playready-h264mpl31-dash",
                                "playready-h264hpl30-dash",
                                "playready-h264hpl31-dash",
                                "vp9-profile0-L30-dash-cenc",
                                "vp9-profile0-L31-dash-cenc",
                                "av1-main-L30-dash-cbcs-prk",
                                "av1-main-L31-dash-cbcs-prk",
                                "dfxp-ls-sdh",
                                "simplesdh",
                                "nflx-cmisc",
                                "imsc1.1",
                                "BIF240",
                                "BIF320"
                            ]
                        }
                    ],
                    "profiles": [
                        "webvtt-lssdh-ios8",
                        "webvtt-lssdh-ios8",
                        "heaac-2-dash",
                        "heaac-2hq-dash",
                        "playready-h264mpl30-dash",
                        "playready-h264mpl31-dash",
                        "playready-h264hpl30-dash",
                        "playready-h264hpl31-dash",
                        "vp9-profile0-L30-dash-cenc",
                        "vp9-profile0-L31-dash-cenc",
                        "av1-main-L30-dash-cbcs-prk",
                        "av1-main-L31-dash-cbcs-prk",
                        "dfxp-ls-sdh",
                        "simplesdh",
                        "nflx-cmisc",
                        "imsc1.1",
                        "BIF240",
                        "BIF320"
                    ],
                    "requestSegmentVmaf": False,
                    "showAllSubDubTracks": True,
                    "supportsPartialHydration": False,
                    "supportsPreReleasePin": True,
                    "supportsUnequalizedDownloadables": True,
                    "supportsWatermark": True,
                    "titleSpecificData": {
                        str(self.client_config.viewable_id): {
                            "unletterboxed": False
                        }
                    },
                    "type": "standard",
                    "uiPlatform": "SHAKTI",
                    "uiVersion": "shakti-v0f92b626",
                    "useHttpsStreams": True,
                    "usePsshBox": True,
                    "videoOutputInfo": [
                        {
                            "isHdcpEngaged": False,
                            "outputType": "unknown",
                            "supportedHdcpVersions": [],
                            "type": "DigitalVideoOutputDescriptor"
                        }
                    ],
                    "viewableId": self.client_config.viewable_id,
                    "xid": xid
                },
                "url": "licensedManifest",
                "version": 2
            }

        self.logger.debug("requesting manifest")
        request_data = self.__generate_msl_request_data(manifest_request_data)
        proxies = getSystemProxies()
        resp = self.session.post(nf_cfg.MANIFEST_ENDPOINT, request_data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}, verify=False,cookies=cookie,proxies=proxies)

        data = {}
        data_hpl = {}
        data_sd = {}

        try:
            # if the json() does not fail we have an error because the manifest response is a chuncked json response
            resp.json()
            self.logger.debug('Error getting Manifest: '+resp.text)
            return False, None
        except ValueError:
            # json() failed so parse the chunked response
            global data1
            self.logger.debug('Got chunked Manifest Response: ' + resp.text)
            resp = self.__parse_chunked_msl_response(resp.text)

            self.logger.debug('Parsed chunked Response: ' + json.dumps(resp))
            data = self.__decrypt_payload_chunk(resp['payloads'])

        return data


    def get_license(self, challenge, session_id):


        
        #print(data)
        
        id = int(time.time() * 10000)
        self.logger.info("doing license request")
        #self.logger.debug(challenge)
        #.decode('latin-1'),
        #'challengeBase64': base64.b64encode(challenge).decode('utf-8'),
        #challenge1 = "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"
        
        #self.logger.debug("challenge - {}".format(base64.b64encode(challenge)))
        
        license_request_data = {
            #'method': 'license',
            #'licenseType': 'STANDARD',
            #'clientVersion': '4.0004.899.011',
            #'uiVersion': 'akira',
            #'languages': ['en-US'],
            #'playbackContextId': self.playbackContextId,
            #'drmContextIds': [self.drmContextId],
            #'challenges': [{
            #    'dataBase64': base64.b64encode(challenge).decode('utf-8'),
            #    'sessionId': "14673889385265"
            'version': 2,
            'url': links_license, #data1['result']['links']['license']['href'],
            'id': id,
            'esn': self.client_config.config['esn'],
            'languages': ['en-US'],
            'uiVersion': 'shakti-v25d2fa21',
            'clientVersion': '6.0011.511.011',
            'params': [{
                'sessionId': session_id,
                'clientTime': int(id / 10000),
                'challengeBase64': base64.b64encode(challenge).decode('utf-8'),
                'xid': int(id + 1610)
            }],
            #base64.b64encode(challenge).decode('utf-8')
	    #self.client_config.config['esn']
            #'clientTime': int(time.time()),
            #'clientTime': int(id / 10000),
            #'sessionId': '14673889385265',
            #'clientTime': int(id / 10000),
            #'xid': int((int(time.time()) + 0.1612) * 1000)
            'echo': 'sessionId'
        }
        #license_request_data = str(license_request_data)
        request_data = self.__generate_msl_request_data_lic(license_request_data)

        cookies = parseCookieFile('cookies.txt')
        resp = self.session.post(nf_cfg.LICENSE_ENDPOINT, request_data, headers={'User-Agent': 'Gibbon/2018.1.6.3/2018.1.6.3: Netflix/2018.1.6.3 (DEVTYPE=NFANDROID2-PRV-FIRETVSTICK2016; CERTVER=0)'}, verify=False,cookies=cookies)

        """
        try:
            # If is valid json the request for the licnese failed
            resp.json()
            self.logger.debug('Error getting license: '+resp.text)
            exit(1)
        except ValueError:
            # json() failed so we have a chunked json response
            resp = self.__parse_chunked_msl_response(resp.text)
            data = self.__decrypt_payload_chunk(resp['payloads'])
            self.logger.debug(data)
            #if data['success'] is True:
            if 'licenseResponseBase64' in data[0]:
                #return data['result']['licenses'][0]['data']
                #return response['result'][0]['licenseResponseBase64']
                return data[0]['licenseResponseBase64']
            else:
                self.logger.debug('Error getting license: ' + json.dumps(data))
                exit(1)
        """
        # json() failed so we have a chunked json response
        resp = self.__parse_chunked_msl_response(resp.text)
        data = self.__decrypt_payload_chunk(resp['payloads'])
        self.logger.debug(data)
        
        fobj = open("license.json", "w") 
        playlist = str(data)
        fobj.write(playlist)
        fobj.close()
        
        #print(data['result'][0]['licenseResponseBase64'])
        
        
        return data['result'][0]['licenseResponseBase64']
        
        #if data['success'] is True:
        #data[0]
        #if 'licenseResponseBase64' in data:
                #return data['result']['licenses'][0]['data']
                #return response['result'][0]['licenseResponseBase64']
                #return data['links']['releaseLicense']['href']
         #       return data['licenseResponseBase64']


    def __get_base_url(self, urls):
        for key in urls:
            return urls[key]

    def __decrypt_payload_chunk(self, payloadchunks):
        decrypted_payload = ''
        for chunk in payloadchunks:
            payloadchunk = json.loads(chunk)
            try:
                encryption_envelope = str(bytes(payloadchunk['payload'], encoding="utf-8").decode('utf8'))
            except TypeError:
                encryption_envelope = payloadchunk['payload']
            # Decrypt the text
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, base64.standard_b64decode(json.loads(base64.standard_b64decode(encryption_envelope))['iv']))
            plaintext = cipher.decrypt(base64.standard_b64decode(json.loads(base64.standard_b64decode(encryption_envelope))['ciphertext']))
            # unpad the plaintext
            plaintext = json.loads((Padding.unpad(plaintext, 16)))
            data = plaintext['data']

            # uncompress data if compressed
            #data = base64.standard_b64decode(data)
            #if plaintext['compressionalgo'] == 'GZIP':
            #    data = zlib.decompress(base64.standard_b64decode(data), 16 + zlib.MAX_WBITS)
            #else:
            #    data = base64.standard_b64decode(data)

            #decrypted_payload += data.decode('utf-8')
            decrypted_payload += self.__lzw_decode(data)
        #decrypted_payload = json.loads(decrypted_payload)[1]['payload']['data']
        #decrypted_payload = base64.standard_b64decode(decrypted_payload)
        #return json.loads(decrypted_payload)
        decrypted_payload = json.loads(decrypted_payload)
        return decrypted_payload

    def __parse_chunked_msl_response(self, message):
        header = message.split('}}')[0] + '}}'
        payloads = re.split(',\"signature\":\"[0-9A-Za-z=/+]+\"}', message.split('}}')[1])
        payloads = [x + '}' for x in payloads][:-1]

        return {
            'header': header,
            'payloads': payloads
        }

    def __generate_msl_request_data(self, data):

        header_encryption_envelope = self.__encrypt(self.__generate_msl_header())

        header = {
            'headerdata': base64.standard_b64encode(header_encryption_envelope.encode('utf-8')).decode('utf-8'),
            'signature': self.__sign(header_encryption_envelope).decode('utf-8'),
            'mastertoken': self.mastertoken,
        }
        #header["headerdata"] = "eyJrZXlpZCI6Ik5GQ0RDSC0wMi1KNjFXV0VBS0FMNFY0WDlUR0ZXRlZIRDBEQTA0QUZfOTkiLCJpdiI6Im56QmpHZ2E4Vy9waW5aWnphNFF4RlE9PSIsImNpcGhlcnRleHQiOiIyNWE5WmlhZzZtcjhQZzNsZDM4ZUlQeUpwa2tUZk10QVhpOXZ1dEFIQmtRY1NLb3JFeEhJbkJ4T1pkVjI1TWU0c0FJZzZ3UGRKaytHdmpFcE8xb2tPc2tYTGd1VGd5Y2pyNGJRbG53a3NDRnRqQ0l4cWZUMXBkQnNxc0JsdWdBNWNMcldmS0cxNk9yWWgveTRaWkJUMzh3cTJxcWEwYmRrSk1IL0w0NmFjdE9Pc25lZnd3TkZFbStJVDdyMzF6bS9jMk9UQ094UFB3bi9EamJ5WUpNczYvTjQxcG9DRTZvNGg5eklvemhkM1BzeHpzNlpBL3hkYnkwaE5vLzdUTi9QcmpRRkxrVlFkaU5XUlpBTXN6YTBnOElRbHlxSWhSdjhtMEZiT2pnN1hxaUJOaVE0eGFqZjdvMVhvd3hXV0ZaYVBRMlNnWklidHJiZTRQdXRFOG00dkljLzV6TjRQN2NyYzBjTktVM0NNWnhGeXdMc3Q1UW83Ri90aEwwNlR4Vko1Yi9NZUxETklPMkNiblRwMXloUnF2UVdlaVR5VEtHZGNCNmhHcGtyYzBaTDByU3l4c2sza2RoMDdNbXpEYTd5dEp6LzlYS3NkR1JoYXkrNUV3a01scW13Nm1kUDhaVDArWnpUV2QvV3ZtbU5ob2IyY1gyYUlCSjRxUzhkU3pMWmdJTVpDNkRLSnpwKzBlc1BTRVgrMGJhQnBLM05ETitwZFhzVFFpMEtIRFR3Y2hxc1YxYjFzb0U0b0RuMDZaZ0x2QTRmZk1WTm54MzdZdEhaeXdkYWtNYmk0bkh1RVFmSWdaWktKOWNjNk5aRW5tYXJ2bnBkRnJxVEozMjFKcDQwRnhKOXNtMkRacExMeTFSZ3VubDFBcElLRXdtNTRqNHpXWk5IUW9vZW9FWFlRQklhUkdOSE16TTI3cVVEWkxtV1N2eW9ISGlSRjN6MGxGbXNQMS9FdExRdjhkSERDTjZhTUNmaWlaWkk0UHFYNEoyYzJFNjh1SUtweE4ybGRBc1k4bU1Dbk5VVmxKYnoxMXFnRVg2QmZLQzZ0OVpMS0lYWVFFNlh4UGJMU0lPbUp0NDhUOXNvOTgrc2dxUFcydG1tUDkzSkRPcEhsczVyell1emVSQ3g2Z0dyczRkOEVVQjZmenpkeVZnbTZpU2NPVS84cDVKWVBUdkZSNTFsVXFrSURkWWFJbkhMQms4cWdiUXpsRnpXQ0d2SytPMzZhN0svdWtjZFMvQU9qcnlSbTk2OVBQMitGcmR0L2pKQ2xhTjVZTGZjVEVuTHVqYnJiSmIySzBtNVdQS2pONW5JeFM0NXlvSVBBdUhtRWlWZ21aOWZkblpkdXVYbEFJRmRBUUU2UXR1RG9CUzVDQVNUK3FJS0QxcWV2UjJ4VEJNRjd0Q0ZqRy9vbWZlUzhodFNzVmdwcEY3Y012TTVVYzJwSTZIeWNUY0JUS1VZbjlDSDF1RytRUnNxaURMRkhMR1had1JTWmJBZlczRHpRRjFhNFNIUUJVWjRncUFZanhuRHJDNzJpVm10OC8zdTYzY2d4YlhEc2JHWXFEejFseXRDK1pWY2taZEhpNmVhQXU1NWlvQlRXZ1AwRjdsVk1XWFYzOEp1RWQzSmJFb3d5V1p6N1ZhdG5iKzl0SVZqWjByQXRmNW10STBJQks3Umk3NEh0L1RjVWtRd2xCU09Vb3NnaUgwREx1OWsvKzJCQWplamswZUdTMk1BQkRPMzFERitHRzZmbld5eUJsYXhCZGF3blplUS9ybnlwUzRjeVNtTG95TWh2Um5Cei9wVFB5eW5tU29ZMVFoalpoSVcxT040OVd3Sm15NGk4d0RXYTA4YTV5UHJsNzNldnU3WHRrRWc1R1ZXVnlVUWxlTklZN1hNNlg2RDIwYWFMcUJTeWNXU0dCUXdCZXlzTUpHQ2FrK0FVS05QcnRMZWZjWW5QR1lqUGNXeThUcVRicS9taVdjbmlsdUFMZ2F6YStPOWFYVFhjdno0UnZVYzVJVW8xVWxXNWNyVXNqeGtPSjZCTURIV1ZWK0lTM3F2K2pFVXErWE9QVFVHREszcGpyS0QzdHEweTFrQzZGRFdFTDF3dWNkTzRLc0JVS3p0aWw5OEZkK1ZyWTc4YVhlQjhtTnFaZmFRQkRhWlJqNWJjTjdXWWpBQ056NGJWY09nVHcxc0JWcEk0YXNwTVlONCtEZVNRc0M2c0xKVUMzZG1XWXdLV2pEZ2RLejhpcFdEVUNiZHVRT0hCNmFjWlJHQ0wwbDdiTmd3Sy9MQjBod0NDRCtyVldBb1pkZGxZcVVybmc2Q2xlN0RLM004WUZGWW5IMUNFMWg5dEhzNVEyK1czc2RkeXN3VkNmYWVBeXhreWtSa0MvbzM4cnFHcTNLUHJhL1RSbVdKUkx5MjlGdTg5ditqWWs4bEcyb29TcmYrclIySnlaanJsREs0Z2l2eEc0VTZtYWVVV0QyYXBvWVkrQzk2cDBJN3RCQ055U1pqSEpocWkxb0hPejZNOFNoeURjVEx5eXhqcTd6cUFnQlhJb0c5TXQvVU13ZFhjM25VaGo4d2txRmR0c2xoMzF6VWhyd1VGZGV3YmN5Ulh3WVFrV2pUcnZXMmxiN2NSSEJ4RDY5ZjY1OGRjSENITm4wMFVZS0ZsSEJyU0ZoZUg1WHRTTVNEMjFXbzZJM2Y3bkpyT3RFYTB4TXZHeWhrVEtqZVViZ0JMUFBZUWkxUmZOQldySzhSemZTY0N2eW93S2tSb09rY1o1TG8vQVFReVJtVmlEZnp5eHZaUEQ1OTlPaHdadlZaOXNReXdHbE1FL2sxczJNa2NvQW0yeW91VDV5eEJrVVdmczRzWmtYU3B0cEhPL3NHZTlNSFVDR010N21xMDRHQ1dRaGdaY3JZNWthT08rSnpEaG5aYWdxR1lsYnM5bUJXSjRDQStmM1VJSXB1enhEanF1eVdxSEFnS1dtcGhDUjNtZVNqa2pIakZwUGRMM2M4eHJPNDI5b3kyVVdqdU5id2RSakpCUEw5QXF4N1FxbEo4YWRhWU1YbHRaRHVvUFRyR25MNnUwQUhMTVZpZ1hRbG53aWxZdVFvS2pzMmZrcDA4MWViL00zbGk2eEhRY2hjZm5UMFBHWWxuQm5NMXJxK3BhSURxR3A2a0M3eUp3dXEya2dyK3ZpblEyZ2YvTGI3ZVIwbEJQanBNYXFZY2RRUDRMcjZ0dFdQaENNeS9KT2NOVDA5VnpnNFFHdTJRRFV5WXNmTUxteThrZGhCNU5xVUIvWUR3eS9FUitWbWo4dmNSalAyQW5GRjVJM25UTUhHRHVCbUxoTUNCV25ybkNtMzlJcldheEtLVnlvMmNyb0hSV29IWTNzT2pnL2NlMjRTVk03Z2hOWm1aalZNelJEK0JSQTVRZGNXR0RCb3hSdmJLUjN1eU5oWG9KakxVbHBGbkZHNGIvVjBFMzhydmo3OUpsZnVTbW9lRHNwajkyR1pCM3l1T0xJQXpIdWwvS1g2RVBYbklaOEo3UHloMFhTUXhJTXo1ang2UjVzd0Q0SmRLK1F3aGlGNDBUOWVQN3cySit0WDgzVE1jUERPNU5JcVNKN1BoWWpaMnE0dzIrdU5vT3ZYR0lzaERjU0hIRnY1VkZDQlc1NzYrWHN0V3RvVTNxOWIwdElSY3lZMG02VFdBSmEyclhQZzVGTVdJQW1rSStDWU1MV2MxR2dhYSsyUGR0V2Yvalcwc3JldkhuZnNucHhSR0ZoUnUvQnRJTWxHMXlwRVV4bVY1VWhLWlBqZEpyalFoanhKZTRpRXV5L0c0R0g3SC90bUx4M3d5OEVVeGlsZmh2bWtlTFlKOEJQSW91U3VkNUVxdTBjQTlEOTdxdmFGSXJUVzNPNWhEeS8rNFpBUklWRDNZUUxiRk1UOU9HeEJza0QrS3gzODN5OEpLL1BJaTVNckYzOVJOd1pYSlpzR1lJR3V3bFZway9YN3JmTGtHdnJlWElrZkljR1hJcGxOQStNZUo3czkvV29IUEZTandGUk5LTUFMbU5vS0RpRDVMTElQZDZ4Q0hHSWJMVkhFb3hBaWJkYmJYdkN3UDVmeUZPbExudTZ5ZVAxUXduNlpsanFHT1QzMlE1MnA5WmJNa1hpdzdhWFRkV1ZBMlo4eklFdURsdFg5cHJ6dnh6RFpmb3FFcnQ1bzZOeTAra042cHpsTFN1U1RiTEhxZGJ0MXN2ZlBaaDZKUHJHN1RLYmxyL1Ribk1ZQ0doMFRGWW5oT2JFZ1lWOHVPbmVFRVNEWmRUNmtDZndRU2dXZnZjamtNMXZKVzBLRFhWdEtITVRHVXQ3QnVuZC9nSVhpNEVINVZJZlAwc004V2h1WlduckNCek53Wk1EYnZBPT0iLCJzaGEyNTYiOiJBQT09In0="

        # Serialize the given Data
        #serialized_data = json.dumps(data)
        #serialized_data = serialized_data.replace('"', '\\"')
        #serialized_data = '[{},{"headers":{},"path":"/cbp/cadmium-13","payload":{"data":"' + serialized_data + '"},"query":""}]\n'
        #compressed_data = self.__compress_data(serialized_data)
        
        
        data1 = json.dumps(data)


        first_payload = {
            "messageid": self.current_message_id,
            #"data": compressed_data.decode('utf-8'),
            #"compressionalgo":"LZW",
            "data": (base64.standard_b64encode(data1.encode('utf-8'))).decode('utf-8'),
            #"data": (base64.standard_b64encode(self.__lzw_encode(data1))).decode('utf-8'),
            "sequencenumber": 1,
            #"endofmsg": True
        }
        first_payload_encryption_envelope = self.__encrypt(json.dumps(first_payload))
        #first_payload_encryption_envelope = '{"keyid":"NFCDCH-02-J61WWEAKAL4V4X9TGFWFVHD0DA04AF_99","iv":"bj6IlGNwNipykm+s0SQplQ==","ciphertext":"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","sha256":"AA=="}'
        first_payload_chunk = {
            'payload': base64.standard_b64encode(first_payload_encryption_envelope.encode('utf-8')).decode('utf-8'),
            'signature': self.__sign(first_payload_encryption_envelope).decode('utf-8'),
        }
        end_info = self.__generate_msl_end(2)
        end_payload = self.__encrypt(end_info)
        end_payload_chunk = {
            'payload': base64.standard_b64encode(end_payload.encode('utf-8')).decode('utf-8'),
            'signature': self.__sign(end_payload).decode('utf-8'),
        }

        #header = '{"mastertoken":{"tokendata":"eyJzZXNzaW9uZGF0YSI6IkJRQ0FBQUVCRU5VdHVpRDBKRXZ4dXJSSndYeGNHQktCUUJEN05TSFdIMFhUQ2hEc0FqaDR6bE1GenJuWlFwZktudmovdU5kVkUzMXF6SE9QMHZ5SGNsWVJWcXc4Rm1sUUZia2c3MlMrd2ZsbG9rZ1Z0QjV3QmljNk5qRjNIc3dRenQzMUVMejN5M0JZdzZVdm5kM1BybkRlZ2F5NjBxNytFT3o5Qnd5ME8ybUQ1cVZZclA5amtSZHVVdnFsbHFzWWRhdldvcEtVVElHRmxSQlFwTWFFQStuc21Idmh6S005MWNlMnQzK3hrR25uM1lRVnhCN2o5VjJvZmcwd3VJY2k3a1hpVXQwb1NjRnpuUDl0NDhHeTQyZTNaQU9rTFNLZnQyNnR5ZzljVm1QR3FVazlXTVVKMHE2OGpNY2VTaExNQmhUSUhqcWZQS3JQeHhiQVl2YU5XZnNDOVJHQ0hkS2NjWEowYTZkbXF6TWlwbm82anQ3bkErU3pRd2pnYy9hY3F6Z1Y5eCsybS9rUFdOWk5iWnlPa3Z1UEEyZFFyUzY3aitRTWxhZExDQVRQNUIzZ0hjeS9NUnhyTUVwR3JwYzNkMWdIcHMydkV0Z1YiLCJyZW5ld2Fsd2luZG93IjoxNjUzMzU4NzY3LCJzZXJpYWxudW1iZXIiOjc0ODI0MzEyNzEwNDY5OTEsImV4cGlyYXRpb24iOjE2NTQ0ODE5NjcsInNlcXVlbmNlbnVtYmVyIjo5OX0=","signature":"AQEAgQABASAXo5TTlezgbZfWE5J2WypC07MYkzby8/VS27VZz499rarqCDA="},"headerdata":"eyJrZXlpZCI6Ik5GQ0RDSC0wMi1KNjFXV0VBS0FMNFY0WDlUR0ZXRlZIRDBEQTA0QUZfOTkiLCJpdiI6IklMdHR4K0oveUdYc29hNTg4ODZWZlE9PSIsImNpcGhlcnRleHQiOiJnSm5YWExSdmFxVnNXV01ZSWpQdWpIM0JSRE03R05QTkR2K2VkbzN5R1RITStrRzFlSkVFb21EMzFyNGQ2QzNWN1hWUFV0YUVoZ3Q5UEhQb1dTRU1kY0NXSDZONzZUSVRwb3lsdEJJbHBwU2JlaThOTXBkV1R3MFJDZElTamNzRlpId2NwditLNm82THdxMGI0blZzTDBXWEs3VXpYQTUvQlRxT2I3T1JObGdrMWVwQzB4TXE3bFVDamtOOTBvZVZ3Tm9GR1N5emJqQUlReDVpdzltSE1HZ3NaeXRjOGcvNzlWVEtUT0I4UGd5M0hjRkFTK2hCVUM1N3pNaVRXRXdsbUtJcnRycnlVcFB5NDl3MXR0TDlLREM1RXFZSjhVNElDU2hqcUZBRzNPUUdPQzFURUxoWm5hRkRBU0xTWW9zQ2dLWE1lQkhHOHR5OWQrQnBDeFcrK0NNRUNWL3JBaGhseWxpa0dEdmZNaDhqaXFTWFZIZGtibUJ3WkFZYnFJbzBqQ3h6UWoxVHpubjU3YTRNdlNqNHRhaUFxVmR3ejlhYnVsaVE2RDMvTEFwUUZqNFEwTjcySkhHdHo3ZUpuV2V3NlpTN1NwUGxETnZ3RmsrUndLeXBCbDlXMFhEYXllSWZld0cvRnUvZWt6SkRPbEYrVWVoQlYzTUhkUzJBTGZLczVLK0xmN3hMVXZzR2NQWFlLRnhFY1l6cE1xT2dYY3NKNVc1RS9NNEw4VzhFL0pFWjR5TDk5bURyYy80RjlTb2N4dmYvTkNBVUR5MTNuWURoMDVtb2NXa2ptdGtVYlY4WVZsNGJTdkZreFN0cjJwN04rUmtlTVVqdDB5QW5zcC8yWVhMZ1JTMElMYk1hZVFUd0tyU1YvTnhhTG1TblZyLzZ1bEJBcEdRZ0hKS0NZOVJrTVB6eWdKR3BEWFFOTDBmczRsWThaa3cwS2VkU0gwRnNtVHhMb2xtQWo0d2ZXcmtnMVdidTlxb1dKZlJ4RGdYWWhZUVRzUUhFeWV6eTRqV0NvdEZwdXdyQkE5U2ZidWUrdTJOTXg2Y0pGWGxUaHZ1R0dQT0FoS3U2OEEvS1NyRGVPa3NNYWZWOFZqY1UvWEVvMUZPVlFmV240UVdXQVp4U3ozb2lHQ0Z2YXAwaVoyMGtTMEdwR01VVXYrUWI4YTRtZGJHcWNkSUZpVGQrS1JXcVNTYlFVZXdmcHZVSnNoNWp5RzNXTm8wVGlGdmpybjd6VUNUSDlMMzhSaSswckY2Zk91Y3NjT2dBUUNYT0N4SndXSWhIZU5NeGpOZGF1ZnNDRld4VDJBPT0iLCJzaGEyNTYiOiJBQT09In0=","signature":"VUc6+s+y+3xCAMpOUXxQeVL2FUYO/n6LEkiZOIU7lWg="}'
        js_first_payload_chunk = """{"payload":"eyJrZXlpZCI6Ik5GQ0RDSC0wMi1KNjFXV0VBS0FMNFY0WDlUR0ZXRlZIRDBEQTA0QUZfMTgwIiwiaXYiOiJ4a2p6ZGYxUlExdTVZNmJRcVpwdkFBPT0iLCJjaXBoZXJ0ZXh0IjoielRlTFpJYXdpd1kzTDJJcDRPODFnbmV6eXluZzAyMkJuSjZoQThFWTJ5dHo2L3FrWUViRVRZYWR6b21WMVlIZ254NXgzZ1c4TE5RY3ovNmR1QzdZQVY2Y3RNVCtuKy82aURxRm5vcWxPMnNnZXJmVHVhemtJVTNabWtPUFlocW4xT2pOV0J3ZkxyM2NxSzNYdVc4ZzRGUkdPcUxISTZwQ1dZZnhYRElGNU9PUENKdDVMS1g0Zytja1JPOUZNSlV1LzhmdGJtenA5d0F1K0hpM0dIbWp2WW9Fd2M1QXZoMFF0dGZyWUZZbkkxd1hGT01xY2VTMXNLN0xhL1ZWVGR6cEwyUUhIdjNKbnhLNm9uYlNkSDFsVTZoV3BzMmN4UDlUSi9FNE1IVm5POHZhbXhBZTg0WUdmczhMeGVab2c4VDNqZzdCS2MzanhnKzE1YnE0RC91UXBhV0FqeEh2RUhKQXNTdXA3TDMzaGswK1JnUitqZHllUUhmdnZyYlcxMVl5dWhrb1d3dzBsNHEvWE9qdnErMGh5Zm03RUh6SUtLK1plREdEajd1TDFJRnhQYkc0czR3U3E3RnFjZzVZWmVMd1Q3M1MralBlRW5PRmxTV2UrRUpObC9xZEpqVHBRKzdDcW5MWnBnRXJ0WG1jQ0MzWUdseWJONGgzMms4Z3FCeE5EVXRqZ2IwaDdETTZGdVY5S2RFMU5xa3JQeXJOSHlWcVBXbUJxQ0V5bFVBMVZCZFp5OGpnSzhxcjZRK3pSR09LcGlnN2FmQ24vQi9wMVE3ZXRmVnpRdTRqbm0xMnF3YmR2YlRFSVhzcWk3ckRWWDVGTUEvOTU3ZzA1MzlrTVFETlRRSm9UMmdaUE9DbFdoUEt2MHM3UjdXS0xxT1JzaVlVQXJIRG54UjB0dytjWm9QV082WnNEWU41eHNMN2FaNE41SEpvOXNZdEt5d21GM2ExRGkwNVAxRWhQK3IzQUVlb2kvdGpDNlFONmZMdWpBSlVNWVJRNytkakpOczJDOFZKcDgyYmljZTVZSTJDTXJzbzd6bVhsdFRFOFM1NDdEaEM5UUswNjdLbkNxZFByUmExUWN2RDhTcUtBY2I2d2F1S3g0VEFhSjAyNlQrbEloeTJmQzJKajlPZ0hSZ3NvOGREZCtTdnZoL08remVVY2krU3d2MzMzdFgxeENDR1ZkYjc3MEU2REsrQnRERCtmcGRsSG5MemZ6UU1kNWU4VHNOYVpMNG9WSE1kRUNLaExmWDJ5NlJPQi92cDRXWXlGUldxZEFEeDFDZmhub1c3K1RhejVoYVFRWXJMZGFIaUNXNEQzQ1F4dnIwWVJJNE9YYzNONWs4eXNTTkE1ZTZZeS9OTWJKbHJnWVlKS0FtMkFVRFQzZG04TnZLTzc2MVhLNHZ5NnBiTy9qV2xlNHlLL21kdWFuTnlhSlNoa25aYmtCRnhyNFU2aFp2TERUZVEzZ0ptYnZNSkxLbG95QWxRcjg5RWRzOG91ekMyWThnQ0MwdFJabjZrcnc0Mm82YkxQaThHUlU4TmtWaW1WYlRaMHloSGVqZXZuaWJiTkorWm0vRmhrVEJ3MHNtUjQxVGQ3MEgvZFU4dXUyQTU0ZVZMbGxBRHI3cXBtbEZDTUJvVzArZUpudGs4RUZ1ajZxekxwdEVJd0t4Ukp5ZG1GL0YzVWRLT2RJK3k5TGVPeFg1dUhVWDNNWGJZa01BRDRvU0lyeDliUStaeG1samxlOGNqTXBTNTRWQ1BtMXhHRzE0TlRNVE5Sd3p0SnFFU0RHeXlmeCtsaFlORFpnbmxHRzNFMlRZTGdpcm5VT0pDVlFDQ0loTHdXRU5zOHl0RjU4VUd0WWVyOVM2OGJxcm5ZQXRIbnV2cmZhNDRuVjY1a2pseUd5cUJMOVJyVVNVV2xjSUdWNVVrdDJhRmN5cFBnZGpwSXkwN3VqVk9KbTNFUWUrU0RHK1FVdERBZG1OZmxjZGJ5RStvMS9sWi9aMjJsQzlvMnNFMlFxWkpxQ1NwWlpYZDIzWXJKeDF4WmVnMC9oT3BxUHR5Rm1EcFpwcVNyUnlkSkhheHVIWmVjcThSV2haNkI1OVIvMEEyTmJYR1g0TXRBUE1wM3FIMGlIODVQSFNQWUY2Z1d2c0JxNDFuSmw0UktKR0M2b1FVZ3ZEdmNtUms1WEtjbk96c2NHeGgwUzhWRzh0WUlhaW5QQ1RzSzk0bFE0SGJ4UWp3bCsxdlh2U0FCMnkzK3dwNGhIYmhjTU1aOEJ6a3NVWm4xNVF4eTJNZUxyZ2JmeU1EcXhDVWdiVjgwYXVRZzM3Y0ZhR3Z1OExNVFFSRDdsbTJQZzNkT080YlZqTFdnRVEzdjRsSTBabGdCcjdWSFo5aUtSQmpoVXU3SjVUYWdVRGRQNFZudDErSXljYjlUMkFVN0phckpzeEFPSUtVdmV0WU5Ed01aZUZHeGVvM0VYZ2NzZDNmK0JmWU5Xdk5zWmN0MUtIdXk2aGVkL1hGYUVFOHNtTWJ0QjdmazhONmtUOTVHeldiT29JdGVkQTJzR2FWWjFwYUJQRHN6NmpjdlZobjJCWXYyTUllZENkQWtSTTMwY2ZsNGp5MHh3a2ZQd2JlbEtQM2U2RmdUWWlmeURWUjI2dDB6OEYySjBnZm9ERFB3Vmg2RXNIYm1ITEM1dkNRUmlQc0tOVTBQNGMySFZXR0J0ejRaUGVNMnBvOE1KQ0hkcE9XV3U0VVhDODBiN3MxV1ZFbjEyVTJPTFp6WnZCSUJBalIyd0FReUN0T2hkazVEa2FhVVVxWjgrNG5GbmlCZ0hTVE9lTUtvYzFmNk00TVozK0pPVWFaY1RrdVBUcTFCcUpiR3l5RThmMG1DUWJXeDhUUkZta3BmR0hYais1bzNrRjBHQjNTRVFmOGZDaHFRbXBObVFVUTI4Z2VIb3JOVy9USVBQSU1odHBob1BjY3hvb2RDc3dxTFEydk9nQXJSL0owSkdIR2RwQm9VbHYyekFrMUg2VDA3OWdJajRodEFVdlBBamJHcTlzNXNlSzd3NkVEeXErQTRlcS9YVDVvN3ovSFRNNVFjTnRxT2dFS0ZKSERYMU1mNmMxMWZxVlYrM0JmSGU0OGhabGkwcXFJQlgvNXBoVmdWRHd3aUpKM09Hb29zcExOTjNLc1ZVcU9wVU0wcTBiYkNEZTFic3lCSFRCOENXbVZ0YlZ3RlBmanJkZFJnRUZhVTFKS2RLYlIxYldUOEtyc0xyS0ppMEpiR0JNdHFNeEp0dUY3MUJtazM2Zit2UHh5eUZTNjNvQ2hLaU50cnFLVm1ra3piMFI2QmZVZWc5ZGJITXJRZ2NFMlcyYkpDSUllUm5IUFB1TlhhdG1wbGhKaWh0VGxTcElPQWpkTWpEdHAyNGVQOERZL2Nhd0plbW9qejJ0YlhkaHBFZEI1dVF3a1EvdW94VWRzcVRoUzA4bXFEaXp1UG9Sb1RsZmJ1RnNQbVk1QTJnT2Ixc0JZUExpL2E0dVRLL29DMndpa2JiUDdDaFUxaE03OWh6d0hzNlFBNVpCTStWeFdka1cxcTdQdlVHdkljVGJsUFQyQ1F3UU5NYld5b0JXRDN3SWdwWWdzcHBFTDZCbEF0ZUtnUHFHNXl5THBydVFWUWhKVzJrc3hPVUZ4cTQ0Z01jWHFWZHR6SlFJYngvRmdlN0Q2cllhRnVRbE5hSHZEdDhYTzZZZzVYcktRZ25mdll4TmYxK1hNNlE3VS80RmNGSHY3ZjllMW9PWUVWNzl2d3VhQjJETGw2VWY3bkxQUm1xVmNZTFBWQnFRTGNCbkxJRk1SZ1U1TW56VCtWTW5WQjJkSTl6dVdnYUVYSldTQnVGaXU0K242UUJGL05xWURVMlREdWtiMlpyNis4NXpSQU9xMlVkeVNBNTBKTjgrdWlHWFJiTFBvQUljc29WYW1zOTFJazlUWkhleVN4d3kwdTduREZ4SUt4aitleHRyMUs0S3JsN1J4L3dIRW8zY0E1MmExZldiYUNVaTdEOWRRYkFsVS9nN0pIdnpFNHdZT2IxUVBwT0FKYWoyNjRUc0R4NGVYdmIzMzRQZy9lS1F6NG4wcGJMc3BHdmo0REN4WTZiQW1aKzFiR3dza2ZJeklveDlnVS9oR0NmS2o1dzlyTEdiLzZpWnFHdFhoUEUvRmtvZ2dWbzlCcHB5OXIvT25ZSUNQNDJ3eWszV2FVb2hyVkh5bzhJM2t2RHVDRko0WjR1bGRhcmFCZTJzRDRxaHJEeTZsajFCN3FCWmZHNngzOHNpREVyRTREck10SDBmbnF2OHUzanB6ZW9MWDBkY0s4UW1EaWc5K2dJZG4wYmJ6a0I1elBWZkRWbkhpRHd3RnVWNjdDSXFOQzM1Tm0xbjUvNkpQOSt1c1ZOOHhTTU4vUC85dURkV01PWXYxNXpTVmZaQXlXc3liMVptRE9NZDJaRVhhZVlIV3dkMUFpMTc1RHFxVE43T09oaWlKS2Job0wxZTE5QmZxT00xQ1dWZ3E2YW9vRzNONGRuUWlSTzFqYllIV1VYMGZZbGgvb2Jwa2I2aDZ0Z2NhWnVLeXpmdFk4VkpzMFZnTmQ3VXIwVjRBRlBBVTY0YWxMSnV3dnRndWowYWV3VUJ4Y1RTOTVMeVdjNGlPdmhoSWtud0tlK1FKVjk3TlJvaENWT1lTZUNVQWp6UzBNc0hYR05tQ2J5V2xKVVA4YmJHNTNTemhYN0ZWNW5WYlFhN0RDeFJ6MnZxUEIxRXNiYnB5ZHJUYWxYOVdNcEM2dVQraFNsWGRmbkF1TFUzRWR2Vk4yK3lzODN1cGhaSFlhR0Q4RWEvWEdDQW1ldHNnN1pHQjVUWmtPZ1JhcDZWVG0zbytBOTNOVDI4am9iZGllL2VHZDhhRnFkK3FXT1pXUi83WXhqZWxKQTVjYnBuUE1JNHd4RXIra0pQQk5SNURDMEtIMUNGRU11RTRnbnVRbWJ2dnVkeDg0UStaL25VL0xQWnA3SWRUaUV5Uk5nNFZaWFZpR1ptWTRLYTV0eGJZbXBPVnk4YUJubkpkb3N3OVdTRmlHMDd3RXVwdEpUd1NIdnBwR3lLOFl5MlZ4cDFMdlFEdlZCdUNyQ0dUNWdtMk43OTdkNGNWYisyZ3FURU5XNGI3SnNQckFaMzlrUzhrMVJmS2ovY0lJdFhsVVN2VGRBMWtvTVhHbTFjK1N5Rko2bmphTnFna0d5SVdFVWNkaVUwZ0xxL3lWU1o4TzNUNGxBZ0JFSHFvalJoQjZMYTlyYU0xWGNoRnR5VHFCZ1BHRFJTdEQrbmlVcms5VjBQOXU2c2xuc0k0WXNSeVpVYi9aWUFhSDMxVWY4UlZsTnM1K0Q3TUZWRHFoRExvSkp5ODhMVUlmanRqTnBEc1Z5Qk9SbzdkQkx6SUpoN2F2QUFVZjZqUE5PQ3pUNEFBTnNOa0pjLzlEcXJUTk42QlFpdzRkRzVweHlZbTlqOFVrRGRydVdFcVIvQzRFb3BtQjBUUDdSK1owR29SaStjb0JlSm90aWJ6RHl3YURvREFkb1hOSVp3dzBlUXMzQVZFdG9yM0tacWxGWDI3SHFNUzNObFVpL2lGb3EzVXFNWEVxbDYrbWRlZjZuamdxL2RGOW5VSzZ6TWZKZm15dlhaT1lHRHZBNDVqdzUyTTF0bitYZ2hIVGUyMDBBWXJuWTFTaXdMM2RCajlIZ3kyUFc0MlFPbFBnbGZtNm5XYXdGNjJhN1NLVThDNWxmdHhYT3BFMEo4c1I4T1FyRThEQUJUUmNJbW5jdHBvT0ZIQWQxa2pkekpYVVRFMzBGdDNJVWdGUUFYNER6U0l5UUFiUTZBOE1CdU03L2twMkZSdnJEUDNwNkQ0LzlFc0lOZGpxdDl4NkFDYzdsRVVEeDVoVHNYbjJhT0RiU3lmWU0rYk5zU3JQelZsRCtBT2ZLVllaVUlnMEdXdEVuUEUwcThaWTNIRHdGdVh2OHIzbGt6MkgzaHZkazB0V2sya2hPQzBLK2I1dEMvaDBMUGl2eG9IMzdGaGFDeUNtRm40Y1lGTW5BWE9rajNXTFA4OUV0dElGc2xtT0FDdjVHVXRYRExaVjNQSUlHODB0ZVk2Slc1TnIzTi9vNVVCSDR3WWJJNzNINEtvNnpPWDNGQnBVeWFuRmQweG5jc0dmeW5OVzhsWGM5TzFYM2pIL3RhUGdIbzdzbDc0ejFOL3lVeGFmbXF0THNDVjQ3ZnU3bzEzMFgrdnBHY0dPeUR2MktDUFQxcGdNU2ZmVkZsVFFva3dLR0tSRFRCYWtPMmdCRnJHbk5VVzdybG1BMHdDeU9nZEtXY0xHVFljMm9penhWaFlPQmxCUnJONC90ekdUV3lWS3VlT0lqaUYrcDhZNC82enMrMlJ3dWt6TWVZN1p3dkJ1ZjdVNUJVbFlZak9zQ21lMncwZlB4VXBaaTZkaytQRDZVaHpRWk9Qc2JvaGhVREszaE8ydEVrczQ4ZHB4OXZMaTVLZmtWK2hCUTEyeC9YVjFTZDVUTmw3cFlPVHlqTC8zZVJVVkJxdWxFWGk5Rlk1Q1R1MXBXeXZBV011OUdQaldET2crb3ZGWks3enFBcFRiNWRLbTJvMkRGZWhlM2I0Tmx5bzN1UmtCak0reE9aUDZGU2NMZVk3bHJCMVYvRFpRbXZJMVN1SmZuMEhjWUowV1JFcSs5aTFzNVZnZVh2UzZDdDBtNDJGUFNpeVZKemVlcXZkQ0R5Z0g1b2xXL2lienNtMEJwZ0kvU1Q2RTh3R0orU2ZMaGJWOFVGVnBmVk1SOWwzZGQ5V2JTQnBFZWZiTEJKWFE1cHNteWVyT3UvOUY4bTNnRi81eHNMMSs4U2YxR3FHRzRxSVBPbTFmdjFhdFpUUTBKTHNHOGRiaURnQk42N2pILzZTbjNnNStiTlFJb1ZUcUpCc1ZoMWdpTCtUdGYxa1BUZ3M5NEpLd2FzMUVQQ0VWM3NQVWtqVWVPYkNoZWN2ckpIeHZZYXA4aDdIYnMreC85aHkweUtnMnd3SEJkNDYrV3BTM1h0WkhRTUVlVWs5SS9GNHlRN1RyTHFYcXJlM0pZdDc0K0dmemg0eURNOWpSYTYzWTV1Sk1DUTViZGFmNG5sbUp6THZNY3JXek1FSjZaNUpTN2ZCcXVMVko3em9UV2FsSTJHdnlRUEMxNmVsME9ZeU56eUVHNTZCYndPQ09ia21OS2lGc29PNTlrdTZ3QXdwTjI0Vmh3Q3dpdjhBeEQ3MWtud3pZWW4yRFkvY0ZldDZPTnBEYlVKaEVlMjgyRzFNcWtDNzJzQ0cvV3Y0YkFUUTJoeUxZWXV2L2UwaWRzWVdiT3VnRDZobDVaVVdlZFFyNDh2Ym1kNFBTcGJEeFVEQ2N4NmhmaWt2TmQ1d0RLL1hPeFE2U2l4ZWh0ZzdmSDY2R0xrcGptcXpSTlNsWDVZOUQ1WnFYZXRoL3FCWTFZeUN5dm40dHlaUkZHSmMyaTVoamxTTTVLbml2V3dvakY2S1UrUitvcHZPUG5KMkxyaTFLeU5BN2xmd3A2NTN5aDFnOHJBd0I4aURzNW5FdGc1RkZIWWpEVmt5ZWpxSmt3TlBDdVUySG82NitMTm5RWEd4OGtRVGJXcmRsOGtxYzl4U3A1U09UdHY4WmVKLzJyZm5pVThsTEN5OUcybkJ5eUM5RmdUSVgxRnBPR0ZjNG5WZ0VnbTRhaU1BcjQ5blFaZWt0Tnh3REVEei9KYUxnSjNxZFIwQ2VjM2NQaG9sTXY0MTNqNnBlM3lZdEU2c3lIS0R3M1hscTFURHVwUUVKVWJ6R3ovZ3RkSW9OcXZJTVAzOWdrcFFxb1g2MUdPZkRBZER4Q3Blcnc3YlgwWEF1Slo0ek5RVGFqRkk3MjVOcmR0V25MRFppQlk2N3Z1eVdZSWZqajg5LzExd1prQ091NnVmcTFrVVVlUXJPemtJTWNNUHNyYjRpb3VKTFJQNktEckI5TWtuaTVTTHhBZko2SFplUDI1UW9TSlVwMVgvSEdXTUc0YkM3WHhCamRPdWM1Wi81NGxubElMNkI0UDZnV1RocUNXbzdQUXRjMlBtTExJem9CQWpNVS9ta1V6bDJLdFR2SUJOVzVSSDlRWUJEQTE1L2NvRGk5MEN4RHFPaDFDaGRnMW1qeFF4Z2dzdHFJNXN1bUp0V2ZOUU5rL3lLWWZNTzZMNWJaOWNML3FRYm1qREd0QWc1ekVzWnEvRDZNZ1ZVc0NYMVdNVGZWODR2SXJDZ0t0aklBZ3E5SUhOVnFJSkg1THRQcUJ1eFcwQmdIYldBQUlpdFc2bmVja1RnMS8yazAvcllBNDc4OU96dTIvN1lvVU5TVy9KRkpvVjFtUlpDR1VLNnV1NzJ4T2NybzFTY3FJNzYzUWU2TFNoTERBOW9uVjM4S1RDQ3JVNHcyRm1yeDh3UHNqd1BqeW5JNzM2MXZFMTlIdGlWempaK2VpYWJhcWh1aGxJSy9sdVdyS2ZpNXBKakNjcU94SHl2UUhhUGdlR0o5czh2eEhMNGRXUXg0emVFSVZKYmRMN1ZEVjFkUWNqalhCVVUvZDF1c0JqLzdWbVNub2FUTGhQeEwzcUg1L0R3WjRYRW95dy90ZW1qdGZjVkJvdm94MG5neWoyNGpuWUNLNGpOSFZlbUQxWUNkMTRyd09wNU90di9IWFNRaXRUSVU1UStQQWxzdWdaVkx3Qnl6d1pGelhuY2YxcldiUzBWaFowOW4vY1E4cXRnQnZUVFlZZEMyZDZlaDFvZGxscjdsWHhDN21CS1h1ZzFqbVlmNzNsV0wzUnlTeEFObGw3ajY2OUcwTWdyMWpzSHluVWJQMWp0cHFRRGwxZXlvK2hHdldyVkZiM0xseXpXcytnVkR3OWxJVXpsNWJaOFlCV2t5bmlWOFlMYjJnRUxUT3NtdjZCTDlDSFFHZXE0OEIwM0FobWhVdVBnU3Azd2NyLzFsQVdIOHVzbjhEeXlFMElPRk5Pcm1iYnNuT3c3eUptVkJUUGFkNG9hSStXRUpHUmhBM2R2eVpFcFEzWFFiVlVFZzh0aDI2YVlmNHRNMkJMZDBsMHI3TEVzelQyTXdHVnVvbmp2T3ZzUHFha1pEbkc5ZjJzVldKVE4rVlVzTVhwWUNpR2JuVCtUUUx6ekd5SUMzUVA2NjNrMC9HVDJ5TmluTlltdmhYN3ZyaXl4NlQxamxkS0R2SUptVVIwd2w2d2NTYnd4TWZMcnduRU9qejllMU1mWVdtS2dNVy83Y0VJSmJ5Z0kwN05aekUzME4ydkdXWHB0SGxkSThGSXJKS3lyR05oWW8rYlY2ZGRackFhUnN2OU9NUEMyRlRsbWdycGJCdDJ3V2RFQ1NHMWxuNzhZTUJqRUJ3VGdseEUvU2VhS29tdENjTk5Va05GNkE0OS9YUmRJQWwyWXljaUptMy80SjE1dzlhR1JNOE1pQVN2SStQZUZnYXp1MWM2Ykpyaks4c1ZQQzB2UzhjODVnS3dDN3VMdWFsSlFEcjBsc3dOTTlYSzNuREFUQTZYTVc1WW8wZkJURkpWSi9QWU1xalJ0eitML1MrWWM2dTUrUi9aVDJDcDlQNVBsN2xIOTFLTWZNV2VuTjhWeGhObGIySEhzTll3dGtMOThKdjlkVHI0T3E3MkNyOWNURngxUXFWdUk3aXo0MTgzaEFKM2Mxb0JXbnB2dGVYaS9GZDZiMk9kdmp5VENnYWRBQy9TUDFkZ05iRC82NjQrMmx1OVZiWkFFK2RJd2VyelVnUFc4VDd6YzBUUXZTajVYMSt2NWFyZGhKb1BzQnowTXY2UlNLc3ljZ2tnc0hzNHFnSXQxOWJZTVpYN1NBWUdqbTdvb244M2pqRWNZREp3anlESnNVaVRockhUcGZSbnhwcVlLNnQ0c1hIeDlINGxLRUpISE9hQWtjZnY2Wk1TQjZuWUxzNVpXYXBxZlNzVHMzZ1NqSXFYckt0bzlaL1NxeTZ3THhWUFF5dDdpRXR1cmRLb3I2UDBHZVplb1lCWW1rTmExTTQ3NUZFYW40Y1RUWllLNHZkNUN1NXhpOWNtU1RROXZKTXRMOUhsMTJyb29DR01ETmtPaDA4aUFJdGpndm8wREpKRlI5QnZ1Zm1RczNIRFZtTE9QV0YxcWpYaWFWNk9teDg1THBxU2pqRnk1NlZpdnFvUnpLZExJVzJpWjJnN3F0dkJ1bDdleWZDM3o2OGZERktVUXhrNjZuMHRTWTJxN1NldkdKQjRkMXAxZXg4SkZwOWJoVDdKQ1QzQWw2cStKaG0zTFlnMDVueFo5bmFRK3IzWlRIOGpqWS9KWTB2WWRSTW1oRTB3bXRvQjBselFta2poaEpsZnBNS1RuWTJmdWE2ZTcxTjN6S1NXaFJhU054RmZGTHVkUWdGUXVGZlFCdmFocHRsMWs0L0srcEhlNEdEYmJmMGZobWU0WnBnRTh4d2ZQZnVzWFdpVFQ1L2ZQUkhVL21OOEN2bFJyK0xEZGxLR2dhRlQxWmdIWGtoN09RdkE5djFSZFRvTDNnRG9USGx4Wmw1emlSczVLMjZYSHJJZHcvekZDSnJmQi9hWkVFUDQ2TCtKM2FuVzRkdkNaQW1TUXB5aERIT1hxK3NpLzNYdmNRbXNTdml1di9yUkRNcGRNYWlhSXQ4TU9wbGoxaEVPY1NXTlhDK3AvVzljQklGeVN2YXVFZEc5cUh1WnBkVERaNDZBRkpuSTNpMERudHdQTUhSaGMyQzZhakxPTjJBVVZDUEN0WUp1MGVMcGg3MWVRVnpTMEJFQ3FDQ2pIWE5ZWk9DU3d6NWJwVG9sRFg3OHpHeFlDaU9hVlF0WExPaktQTGJCUXlYNzg5a25mVFVPZWR3TlB4S2QvNEZxSXhZYXJpUm5MUnNyNlpIbTRsYnZ5L2dmdFVDQ0VjRWhvTE91VGZKcWx6ZmttV3BlZWhIbSt2UmZKcm8wV080ZUNZbnB1bnlQL2xrWEdWZ3psUUJFTmk3WUJqRzd2QTduUWtOZ3ZDVEdnaCsyWm9iUUZLa2xoaXhWcEtnNktvVGpGcE81eGFCMnpNMnpURjVZQWxzNGdGZSs5amU1ZlgxTUEyRmc5UVY3QlVmbDQ2dklXVmxsZThBWVJEd1grWG5rN0lEdjNheFB6Szk2TmptRHJXS3lnQVJmaFo2NGRnanJsdGxROFZsSWFZMkdpajY0QWFIV0NEci8zSXhsVTc2MlphMytEMXBvSDBOWnQ2VmRQWDhYd2lkUGxBa21jRG9Wd1hCeG5WemZrcDhFOHp5am9zOENBYlMrTlNlZTcwTnJaYi9QYWxuVUlsNHI1MTMyM3R0SjU1THVSdlYrT3pIUlRqd0ticUl5U2tKaXZrMFJSb0FSUlg1ZzJocjJuVTJmL3RtaHZyaWl0YXcvbWNtTTk2STY2L3h4U2REVDh3cnNiK0taVlNDREV2NzhNRHloMFZmczNaSXliTW1WM1IzVGJiMHhWNjhSWS9OYXc1UTVwOWFCUnROR3N5em1EYkxpTzN4NGZPcUxOSVQrQkwrN21sSklTaDJlMEJWWlZEQ29FaHBYY25qOUEybUtVZG1ZOTA2UmNQTUxtaG1zYlUybG04aHNzOCs2MkJ3R01mTWd3TE5UcVkrRG5mbTJJUHFLbVE5dHo3SXVOUFZMNmw5eVNZcFpOMEhlbE9FOWxZMUpDcTJFc0MwS2dmQll2WXpaLzNEamNSL0pKMk1RVlJFR0VVb2dSV1FQUUdQQzVzbDFCZzZBczZNSHlOUGtmMWU5eXJScnhSUDlEZDNiT3YrUC9RcS8va0p0OW5qcDZkRkppeU1ualpQVUlSZjJ2amdZMlluQlJ4YlhYalEvWTl5LzRiTHNVU29Ga3pnSk9vMDUrOXVtOFVsb0tDTUxPS0dqU2RIVFZldllwL29sM1FvdzF5RUg0NFlybDlRZS9uNjRtSFI5bnkvajNZb2FFdE1CaTJXSHZUWGtBZ3Rjek1DNFlmdkJOVkg5ZzBwUjdlZUM5SHJEenZVL2hzR2wvNkJDRmZFTy9mOEY3K0pMQWdJUkRMRzB1ZkNyamdVVHdPREg0TFVlek03d3o4SFRJaFVRMzU3TUxaeEc5cEozQXh2L2FMd1ZqeVU1SGkxUXJkNGNSbUxrUW42bnYrSnNsNXdkRjJPODdXUVppcFhtbkg2V2htWW5DNlV4UUJUTmdpNkpGTHo5WHN0ZmtlU0RlTUsva2RXRXFwZjFQMGVyOFpJUGZKRS9jcW1GMkNad1dtSThaZXYxdy9oUkhGQm5hTXNtZkRQWWlvMngxU05FQ0NkTmFzQXdNeWlwbUh6ZjQyRHN4SEc1UW1keXVHREQ5dVovckRnbUJvQnJHenZBRlZBYmthdkRhQnYzZFNOTERsVU1QQVhrYU1WN0JoYjAzcThGMzRjanB6enozeHl1ZmQxdUk5NTcwdWlKeDRqZk1uNXc2RUxVN0wxM2dVdHZJN2NaM1FMM2tOcUxXWTEwdlhSMDREZG9PbWhvSHBpaEV3NmYralZmVlkwSWkzckRpL3dmdzREN0ZscTRUaS8vNTFhRHZ5WVA4MVNObVlPYUdnRlRWeXc4ZmFQN1Nvai9ZeEIvQkpPdmhhOUY4ellrTGRnQkRTL2doamJNa0gvdEpRbWJmaEQ3L2luNFI5NzdCQWI5YTY2YW1XMnRlVUFYUEMzWFJvcjBheERIaXFpWUllQllSOEtQTU5LMXA4cmNTYWU0b0R5b2dSYXhqZmRaOStGOHZoSFk1eHJoN0FCVHdsVmYySDBmMTR6Nmh0c2pqcHNRVFBGeTdQeFB6RjkwM1JNN0lHVHVUV1Y3QTJYZDhrTmN6QzQ4Skt4K00yY1VzMHhnZGhPTHpiWFR3TXMvQ2RyQjhzQUZDTDA3TnVSNWVtdWxGNWVyMFYrYlhhYzdjVldyMUd4TVo3MWU2Z0x1dzlwU0Y3bHg5TkhCUkNkaEtkM2hqQVpZUVNGZmdpZFpGd0pXRzNBOXE3RmVqVmIxa09xQmFhUnNqYnd0QitzWTFsUXcxVkZScE93RmFCUmdveHZHNG1wYjNEMWFnY0lsd1NmWlBhdnRVMnBCTEJvYU44a3ZGUFB0V2prS1M2S3YyTjNraE1sczlxZWJlZWlabU02VmRSdlNPMnZSYVZhK3VQbFkzcmpDdWtPaWFNTDZRUVgranJVelo4cVBoM09lVGphVTFHWjl5V3Uxbm9ESnB3OVRQYmhQUFN5RUh5TzhYS2FHV3BWN2F3ZUtVRm5MZHVrTWtHM2l4QitodjNneXd3dVBFVVJsc2RTZGVNc2VHam4zRWduSkE1ZVlIQVBqUnNvN0h0b0JUWlE3bnJudVBCZUhLN21NbHpnTVhhY1hqTVFXY3U3cjc4QkZNWVJVMGo4T2cvNlJYbEt4Ry95aW1JVjFFQ05ibHdySjgzSTNqeDRIeHZBN0RMVWd6VGtUdDdLQ05YR3Q5cU4rcVlvdm5iNkFtcEh3VCtQTU9RZHVQTWFNWEQ3UnRBM3R5VXRud2pTV3RHdDJzNlZ0NUl4aFJnb1ZlOG1UZ0ZyNXphRStlUDNYSXVXbnNIQzQxdGZOM2RPSCthRW05ZDJ3T2NCVndOclJsMG16V2ZaSlh5UEw5REFlTWNJYzdiamM4ZWIrLzhNTCtBaVJqRlpLQk1wR2xJd0tEK3B5enE3Mm1XSmM4b1pSVTNoUXdTYTFxRUxOQlpEcnhKZE1OS2VaVXhqdXlkQVhWZHU3d0UxMG5FUlhSZUFuQVlDaTFmeE1hbjhWd2QxcDJOUDFOSWpyUUZCL0N4MENSNmZZNVZaVWtzUzdBdFRLM1F2VFBFUVNkSGxESnpCRTZBa1hia2FZWWhrb09uQWZ0TFFYRkVwL3ozdjdJRUYwN3owQUxFYkJTcVAvSCtwTmRXMzRUeXFUQkxDRXpGREw0Vm1WV0Q5bUJiZjZIWm82d3dhaVc2ektHV3ZZb0RHbzVCdmNxK1NkSUJpcDRuKzZSdDY0RDZmbnVMbUZId3k2dlpkUXVEYStUTjhBcXgxcDFIYVFwOHV1S3BSOXVnM1RGQTB1STQ0SnhnSUdoVDV1TEg2ekNEbmdURnlrU09yMUV3QzkzT3Z2RHZWb0tNbng0YXJrUHl0Vm8wbm0wWlpyNUZJZktHcVZXZDdHMnk0N2xHRW4yczZ3WHhYbjJnUGRVSkFTMFUvcmQyKzlCNEp4S0F6SGhaVjhXaGVsRzFNeG81MTM1M1pEaDR1d2lwd1NDM3VzQVFGcWYzS2c5anQvWkF0VTJYeGs1dVI2dXBpeUIwTnJNV3ozT2UyQnd6dUVhc0dMUzYrV2RLY1lPblhxMGt5UFhuR3dTRGwva1BNc0hCa1hoSnBCa1FPZ0x3Z0ZhM2tWUUxQZkgvcEJIZDlXQWF1OFB3blFmODNVQUM3aHlSN3RjdE5idHR6ZTBSZE1oT2JxUk5QZDFZdEI4N2poYjNvcDZ1cHV3aUpJTElSWCtWY2ZoZUNqU09VcDdhcG5FaE9LMnErZWZFQU5wMWJOMEZudmFRRllQbzdaVE5aMVRyTGYrQnZYamlyYzh0cE9FRyswTi9tMmNZNGFVRWxvTjRzU20zZlNmSFZ4WmhLRmt4UUMwcUNCc0tROTJGQmdyS1NFQm5XN2Q1QjlLME1PMlBnVkdlcUE3R05qaHJlTUk4YW5EK1Q5RzhiYjRvVGhnMjlPc2Y1cjA5R0lndTZQZUkxelprTlhqQlM5SklSaVdZQWF3aVdmaTRWWTZMUklLeVpwMWxiUVpIZmdOMThBVVMxS0Z3YkxPcE1yZkZITm9MeGVvMml3eXh3eG4wNW5aTUhJemNlcmlTVGhFVkk4SXdQZW80dGhJd2dIY3l0eFAySGlWSExxQTlNVEVNYkQxNlRZc3ZoZnNlY3JJNGtXcnFIaTk1eE9HM2gvem04dlZvR25PODZmLzBlQnUrWFpNRWRPYkZGWDFRT3JFZWdIemp3dkU2aFg2WmtMME9kOHltc3VOUXpUcGtmYnJKNGdWQit2a0QrbW8vU0svQ0wycDhYWUVaK0Y3ZlBIU2I4Q09VaHp5YzVJOEVybmY4WHovcnpkWmFvbmNqRWVtYjZFemc5YUhmOEY3cjNMRGJzM2NmeHJXVmdjeWVicGlDL2gvWmdsRVNSMkZLZ1Q2enNOV1VORTJKbjR4R01EeXA4T1FDVm1aajlVUzd3RlBOMHNKaXF1SzY5YllvVWNJR0tBQU84QVZyOHAwOUwzVFE3STZ4RjlZMllVU0lWRnd2WVorV3R1NmFvdnJRd0JjdUpBcXBZcUoyUHAzUEljTVJ1T1RUM1BHT0Vxc0l6S2JhUUNIY21tZTliTlNib1JiOUFSMDhncjdCUGZYUmRQbjlJNm9Td3YrK2NHUmQweUFqMkN6NW1uMkN5SW5YSHI5Rkc2RnIzaElRRmJlT0x2UEFSOWt4WGw0b3Y0VEc2QUwvUTBCSHBqU0JUWEIwdmdlZERjUjgyZmNnaTdwc3hRbnZPZmNPTUJaRHQzMEorV1ZXMnpZRHc1MzBucDRZK1hQN1NkN2xaUzFHdUdoNVBmVFA2ZWR6SDk2R1RLY0sxQnNqb3FRNkNPOGdHcjZPQUUvekVmOFlsajhjeVgyRnhEU1NjVkUwZU8ySy9JOGZWZEltbmdFT2sxVEFGMm8rQWVzOW03TGdVM1BRM2pvZm1mWnI2cVgycGpZQXhqdGJWZjFmOEtRRmhOKzVvTEpHNmxBNUM5R2UrbjFvV0poQm9JelMrRTJ1bktGNS84UTUxZzNPR2NId3BUQWQ3a214M3Zmclc4QmVleTJjSVg1b1NRVkovU2poM3dxWWVxUDlLLytvVThsYnBIMC8yKzFzT1pSaHU1d3hneWxCN1dqcVFIRnI4UmZXdFpkSUhES1BXazdUL1R4cDN2U1lZZnh2NVpuaUlpV1pEWDZ1S1ltbVBOTUV6RkNua3VyUjhjSHV1Qmd5TXRSdWQ2Rmp1NHRUaGhPN2VpQ0FqKzRxdStKWk5mUlZ2aVFFNEdNZDRKWC9qWEIyOExlbHJzV1JUYjlBVWVxQ2NzMFY3SDRMSW1iZDh5bU1XZDV2eU94ekVqSms1TWUxQXlZT1dIYTRIbForZkRYdUUrNDRNNkY3TEQzamFWMTU1SXBoRHB6dnJBY1E0cnhjajdzdlVyL0c4MlFnQjRvekxIMk5pV1RjWk1YWHJxV1JhWGRZd2FZK1plTHFNeHF4ODJoNW5uUkQ0NUc3Qk04aHNIMDhubkRlNmFSUDlQZ2pUK3RLTWllUFhKeDdwUHVUbkdiVHlpWjg1NWFrREx4bUUwUnRyTFpPTXVMRmlaSm5oQUJ4a252RDNFUHBzVkcySThtM3VwZFk2RC80N0U1R3g1MUNma2dpditOWXJWdTY5REIrSWRhSGNzdFUyblhhZ1ZlQStZaThJWWVNWThxRFlReXU2SWdaNkd0Qi9lYWJxRzFhWXRXcWc1WEo4UkJHR3FkWlQ4ZWtnZ3hqV0VrQTNYVTErWHp4endMQ3ZjUDAyVkFqeGY2S3gwbzg4cFIzVzl5a0Zqd1F2MjczcW5YK0R1aVordU5HcmFURFI2Y0V2WWpHelRWa0E5NVdxdEpGWDBXckp3cnRPOFFIM3FKYk8zb0hUTEFoNUd2czZ6Q1ZxMG1uUlNhQW85UnA3WUd2Zk9FOGhFNnFoR3lubDgwU1ByWlAyclo5ZFZtSUdRR2NvYW5TdEthY0llZnJ3bDlJQWtDVFNOellpSjRTNjVYSGJGUWM3RjY4NlhQNVRPemlHa2dBRE1mc3htSUtCMXZWdFBuV3d1bXNCSXlGTlFpNVQ4eW53cmJpM01icEY3bHp5eXpQUU9wOTc2SUFVbk1TZkQyQVgyWnR6OHJ4N3ltWHRjQ1BBaGxvUG1jZktwc1BmT3BMVWl2cGJhZUY3YTVvZ1VrY1AxbGRKTVFQanhtMTVqSW9zem5kMjZ4UmtieGNjTytib3Y0eFNYbU9HSjhkb2ZZeHp3SFNDTTBXVHBzbm5vOSt1TWd1NWdkZk5Nc3M5VUxiVkhGR2hlOUZTVkNHTUdxRENyVTBYbC96M1g1bWhLa1VSQlJnNW9kWHgrSU4wYVNIaWMwR05TRGYxVDh0UDU3T2ZnUzYyK1VUQ09YbHJxZXVFODVHUTE1SXlnYVNnK00wTDVrYTRXVHNlL3Y4WFFnQT09Iiwic2hhMjU2IjoiQUE9PSJ9","signature":"+6meDZfdrORlrzQ6kbNmZYltOPmr46u9jgcfDsxhEMg="}"""
        js_end_payload_chunk = """{"payload":"eyJrZXlpZCI6Ik5GQ0RDSC0wMi1KNjFXV0VBS0FMNFY0WDlUR0ZXRlZIRDBEQTA0QUZfMTgwIiwiaXYiOiJ2VlNLbGh3V3VjZVB1eWhVRS85V2tRPT0iLCJjaXBoZXJ0ZXh0IjoiWWdyT1lSU0hxU1ZvQnlBdmFyQ3B5aUM0ZTdVM3gyR1k5QXZxcGYvbVhhRnZWdjNxcWdnZXUwOStPbVdINng4SEJJV0pPUzZlOE5nc1NXdG5CU0ZnQjRCTW9rWTUwSzlRM2dpc2pyVjI5azArS2NxNWFzc2dLSFNJV243VEczdGFhUTl5bTlmRWJtbHU2ZEpza1VaUldnPT0iLCJzaGEyNTYiOiJBQT09In0=","signature":"yMwHdnDvhldeQ1gixbZKOO8r2E8pK7effAjpZY0vp6E="}"""
        js_header = """{"mastertoken":{"tokendata":"eyJzZXNzaW9uZGF0YSI6IkJRQ0FBQUVCRUU3aGN3bG9rT0sveGZYNlBYYUxoT0tCUU04Z3FhWkNDWWRRYm5lekdqRXZmOEVxVE5sekhDTzhKV0p0dWFKcm9BTTFObWUzaHJqZERncUhQUjlsRnV0ZDRNTE5OVlcyTS9QcHhFT0ZLZXhuTHZuUWdrbllLaHAycWJjZk9KNllHL3M0YXExcVNHejRLSVVUZ1h2d2YrcVF5WkduQUYyd1RPVHdVN0pDdGwrTFhKT3g0NS9SM1YrSnprWE9YT20wekx5V0RpaTNmeFZNclFnejN1Ni94ZmJiWkdGSXNXTEpRdGZHa1ptTGxVVWNwRXdDYmlZVHJ6K2xPMVA0MjlSWEp5SEtucWFSYWRiZVNHRlAvRGJMYUxVSHRPUXp1TGlNTWdqUW5uT0xpdThBeTNISDFBN0RPek9wZEZodDZIbnYvb1I1WXVwNVA4MkZrMGlzNU9KcWwyVWYxNEF2UktDNy8vRTBNeUZiU0pDc2NJWVJpWkxNR1pvN3ZaYnZzSEZGemRsQUZZNW9ncm9TaEQ0VVU4YnRIQmdsZ0I0TVpPRG10TVB3Rjdpc08xamUvRVRQZWNaVWZOelVNaFR4SVhnWWl3c20iLCJyZW5ld2Fsd2luZG93IjoxNjU0Njg5ODAxLCJzZXJpYWxudW1iZXIiOjU2MzI2NjQ3NTMxMzY1LCJleHBpcmF0aW9uIjoxNjU1ODEzMDAxLCJzZXF1ZW5jZW51bWJlciI6MTgwfQ==","signature":"AQEAgQABASDQ40QfmcGDeHcb3PZHcuzmWQtOR0AYe0KCRHahyanLn9kfL0A="},"headerdata":"eyJrZXlpZCI6Ik5GQ0RDSC0wMi1KNjFXV0VBS0FMNFY0WDlUR0ZXRlZIRDBEQTA0QUZfMTgwIiwiaXYiOiJrVFNNbjJCaXpuYkR6WGJyT1FKS0t3PT0iLCJjaXBoZXJ0ZXh0IjoiMVB1TzBkTmc0cGltZWdZaGZGWTY1WjVHalN4K09oQWRXMnd3d2RmWjF5OU14RmpxejBvUVpRL1JvRHlDQkRmeWxsWXNOdDZmeElROWdvS0c0SHJVKzRZeFdia1p3UGh6bU5lZ1BNWU9uQnZEMUlybWlNODBESXFva3F6eHYySmRVSmFKaTVpQ1R0enVjNFhCWVV2d2ROcjdUL2tteGc5NXBleHdXSEdTZE5hUzFQMDRQeG1ydGhsMWJMUHAvOXVLUFlnSEFZWlB2TDFYeFdZMmF5MGxOQUxTMHlLalFveWc5SDEyTWVhQnNVT2w2MTFvZi9udkVzeUZDSW1QOGpDeW9TUmRwWFMzczFocktnMHdMdEoxNDZUVkd2NFpNWWxhTFlKQ005c0dHWlV1bFRxUTRSeFJtbS9pOGNnUnBNREhuMEpLT0paQ05NSWJCS000dHhOUmIzMU9ER1dVSjdLamxmSVhNNGFUMDlqNnFmNWo3N0IvSGU1b1hQWmZpdjhXd243NGZRVTJBbGpuMXNFY1JlWnJxY0N1MnhHUUFPT2xMQ2hTQmQzLzJ4QllyZTk2UE9jUUFxTll5cnNQVzBaL3VqRnpwa05tUjVOS1pkTWVCZDB2ZERnR1ZyZEdUN2pkQXAzYkdvdlZ3ZEx3SW5BVUtlcTN1aWpnenhFd2ZIaHQ3eTRUK1BMZUIrVEtDVTRQQnV0QWtOeGlub1F6RHRhSFhHdXZ2dXBjQlQrdlNVR3MyRzRvU2J2NXNvVnd5VzAzbCtNeXErcDVFSnpORHEwMGtpaklqaEY4MmNZTkRueVQ1K3VzYkRUSXVKcklJN1dzbWR5VlUyM1h5dWRWZ256YTJlK3JFZWptb2FBK0x3d1VJSGhxSndDRGJabjA1YlhuSWMwd1p2Q2pGR2VVeW4xZGx3ZEYxMEFGa0QvOGhmOXJ2UlVIcXNUeVQ4elg2MjdTWDRKVG9JS3dIQlFWd0dBZk5MYUVLb3dzWlp4cWRZSTRkMnVVTnBVb3NRTy93V1gvVG5JTjl1N2UwbFlvNjNWVjgvUUt6MWxER1hQQkpleU5ibHJhNG1ZT3plQWYveHdYYVVubGxDYW5jSnF6azRZeEsrUWhtbHdZdmJZckxKcTBGZDZ4dERLcUsvQU9YNXM0VjdZM3Zqc2t6aEJSdGhNV0RaRUtSNFZnbjJvUVkxK2dOd0I1UEpQejFrM1pzTUQ4Z1ZITkg4RVlZRndOSFg2VkJpcG9PeDlWeWwyT29TQVYzQWtkbjc3RHhGME5KMk10VEhCM0ZxbGtvQzByUTVUYzFVWmdlcWRPQW14akZqeis5alZ1NDVzZnExaUdNdjNDWWRiUnc4RmhXODU1TmVWUEZ0S2Q5SXhsQ0xCcUZDbUQ4cWlPbEt1VTFmbDJ3eDJDWDZLVDFiZE1PejlsTkZ2Zy9GUTk0YmpQRlNPQTJQaE1uYUI1RzNUZCtVb0JLYm5SdWNTMGovTnlLc3pqZXdlcGt3VmhnQlJMb25SZjZneW0wdHl5Qm5kVE9ObWJsYTVQK1VoRFlwbEU2emxObHIza1l2RW9DZWsvTTYzWUxRWEU1RVE1bCtVdnpnRldLbDdOQm1IMkY5ZGRNSUpHY25FWENkR2tYZ2ZQOHJqcEJ0S0IzVVVCbXVoeGpOZ3RsNUhSRlNEdmNWUUdSNFRoaGFEeDhBeTI3Uzdoa3RJUklqRUpYbjdMUXhHaFhRcC9IZ3cxckk5SzB1TEdpTWx0elpNRzlJaUNDWWtTZlovU1ZobmFjY3Z3cTg5enF3bzJObHI1WUlnYjRXT0hmMyszbmE2bDJRNmxvZ0kyMXYvUTVtbFRZMVl3S2YzNGNrR0pLRHE3YWdmWW1wL0RHREQydDg4ZGUwU2tqOWJxd3FXMXdMVVMrWm56bzFoQmZiSlFvNytNYXQxeG92WXkrTjB2Ry9rWEZ4NXEzTXNzemRKZ1VqWHZYOWVGY240K3NmRkdtQ01Ma3o4S0RvUEpZUThidUNIaEpEOVpMeCtjcTRQaFdwUEg4eHZzZUFWZ29PSXhrbnlBdDhyUTMwMDlxa1huZnQ0NDJjbmpBa0JJSkpuZ2EySXpYWnR2K2g3Zkt5ZTVlNFBPRlR5NjdvYlVkcUtUeCtPV2I4dXM0RVVRVUszSGNmcnBRWmNyakd2Q2NDdUZhdTdKbkYxelZoRDVTUG9OUnVnM0pPU2s1cmkyTzIzZ3ZYa0lCZlNGbXJUNTVGMjM3ZlN0Zi9vU2pCMVAwVDdRb3ZDNFhHZEdOSFE0akRGLzczeHZqaWdTYjREcXJUZ3RnRWNVeGo4bUtHOXl0L0NEdVo0aW13bXlralpPRXpIVVpnb1lJUjdBWjJjV0NMZ2JwYkpXbE9pOUFhd3lUMElySjhrMlljUW1zb201YUtHZWpOTGxzT0Y2SXRpR3hCM1ovYjhTZitpUUFYSko1SW92N1pkWXV1cGhBZ1liaGVOR3BOLzhHYmJVU1BOd0JXVkpjbmlYMVAxNVowZ005bnJJZVdrQ0VXNDdZb2pBWDBWNkUyTk1vdmFsVW5qYTlETjZoSTQveXI3ZXZrOC90NWo0am5ZWlMzVlh6aHdxUW9tdDMrQ3l1cnZJNXllS0o4NjYzTFh2Y3V0WnkwOHQwV1M5U25Yc25oc1RqTGp4V1phQy95bThBYU42c3l0aTV2QWl3RVpWNFA4dUgreFlvUU9PajhzNDJrVjJZTjZkdmpPV1R6RXByaWZRa3AwT3R5MXZLYnYva0ZQMVNlRktrbDl3bWVLL0tuai8vbmZldk5xQlEyV3l5S21rWEpJVTZyelVEVnYxdGZkamZpcnZGMEMzVzFYZnVuTERwZWp0ODFSbTRJWmdaYmZMdkFUdmQ4dVZxVkdiK28reVd1eHVQNkNUd2NpQU9NUFpRc0hPZ2VicVgwTm9tOER5dE9CWHhQSktVemFWbng1aUN0Z1hHL0NpSW1JeVNTYlRTY3Z3WlBvNDBVN0JQVnBtS1REckhuZW1UZks2Z2JkRFRXOEZaMUZNM0xTa0t4TVZBaWN3eGd6d2FHZ0VJN1RGVkJNcTNaZDQxaGRsbHlGN3NCaFNSa2hLRFNLWVA1ZTFvcThBUjBtajBoTldLZEJnUnFFc0M0bjhuenUwMURZMzh2Tk5zUjZZVlQ1UWpyb09aNGtLNzlHUkU1RFZmZjdjeW44SmF4YlhuNFFpaWU1aUJvVlZsMjFwVHRKMlk3ZlFPSjZGNTkzN3dCcmVjZzhGYkNvei9BV2NOWmJjSVJGbkN1NHNxdTBESWJaMTVYdHdLOWc1enF3Mk9oT25WU3FUWXBKWDVkclZNQWw0cmJ2UER5MFFCbi9jZUxyMlhMVXhvTWloNEEyRVFRMGEwMHR0THRvTXZielVtenJyMDJhWWU4TEg5SllwMDJPYjdxeHlTM3hiQTBaRzFnRnorWW5DQitPeE16REQvNmo1YzlOM3N4RnI4anF6V0VjSVpsc1BUd3pxK1pNRnVYeDhKK3F0b28vT1JJUUc5c2syRzRibXZQZW15TzIyTFEwOVQ3U1lwRW1qaDc0c3BnNXVQbXkrMktjMk9HRVN3VllRRUp0aGpiRHN1TEdWQTFSRGk5V1JrRXdRMWhLeUFFbVo1Nks5eUNvMnZzNElZbkZaNXp4aDFYOWRyLzFBZkhLdFJZV0NKQWNSUjBxMm15MWRsSVl1MlVBV1NvSXd6d095endpeFZlc1FRZEdxTXRGd2wzMlVUQ1FmK3NSZjZnbEN5UUl1Si9uUitwMksrOC9ydFdkNTNNdVV0dDdSZTlNNTNPTk9FdHQ4cEhwcUZvZFdNOGtXeUNDemlKY3hvSG0rS05qUmRocVg5UVVLZzRhTkdvdE4xZmxtUEFsM3M3Q0lKbjBnTDBPRTRJalM2YkRsZU5uWkJ3WkZ1UmwwNmc4ZEVWUG5CbTd2NTkrOVRYQ3FGbENscms4dUxKcnJRb1p5cWQ3NllzUjQxbUNHY2F2dDFrdGZKejNjUnZLaThGSUxlNVlwR0xYRlViUSs4QVBOd0lxb2xtYTN5R09mSU1hcXAwcDdqUVpWcGlRenBKcUhQd1VGWTlEKzRUODBza2l5aDZNK0x2RUlVRXg0MnBRMlZhVVJyMEhPbHQ5dGVYZ2JadW5HOG9sSGRWc2NSSERIUW1mTy81blc4Q2gzOW0razFjQzJEZ1o1VkZOWFRNcno3NHYzeXR5bGRqL1NSOC9iNitYc0cvY2I2OVI5Z1dZQkVTdFBjL3NxcFp1cE1ma3pCWVVrWjE3cUFGK2lpMXF0azh2R0tMQjFyOENxNVlpajZXVi9EWW80OHNVQldYeEF0VFVHUGJrOTIzSlh0UzNVell5NUtXUmxPQmtxUUlmQzMwTkI5eUhwN3FUM2JrYjlXYUd0ZWpOcm03Q2p5RnF2K3hyQmx0UjlYQXhGRG1UZyIsInNoYTI1NiI6IkFBPT0ifQ==","signature":"m79vBnem54qC3O2moO4QjfUms5IPzT745X0VCeJJuLU="}"""
        request_data = json.dumps(header) + json.dumps(first_payload_chunk)+json.dumps(end_payload_chunk)
        return request_data
        
    def __lzw_encode(self,data):
        with open('lzw.js', 'r', encoding='UTF-8') as f:
            js_code = f.read()
        context = execjs.compile(js_code)
        #string = '{"version":2,"url":"licensedManifest","id":165329016374135650,"languages":["en-TW"],"params":{"type":"standard","manifestVersion":"v2","viewableId":81509456,"profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"],"flavor":"STANDARD","drmType":"widevine","drmVersion":25,"usePsshBox":true,"isBranching":false,"useHttpsStreams":true,"supportsUnequalizedDownloadables":true,"imageSubtitleHeight":1080,"uiVersion":"shakti-v4f4fb02e","uiPlatform":"SHAKTI","clientVersion":"6.0035.000.911","supportsPreReleasePin":true,"supportsWatermark":true,"videoOutputInfo":[{"type":"DigitalVideoOutputDescriptor","outputType":"unknown","supportedHdcpVersions":[],"isHdcpEngaged":false}],"titleSpecificData":{"81509456":{"unletterboxed":false}},"preferAssistiveAudio":false,"isUIAutoPlay":false,"isNonMember":false,"desiredVmaf":"plus_lts","desiredSegmentVmaf":"plus_lts","requestSegmentVmaf":false,"supportsPartialHydration":false,"contentPlaygraph":["start"],"challenges":{"default":[{"drmSessionId":"9DC6975C72BA7FB0FBC979E67EDF8F29","clientTime":1653290163,"challengeBase64":"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"}]},"profileGroups":[{"name":"default","profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"]}],"licenseType":"standard","xid":"165329016333614430","showAllSubDubTracks":false}}'

        result = context.call("lzw_encode",data, {}) # 参数一为函数名，参数二和三为函数的参数
        result = bytes(result.values())
        return result
    def __lzw_decode(self,data):
        with open('lzw.js', 'r', encoding='UTF-8') as f:
            js_code = f.read()
        context = execjs.compile(js_code)
        #string = '{"version":2,"url":"licensedManifest","id":165329016374135650,"languages":["en-TW"],"params":{"type":"standard","manifestVersion":"v2","viewableId":81509456,"profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"],"flavor":"STANDARD","drmType":"widevine","drmVersion":25,"usePsshBox":true,"isBranching":false,"useHttpsStreams":true,"supportsUnequalizedDownloadables":true,"imageSubtitleHeight":1080,"uiVersion":"shakti-v4f4fb02e","uiPlatform":"SHAKTI","clientVersion":"6.0035.000.911","supportsPreReleasePin":true,"supportsWatermark":true,"videoOutputInfo":[{"type":"DigitalVideoOutputDescriptor","outputType":"unknown","supportedHdcpVersions":[],"isHdcpEngaged":false}],"titleSpecificData":{"81509456":{"unletterboxed":false}},"preferAssistiveAudio":false,"isUIAutoPlay":false,"isNonMember":false,"desiredVmaf":"plus_lts","desiredSegmentVmaf":"plus_lts","requestSegmentVmaf":false,"supportsPartialHydration":false,"contentPlaygraph":["start"],"challenges":{"default":[{"drmSessionId":"9DC6975C72BA7FB0FBC979E67EDF8F29","clientTime":1653290163,"challengeBase64":"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"}]},"profileGroups":[{"name":"default","profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"]}],"licenseType":"standard","xid":"165329016333614430","showAllSubDubTracks":false}}'

        result = context.call("lzw_decode",data) # 参数一为函数名，参数二和三为函数的参数
        #result = bytes(result.values())
        return result
    def __generate_msl_request_data_lic(self, data):
        header_encryption_envelope = self.__encrypt(self.__generate_msl_header())
        header = {
            'headerdata': base64.standard_b64encode(header_encryption_envelope.encode('utf-8')).decode('utf-8'),
            'signature': self.__sign(header_encryption_envelope).decode('utf-8'),
            'mastertoken': self.mastertoken,
        }
        # Serialize the given Data
        #serialized_data = json.dumps(data)
        #serialized_data = serialized_data.replace('"', '\\"')
        #serialized_data = '[{},{"headers":{},"path":"/cbp/cadmium-13","payload":{"data":"' + serialized_data + '"},"query":""}]\n'
        #compressed_data = self.__compress_data(serialized_data)
        
        
        print(data)
        #print('\n')
        
        #data1 = json.dumps(data)
        #print(data1)
        #data1 = data1.encode('utf-8')
        
        
        
        # Create FIRST Payload Chunks
        first_payload = {
            "messageid": self.current_message_id,
            #"data": compressed_data.decode('utf-8'),
            #"compressionalgo": "GZIP",
            #"data": (base64.standard_b64encode(data1)).decode('utf-8'),
            "data": base64.standard_b64encode(json.dumps(data).encode('utf-8')).decode('utf-8'),
            "sequencenumber": 1,
            "endofmsg": True
        }
        first_payload_encryption_envelope = self.__encrypt(json.dumps(first_payload))
        first_payload_chunk = {
            'payload': base64.standard_b64encode(first_payload_encryption_envelope.encode('utf-8')).decode('utf-8'),
            'signature': self.__sign(first_payload_encryption_envelope).decode('utf-8'),
        }
        request_data = json.dumps(header) + json.dumps(first_payload_chunk)

        return request_data

    def __compress_data(self, data):
        # GZIP THE DATA
        out = BytesIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
            f.write(data.encode('utf-8'))
        return base64.standard_b64encode(out.getvalue())
        
    def parseCookieFile(self, cookiefile):
        """Parse a cookies.txt file and return a dictionary of key value pairs compatible with requests."""
        cookies = {}
        with open (cookiefile, 'r') as fp:
                for line in fp:
                    if not re.match(r'^\#', line):
                        lineFields = line.strip().split('\t')
                        cookies[lineFields[5]] = lineFields[6]
        return cookies

    def __generate_msl_header(self, is_handshake=False, is_key_request=False, compressionalgo="GZIP", encrypt=True):
        """
        Function that generates a MSL header dict
        :return: The base64 encoded JSON String of the header
        """
        self.current_message_id = self.rndm.randint(0, pow(2, 52))

        header_data = {
           # 'sender': self.client_config.config['esn'],
            #'handshake': is_handshake,
           # 'nonreplayable': False,
            'capabilities': {
                'languages': [],
                "compressionalgos": [
                    "LZW"
                ]
                #'languages': ["en-US"],
                #'compressionalgos': [],
                #'encoderformats' : ['JSON'],
            },
           # 'recipient': 'Netflix',
            'renewable': True,
            'messageid': self.current_message_id,
            #'timestamp': time.time()
        }

        # Add compression algo if not empty
        #if compressionalgo is not "":
        #    header_data['capabilities']['compressionalgos'].append(compressionalgo)

        # If this is a keyrequest act diffrent then other requests
        # If this is a keyrequest act diffrent then other requests
        if is_key_request:
            if not self.wv_keyexchange:
                public_key = base64.standard_b64encode(self.rsa_key.publickey().exportKey(format='DER')).decode('utf-8')
                header_data['keyrequestdata'] = [{
                    'scheme': 'ASYMMETRIC_WRAPPED',
                    'keydata': {
                        'publickey': public_key,
                        'mechanism': 'JWK_RSA',
                        'keypairid': 'rsaKeypairId'
                    }
                }]
            else:
                self.cdm_session = self.cdm.open_session(None,
                                   deviceconfig.DeviceConfig(self.client_config.config['wv_device']),
                                   b'\x0A\x7A\x00\x6C\x38\x2B', # raw
                                   True) # persist
                # should a client cert be set? most likely nonreplayable
                wv_request = base64.b64encode(self.cdm.get_license_request(self.cdm_session)).decode("utf-8")

                header_data['keyrequestdata'] = [{
                    'scheme': 'WIDEVINE',
                    'keydata': {'keyrequest': wv_request}
                }]
        else:
            # public_key = base64.standard_b64encode(self.rsa_key.publickey().exportKey(format='DER')).decode('utf-8')
            # header_data['keyrequestdata'] = [{
            #     'scheme': 'ASYMMETRIC_WRAPPED',
            #     'keydata': {
            #         'publickey': public_key,
            #         'mechanism': 'JWK_RSA',
            #         'keypairid': 'rsaKeypairId'
            #     }
            # }]
            header_data["sender"] = self.client_config.config['esn']
            if 'usertoken' in self.tokens:
                pass
            else:
                header_data['userauthdata'] = {
                    'scheme': 'NETFLIXID',
                    'authdata': {
                    }
                }


        return json.dumps(header_data)
    def __generate_msl_end(self,sequencenumber=1,is_handshake=False, is_key_request=False, compressionalgo="GZIP", encrypt=True):
        payload = {
            "sequencenumber": sequencenumber,
            "messageid": self.current_message_id,
            "endofmsg": True,
            "compressionalgo": "LZW",
            "data": ""
        }
        return json.dumps(payload)
    def __encrypt(self, plaintext):
        """
        Encrypt the given Plaintext with the encryption key
        :param plaintext:
        :return: Serialized JSON String of the encryption Envelope
        """
        iv = get_random_bytes(16)
        encryption_envelope = {
            'ciphertext': '',
            'keyid': self.client_config.config['esn'] + '_' + str(self.sequence_number),
            'sha256': 'AA==',
            'iv': base64.standard_b64encode(iv).decode('utf-8')
        }
        # Padd the plaintext
        plaintext = Padding.pad(plaintext.encode('utf-8'), 16)
        # Encrypt the text
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(plaintext)
        encryption_envelope['ciphertext'] = base64.standard_b64encode(ciphertext).decode('utf-8')
        return json.dumps(encryption_envelope)

    def __sign(self, text):
        """
        Calculates the HMAC signature for the given text with the current sign key and SHA256
        :param text:
        :return: Base64 encoded signature
        """
        signature = HMAC.new(self.sign_key, text.encode('utf-8'), SHA256).digest()
        return base64.standard_b64encode(signature)

    def __perform_key_handshake(self):
        header = self.__generate_msl_header(is_key_request=True, is_handshake=True, compressionalgo="", encrypt=False)
        payload = self.__generate_msl_end(1)
        request = {
            'entityauthdata': {
                'scheme': 'NONE',
                'authdata': {
                    'identity': self.client_config.config['esn']
                }
            },
            'headerdata': base64.standard_b64encode(header.encode('utf-8')).decode('utf-8'),
            'signature': '',
        }
        request2 = {
                "payload":base64.standard_b64encode(payload.encode('utf-8')).decode('utf-8'),
                "signature": ""
            }


        self.logger.debug('Key Handshake Request:')
        self.logger.debug(json.dumps(request))
        totalRequest = json.dumps(request) + json.dumps(request2)
        proxies = getSystemProxies()
        resp = self.session.post(nf_cfg.MANIFEST_ENDPOINT, totalRequest, headers={'User-Agent': 'Gibbon/2018.1.6.3/2018.1.6.3: Netflix/2018.1.6.3 (DEVTYPE=NFANDROID2-PRV-FIRETVSTICK2016; CERTVER=0)'}, proxies=proxies)
        if resp.status_code == 200:
            resp = resp.json()
          #  resp = """{"headerdata":"eyJjaXBoZXJ0ZXh0IjoidlJuQmpxdHo4LzF0elpGZ0tRc3hVa3dQZnNmTVRKZjhDUEZoenZTam1NalZiZmtoUnRDRFp6VkhqREdIZC9WTVRnUUZ5enpHN2tWOFlPOW5vcjc3dTRqS1pESHhUOEFnS21pSmhaZnFRbldWbUJIYWJUNTlieUdReHFnUHZPN2JPZjYzNy9oRVJZS1VhUXZLMlUrS2d3d090QVNKdWNQU2hnYlZqSHRLTGpDNkV1eHl0dFlZTUY1Qlh1MFN0SnZicklnMGo4R1JmajdRczZOcFZnaVFGL1dadElJNmxpdGZ3cVJESVIweUpHaXBqdVhjdU02eTRTZTdDMzFVQ0tSaGQ4dGdXRE50TzdnMlY4TjAvL3JtTnZTdzg2Nm1sYlJwNEZDb1FzRVBPNmZuM09EMmpCd3BZOTN3S1JKcjF5QnZPVUlrV3orMWJFOWt0cUJZak40RWc0eHNHRWRvcmFnWDhOVU9PQW5DRzYrN2piNkZzSkVlMFRERGdIYTJyRDlkaGQzeFhGakhjamU4b08rMUZlOFl4UTBKcVlaYyt2ck1yWmVvb3dLVVRCeTk5aDBBZjlkRG1BalVDb2tDRWVIVVRKLzJDd0ZOY0tUdVN4ZjZEdFBsUmREcFRkUzRnWWd1Z3N6ODZDbGppeTV6NGNCZk9GdXlPM2VzaW1YRnF4RXRYNzlhQ3JONXhIQUNaZlc3NWRaVDdEWWZqYzlVRmczV2FXa3IwRWs3ZHR0TENGTjc1amlTWlJ4UXFsT1RNdkRWWk4wT2s5NitMdXV2dmJnK3NBRGpFbUJDVG5yZ0VBd3BiMktQS3V3NTVqbUQzb3BJS20yYWg3RXd5RWlmSlgveTEwRGVwWnJsRTRoUTFjVnBMZTdGdHlvZTJEOXNoVS9LNUVYSnNPUkNaSnRGMUd4eHE3Nm9GWHBaTDlka3ErMSt3cG1LZ3I1TUxjNlBQdWk1OWdveFZvSlA4Rk9FcFdvMUJWMy94Y2w4REZNZk54UDV2NmNYd3ZGTHZmbC9qUEZWU2x3T08weFVMMTczVDlrZi92MEFiRmVqVUkrOElXdHEzcittMG9xWERYanBkdWtOODFRM21HQVQ2Z0FKR1ZrSjZSUXpvK01iVWM5bzB2MEVFSklTdk00aWgxS1ZXWDNTSHFFM3NiVlhvR1Iydi9SaENMamlmMnRYWXVTL1I4ajVXbjBJY0RnbGd6MjlCS29KRUZWc3JqSlIvRExRM0VvR2V0UzR6UzQzV0ZMWVFrUE1PYy92aG95ZXg2RkZ3dzNFcFFxSlJCS1ZIY3lYMXNlSXdTaENLNitBSzFvN2pYTnd3NzJwY0p5VUthTGpLZ0JEMi8zOTVoRGVKRDVBRy8vWTVaZm1wa2VTcGFKY3NTckZxS2VuT1hNYm80OG9JUlNZTDRGZnN4bXF4US8yMDhxS3ZhQTk0ZGI2WnpMSVorZmF1elNwUFFmN09PejhBMXE3R2lLbEpic2xIbEpXTHQvTlJqbzMzWURMalBhYys1SmRGYU9wUHdneUQwV1lGTXhZTVA0QlFFcVc0ZlkwbjBhWTlINGtRSmV6YkJXNE45N1B1Mmd1WVNwd1ZNTFNYNFk5MU5OT2ViVlNRRDF6bWJ1Z0tmUDBxaEtpdDVPa2ZyMDdVVjV0cUNpOFh2cWdCSVBNRHFnc2JlVVNld2t2RHB0Mzk2MWhDdThhTGpBb1E3Tm5VNUhwWXFMdVNBeS9BWE5xcXo3SjJDMVZZY2Fzd2trUXpSbjhyeWJGS1IwSFM5aVZzTnhVSWlkamY0Y2gzeURZYkpCNS8vNmV0ME8wU1JDQ1YxT0ZrMnpNTWsxWE43MWJ0aVZhMTMwb0dlc1l0eUcxc0dyRFdISldpM0ZKb2hQcUJ0bVNNSE1FZ2VzUWZLZForbnhCeGw1NWYrQm52ck5ZNzdhaTY1aWZFM2tGVzg2VFZnS1N6aWg2eDRUSXIvTE5DK0tidXpqcWR0c0p2WU80cm1QbUxWOHNWVS9vdk82TlhUSFFhWDBFTWZGcnNCS2dURVhlUytNUk9mNUJtcmVIYmRWL3lvaVd5bUVJTytsZTBYMlpMM1NtbFc3NXRzV0JNMjJSUGtSQmNHZlhGdG1qdVBueXpzZ0F1dUM2dktZVHB5R0NIVEVPZnhIRDhsTlkwSWlkTVlXNVcveUhTUHRHamZQVHNvWldwOVlMZmZLSDNLR3BlVmNJbEpRVzIrVXJKQVhFY09wTGYrNVI0VGlvWnBmRVNVYjRZRWFVRlhMTjI3cERxOFZ2dUFXVmY2ck5oOUEvTURpcU1nVjdUN2VTck1qSy8rcnVTd2Y0MDZ5WC83L3BrVlUrc24yT1g4TU4wVlJwUnhCZUdOdDE0UWZsNTlIekduVVFkeG5PT2lwb1NHVHp4MCtDcTdkSDk4aGhwWnUvLzVFTXFOcVN6MjZFNlhsaUR0U3VHaW1EcllSZ1poUWJKT1dJRUJGOXlRR1k0dFQ1MkkvcVh2YjBlVmVtVGdoR1BzSndVbTUyUWVHTDFGNTc4aGI0elgxUUwxdExiOThiZlJ6WVd1b0M5eUZDdFNEbE9QTXJBOC9Ib1ZOVy91LzBVMEJ2V0t4aDh6bkMxQmY0dUJUd3hLS1FrV08zWWZGeHZ2aFU4VXpQbWR2eHpIdkZNTWJ5R3FkMUhETmgvQWZ3cTlFSnNkcEQvVENkSFpxdThWWFFOSGdzNm5ZQ095b2pqUkJLQUppaHNvUjBuTGhNNXdvMkNJS09LUk1semxvYWgxa3YzSzl6SzZ6cG5LNTY1MnRTcDlGSWxqaEpkZko2Rk9zaWxLa3dJcnE2Iiwic2hhMjU2IjoiQUE9PSIsImtleWlkIjoiTkZDRENILTAyLUo2MVdXRUFLQUw0VjRYOVRHRldGVkhEMERBMDRBRl82IiwiaXYiOiJqa2lBZGtmWHhrUVB6anlUY0k3MDl3PT0ifQ==","signature":"TGPdTlg20UGTSmc2VAHrWseQRaSTKr/4FxAT2PHZjjs=","mastertoken":{"tokendata":"eyJzZXNzaW9uZGF0YSI6IkJRQ0FBQUVCRUFoa1R4bmthcG5TMnR0aEhnZEZEMWVCUUxIY0o4T3RRQWc5Q0FNL2ZZM3ZmRjJGR2VUbEJ5S0YvVzRZdTRkRHB3R042Q21UYXNETHU4b1FGUjBiMjVKY05LV2xKV0l4YVFjM2dRUFVnbzgwTENLbjBEZUFJaWFYeVExa2I0NWt5Mmh0RjdITU5wdmVRMDVTaGl1aGloVWpNaEEvZjhaL3JBMHE1VGJFYk1UYWM4dkhPWVBQOWNvQmhFV2ZBczlWZVM5dVFQSjhqVjJrWVBSdFcyb09uWHVWRzNBNkRQamlrMHJONjJKeHg5MVl6VFl5TXBCeUFUMFh6NjE0M3NvMmJwM3B1dlM5VEdwWkF1M1FwdW1JMjZpK3ZFTURRSE15RHNQbnpZMGIzOHpIUXBKK3Z0MXY2T2dENE5sR2tlZEpoL3BXaGxQcUh5cjVMNjI1Y1lJRDVqa3pWOHgrVzVwZVQ1RlNoQnRzZk1aM0M5VXBpTHZveXJkTk01ODZVVnVzWnluTVJVbm96MHJxd081dzBNRGpSVTc4U2FYMjlFQnRkaEF6eHRHM3piZXFqT1Z3R0xnK2laM2NmdU1mTDZYMklKYWYiLCJyZW5ld2Fsd2luZG93IjoxNjUyODQ2MDg3LCJzZXJpYWxudW1iZXIiOjgwOTU2NDkzMzQxMDMxMDUsImV4cGlyYXRpb24iOjE2NTM5NjkyODcsInNlcXVlbmNlbnVtYmVyIjo2fQ==","signature":"AQEAgQABASCJ2aGDokA/MiT7wQ+p+3SPV2FtPrn+G+Hl3zeefLxezfrNfRA="}}{"payload":"eyJjaXBoZXJ0ZXh0IjoiY0x5QVozeEYySzR0NjZjanRQK2VuOHcxamtUYTZ5YUNCWmxDaTh2ZDVXbGxKS2V1WDlnUTMyaE9lZTBwZzVUTHFwYjFGdkNZSWlwRmNXWlBoQTJOYU56NzFNWTFDTi9VYVJzQlVkemtFdW8zeEd0WDVqVlVORnNwRGlydGd6dGVOMWxmbVdaeDZPSWtlVExSblluOUdSNFJVQW8rampjRHgwWDF2aDJjalVBQ2c4bU10TEJKeDA5Y3c2WXdsZDJlUXF6WmZSN0R3RHl4Szl5MzFPTExiblVySk42K3dGOGZOd1J0cHlnbGYzdTkxbCt6RS9hT1NZRGlvVk1CSlFuQi9CUUk3WTV2MTRwcEpQNEJrZW5JR0ZNR1RLb2J0TjlKb3JjaXc0YmNHaEE9Iiwic2hhMjU2IjoiQUE9PSIsImtleWlkIjoiTkZDRENILTAyLUo2MVdXRUFLQUw0VjRYOVRHRldGVkhEMERBMDRBRl82IiwiaXYiOiJNekVlTldXOE50WG9PV0xSRkNidG9nPT0ifQ==","signature":"OwlDDUqo6ItFs8M+9LH1dX9xjqVhlEmhN2Pq2zUvjz8="}"""
           # resp = json.loads(resp)
            if 'errordata' in resp:
                self.logger.debug('Key Exchange failed')
                self.logger.debug(base64.standard_b64decode(resp['errordata']))
                return False
            self.logger.debug(resp)
            self.logger.debug('Key Exchange Sucessful')
            self.__parse_crypto_keys(json.JSONDecoder().decode(base64.standard_b64decode(resp['headerdata']).decode('utf-8')))
        else:
            self.logger.debug('Key Exchange failed')
            self.logger.debug(resp.text)

    def __parse_crypto_keys(self, headerdata):
        keyresponsedata = headerdata['keyresponsedata']
        self.__set_master_token(keyresponsedata['mastertoken'])
        self.logger.debug("response headerdata: %s" % headerdata)
        #self.__set_userid_token(headerdata['useridtoken'])
        if self.wv_keyexchange:
            expected_scheme = 'WIDEVINE'
        else:
            expected_scheme = 'ASYMMETRIC_WRAPPED'

        scheme = keyresponsedata['scheme']

        if scheme != expected_scheme:
            self.logger.debug('Key Exchange failed:')
            self.logger.debug('Unexpected scheme in response, expected %s, got %s' % (expected_scheme, scheme))
            return False

        keydata = keyresponsedata['keydata']

        if self.wv_keyexchange:
            self.__process_wv_keydata(keydata)
        else:
            self.__parse_rsa_wrapped_crypto_keys(keydata)

        self.__save_msl_data()
        self.handshake_performed = True

    def __process_wv_keydata(self, keydata):
        wv_response_b64 = keydata['cdmkeyresponse'] # pass as b64
        encryptionkeyid = base64.standard_b64decode(keydata['encryptionkeyid'])
        hmackeyid = base64.standard_b64decode(keydata['hmackeyid'])
        self.cdm.provide_license(self.cdm_session, wv_response_b64)
        keys = self.cdm.get_keys(self.cdm_session)
        self.logger.info('wv key exchange: obtained wv key exchange keys %s' % keys)
        # might be better not to hardcode wv proto field names
        self.encryption_key = self.__find_wv_key(encryptionkeyid, keys, ["AllowEncrypt", "AllowDecrypt"])
        self.sign_key = self.__find_wv_key(hmackeyid, keys, ["AllowSign", "AllowSignatureVerify"])


    # will fail if wrong permission or type
    def __find_wv_key(self, kid, keys, permissions):
        for key in keys:
            if key.kid != kid:
                continue
            if key.type != "OPERATOR_SESSION":
                self.logger.debug("wv key exchange: Wrong key type (not operator session) key %s" % key)
                continue

            if not set(permissions) <= set(key.permissions):
                self.logger.debug("wv key exchange: Incorrect permissions, key %s, needed perms %s" % (key, permissions))
                continue
            return key.key

        return None

    def __parse_rsa_wrapped_crypto_keys(self, keydata):
        # Init Decryption
        encrypted_encryption_key = base64.standard_b64decode(keydata['encryptionkey'])
        encrypted_sign_key = base64.standard_b64decode(keydata['hmackey'])
        cipher_rsa = PKCS1_OAEP.new(self.rsa_key)

        # Decrypt encryption key
        encryption_key_data = json.JSONDecoder().decode(cipher_rsa.decrypt(encrypted_encryption_key).decode('utf-8'))
        self.encryption_key = base64key_decode(encryption_key_data['k'])

        # Decrypt sign key
        sign_key_data = json.JSONDecoder().decode(cipher_rsa.decrypt(encrypted_sign_key).decode('utf-8'))
        self.sign_key = base64key_decode(sign_key_data['k'])

    def __load_msl_data(self):
        msl_data = json.JSONDecoder().decode(
            self.load_file(wvdl_cfg.COOKIES_FOLDER, self.client_config.config['msl_storage']).decode('utf-8'))
        # Check expire date of the token
        master_token = json.JSONDecoder().decode(
            base64.standard_b64decode(msl_data['tokens']['mastertoken']['tokendata']).decode('utf-8'))
        valid_until = datetime.utcfromtimestamp(int(master_token['expiration']))
        present = datetime.now()
        difference = valid_until - present
        difference = difference.total_seconds() / 60 / 60
        # If token expires in less then 10 hours or is expires renew it
        if difference < 10:
            self.__load_rsa_keys()
            self.__perform_key_handshake()
            return

        self.__set_master_token(msl_data['tokens']['mastertoken'])
        #self.__set_userid_token(msl_data['tokens']['useridtoken'])
        self.encryption_key = base64.standard_b64decode(msl_data['encryption_key'])
        self.sign_key = base64.standard_b64decode(msl_data['sign_key'])

    def __save_msl_data(self):
        """
        Saves the keys and tokens in json file
        :return:
        """
        data = {
            "encryption_key": base64.standard_b64encode(self.encryption_key).decode('utf-8'),
            'sign_key': base64.standard_b64encode(self.sign_key).decode('utf-8'),
            'tokens': {
                'mastertoken': self.mastertoken,
                #'useridtoken': self.useridtoken,
            }
        }
        serialized_data = json.JSONEncoder().encode(data)
        self.save_file(wvdl_cfg.COOKIES_FOLDER, self.client_config.config['msl_storage'], serialized_data.encode('utf-8'))

    def __set_master_token(self, master_token):
        self.mastertoken = master_token
        self.sequence_number = json.JSONDecoder().decode(base64.standard_b64decode(master_token['tokendata']).decode('utf-8'))[
            'sequencenumber']

    def __set_userid_token(self, userid_token):
        self.useridtoken = userid_token

    def __load_rsa_keys(self):
        loaded_key = self.load_file(wvdl_cfg.COOKIES_FOLDER, self.client_config.config['rsa_key'])
        self.rsa_key = RSA.importKey(loaded_key)

    def __save_rsa_keys(self):
        self.logger.debug('Save RSA Keys')
        # Get the DER Base64 of the keys
        encrypted_key = self.rsa_key.exportKey()
        self.save_file(wvdl_cfg.COOKIES_FOLDER, self.client_config.config['rsa_key'], encrypted_key)

    @staticmethod
    def file_exists(msl_data_path, filename):
        """
        Checks if a given file exists
        :param filename: The filename
        :return: True if so
        """
        return os.path.isfile(os.path.join(msl_data_path, filename))

    @staticmethod
    def save_file(msl_data_path, filename, content):
        """
        Saves the given content under given filename
        :param filename: The filename
        :param content: The content of the file
        """
        with open(os.path.join(msl_data_path,filename), 'wb') as file_:
            file_.write(content)
            file_.flush()
            file_.close()

    @staticmethod
    def load_file(msl_data_path, filename):
        """
        Loads the content of a given filename
        :param filename: The file to load
        :return: The content of the file
        """
        with open(os.path.join(msl_data_path,filename), 'rb') as file_:
            file_content = file_.read()
            file_.close()
        return file_content


    def get_track_download(self, track):
        return self.session.get(track.url, stream=True, proxies=self.client_config.get_proxies())

    def get_subtitle_download(self, track):



        try:
            req = requests.get(track.url)
            req.encoding = 'utf-8'
        except:
            while True:
                try:
                    req = requests.get(track.url)
                    req.encoding = 'utf-8'
                    return req
                except:
                    continue
        return req




    def get_wvconfig_options(self):
            return {'server_cert_required': True, 'pssh_header': True}

    def needs_ffmpeg(self):
        return True

    def finagle_subs(self, subtitles):
        return subs.to_srt(subtitles)

