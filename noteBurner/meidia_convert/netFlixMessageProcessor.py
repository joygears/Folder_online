import json
class NetFlixMessageProcessor():
    def __init__(self,data,track_info):
        self.data = data
        self.track_info = track_info

    def get_videoinfo_by_quality(self,quality,bitrate=0):
        result = self.track_info['result']
        video_track = result["video_tracks"][0]
        streams = video_track["streams"]

        filter_s = []
        for s in streams:
            if quality <= s['crop_h']:
                filter_s.append(s)
        if len(filter_s) == 0:
            filter_s.append(streams[-1])
        taget_s = filter_s[-1]
        for s in filter_s:
            if bitrate <= s['bitrate']:
                taget_s = s
                break

        return {"url":taget_s["urls"][0]["url"],
                "height":taget_s["crop_h"],
                "width":taget_s["crop_w"],
                "keyid":taget_s["drmHeaderId"],
                "bitrate":taget_s["bitrate"]
                }

    def get_audioinfo_by_lan(self,lan="en",languageDescription="",channels=""):
        result = self.track_info['result']
        audio_tracks = result["audio_tracks"]
        target_a = audio_tracks[0]
        for audio in audio_tracks:
            if audio["language"] == lan:
                target_a = audio
                if languageDescription == audio["languageDescription"] and channels==audio["channels"]:
                    break
        height_s = target_a["streams"][-1]
        return {
            "url": height_s["urls"][0]["url"],
            "language":target_a["language"],
            "languageDescription":target_a["languageDescription"],
            "channels":target_a["channels"],
            "bitrate": height_s["bitrate"]
        }
    def get_subtitleinfo_by_lan(self,lan="en",languageDescription=""):
        result = self.track_info['result']
        timedtexttracks = result["timedtexttracks"]
        target_s = timedtexttracks[0]
        for subtitle in timedtexttracks:
            if subtitle["language"] == lan:
                target_s = subtitle
                if languageDescription == subtitle["languageDescription"]:
                    break
        ttDownloadables = target_s["ttDownloadables"]
        simplesdh = list(ttDownloadables.values())[0]
        downloadUrls = simplesdh["downloadUrls"]
        url = list(downloadUrls.values())[0]
        return {
            "url": url,
            "language":target_s["language"],
            "languageDescription":target_s["languageDescription"]
        }
    def get_title(self):
        video = self.data["video"]
        return video["title"]

if __name__ == "__main__":
    with open("track_info","r") as fp:
        track_info = json.loads(fp.read())
    with open("data","r") as fp:
        data = json.loads(fp.read())
    messager = NetFlixMessageProcessor(data,track_info)
    video_info = messager.get_videoinfo_by_quality(1080)
    audio_info = messager.get_audioinfo_by_lan("en")
    subtitle_info = messager.get_subtitleinfo_by_lan("zh-Hans")
    title = messager.get_title()
    print(video_info)
    print(audio_info)
    print(subtitle_info)
    print(title)