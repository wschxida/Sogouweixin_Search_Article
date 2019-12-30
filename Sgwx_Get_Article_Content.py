__author__ = 'cedar'

import sys
import requests
import re, time
import random



def Get_proxies(proxy_list):
    count = len(proxy_list)  # 获取个数
    # print(count)
    proxynum = random.randrange(0, count, 1)  # 生成随机序号
    proxy = proxy_list[proxynum]
    # print(proxy)

    # 阿布云的形式http-dyn.abuyun.com:9020/H2R0E7OZ43KD761D:5C9E0CC2F242B04D
    # 结果为http://H2R0E7OZ43KD761D:5C9E0CC2F242B04D@http-dyn.abuyun.com:9020'
    if '/' in proxy:
        proxy = proxy.split('/')
        proxy = 'http://' + proxy[1] + '@' + proxy[0]
    # print(proxy)
    proxies = {
        "http": "{}".format(proxy),
        "https": "{}".format(proxy),
    }
    return proxies


def Sgwx_Article_Content(query_url, result_file_name):

    proxy_file_abuyun = "D:\\KWM\\Extraction_Server\\Config\\ProxyList\\abuyun_weixin.txt"
    proxy_file_aliyun = "D:\\KWM\\Extraction_Server\\Config\\ProxyList\\aliyun_squid.txt"

    with open(proxy_file_abuyun, 'r') as f1:
        proxy_list1 = f1.read().split('\n')
    with open(proxy_file_aliyun, 'r') as f2:
        proxy_list2 = f2.read().split('\n')

    # 由于阿布云的IP池比较大，所以*100增加被抽取到的概率
    proxy_list = proxy_list1*100 + proxy_list2
    # print(proxy_list)

    # 不要加上，因为有跳转
    headers = {
        'Host': 'mp.weixin.qq.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    retry_num = 1
    text = ""
    response = ""
    while retry_num < 6:

        print(retry_num)
        proxies = Get_proxies(proxy_list)
        print(proxies)
        try:
            response = requests.get(query_url, proxies=proxies, timeout=5)
        except:
            pass
        # response = requests.get(query_url, proxies=proxies, timeout=2)

        if response:
            response.encoding = "utf-8"
            text = response.text
            # print(text)
            print(response.status_code)
            if re.search('class="rich_media_title"', text):
                break
        retry_num += 1


    with open(result_file_name, 'w', encoding="utf-8") as w:
        if text:
            w.write(text)
        w.write(text)


if __name__ == '__main__':
    Sgwx_Article_Content(sys.argv[1], sys.argv[2])
    # Sgwx_Article_Content('http://lumtest.com/myip.json', 'myip.txt')
    # Sgwx_Article_Content('https://mp.weixin.qq.com/s?src=11&timestamp=1567757282&ver=1835&signature=LN8vtkAw4dSxV4-AG2JWXBiCY-FhHFPxXZ*G3iqI91hm2eaep4bNLocDChJtFZmSCsfpEurnXBUtAEtu9TxHPYl94fwNXYLYHDdHdmSIO7jDQrbKMkVJkNiALirj52lk&new=1', 'result.html')