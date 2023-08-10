#!/usr/local/bin/python3.9
# -*- coding: utf-8 -*-
# @Author skillnull
# @Function 获取网易云音乐评论

import os
import random
import sys
import json
import time
import base64
import codecs
import requests
import multiprocessing  # 多进程
from Crypto.Cipher import AES

import re  # 正则表达式库
import numpy as np  # numpy数据处理库
import collections  # 词频统计库
import wordcloud  # 词云展示库
import jieba  # 结巴分词
import matplotlib.pyplot as plt
from PIL import Image  # 图像处理库

ID = input('请输入歌曲ID:')
name = input('请输入歌曲名称:')

url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_551816010?csrf_token='
header = {
    'Host': 'music.163.com',
    'Origin': 'https://music.163.com',
    'Referer': f'https://music.163.com/song?id={ID}',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7'
}
print(header)
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
        first_param = b'{"rid":"", "offset":"%b", "total":"false", "limit":"20", "csrf_token":""}' % offset.encode(
            'utf-8')
        params = aesEncrypt(first_param, forth_param)
    # print(f'params的随机值是:{params} ')
    params = aesEncrypt(params, strw.encode('utf-8'))
    # print(f'第二次加密后的随机值是：{params}')
    return params


# 获取rsa加密参数
def get_rsa_params(text):
    encseckey = rsaEncrypt(second_param, text, third_param)
    return encseckey


# 抓取评论
def get_json(url, pm, esk):
    form_data = {
        'params': pm,
        'encSecKey': esk
    }
    json_text = requests.post(url, headers=header, data=form_data)
    return json_text.text


# 解析评论
def get_all_comment(url):
    params = get_aes_params(1)
    encSecKey = get_rsa_params(strw)
    json_text = get_json(url, params, encSecKey)
    json_dict = json.loads(json_text)
    comments_num = int(json_dict['total'])

    if comments_num % 20 == 0:
        page = comments_num // 20
    else:
        page = int(comments_num // 20) + 1

    print(f'共有{comments_num}条,{page}页评论!')

    os.makedirs(f'musicComments/{ID}', mode=0o777, exist_ok=True)  # 创建歌曲文件夹目录

    get_page = input(f'获取多少页评论,最多{page}页:')
    int_get_page = int(get_page)
    if page > int_get_page:
        handler_comments(range(int_get_page))
    else:
        handler_comments(range(page))


# 处理解析后的评论
def handler_comments(comments):
    p = multiprocessing.Process(target=save_to_html, args=(comments,))
    p.start()
    p.join()

    time.sleep(3)

    p = multiprocessing.Process(target=save_to_txt, args=(comments,))
    p.start()
    p.join()


# 将评论存储为html
def save_to_html(comments):
    print(f'抓取{comments}页')
    with codecs.open(f'musicComments/{ID}/{ID}.html', 'w') as file:
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
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">点赞总数</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">评论时间</td>'
                   f'<td style="min-width:65px;border: 1px solid #f4f4f4;padding: 5px;">IP属地</td>'
                   )
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
                TIME = item['time']
                if len(f'{item["time"]}') == 13:
                    TIME = float(TIME / 1000)
                _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(TIME))  # 评论时间
                likedCount = item['likedCount']  # 点赞总数
                location = item['ipLocation']['location']  # IP属地
                avatar = item['user']['avatarUrl']  # 头像
                file.write(f'<tr>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{userID}</td>')
                file.write(
                    f'<td style="border: 1px solid #f4f4f4;padding: 5px;"><img src="{avatar}" width="50" height="50" /></td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{nickname}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{comment}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{likedCount}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{_time}</td>')
                file.write(f'<td style="border: 1px solid #f4f4f4;padding: 5px;">{location}</td>')
                file.write(f'</tr>')
                sleeptime = random.randint(0, 2)
                time.sleep(sleeptime)
        file.write(f'</table>')
        file.write(f'</body>')
        file.write(f'</html>')


# 将评论写入文本文件
def save_to_txt(comments):
    print(f'抓取{comments}页')
    with codecs.open(f'musicComments/{ID}/{name}.txt', 'w', encoding='utf-8') as file:
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
                TIME = item['time']
                if len(f'{item["time"]}') == 13:
                    TIME = float(TIME / 1000)
                _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(TIME))  # 评论时间
                location = item['ipLocation']['location']  # IP属地
                comment_info = f'{userID} | {nickname} | {comment} | {likedCount} | {_time} | {location}'.replace('\r',
                                                                                                                  '').replace(
                    '\n', '')
                comment_info += f'\r\n-----------------------------------------------------\r\n'
                commentsList += comment_info
            file.writelines(commentsList)
            sleeptime = random.randint(0, 3)
            time.sleep(sleeptime)
            print(f'第{i + 1}页写入文件成功!')
    get_wordcloud()


# 生成词云
def get_wordcloud():
    # 读取文件
    fn = open(f'musicComments/{ID}/{name}.txt', encoding="utf-8")  # 打开文件
    string_data = fn.read()  # 读出整个文件
    fn.close()  # 关闭文件

    # 文本预处理
    pattern = re.compile(u'\t|\n|\.|-|:|;|\||\)|\(|\?|\？|"')  # 定义正则表达式匹配模式
    string_data = re.sub(pattern, '', string_data)  # 将符合模式的字符去除

    # 文本分词
    seg_list_exact = jieba.cut(string_data, cut_all=False)  # 精确模式分词
    object_list = []
    # 自定义去除词库
    remove_words = [
        f'在', f'了', f'通常', f'如果', f'我们', f'需要', f'的', f'，', f'和', f'是', f'随着', f'对于', f'对', f'等',
        f'能', f'都', f'。', f' ', f'、', f'中', f'1', f'2', f'3', f'4', f'5', f'6', f'7', f'8', f'9', f'0', f'2023'
    ]

    for word in seg_list_exact:  # 循环读出每个分词
        if word not in remove_words:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表

    # 词频统计
    word_counts = collections.Counter(object_list)  # 对分词做词频统计
    word_counts_top = word_counts.most_common(50)  # 获取高频的词
    print(word_counts_top)  # 输出检查

    # 词频展示
    mask = np.array(Image.open('musicComments/wordcloud_bg.jpg'))  # 定义词频背景
    wc = wordcloud.WordCloud(
        font_path='/System/Library/fonts/PingFang.ttc',  # 设置字体格式
        mask=mask,  # 设置背景图
        background_color="white",
        mode="RGBA",  # 当参数为“RGBA”并且background_color不为空时，背景为透明
        max_words=500,  # 最多显示词数
        max_font_size=90,  # 字体最大值
        scale=1
    )

    wc.generate_from_frequencies(word_counts)  # 从字典生成词云
    image_colors = wordcloud.ImageColorGenerator(mask)  # 从背景图建立颜色方案
    wc.recolor(color_func=image_colors)  # 将词云颜色设置为背景图方案
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    # plt.savefig(f'musicComments/{id}/{name}.png', dpi=200)
    plt.show()
    wc.to_file(f'musicComments/{ID}/{name}.png')


if __name__ == '__main__':
    start_time = time.time()  # 开始时间
    get_all_comment(url)
    end_time = time.time()  # 结束时间
    print(f'程序耗时{end_time - start_time}秒')
