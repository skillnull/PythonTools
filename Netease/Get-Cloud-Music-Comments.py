#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 获取网易云音乐评论

import base64
import codecs
import json
import requests
import time
from Crypto.Cipher import AES
import multiprocessing  # 多进程
import os

# 感谢你曾来过 460578140
id = input('请输入歌曲ID:')
name = input('请输入歌曲名称:')

url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_551816010?csrf_token='
header = {
    'Host': 'music.163.com',
    'Origin': 'http://music.163.com',
    'Referer': f'http://music.163.com/song?id={id}',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7'
}
# 设置代理服务器
proxies = {
    'http:': 'http://121.232.146.184',
    'https:': 'https://144.255.48.197'
}
# rid 是歌曲的 id 标志 offset是控制翻页的标志
first_param = ''
second_param = '010001'
third_param = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa' \
              '76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee' \
              '255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
forth_param = b'0CoJUm6Qyw8W8jud'
# params 需要第一个和第四个参数 encSecKey需要一个随机的16位字符串和第二个和第三个参数
strw = 'S' * 16


# aes加密
def aesEncrypt(text, key):
    iv = b'0102030405060708'  # 偏移量
    pad = 16 - len(text) % 16  # 使加密信息的长度为16的倍数
    tt = pad * chr(pad)  # 返回整数i对应的ASCII字符
    text = text + tt.encode('utf-8')
    encrpyptor = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = base64.b64encode(encrpyptor.encrypt(text))
    return cipher_text


# rsa加密
def rsaEncrypt(pubkey, text, mouduls):
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubkey, 16) % int(mouduls, 16)
    return format(rs, 'x').zfill(256)


# 获取aes加密参数
def get_aes_params(text):
    if text == 1:
        first_param = b'{"rid":"", "offset":"0", "total":"true", "limit":"20", "csrf_token":""}'
        params = aesEncrypt(first_param, forth_param)
    else:
        offset = str((text - 1) * 20)
        first_param = b'{"rid":"", "offset":"%b", "total":"false", "limit":"20", "csrf_token":""}' % offset.encode('utf-8')
        params = aesEncrypt(first_param, forth_param)
    # print(f'params的随机值是:{params} ')
    params = aesEncrypt(params, strw.encode('utf-8'))
    # print(f'第二次加密后的随机值是：{params}')
    return params


# 获取rsa加密参数
def get_rsa_params(text):
    encseckey = rsaEncrypt(second_param, text, third_param)
    return encseckey


def get_json(url, pm, esk):
    form_data = {
        'params': pm,
        'encSecKey': esk
    }
    json_text = requests.post(url, headers=header, data=form_data).text
    return json_text


# 抓取一首歌的全部评论
def get_all_comment(url):
    params = get_aes_params(1)
    encSecKey = get_rsa_params(strw)
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])

    if comments_num % 20 == 0:
        page = comments_num / 20
    else:
        page = int(comments_num / 20) + 1

    print(f'共有{comments_num}条,{page}页评论!')

    os.makedirs('musicComments', mode=0o777, exist_ok=True)  # 创建文件夹目录

    handler_comments(range(page))


# 处理抓取到的评论
def handler_comments(comments):
    p = multiprocessing.Process(target=save_to_html, args=(comments,))
    p.start()
    p = multiprocessing.Process(target=save_to_txt, args=(comments,))
    p.start()

    p.join()


# 将评论存储为html
def save_to_html(comments):
    with codecs.open('musicComments/output.html', 'w') as file:
        file.write(f'<html>')  # 设置输出的html文件的格式
        file.write(f'<head>')
        file.write(f'<meta charset="utf-8">')
        file.write(f'<title>{name}</title>')
        file.write(f'</head>')
        file.write(f'<body>')
        file.write(f'<table style="font-size:12px;font-weight:300;">')
        file.write(f'<thead>')
        file.write(f'<tr>')
        file.write(f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">评论者id</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">头像</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">昵称</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">评论内容</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">点赞总数</td>')
        file.write(f'</tr>')
        file.write(f'</thead>')
        for i in comments:  # 逐页抓取
            params = get_aes_params(i + 1)
            encSecKey = get_rsa_params(strw)
            json_text = get_json(url, params, encSecKey)
            json_dict = json.loads(json_text)
            for item in json_dict['comments']:
                userID = item['user']['userId']  # 评论者id
                nickname = item['user']['nickname']  # 昵称
                comment = item['content']  # 评论内容
                likedCount = item['likedCount']  # 点赞总数
                avatar = item['user']['avatarUrl']  # 头像
                file.write(f'<tr>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{userID}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;"><img src="{avatar}" width="50" height="50" /></td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{nickname}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{comment}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{likedCount}</td>')
                file.write(f'</tr>')
        file.write(f'</table>')
        file.write(f'</body>')
        file.write(f'</html>')


# 将评论写入文本文件
def save_to_txt(comments):
    with codecs.open(f'musicComments/{name}.txt', 'w', encoding='utf-8') as file:
        for i in comments:  # 逐页抓取
            commentsList = ''
            params = get_aes_params(i + 1)
            encSecKey = get_rsa_params(strw)
            json_text = get_json(url, params, encSecKey)
            json_dict = json.loads(json_text)
            for item in json_dict['comments']:
                comment = item['content']  # 评论内容
                nickname = item['user']['nickname']  # 昵称
                userID = item['user']['userId']  # 评论者id
                likedCount = item['likedCount']  # 点赞总数
                comment_info = f'{userID} | {nickname} | {comment} | {likedCount}'.replace('\r', '').replace('\n', '')
                comment_info += f'\r\n-----------------------------------------------------\r\n'
                commentsList += comment_info
            print(f'第{i + 1}页抓取完毕!')
            file.writelines(commentsList)
            print("写入文件成功!")


if __name__ == '__main__':
    start_time = time.time()  # 开始时间
    get_all_comment(url)
    end_time = time.time()  # 结束时间
    print(f'程序耗时{end_time - start_time}秒')
