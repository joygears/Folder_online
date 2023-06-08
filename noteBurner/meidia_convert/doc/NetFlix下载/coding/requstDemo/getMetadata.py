# from urllib.request import getproxies
#
# import browser_cookie3
# import requests
# from datetime import datetime
#
# from Crypto.Cipher import AES
#
#
# def geturlMetaData(movieid):
#     # Getting the current date and time
#     dt = datetime.now()
#
#     # getting the timestamp
#     ts = datetime.timestamp(dt)
#     url = "https://www.netflix.com/api/shakti/v9b6798ed/metadata?movieid="+movieid+"&imageformat=jpg&_="+str(int(ts))
#
#     cj = browser_cookie3.Chrome(domain_name="netflix.com").load()
#     response = requests.get(url,cookies=cj)
#     return response.json()
#
# metaData = geturlMetaData("80242724")
# url = "https://occ-0-325-395.1.nflxso.net/dnm/api/v6/9pS1daC2n6UGc3dUogvWIPMR_OU/AAAABVdJxeBTw9GOSfZv39qhfsqLyZIbf_TdScdCF8lxguy6txINjhF_QAaXxuKHixp9D1UBh26noTY7JWsRkvUFcBBZPuD1P-J_-ZcyynyJCvwkwoobEZfHiZem.jpg?r=9f6"
# # url = "https://occ-0-325-395.1.nflxso.net/dnm/api/v6/9pS1daC2n6UGc3dUogvWIPMR_OU/AAAABayr0AheemJo8i2sl6HWAkrQI2mlbPAdx2pLHyEww3kpCMAb-dkK-ohZvMMCbiSQTyRtDOwbTxv61T5viamlFBiRFJPoHZxdGN1Cf6WgdiZP2wv9CC_-nBW79Q.jpg?r=9f6"
# # cj = browser_cookie3.Chrome(domain_name="netflix.com").load()
# # response = requests.get(url, cookies=cj)
# # print(response)
# # with open("2.jpg","wb") as fp:
# #     fp.write(response.content)
# # plaintext = ""
# # encryption_key = ""
# # iv =""
# # cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
# # ciphertext = cipher.encrypt(plaintext)
#
import json

with open("tset.json","r",encoding="utf-8") as fp:
    json_str = json.load(fp)

print(json_str)