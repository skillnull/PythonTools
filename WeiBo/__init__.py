#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 微博热搜

import requests
from bs4 import BeautifulSoup

def main():
  url = 'https://s.weibo.com/top/summary?cate=realtimeho'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'SUB=_2AkMSjdLlf8NxqwFRmfoTzmnhZYl-zwvEieKk0SM-JRMxHRl-yT9kqncGtRB6OQ38CnPn9yiFClr7gzx-ILSdTDQSsBJc; SINAGLOBAL=2793368918109.54.1728635143817; UOR=,,www.google.com; XSRF-TOKEN=ViGiZBdjo8lbaz861ak3d94E; WBPSESS=V0zdZ7jH8_6F0CA8c_ussems2ooi2oISTjoqrgw0BPb0xOXeRG8fgtsfCCwK4z-89gPFGQRBnTVKBZ_pjoEXUS_cWlvZBQM5OWeOo5W3kFwLijeTaAPGZRRSYGC8W2O2yBjahwkNrh-gn4zb9dSzlAmG6gLvY_iRkHtFrrzxdPw=; _s_tentry=-; Apache=9536736833525.607.1734512411018; ULV=1734512411028:3:1:1:9536736833525.607.1734512411018:1731035876374'
  }
  res = requests.get(url, headers=headers)
  res.encoding = "utf-8"
  html = BeautifulSoup(res.text, "lxml")
  lists_box = html.find('div', id='pl_top_realtimehot')
  lists = lists_box.find_all('td', class_='td-02')

  for item in lists:
    text = item.find('a').get_text()
    print(text, '\r\n')

if __name__ == '__main__':
  main()