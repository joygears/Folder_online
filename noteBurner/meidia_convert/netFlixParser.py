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
    def get_track_and_init_info(self):
        nf_cfg = NetflixConfig(self.movieid, None, None, [], ['all'], None, None)
        nf_client = NetflixClient(nf_cfg)
        if nf_client.login() == False:
            exit(1)
        return nf_client.get_track_and_init_info(self.cookie)





def getTrackInfo(url):
    cookies = get_cookie(url)
    parser = NetflixParser(url, cookies[0])
    track_info = parser.get_track_and_init_info()
    return track_info
if __name__ =="__main__":
    url = "https://www.netflix.com/watch/60034587?trackId=255824129&tctx=0%2C0%2CNAPA%40%40%7C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2CNAPA%40%40%7C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750_titles%2F1%2F%2F%E5%B0%8F%E5%A7%90%E5%A5%BD%E7%99%BD%2F0%2F0%2Cunknown%2C%2C01fa823c-2c60-4711-9729-ce2dd8af52a1-291837750%7C1%2CtitlesResults%2C60034587%2CVideo%3A60034587%2CminiDpPlayButton"
    cookies = get_cookie(url)
    parser = NetflixParser(url,cookies[0])
    data = parser.fetch_metadata_movie()
    track_info = parser.get_track_and_init_info()
    print(data)
    print(track_info)
