#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 百度热搜

from bs4 import BeautifulSoup
import json

def BaiduHot(page_source):
  soup = BeautifulSoup(page_source, 'lxml')
  data = soup.find('textarea', id='hotsearch_data').get_text()
  hotList = json.loads(data)['hotsearch']

  for item in hotList:
    print(f"{int(item['index'])+1}. {item['card_title']}")
