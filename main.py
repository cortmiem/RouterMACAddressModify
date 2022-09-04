import random
import re
import time

import requests


def get_current_time():
    return time.strftime("\033[1m[%H:%M:%S]", time.localtime())


def check_net_connectivity(server):
    try:
        r = requests.get(server, timeout=6)
    except ConnectionError:
        return False
    except:
        return True
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
    print('\n' + get_current_time() + "login success: token: " + pwd)
    return pwd


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
    p.write(get_current_time() + "requests response: " + message[0])


if __name__ == "__main__":
    print("RMACAM 7.0")
    print("For internal use only.")
    while True:
        if check_net_connectivity("http://mirrors.gdut.edu.cn/"):
            time.sleep(1)
            p.update(1)
        else:
            time.sleep(1)
            token = login()
            post_new_mac(token)
            time.sleep(10)
