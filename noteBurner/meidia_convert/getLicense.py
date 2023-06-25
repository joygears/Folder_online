import re
import sys
from http.cookiejar import CookieJar

from Cookies.BrowserCookie import create_cookie
from netFlixParser import getTrackInfo



url = "https://www.netflix.com/watch/80231419?trackId=255824129&tctx=0%2C0%2CNAPA%40%40%7C2db68cf5-fe67-4ebb-a961-2b48bac932c1-1511764_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2CNAPA%40%40%7C2db68cf5-fe67-4ebb-a961-2b48bac932c1-1511764_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2Cunknown%2C%2C2db68cf5-fe67-4ebb-a961-2b48bac932c1-1511764%7C1%2CtitlesResults%2C80231419%2CVideo%3A80231419%2CminiDpPlayButton"
session_id,challege = sys.argv[1:]
track_info = getTrackInfo(url,session_id,challege)
license = track_info['result']['video_tracks'][0]['license']['licenseResponseBase64']
print("\nlicense:%s\n" % license)