#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function NHK

import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import asyncio

async def japan():
  url = 'https://www3.nhk.or.jp/news/'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Referer': 'https://www3.nhk.or.jp/news/'
  }
  res = requests.get(url, headers=headers)
  res.encoding = 'utf-8'
  html = BeautifulSoup(res.text, 'lxml')
  title = html.find_all('em', class_='title')

  for item in title:
    traslator = Translator()
    res = await traslator.translate(item.get_text(), src='auto', dest='zh-CN')
    print('\r\n%s' % res.text)

if __name__ == '__main__':
  asyncio.run(japan())