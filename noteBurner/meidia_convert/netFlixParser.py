import json
import time
import requests
import re

from browsercookie import get_cookie
from pywidevine.clients.netflix.client import NetflixClient
from pywidevine.clients.netflix.config import NetflixConfig
from utils import getSystemProxies


class NetflixParser():
    def __init__(self,url,cookie):
        self.url = url
        self.cookie = cookie
        self.movieid = self._pick_up_movieid(url)

    def _pick_up_movieid(self,url):
        regex = r"https?://www.netflix.com/watch/([0-9]+).+"
        match_obj = re.match(regex,url)
        return match_obj.groups()[0]

    def fetch_metadata_movie(self):
        proxies = getSystemProxies()
        ts = int(round(time.time() * 1000))
        url = 'https://www.netflix.com/nq/website/memberapi/v4cfc34e6/metadata?movieid=' + self.movieid + '&imageFormat=webp&withSize=true&materialize=true&_=' + str(ts)
        req = requests.get(url, cookies=self.cookie, proxies=proxies)
        return json.loads(req.text)
    def get_track_and_init_info(self,session_id="",challengeBase64=""):
        nf_cfg = NetflixConfig(self.movieid, None, None, [], ['all'], None, None)
        nf_client = NetflixClient(nf_cfg)
        if nf_client.login() == False:
            exit(1)
        return nf_client.get_track_and_init_info(self.cookie,session_id,challengeBase64)





def getTrackInfo(url,session_id="",challengeBase64=""):
    cookies = get_cookie(url)
    parser = NetflixParser(url, cookies[0])
    track_info = parser.get_track_and_init_info(session_id,challengeBase64)
    return track_info
if __name__ =="__main__":
    url = "https://www.netflix.com/watch/80142058?trackId=255824129&tctx=0%2C0%2CNAPA%40%40%7C7d73b5e8-cd7b-4737-988e-1c504b531ab4-98736352_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2CNAPA%40%40%7C7d73b5e8-cd7b-4737-988e-1c504b531ab4-98736352_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2Cunknown%2C%2C7d73b5e8-cd7b-4737-988e-1c504b531ab4-98736352%7C1%2CtitlesResults%2C80142058%2CVideo%3A80142058%2CminiDpPlayButton"
    session_id="09F02746A7F7EC0A17F1A79BBE380C3D"
    challengeBase64="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"
    cookies = get_cookie(url)
    parser = NetflixParser(url,cookies[0])
    #data = parser.fetch_metadata_movie()
    track_info = parser.get_track_and_init_info(session_id,challengeBase64)
    #print(data)
    print(track_info)
