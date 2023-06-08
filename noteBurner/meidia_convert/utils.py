import sys
from urllib.request import getproxies


def getSystemProxies():
    auto_proxies = getproxies()
    if auto_proxies != {}:
        proxies = {
            'http': auto_proxies['http'].replace("http://", ""),
            'https': auto_proxies['https'].replace("https://", ""),
        }
    else:
        proxies = {}
    return proxies

def flush_print(data):
    print(data)
    sys.stdout.flush()