# 知乎热榜

import requests
from bs4 import BeautifulSoup
import json

def billboard():
  url = 'https://www.zhihu.com/billboard'
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'lxml')
  data = soup.find('script',id='js-initialData').get_text()
  hotList = json.loads(data)['initialState']['topstory']['hotList']
  # print(json.dumps(hotList, indent=2, ensure_ascii=False))

  for item in hotList:
    print(item['target']['titleArea']['text'])
    print('\r\n\t--------', item['target']['excerptArea']['text'], '\r\n')