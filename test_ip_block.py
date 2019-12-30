__author__ = 'cedar'

import sys
import requests
import re, time,json
from lxml import etree

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


def test_ip_block():

    with open('article_url.txt', 'r', encoding="utf-8") as r:
        url = r.read()
        url_list = url.split('\n')
    # print(type(url_list))
    # print(url_list)

    while True:
        request_count = 0
        start_time = time.time()
        print('开始时间：{}'.format(start_time))

        for url in url_list:
            request_count +=1
            print(request_count)
            response = requests.get(url, timeout=2)
            time.sleep(0.0)
            if response:
                response.encoding = "utf-8"
                text = response.text
                # print(response.status_code)
                # print(text)
                html = etree.HTML(text)
                html_data = html.xpath('//*[@id="activity-name"]')
                for i in html_data:
                    title = i
                    title = get_elem_text(title).replace("red_beg", "").replace("red_end", "")
                    print(title)

                if re.search('请用微信扫描二维码进行访问', text):
                    print('出错信息：' + '请用微信扫描二维码进行访问')
                    time.sleep(300)
                    break
                # if request_count>=10:
                #     break

        end_time = time.time()
        print('结束时间：{}'.format(end_time))
        print('请求次数：{}'.format(request_count))
        print('时间差：{} 秒'.format(end_time-start_time))
        print('---------------------------')

        with open('result.txt', 'a+', encoding="utf-8") as w:
            w.write('开始时间：{}'.format(start_time))
            w.write('\n结束时间：{}'.format(end_time))
            w.write('\n请求次数：{}'.format(request_count))
            w.write('\n时间差：{} 秒'.format(end_time-start_time))
            w.write('\n-----------------------------\n')

if __name__ == '__main__':
    test_ip_block()