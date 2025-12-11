#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function V2EX

import requests
from bs4 import BeautifulSoup

def all_topics():
  url = 'https://www.v2ex.com/'
  res = requests.get(url)
  html = BeautifulSoup(res.text, 'lxml')
  topics = html.findAll('a', class_='topic-link')
  for item in topics:
    print('\r\n%s' % item.get_text())

if __name__ == '__main__':
  all_topics()