import argparse
import logging
import random
import sys
import time

import requests
import re
import json

from encoder import lzw_encode

try:
    from http.cookiejar import CookieJar
except ImportError:
    from cookielib import CookieJar

import colorama
from pywidevine.clients.netflix.client import NetflixClient
from pywidevine.clients.netflix.config import NetflixConfig
from pywidevine.clients.netflix.profiles import NetflixProfiles
from pywidevine.downloader.wvdownloader import WvDownloader
from pywidevine.downloader.wvdownloaderconfig import WvDownloaderConfig
# import execjs
# with open('lzw.js', 'r', encoding='UTF-8') as f:
#     js_code = f.read()
# context = execjs.compile(js_code)
# string = '{"version":2,"url":"licensedManifest","id":165329016374135650,"languages":["en-TW"],"params":{"type":"standard","manifestVersion":"v2","viewableId":81509456,"profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"],"flavor":"STANDARD","drmType":"widevine","drmVersion":25,"usePsshBox":true,"isBranching":false,"useHttpsStreams":true,"supportsUnequalizedDownloadables":true,"imageSubtitleHeight":1080,"uiVersion":"shakti-v4f4fb02e","uiPlatform":"SHAKTI","clientVersion":"6.0035.000.911","supportsPreReleasePin":true,"supportsWatermark":true,"videoOutputInfo":[{"type":"DigitalVideoOutputDescriptor","outputType":"unknown","supportedHdcpVersions":[],"isHdcpEngaged":false}],"titleSpecificData":{"81509456":{"unletterboxed":false}},"preferAssistiveAudio":false,"isUIAutoPlay":false,"isNonMember":false,"desiredVmaf":"plus_lts","desiredSegmentVmaf":"plus_lts","requestSegmentVmaf":false,"supportsPartialHydration":false,"contentPlaygraph":["start"],"challenges":{"default":[{"drmSessionId":"9DC6975C72BA7FB0FBC979E67EDF8F29","clientTime":1653290163,"challengeBase64":"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"}]},"profileGroups":[{"name":"default","profiles":["heaac-2-dash","heaac-2hq-dash","playready-h264mpl30-dash","playready-h264mpl31-dash","playready-h264hpl30-dash","playready-h264hpl31-dash","vp9-profile0-L30-dash-cenc","vp9-profile0-L31-dash-cenc","av1-main-L30-dash-cbcs-prk","av1-main-L31-dash-cbcs-prk","dfxp-ls-sdh","simplesdh","nflx-cmisc","imsc1.1","BIF240","BIF320"]}],"licenseType":"standard","xid":"165329016333614430","showAllSubDubTracks":false}}'
#
# result = context.call("lzw_encode",string, {}) # 参数一为函数名，参数二和三为函数的参数
# result = bytes(result.values())
# print(result)

parser = argparse.ArgumentParser(
    description="netflix content downloader"
)

parser.add_argument('-t', '--title',
                    help='title id',
                    nargs='+',
                    type=int,
                    required=True)
parser.add_argument('-o', '--outputfile',
                    default='out',
                    nargs='?',
                    help='output filename (no extension)')
parser.add_argument('-q', '--quality',
                    default='432p',
                    help='video resolution',
                    choices=['480p', '720p', '1080p', '2160p'])
parser.add_argument('-a', '--audiolang',
                    default='en',
                    help='audio language',
                    type=lambda x: x.split(','))
parser.add_argument('-p', '--profile',
                    default='h264_main',
                    #choices=['h264', 'hevc', 'hdr', 'all'],
                    choices=['h264_main', 'h264_high', 'hevc', 'hdr', 'vp9', 'all'],
                    #choices=['h264', 'h264_hpl', 'hevc', 'hdr', 'vp9', 'all'],
                    help='video type to download')
parser.add_argument('-k', '--skip-cleanup', action='store_true', help='skip cleanup step')
parser.add_argument('-m', '--dont-mux',
                    action='store_true',
                    help='move unmuxed tracks instead of muxing')
parser.add_argument('-i', '--info', action='store_true', help='print track information and exit')
parser.add_argument('-d', '--debug', action='store_true', help='print debug statements')
parser.add_argument('-S', '--subs-only', action='store_true', help='download subtitles and exit')
parser.add_argument('-u', '--sub-type', default='srt', choices=['srt', 'ass', 'none'],
                    help='subtitle type (or none)')
parser.add_argument('-s', '--season', type=int, help='lookup and download season from title id')
parser.add_argument('-e',
                    '--episode_start',
                    dest="episode_start",
                    help="Recursively rip season number that provided viewable ID belongs to, starting at the episode provided")
parser.add_argument('--skip', type=int, default=0, help='skip episodes in season mode')
parser.add_argument('--region', default='us', choices=['us', 'uk', 'jp', 'ca', 'se', 'ru'], help='region to proxy')
parser.add_argument('--license',
                    action='store_true',
                    help='do license request and print decryption keys only')

args = parser.parse_args()
DEBUG_LEVELKEY_NUM = 21
logging.addLevelName(DEBUG_LEVELKEY_NUM, "LOGKEY")


def logkey(self, message, *args, **kws):
    # Yes, logger takes its '*args' as 'args'.
    if self.isEnabledFor(DEBUG_LEVELKEY_NUM):
        self._log(DEBUG_LEVELKEY_NUM, message, args, **kws)


logging.Logger.logkey = logkey

logger = logging.getLogger()

if args.license:
    logger.setLevel(21)
else:
    logger.setLevel(logging.INFO)

if args.debug:
    logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

colorama.init()

BUILD = ''
SESSION = requests.Session()


"""
login_pag = SESSION.get("https://www.netflix.com/login").text
authURL = re.search('name="authURL" value="([^"]+)"', login_pag)
print(authURL)
#authURL = re.search(r'authURL\" value\=\"(.*?)\"', login_pag)
authURL = authURL[1]

def login(username, password):
    #
    post_data = {
        'email': username,
        'password': password,
        'rememberMe': 'true',
        'mode': 'login',
        'action': 'loginAction',
        'withFields': 'email,password,rememberMe,nextPage,showPassword',
        'nextPage': '',
        'showPassword': '',
        'authURL': authURL
    }
    
    req = SESSION.post('https://www.netflix.com/login', post_data)
    #match =re.search (r'.*"BUILD_IDENTIFIER":"([a-z0-9]+)"', req.text)
    match = re.search(r'"BUILD_IDENTIFIER":"([a-z0-9]+)"', req.text) #fix by Castle / https://gist.github.com/xor10/8f65c1e66a34386e1131f8c28ff6bf64#gistcomment-2668063
	
    if match is not None:
        return match.group(1)
    else:
        return None
"""


def login(username, password):
        r = SESSION.get('https://www.netflix.com/login', stream=True, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})
        loc = None
        while 'Location' in r.headers:
            loc = r.headers['Location']
            r = SESSION.get(loc, stream=True, allow_redirects=False, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'})

        x = re.search('name="authURL" value="([^"]+)"', r.text)
        if not x:
            return
        authURL = x.group(1)
        post_data = {'userLoginId':username, 
         'password':password, 
         'rememberMe':'true', 
         'mode':'login', 
         'flow':'websiteSignUp', 
         'action':'loginAction', 
         'authURL':authURL, 
         'withFields':'userLoginId,password,rememberMe,nextPage,showPassword', 
         'nextPage':'', 
         'showPassword':''}
        req = SESSION.post(loc, post_data, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.90 Safari/537.36 CrKey/1.17.46278'})
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(e)
            logger.error(e)
            sys.exit(1)

        match = re.search('"BUILD_IDENTIFIER":"([a-z0-9]+)"', req.text)
        if match is not None:
            return match.group(1)
        else:
            return



"""
def fetch_metadata(movieid):
    #Fetches metadata for a netflix id
    req = SESSION.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid)
    return json.loads(req.text)
"""

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



#proxies = {"https": "159.100.246.156:45382"}

def get_build():
        cookies = parseCookieFile('cookies.txt')
        post_data = ''
        #req1 = SESSION.get('https://www.netflix.com', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}, cookies=cookies, proxies=proxies) 
        #print(req1.text)
        #exit(1)
        req = SESSION.post('https://www.netflix.com/browse', post_data, headers={'User-Agent': 'Gibbon/2018.1.6.3/2018.1.6.3: Netflix/2018.1.6.3 (DEVTYPE=NFANDROID2-PRV-FIRETVSTICK2016; CERTVER=0)'}, cookies=cookies)
        #req = SESSION.get('https://www.netflix.com/browse', headers={'User-Agent': 'Gibbon/2018.1.6.3/2018.1.6.3: Netflix/2018.1.6.3 (DEVTYPE=NFANDROID2-PRV-FIRETVSTICK2016; CERTVER=0)'}, cookies=cookies, proxies=proxies)
        match = re.search(r'"BUILD_IDENTIFIER":"([a-z0-9]+)"', req.text) #fix by Castle / https://gist.github.com/xor10/8f65c1e66a34386e1131f8c28ff6bf64#gistcomment-2668063
        return match.group(1)

def fetch_metadata(movieid):
        global BUILD
        cookies = parseCookieFile('cookies.txt')
        #BUILD = get_build()
        BUILD = 'vafe38bd5'
        print(BUILD)
        #cookies = 'on'
        #if BUILD == '':
        #    BUILD = login(username, password)
        """
        if cookies == 'off':
            req = SESSION.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false')
        else:
            req = requests.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false', cookies=cookies)
        """
        req = requests.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false', cookies=cookies)
        return json.loads(req.text)
        

def fetch_metadata_movie(BUILD, movieid):
        #global BUILD
        #cookies = 'on'
        #if BUILD == '':
        #    BUILD = login(username, password)
        cookies = parseCookieFile('cookies.txt')
        #BUILD = get_build()
        BUILD = 'vafe38bd5'
        print(BUILD)
        """
        if cookies == 'off':
            req = SESSION.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false')
        else:
            req = requests.get('https://www.netflix.com/api/shakti/' + BUILD + '/metadata?movieid=' + movieid + '&drmSystem=widevine&isWatchlistEnabled=false&isShortformEnabled=false&isVolatileBillboardsEnabled=false', cookies=cookies)
        """
        ts = int(round(time.time() * 1000))
        url = 'https://www.netflix.com/nq/website/memberapi/v270af61a/metadata?movieid=' + movieid + '&imageFormat=webp&withSize=true&materialize=true&_='+str(ts)
        req = requests.get(url, cookies=cookies)
        return json.loads(req.text)

episodes = []
if args.season:
    nf_cfg = NetflixConfig(0, None, None, [], ['all'], None, args.region)
    username, password = nf_cfg.get_login()
    #BUILD = login(username, password)
    if BUILD is not None:
        info = fetch_metadata(str(args.title[0]))
        serial_title = info['video']['title']
        serial_title = re.sub(r'[/\\:*?"<>|]', '', serial_title)
        for season in info['video']['seasons']:
            if season['seq'] == args.season:
                episode_list = season['episodes']
                #print(len(episode_list))
                if args.episode_start:
                    #episode_list = episode_list[(int(args.episode_start) - 1):]
                    episode_list = [episode_list[(int(args.episode_start) - 1)]]
                    #print(episode_list)
                for episode in episode_list:
                    if episode['seq'] > args.skip:
                        episodes.append((
                            episode['episodeId'],
                            "{}.S{}E{}.{}".format(
                                serial_title.replace(' ', '.').replace('"', '.').replace('"', '.').replace('(', '').replace(')', ''),
                                str(season['seq']).zfill(2),
                                str(episode['seq']).zfill(2),
                                episode['title'].replace(',', '').replace(':', '').replace('?', '').replace("'", '').replace(' ', '.').replace('/', '').replace('"', '.').replace('"', '.').replace('(', '').replace(')', ''))))
else:
    episodes = [(args.title[0], args.outputfile)]

def get_movie_name():
    #nf_cfg = NetflixConfig(0, None, None, [], ['all'], None, args.region)
    #username, password = nf_cfg.get_login()
    #BUILD = ''
    #BUILD = login(username, password)
    #print(BUILD)
    BUILD = globals()['BUILD']
    if BUILD is not None:
        info = fetch_metadata_movie(BUILD, str(args.title[0]))
        serial_title = info['video']['title']
        #serial_title = 'title'
        synopsis = info['video']['synopsis']
        #synopsis = ''
        # year = info['video']['year']
        year = info['video']['seasons'][0]["year"]
        #year = str('2019')
        try:
         boxart = info['video']['boxart'][0]['url']
        except IndexError:
         boxart = ''
        serial_title = re.sub(r'[/\\:*?"<>|]', '', serial_title)
        #print(serial_title)
        logger.info("ripping {} {}".format(serial_title, serial_title.replace('"', '.').replace('"', '.').replace('(', '').replace(')', '')))
        logger.info("boxart {} ".format(boxart))
        logger.info("synopsis {} ".format(synopsis))
        logger.info("year {} ".format(year))
        return str(serial_title.replace('"', '.').replace('"', '.').replace('(', '').replace(')', ''))
    else:
        return str('')

nf_profiles = NetflixProfiles(args.profile, args.quality)


for title, outputfile in episodes:
    if args.season:
        
        if args.profile == 'h264':
                codec_name = 'x264'
        if args.profile == 'h264_main':
                codec_name = 'x264'
        if args.profile == 'h264_high':
                codec_name = 'x264'
        if args.profile == 'hevc':
                codec_name = 'h265'
        if args.profile == 'hdr':
                codec_name = 'hdr'
        if args.profile == 'vp9':
                codec_name = 'VP9'

        if args.profile == 'all':
                codec_name = 'x264'

        group = 'MI'
        logger.info("ripping {}: {}".format(title, outputfile))
        outputfile = outputfile + '.' + str(args.quality) + '.NF.WEB-DL.' + 'AUDIOCODEC' + '.' + codec_name  + '-' +  group
        outputfile1 = outputfile + '.' + str(args.quality) + '.NF.WEB-DL.' + 'AUDIOCODEC' + '.' + codec_name  + '-' +  group
    if not args.season:
        
        if args.profile == 'h264':
                codec_name = 'x264'
        if args.profile == 'h264_main':
                codec_name = 'x264'
        if args.profile == 'h264_high':
                codec_name = 'x264'
        if args.profile == 'hevc':
                codec_name = 'h265'
        if args.profile == 'hdr':
                codec_name = 'hdr'
        if args.profile == 'vp9':
                codec_name = 'VP9'

        if args.profile == 'all':
                codec_name = 'x264'

        group = 'NFT'
        logger.info("ripping {}: {}".format(title, outputfile))
        info = fetch_metadata_movie(BUILD, str(args.title[0]))
        #print(info)
        year = info['video']['seasons'][0]["year"]
        #year = str('2019')
        outputfile = get_movie_name().replace("'", '').replace(' ', '.').replace('"', '.').replace('"', '.').replace('(', '').replace(')', '') + '.'+ str(year) + '.' + str(args.quality) + '.NF.WEB-DL.'+ 'AUDIOCODEC' + '.' + codec_name + '-' +  group
        outputfile1 = get_movie_name().replace("'", '').replace(' ', '.').replace('"', '.').replace('"', '.').replace('(', '').replace(')', '') + '.'+ str(year) + '.' + str(args.quality) + '.NF.WEB-DL.'+ 'AUDIOCODEC' + '.' + codec_name + '-' +  group
    if args.audiolang:
        audiolang = args.audiolang
    else:
        audiolang = None
    if args.quality is not None:
        profiles = nf_profiles.get_all()
    else:
        profiles = nf_profiles.get_all()
    nf_cfg = NetflixConfig(title, profiles, None, [], ['all'], audiolang, args.region)
    nf_client = NetflixClient(nf_cfg)
    """
    if not args.season:
        outputfile = outputfile + '_' + str(args.profile)
        outputfile1 = outputfile + '_' + str(args.profile)
    else:
        outputfile1 = outputfile + '_' + str(args.profile)
        outputfile = outputfile + '_' + str(args.profile)
    """
    wvdownloader_config = WvDownloaderConfig(nf_client,
                                             outputfile,
                                             args.sub_type,
                                             args.info,
                                             args.skip_cleanup,
                                             args.dont_mux,
                                             args.subs_only,
                                             args.license,
                                             args.quality,
                                             args.profile)

    wvdownloader = WvDownloader(wvdownloader_config)
    wvdownloader.run()
