import re
import sys
from http.cookiejar import CookieJar

from Cookies.BrowserCookie import create_cookie
from netFlixParser import getTrackInfo



url,session_id,challege = sys.argv[1:]
track_info = getTrackInfo(url,session_id,challege)
license = track_info['result']['video_tracks'][0]['license']['licenseResponseBase64']
print("\nlicense:%s\n" % license)