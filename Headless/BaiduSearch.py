#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 百度搜索结果

from bs4 import BeautifulSoup

def SearchResult(data):
  html = BeautifulSoup(data, 'html.parser')
  content = html.find('div', id='content_left')
  result = content.find_all('div', class_='result')

  for item in result:
    res = item.find_all('h3',class_='c-title')
    title = res[0].a.get_text()
    print(title)