__author__ = 'cedar'

import sys
import requests
import re, time, random, logging, base64, json, traceback
from urllib import parse
from urllib import request
from lxml import etree


def list_or_empty(content, contype=None):
    assert isinstance(content, list), 'content is not list: {}'.format(content)

    if content:
        return contype(content[0]) if contype else content[0]
    else:
        if contype:
            if contype == int:
                return 0
            elif contype == str:
                return ''
            elif contype == list:
                return []
            else:
                raise Exception('only can deal int str list')
        else:
            return ''

def get_elem_text(elem):
    """抽取lxml.etree库中elem对象中文字

    Args:
        elem: lxml.etree库中elem对象

    Returns:
        elem中文字
    """
    if elem != '':
        return ''.join([node.strip() for node in elem.itertext()])
    else:
        return ''

def get_first_of_element(element, sub, contype=None):
    """抽取lxml.etree库中elem对象中文字

    Args:
        element: lxml.etree.Element
        sub: str

    Returns:
        elem中文字
    """
    content = element.xpath(sub)
    return list_or_empty(content, contype)

def get_Sgwx_Search_Article(query_url):
    print(query_url)
    # query_url = "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E4%B8%AD%E5%9B%BD&ie=utf8&_sug_=n&_sug_type_="
    # Cookie = "SUV=00AB252771745A655CD56E8452425166; SUID=415874715018910A000000005CD8CD5F; ABTEST=8|1557712224|v1; ld=bkllllllll2tcOMalllllV8Agc7lllllbUB69Zllll9lllllVllll5@@@@@@@@@@; YYID=41C9BC23F7899AAD68D33D05D0666850; LSTMV=344%2C216; LCLKINT=9438; pgv_pvi=7342263296; IPLOC=CN4403; usid=tG73kupHmJH58rCD; SNUID=EF3945895456DDCA5D0EC86154C9EA96; JSESSIONID=aaaMFNy3loNS7dR2wZfRw"
    Cookie = ";com_sohu_websearch_ITEM_PER_PAGE=50;"
    print(Cookie)



    headers = {
        "Host": "weixin.sogou.com",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        # "Referer": "https://weixin.sogou.com/weixin?type=2&s_from=input&query=%E5%9C%B0%E6%96%B9&ie=utf8&_sug_=n&_sug_type_=",
        "Accept-Encoding": "gzip, deflate, sdch, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cookie": "{}".format(Cookie),
    }


    proxy_file = "D:\\KWM\\Extraction_Server\\Config\\ProxyList\\abuyun.txt"
    with open(proxy_file, 'r') as f:
        proxy = f.read().split('\n')[0]
    proxy = proxy.split('/')
    proxy = 'http://' + proxy[1] + '@' + proxy[0]
    # print(proxy)
    proxies = {
        "http": "{}".format(proxy),
        "https": "{}".format(proxy),
    }
    # print(proxies)
    # query_url = "https://ip.cn/"

    retry_num = 0
    response = ""
    text = ""
    while retry_num < 10:

        try:
            response = requests.get(query_url, headers=headers, proxies=proxies)
        except:
            pass
        if response:
            response.encoding = "utf-8"
            text = response.text
            # print(text)
            print(response.status_code)
            if re.search('的相关微信公众号文章 ', text):
                break
        retry_num += 1


    if text:
        html = etree.HTML(text)
        html_data = html.xpath('//a[contains(@id,"sogou_vr_") and contains(@id,"_title_")]')
        for i in html_data:
            title = i
            title = get_elem_text(title).replace("red_beg", "").replace("red_end", "")
            print(title)

        with open('result.html', 'w' , encoding="utf-8") as w:
            w.write(text)


if __name__ == '__main__':
    get_Sgwx_Search_Article(sys.argv[1])