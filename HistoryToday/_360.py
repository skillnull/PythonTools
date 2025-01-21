#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 360历史上的今天

import requests
from bs4 import BeautifulSoup

def getLists():
  url = 'https://hao.360.com/histoday/'
  res = requests.get(url)
  res.encoding = "utf-8"
  html = BeautifulSoup(res.text, "lxml")
  items = html.find_all("dl")

  for item in items:
    title = item.find("dt").get_text()
    desc = item.find("div", class_="desc")
    print('\r\n%s' % title, '\n\r\t%s' % desc.get_text().strip())
