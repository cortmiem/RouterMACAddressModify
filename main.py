import random
import re
import requests
import time
from urllib import request


def get_current_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())


def check_net_connectivity(server):
    try:
        print(request.urlopen(url=server, timeout=3.0))
    except:
        return False
    return True


def get_random_mac():
    getmac = [random.randrange(0x00, 0xff, 2),
              random.randint(0x00, 0xff),
              random.randint(0x00, 0xff),
              random.randint(0x00, 0xff),
              random.randint(0x00, 0xff),
              random.randint(0x00, 0xff)]
    mac = '-'.join(map(lambda x: "%02x" % x, getmac))
    print(get_current_time() + "generate MAC: " + mac)
    return mac


def login():
    url = "http://192.168.1.1"
    payload = "{\"method\":\"do\",\"login\":{\"password\":\"xlZ49Jw29TefbwK\"}}"
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': '192.168.1.1',
        'Content-Length': '54',
        'Connection': 'Keep-Alive',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    pwd = re.search(r'stok":"(.*)"', response.text, re.I).group(1)
    print(get_current_time() + "login success: token: " + pwd)
    return token


def post_new_mac(stok):
    url = "http://192.168.1.1/stok=" + stok
    mac = get_random_mac()
    payload = "{\"protocol\":{\"wan\":{\"macaddr\":\"" + mac + "\",\"wan_rate\":\"auto\"},\"pppoe\":{\"dial_mode\":\"auto\",\"conn_mode\":\"auto\",\"mtu\":\"1480\",\"access\":\"\",\"server\":\"\",\"ip_mode\":\"dynamic\",\"dns_mode\":\"dynamic\",\"proto\":\"none\"}},\"method\":\"set\"}"
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://192.168.1.1/',
        'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.7,ja;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Host': '192.168.1.1',
        'Content-Length': '226',
        'Connection': 'Keep-Alive',
        'Cache-Control': 'no-cache'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    message = re.findall(r'{(.*?)}', response.text)
    print(get_current_time() + message[0])


print("RMACAM 7.0")
print("For internal use only.")
while True:
    if check_net_connectivity('https://www.baidu.com'):
        time.sleep(1)
    else:
        token = login()
        post_new_mac(token)
        time.sleep(5)
