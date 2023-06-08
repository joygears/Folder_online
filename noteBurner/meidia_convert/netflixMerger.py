import os
import subprocess


class NetflixMerger():
    def __init__(self,video_path,audio_path):
        self.video_path = video_path
        self.audio_path = audio_path
        self.out_path = self._get_merger_path(video_path)
    def _get_merger_path(self,encrypt_path):
        forward,ext = os.path.splitext(encrypt_path)
        return forward+"_merger"+ext

    def build_commandline_list(self):
        commandline = ["binaries/ffmpeg.exe"]
        commandline.append('-y')
        commandline.append('-i')
        commandline.append(self.video_path)
        commandline.append('-i')
        commandline.append(self.audio_path)
        commandline.append("-vcodec")
        commandline.append("copy")
        commandline.append("-acodec")
        commandline.append("copy")
        commandline.append(self.out_path)
        return commandline
    def merge(self):
        commandline = self.build_commandline_list()
        wvdecrypt_process = subprocess.Popen(commandline)
        wvdecrypt_process.wait()
        os.replace(self.out_path,self.video_path)
        os.remove(self.audio_path)

if __name__ == "__main__":
    decryptor = NetflixMerger("temp1/123.mp4","temp1/123Italian.mp3")
    decryptor.merge()
