#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 36kr

import requests
from bs4 import BeautifulSoup

def main():
  url = 'https://36kr.com/newsflashes'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Cookie': 'sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22193d9166304581-06ad155dcc37fc-1e525636-2073600-193d91663051380%22%2C%22%24device_id%22%3A%22193d9166304581-06ad155dcc37fc-1e525636-2073600-193d91663051380%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24latest_referrer_host%22%3A%22www.google.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_713123c60a0e86982326bae1a51083e1=1734513943; HMACCOUNT=0A571937ECA8AEF4; Hm_lvt_1684191ccae0314c6254306a8333d090=1734513943; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1734514053; Hm_lpvt_1684191ccae0314c6254306a8333d090=1734514053'
  }
  res = requests.get(url, headers=headers)
  res.encoding = "utf-8"
  html = BeautifulSoup(res.text, "lxml")
  lists_box = html.find('div', class_='newsflash-catalog-flow-list')
  lists = lists_box.find_all('div', class_='newsflash-item')

  for item in lists:
    text = item.find('a').get_text()
    desc = item.find('div', 'item-desc').find('span').get_text()
    print('\r\n%s' % text)
    print('\t------%s' % desc)

if __name__ == '__main__':
  main()