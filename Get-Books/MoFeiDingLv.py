#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 获取在线文本内容

import requests
from bs4 import BeautifulSoup
import re
import codecs

url = 'https://www.shuhaige.com/7518/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'Origin': 'https://www.shuhaige.com',
    'Host': 'www.shuhaige.com'
}
# 设置代理服务器
proxies = {
    'http:': 'http://121.232.146.184',
    'https:': 'https://144.255.48.197'
}


def getContent():
    contents = requests.get(url, headers=header).text
    html = BeautifulSoup(contents, 'html.parser')
    lists = html.select('dl')[0].select('a')
    for list in lists:
        itemUrl = f'https://www.shuhaige.com{list["href"]}'
        itemContent = requests.get(itemUrl, headers=header).text
        itemHtml = BeautifulSoup(itemContent, 'html.parser')
        saveToTxt(itemHtml.select('div .content')[0], list.string)


# 写入文本文件
def saveToTxt(comments, title):
    commentsList = ''
    for item in comments:
        comment_info = f'{item}'.replace(f'<br/>', '')
        comment_info = re.sub(f'<p>.*</p>', '', comment_info)
        commentsList += comment_info
    with codecs.open(f'MoFeiDingLv/{title}.txt', 'w', encoding='utf-8') as file:
        file.writelines(commentsList)

    print(f'{title}写入文件成功!')


if __name__ == '__main__':
    getContent()
