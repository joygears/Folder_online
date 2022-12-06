import time, requests, re, json, subprocess
from hashlib import md5


class IQIYI:

    def __init__(self, cookie):
        self.cookie = cookie

    def cmd5x_vf(self, x):
        text = 'node iqiyi.js "{0}"'.format(x)
        p = subprocess.run(text, shell=True, stdout=subprocess.PIPE)
        result = p.stdout.decode("utf-8")
        return result[-33:].strip()  # 运行js代码，里面有未知错误，但能正确解出vf值， 这里用切片，得到vf

    def authKey_md5(self, tm, tvid):
        text = "d41d8cd98f00b204e9800998ecf8427e" + tm + tvid
        md = md5()
        md.update(text.encode())
        res = md.hexdigest()
        return res

    def html_parser(self, url):
        headers = {
            "authority": "www.iqiyi.com",
            "method": "GET",
            "path": url.replace("https://www.iqiyi.com", ""),
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            #"cookie": self.cookie,
            "referer": "https://www.iqiyi.com/",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }
        resp = requests.get(url=url, headers=headers)
        html = resp.content.decode("utf-8")
        param_tvid = re.compile('''"tvid":(.[0-9]+),''', re.S | re.M | re.I)
        param_vid = re.compile('''"vid":"([0-9a-z]+)",''', re.S | re.M | re.I)
        subtitle = re.compile('"subTitle":"(.*?)"')
        title = subtitle.findall(html)[0]
        tvid = param_tvid.findall(html)[0]
        vid = param_vid.findall(html)[0]
        return {"title": title, "tvid": tvid, "vid": vid}

    def play(self, x):
        text = 'ffplay -protocol_whitelist "file,http,https,rtp,udp,tcp,tls" -loglevel quiet -i "%s"' % x
        subprocess.call(text, shell=True)

    def m3u8_down(self, title, text):
        with open(f"m3u8_down\\{title}.m3u8", "w") as f:
            f.write(text)

    def m3u8_url(self, tvid, vid, authkey, tm, vf,bid):
        url = "https://cache.video.iqiyi.com/dash"
        # url = "https://cache.video.iqiyi.com/dash?tvid=8485811691506600&bid=300&vid=40c2bd99fbabed1d387da08362c406b6&src=01010031010000000000&vt=0&rs=1&uid=628184907449420&ori=pcw&ps=1&k_uid=c55d485ee178762fe5e2135b9bddf52d&pt=0&d=0&s=&lid=&cf=&ct=&authKey=c45e671cc7f74b52f477dc8fb32e27ba&k_tag=1&ost=undefined&ppt=undefined&dfp=a0373263bc4e6a45538738180efbee117e17a685d4a066dc60d1c316825045623c&locale=zh_cn&prio=%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D&pck=7beFNi8KSGasx94870BzsDHSKGhfCR6VFBGZt7QSgKsQ81m1yfqm1sKKm2u4B6KBwm3Am3ta3&k_err_retries=0&up=&qd_v=2&tm=1625936950392&qdy=a&qds=0&k_ft1=706436220846084&k_ft4=36283952406532&k_ft5=1&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a0373263bc4e6a45538738180efbee117e17a685d4a066dc60d1c316825045623c%22%7D&ut=0&vf=32055b12a81c6aa265d5110ab1956ba9"
       # f"https://cache-video.iq.com/dash?tvid=3598215181648700&bid=200&ds=0&vid=abe2c4788688b54418ebe6a4119bf1a5&src=01010031010024000000&vt=0&rs=1&uid=0&ori=pcw&ps=0&k_uid=558078d47d736d5d367bec2fa30cc166&pt=0&d=0&s=&lid=&slid=0&cf=&ct=&authKey=cc1b2594420c20a294ee4dfcc206641e&k_tag=1&ost=0&ppt=0&dfp=a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495&prio={\"ff\":\"f4v\",\"code\":2}&k_err_retries=0&up=&su=2&applang=en_us&sver=2&X-USER-MODE=hk&qd_v=2&tm=1652522498&qdy=a&qds=0&k_ft1=143486267424900&k_ft4=34361319428&k_ft7=4&k_ft5=262145&bop={\"version\":\"10.0\",\"dfp\":\"a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495\"}&ut=0&vf=3b714340773401cd63f87aee40d4c3bc"
        params = {
            "tvid": tvid,  # 值可变， 源码可得值
            "bid": bid,  # 1080P 600  超清值为500，  高清值为300
            "ds":"0",
            "vid": vid,  # 值可变， 源码可得值
            "src": "01010031010024000000",
            "vt": "0",
            "rs": "1",
            "uid": "0",  # 未登陆是空 ， 628184907449420
            "ori": "pcw",
            "ps": "0",  # 超清值为0，  高清值为 1
            "k_uid": "558078d47d736d5d367bec2fa30cc166",
            # 未登陆是 40828cdfb5dbdb55492bd373d1720881     c55d485ee178762fe5e2135b9bddf52d
            "pt": "0",
            "d": "0",
            "s": "",
            "lid": "",
            "slid":"0",
            "cf": "",
            "ct": "",
            "authKey": authkey,  # 变化值 md5("d41d8cd98f00b204e9800998ecf8427e"+tm+tvid) 测试为真
            "k_tag": "1",
            "ost": "0",  # 超清值为 0 ， 高清值为 undefined
            "ppt": "0",  # 超清值为 0 ， 高清值为 undefined
            "dfp": "a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495",  # 可能固定，也可能变，待观察
            "prio": '{"ff":"f4v","code":2}',
            "k_err_retries": "0",
            "up": "",
            "su": "2",
            "applang": "en_us",
            "sver": "2",
            "X-USER-MODE":"hk",
            "qd_v": "2",
            "tm": tm,  # 这个值还不能随便给时间戳，估计与其他值有联系， 这里一变，其他值也应要变
            "qdy": "a",
            "qds": "0",
            "k_ft1": "143486267424900",
            "k_ft4": "34361319428",
            "k_ft7": "4",
            "k_ft5": "262145",
            "bop": '{"version":"10.0","dfp":"a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495"}',
            "ut": "0",
            "vf": vf,  # 变化值
        }

        headers = {
            "authority": "cache.video.iqiyi.com",
            "method": "GET",
            # "path": "/dash?tvid=4742103680293600&bid=500&vid=49c24d898faba42db5d70fb7db4f57c8&src=01010031010000000000&vt=0&rs=1&uid=628184907449420&ori=pcw&ps=0&k_uid=c55d485ee178762fe5e2135b9bddf52d&pt=0&d=0&s=&lid=&cf=&ct=&authKey=f39c6550d42daea8c13722e0351a789c&k_tag=1&ost=0&ppt=0&dfp=a0373263bc4e6a45538738180efbee117e17a685d4a066dc60d1c316825045623c&locale=zh_cn&prio=%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D&pck=7beFNi8KSGasx94870BzsDHSKGhfCR6VFBGZt7QSgKsQ81m1yfqm1sKKm2u4B6KBwm3Am3ta3&k_err_retries=0&up=&qd_v=2&tm=1625847214729&qdy=a&qds=0&k_ft1=706436220846084&k_ft4=36283952406532&k_ft5=1&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a0373263bc4e6a45538738180efbee117e17a685d4a066dc60d1c316825045623c%22%7D&ut=0&vf=72bfd58cae62bbc4a2cf9cda8795504b",
            "scheme": "https",
            "accept": "application/json, text/javascript",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
           # "cookie": self.cookie,
            "origin": "https://www.iqiyi.com",
            "referer": "https://www.iqiyi.com/v_1nm4qqxmbqg.html",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        }

        resp = requests.get(url=url, params=params, headers=headers)
        # print(resp.text)
        data = json.loads(resp.content.decode("utf-8"))
        video = data["data"]["program"]["video"]
        video_m3u8 = []
        for v in video:
            if v.get("m3u8"):
                m3u8 = v["m3u8"]  # m3u8文件源码
                scrsz = v["scrsz"]  # 视频分辨率
                vsize = v["vsize"]  # 视频大小
                v_url = re.compile("(http://.*?)#", re.S | re.M | re.I)
                video_url = v_url.findall(m3u8)[-1]  # 匹配到最后一段m3u8地址， 然后替换 start 开始位置为 0
                start = re.compile("(start=.*?)&")
                start = start.findall(video_url)[0]
                video_url = video_url.replace(start, "start=0")
                vsize = '{:.1f}'.format(float(vsize) / 1048576)  # 1048576 是 1024*1024的积， 是由bit,转换成M 经过两次转换
                video_m3u8.append({"video_url": video_url, "m3u8": m3u8, "scrsz": scrsz, "vsize": vsize})
        return video_m3u8

    def start(self):
        while True:
            try:
                # url = input("请将爱奇艺视频链接粘贴到这：\n")
                url = "https://www.iq.com/play/the-blooms-at-ruyi-pavilion-episode-1-e56hm44ld0?lang=en_us"
                data = self.html_parser(url)
                tm = str(int(time.time() * 1000))
                tm  = "1652525557094"
                title = data["title"]
                tvid = data["tvid"]
                vid = data["vid"]
                authkey = self.authKey_md5(tm, tvid)
                bid = "300"
                text = f"/dash?tvid={tvid}&bid={bid}&ds=0&vid={vid}&src=01010031010024000000&vt=0&rs=1&uid=0&ori=pcw&ps=0&k_uid=558078d47d736d5d367bec2fa30cc166&pt=0&d=0&s=&lid=&slid=0&cf=&ct=&authKey={authkey}&k_tag=1&ost=0&ppt=0&dfp=a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495&prio=%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D&k_err_retries=0&up=&su=2&applang=en_us&sver=2&X-USER-MODE=hk&qd_v=2&tm={tm}&qdy=a&qds=0&k_ft1=143486267424900&k_ft4=34361319428&k_ft7=4&k_ft5=262145&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495%22%7D&ut=0"
                vf = self.cmd5x_vf(text)
                video_m3u8 = self.m3u8_url(tvid, vid, authkey, tm, vf,bid)
                for video in video_m3u8:
                    video_url = video["video_url"]
                    m3u8 = video["m3u8"]
                    scrsz = video["scrsz"]
                    vsize = video["vsize"]
                    name = f"{title}_分辨率-{scrsz}_视频大小-{vsize}M"
                    self.m3u8_down(name, m3u8)
                    print(f"{name}.m3u8 文件缓存完成。 保存在m3u8_down文件夹中")
                    print("解析成功 >>>  标题：{0}\t 分辨率：{1} 视频大小：{2}M \tm3u8播放地址：{3}".format(title, scrsz, vsize, video_url))
                    file_path = "./m3u8_down/" + name + ".m3u8"
                    self.play(file_path)
            except Exception as e:
                print('error:', e, '或可能cookie设置错误,或可能参数更新需要改改！')
                break


if __name__ == '__main__':
    print("=" * 35 + '>> 欢迎使用爱奇艺视频m3u8地址解析工具 <<' + "=" * 35)
    # cookie = input("\n使用前,请设置爱奇艺的cookie:\n")
    cookie = "0"
    print("\n这是一个循环：可以不停的解析...")
    iqiyi = IQIYI(cookie)
    iqiyi.start()
