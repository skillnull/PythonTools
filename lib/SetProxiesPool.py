#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# IP地址取自：http://www.xicidaili.com/nn/  仅爬取首页IP地址

import random
import urllib

import requests
from bs4 import BeautifulSoup

url = 'http://www.xicidaili.com/nn/'
header = {
    'Host': 'www.xicidaili.com',
    'Origin': 'http://www.xicidaili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'keep-alive',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,da;q=0.7'
}


def get_ip_list(url):
    web_data = requests.get(url, headers=header)
    soup = BeautifulSoup(web_data.text, 'html.parser')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    # 检测ip可用性，移除不可用ip：（这里其实总会出问题，你移除的ip可能只是暂时不能用，剩下的ip使用一次后可能之后也未必能用）
    for ip in ip_list:
        try:
            proxy_host = "https://" + ip
            proxy_temp = {"https": proxy_host}
            res = urllib.urlopen(url, proxies=proxy_temp).read()
        except Exception as e:
            ip_list.remove(ip)
            continue
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


if __name__ == '__main__':
    ip_list = get_ip_list(url)
    proxies = get_random_ip(ip_list)
