import os

from browsercookie import get_cookie
from netFlixDecryptor import NetflixDecryptor
from netFlixMessageProcessor import NetFlixMessageProcessor
from netFlixParser import NetflixParser
from netflixDownloader import NetflixDownloader
from netflixMerger import NetflixMerger

url = "https://www.netflix.com/watch/80179267?trackId=254015180&tctx=0%2C0%2Cdd89ea0a-6989-4b19-933b-794e98deb107-166893810%2CNES_735BD23B46086FF443F513B269BE98-951BB306AEF2A8-54DFB68767_p_1686208449464%2CNES_735BD23B46086FF443F513B269BE98_p_1686208449464%2C%2C%2C%2C%2CVideo%3A80179190%2CbillboardPlayButton"
save_path = "temp1"

cookies = get_cookie(url)
parser = NetflixParser(url, cookies[0])
data = parser.fetch_metadata_movie()
track_info = parser.get_track_and_init_info()

messager = NetFlixMessageProcessor(data,track_info)
video_info = messager.get_videoinfo_by_quality(1080)
audio_info = messager.get_audioinfo_by_lan("en","English","5.1")
subtitle_info = messager.get_subtitleinfo_by_lan("zh-Hans")

vt = {"url":video_info["url"]}
ats = [{"url":audio_info["url"],"language":audio_info["languageDescription"]}]
sts = [{"url":subtitle_info["url"],"language_code":subtitle_info["language"]}]
title = messager.get_title()
downloader = NetflixDownloader(title,save_path,vt,ats,sts)
#downloader.download_subtitle()
video_path = downloader.download_video()
audio_path = downloader.download_audio()

decryptor = NetflixDecryptor(video_info["keyid"], video_path)
decryptor.decrypt()
decryptor = NetflixMerger(video_path,audio_path)
decryptor.merge()
