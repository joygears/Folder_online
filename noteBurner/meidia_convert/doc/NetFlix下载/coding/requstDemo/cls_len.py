# class Hello():
#     a = 1
#     def h1(self):
#         print ('hello 1111')
#         print(self.a)
#
#     @classmethod
#     def h2(cls):
#         print ('hello 22222')
#         print(cls.a)
# class sub(Hello):
#     c = 0
#     pass
# print(sub.__dict__)
import hashlib


def getPcVf(str):

    vf = hashlib.new('md5', (str + 'u6fnp3eok0dpftcq9qbr4n9svk8tqh7u').encode("utf-8")).hexdigest()

    return vf
path = "/dash?tvid=3598215181648700&bid=300&ds=0&vid=abe2c4788688b54418ebe6a4119bf1a5&src=01010031010024000000&vt=0&rs=1&uid=0&ori=pcw&ps=0&k_uid=558078d47d736d5d367bec2fa30cc166&pt=0&d=0&s=&lid=&slid=0&cf=&ct=&authKey=062e96f586672334b5f9ee33673211e4&k_tag=1&ost=0&ppt=0&dfp=a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495&prio=%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D&k_err_retries=0&up=&su=2&applang=en_us&sver=2&X-USER-MODE=hk&qd_v=2&tm=1652518510997&qdy=a&qds=0&k_ft1=143486267424900&k_ft4=34361319428&k_ft7=4&k_ft5=262145&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a1070cf776396d5866b0195d3d261c2138361b79c6c501b8c4658562367e54c495%22%7D&ut=0"
print(hashlib.md5(path.encode("utf-8")).hexdigest())