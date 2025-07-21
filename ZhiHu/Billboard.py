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
    'Cookie': '_xsrf=sHUJiCNw433TP8JWeGwBuH8m6P9e23rg; _zap=a4d60fe1-724a-4ff1-a7e1-7671bc9966c8; d_c0=AAAScU_xARqPTqLlzjwIYBJGOGsANhNePNY=|1739586965; q_c1=fa0db57489034c4caa440cae3f486618|1743410282000|1743410282000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1750662082,1752473685; HMACCOUNT=E34CE8E06DC2A079; __zse_ck=004_z3IDUPO9OuejO4stBVRKkNPYTGhTiMl/XKD6XtNIu3g2Ik1ZEhyxljmlT9Zw6v6OCb4SV8/mQ3GLHIQMcQXodlJUeyw6Gfbi=ubeRLeP6OkqnGRpWk/S5gIdswBaAQH1-eLKiB7dr3GaBtdn6/S7c6sZs80AgMV10uKKeHyL7E4frr9JW7woM/5mfiG7JGGrYjz4+VAuQTfpS4CoSq+mVZiTo+PgW4Sf+o1uUKBI4evUpI1mRNHF3LczfZPn+btrP; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1753095559; SESSIONID=nHaej8y3ffXqJBXNNwrkClKMKncWzOv9LugJxRegbaC; z_c0=2|1:0|10:1753095558|4:z_c0|80:MS4xR0ZkbUFnQUFBQUFtQUFBQVlBSlZUWVpyYTJrTEVPbEhJRFptVk43RkY4ZEtyRGRsMGVPbTNRPT0=|6bebd07d7e8643904d65ad6ede56e5ec7e53d17cce65e4197fcc34fa9cbb13a2; JOID=UFkRC0LMpAJ1KtgHZsac1kB3Iw56oelvEUvje1mhwV8IYZFcLU2wcRci3g5r9xztW4LTjyX-K6QtPBtVTXJhvXY=; osd=VV8dC0rJog51It0BasaU00Z7IwZ_p-VvGU7ld1mpxFkEYZlZK0GweRIk0g5j8hrhW4rWiSn-I6ErMBtdSHRtvX4=; BEC=7e33fec1f95d805b0b89c2974da3470f'
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
