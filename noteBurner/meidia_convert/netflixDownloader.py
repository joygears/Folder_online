import json
import os

import yt_dlp

from netFlixDecryptor import NetflixDecryptor
from pywidevine.clients.netflix.client import NetflixClient
from pywidevine.clients.netflix.config import NetflixConfig
from pywidevine.downloader.tracks import VideoTrack, AudioTrack, SubtitleTrack
from pywidevine.downloader.wvdownloader import WvDownloader
from pywidevine.downloader.wvdownloaderconfig import WvDownloaderConfig
from utils import flush_print


class NetflixDownloader():
    def __init__(self,title,save_path,video_info,audio_infos,subtitle_infos):
        self.video_info = video_info
        self.audio_infos = audio_infos
        self.subtitle_infos = []
        for subtitle_info in subtitle_infos:
            self.subtitle_infos.append(SubtitleTrack(0, "zh",subtitle_info['language_code'], url = subtitle_info["url"], type="srt",default=False))
        self.downloaded_filesize = 0
        self.title = title
        self.save_path = save_path
        nf_cfg = NetflixConfig("123456", None, None, [], ['all'], None, None)
        nf_client = NetflixClient(nf_cfg)
        wvdownloader_config = WvDownloaderConfig(nf_client,
                                                 title,
                                                 "srt",
                                                 False,
                                                 False,
                                                 False,
                                                 False,
                                                 False,
                                                 "1080p",None)
        self.downloader = WvDownloader(config=wvdownloader_config)

    def _hook(self, d):
        if 'status' in d:
            if d['status'] == 'downloading':
                if 'filename' in d:
                    self.hook_filepath = d['filename']
                elif 'total_bytes_estimate' in d:
                    self.pre_filesize = d['total_bytes_estimate']
                else:
                    if 'total_bytes' in d:
                        self.pre_filesize = d['total_bytes']

                    # if 'total_bytes_estimate' in d:
                    #     self.total_filesize = d['total_bytes_estimate'] if d['total_bytes_estimate'] != None else self.total_filesize
                if 'total_bytes' in d:
                    self.total_filesize = d['total_bytes'] if d['total_bytes'] != None else self.total_filesize
                progress = (d['downloaded_bytes'] + self.downloaded_filesize) / float(self.total_filesize)
                if progress > 1.0:
                    self.total_filesize += (d['downloaded_bytes'] + self.downloaded_filesize) - self.total_filesize + 5760
                    progress = (d['downloaded_bytes'] + self.downloaded_filesize) / float(self.total_filesize)
                resp = {'type':"downloading",
                 'msg':{'progress':str('{0:.3f}'.format(progress)),
                  'speed':d['_speed_str'].replace('KiB', 'KB').replace('MiB', 'MB'),
                  'filesize':str(self.total_filesize),
                  'eta':str(d.get('eta',0))}}
                flush_print("\n"+json.dumps(resp))


    def download_media(self,title,ext,url):
        ydl_opts = {'cachedir': False,
                    'no_warnings': True,
                    'noplaylist': True,
                    'playliststart': 1,
                    'playlistend': 1,
                    'retries': 10,
                    "socket_timeout": 5,
                    'quiet':True,
                    'outtmpl': os.path.join(self.save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [
                        self._hook],
                    }
        ie_result = {
            "id":str(0),
            'title':title,
            'direct':True,
            'url':url,
            'ext':ext,
            'protocol':'http',
            'extractor':'generic'
        }
        prepare_filepath = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(ie_result)
        yt_dlp.YoutubeDL(ydl_opts).process_ie_result(ie_result)
        return prepare_filepath
    def download_video(self):
        return self.download_media(self.title,"mp4",self.video_info['url'])

    def download_audio(self):
        for audio_info in self.audio_infos:
            return self.download_media(self.title, "mp3", audio_info['url'])
    def download_subtitle(self):
        for subtitle in self.subtitle_infos:
            self.downloader.download_and_convert_subtitle(subtitle,self.save_path)

if __name__ =="__main__":
    # vt = VideoTrack(True, 797352636, 0, "http://ipv6-c024-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=97&e=1655219462&t=P-cLJ_EOXDuAwbbVKJh-X4jQdgcyRLGRw7Be5fAYUhvLssdAQJ7xex96aOYXGksKfbaQgXEShmtD2kPIXYhj-FU28NcUqozOuSl7-ynGGyMtKlScP00kQokmDZFQWuLA6awAO6PmTNM6eUF8C3zWrDzOUjNDc3Kn927V2wKMa0ce7zv0lJKyCBBQw_hIzdHBEpdfp2ri2t7va4CuDdEVYKaWsNwnAnV6R2UPOYCavKEAm9UyZOHeoGVJTZAMqnhlfYyKbYA-J-qccg4", codec="playready-h264hpl30-dash", bitrate=871, width=960, height=540)
    # ats = [AudioTrack(False,  585643685, 0, "http://ipv6-c057-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=59&e=1655219462&t=zew0rD8fvMHvNF7VTqUEmvrrk2Vt9048ElpIaifIhr1NlGtG5u7SUyvHL88_xSSb8AVqN4hmXbYlH73tXiYYOO2CKQEDJTCLNrEXd3r3tuq8WyEh0MO33RdPcFwZVfcQZQw8_a2flAjWQwh8a8Ra3JS_LwijmA3NogHiXf5b-kBXxk98FiUp539nge0_g6bDYycHJXIkijoTAef6cGfWEl6ujkFFCiMZU9LfHV8hMudJOcAQMRli3ErJBFgSCwQbtFoRuaEXh4GalQ", "ddplus-5.1hq-dash", 640,"English - Audio Description")]
    #sts = [SubtitleTrack(0, "de","de", url = "http://ipv6-c024-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=97&e=1655219462&t=e_UhIhKoXrH71nnci7ajVAWbsfUdAsqm92lgou8rTwQflq5znNlKs9cPh6yL7nZvl3RUyF6V3VrFxcyndTlo5O61VfsjJsbL1pmW-8Bym8L0poIs5mabHD22Gwz1ziL0AgFXKJQL5sgO60fsw-XqGszKCcoHDJSEb0M7D_aCVuTBjYt4FR2Ytp3Pv9V7Pm4SmygGeoBeMfcIcjYHkJ2B4wN0cHwvG_rUBxfkPKwmKs6u-oK5cb5IYN_8eqx6eK2Epw1N63lqE_Q", type="srt",default=False)]
    vt = {"url":"http://ipv6-c037-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=97&e=1655304464&t=rc3xbagX5vf_MKtJmFMwEE_4BfQZcH4dvBjgKNqi1V2_fN3W8juTw03vq34Lr56of-J5flzbfU8Z8u7yYsua5NjiSO8c-Iv_JpEOp6PS7uqBXJ4famUGxHr-aU5Z6_mgQX-U1N0gc8hDytNKLK2TDsqSRIuAR9_p5Uiqq1nxmnlzd-I5_chBeP6K3TysAk_dSDzA93hHSKf4B-fjLTldnOw1I0oAuvxfqZX7phKjD3-kMLwLRfbLhGGVH68Fm-Vz5ad4TKURUI7Wc44"}
    ats = [{"url":"http://ipv6-c022-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=98&e=1655304464&t=pl318FPK2P1TZFFAWR2MwG5vzdeVzAOLOxSaIaFWN0uPg7PxK8LUeFE0SDOiDshsAh8z-LiNGPfQ5A_kMM8jsziRZU5LQme0t2sz6m6Inxe1cTL00C1KpgKF9ljPsaPyLQnXimIVat1Xiij0mnpt-O1ggBk1c-p2YDcYPWqUmXbt4yENRnxj5uOhAP9gT93k0qiCHjd37CbUvo8gotL-S2rydDho3FHy9H604fGOQbHXTZPWzKZYur9p3UPzsmPDi1GaVV0R7w6xzQ",
            "language":"Italian"}]
    sts = [{"url":"http://ipv6-c022-hkg001-ix.1.oca.nflxvideo.net/?o=1&v=98&e=1655304464&t=lNTrG2WbjAxBr7fEbbaCUD7O1CWHdjkDy-wa8K1z7Vt-bWAqy5UidXso_AT9ryKX32ne-gkt-Wj7YO3wRFer6zMnv41HNMHcD1DKuF1cXSm2wa-j8-Z1oYjJzblLF_kwuJXCU35eT5GoAQtB4ym74MkLE8yj4a4sQz07L1dcbxRfBjPvmydft5MAEkvyO-FaEQ68J-spoBzDyn_yUo92WKcfpkC-03gbe4Pa7f89CPjBrIiT8ZUtckdH-GyLsqM-JvumHeyVhDQ",
            "language_code":"en"}]
    title = "123"
    save_path = "temp1"
    downloader = NetflixDownloader(title,save_path,vt,ats,sts)
    downloader.download_subtitle()
    downloader.download_video()
    downloader.download_audio()

