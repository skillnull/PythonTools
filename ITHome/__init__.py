#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function IT之家

import requests
from bs4 import BeautifulSoup

def main():
  url = 'https://www.ithome.com'
  res = requests.get(url)
  res.encoding = "utf-8"
  html = BeautifulSoup(res.text, "lxml")
  nnews = html.find('div', id='nnews').find('div', class_="t-b sel clearfix").find_all("li")

  for item in nnews:
    text = item.find("a").get_text()
    href = item.find("a")["href"]
    time = item.find("b")
    ad = item.find("b", class_="ad")
    if time and ad is None:
      print('\r\n%s' % href, '\t', time.get_text())
      print('%s' % text)

if __name__ == '__main__':
  main()