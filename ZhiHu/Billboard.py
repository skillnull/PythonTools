# 知乎热榜

import requests
from bs4 import BeautifulSoup

def billboard():
  url = 'https://www.zhihu.com/billboard'
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'lxml')
  titles = soup.find_all('div', class_='HotList-itemTitle')

  for title in titles:
    print(title.text)