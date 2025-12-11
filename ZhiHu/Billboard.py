#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 知乎热榜

import requests
from bs4 import BeautifulSoup
import json

def billboard():
  url = 'https://www.zhihu.com/billboard'
  headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G950U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
    'Cookie': 'srf=sHUJiCNw433TP8JWeGwBuH8m6P9e23rg; _zap=a4d60fe1-724a-4ff1-a7e1-7671bc9966c8; d_c0=AAAScU_xARqPTqLlzjwIYBJGOGsANhNePNY=|1739586965; q_c1=fa0db57489034c4caa440cae3f486618|1743410282000|1743410282000; HMACCOUNT=E34CE8E06DC2A079; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1755503916; __zse_ck=004_OGOj5BgLr/2QHd/3Lv2jaVY2o0ICFpWcDdZEAWuN2VuO9YrWd1E3V4NkSwOVfwN2iyElOlEnK1BwK/ygKMhj=af3kgEvTJ4VVyLlFr2VRgKNrReom2qedlrwt6zXgtHS-7TpBnD7D5PF5rctieuY9gxt70TrSkqWSkM0EnEK+Qd6QNFWB+5bWZrFn+xvgR2bd5NsHkvdDFOLQrDu5AcERAYBaTzKgPYBPibU8O3L6wXuwr/mWLHKSudfJvAo3AB1i; tst=r; SESSIONID=m1UOriomvF6PVGamarxmI7kpR6gCn4SYUHSnbqaYY0p; JOID=W1AXC04Ukfx7zg1SEBWsJUeZ_V4BeKqjObBlN3du1sAhlUYyd7stPBLDBlIX0PAaIZVoicIadptLHaj8uiDpqlk=; osd=WlgXBE4Vmfx0zgxaEBqsJE-Z8l4AcKqsObFtN3hu18ghmkYzf7siPBPLBl0X0fgaLpVpgcIVdppDHaf8uyjppVk=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1757920432; z_c0=2|1:0|10:1757920434|4:z_c0|80:MS4xR0ZkbUFnQUFBQUFtQUFBQVlBSlZUYzBCckdubkVFdy1QRTBsNFM2a1hFaWdmUFhNMGJJcGF3PT0=|9ae71f9278519581802f7ea7f90404f43f5861606a3b5fafca995ca3d748b667; BEC=eee8906a1fecdebcee3fda89d6b84517'
  }
  res = requests.get(url, headers=headers)
  html = BeautifulSoup(res.text, 'lxml')
  data = html.find('script',id='js-initialData').get_text()
  hotList = json.loads(data)['initialState']['topstory']['hotList']
  # print(json.dumps(hotList, indent=2, ensure_ascii=False))

  for item in hotList:
    print(item['target']['imageArea']['url'])
    print(item['target']['link']['url'])
    print(item['target']['titleArea']['text'])
    print('\r\n\t--------', item['target']['excerptArea']['text'], '\r\n')
