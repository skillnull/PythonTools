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
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Cookie': '_xsrf=sHUJiCNw433TP8JWeGwBuH8m6P9e23rg; _zap=a4d60fe1-724a-4ff1-a7e1-7671bc9966c8; d_c0=AAAScU_xARqPTqLlzjwIYBJGOGsANhNePNY=|1739586965; HMACCOUNT=E34CE8E06DC2A079; q_c1=fa0db57489034c4caa440cae3f486618|1743410282000|1743410282000; z_c0=2|1:0|10:1745301492|4:z_c0|80:MS4xR0ZkbUFnQUFBQUFtQUFBQVlBSlZUZlI5OUdoX29FRlZLWU80MUhRV3JQWnlfRzV6ZnV0SnpBPT0=|20f2f3458f09c7830d0fae1fb7ffe6ad40a5fc2e180706db7fe812140d585692; tst=r; __zse_ck=004_NKqoEtUKkl=uDbeZ1yhBFZJwN=lpK35ot8N2HyJ=RsLSuk4Qt=J031OKD62FyImAZr0qTFwW/7hr/aLUDlncEBY989uo4OQSrXqSgQCfZALoGZnNRI0tj4uuFHGUUXpb-AQbn1M3XUZ4tJYlqJnI+oeGufA/Df6lJQ37TbbdKVdBwHgombXTBrU8prG0uoAEdIIBeNt0skeVrKP75zdUK+kT0YWkGAlFqGV1Im2FcnC87378hItOGDyarKZ58ihCt; SESSIONID=xEotaBEEMcHqcCh3MOS0XuMPsodWY6VDfAFDQmFnnPr; JOID=UVEcAE3Y12NN1Wh-CNjou3uKmXAYqpIGPLEgO0eQvis2sy4cO1JKfSXaYnQHfEfSnBimk7fYZ-Bs_wPCRgI74Zg=; osd=UVkSBErY321J0mh2Btzvu3OEnXcYopwCO7EoNUOXviM4tykcM1xOeiXSbHAAfE_cmB-mm7ncYOBk8QfFRgo15Z8=; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1745983374; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1745983374; BEC=4da336ae0b6517487a94031e0c3cbd90'
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
