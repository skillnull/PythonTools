import requests
from bs4 import BeautifulSoup

# 登录URL
LOGIN_URL = 'https://www.zhihu.com/login/phone_num'
# 知乎首页
HOME_URL = 'https://www.zhihu.com/'

# 用户输入的手机号和密码
phone_num = input('手机号码：')
password = input('密码：')

def get_data(url):
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'refer': 'https://www.zhihu.com'
  }

  try:
    res = requests.get(url, headers=headers)
    res.encoding = res.apparent_encoding
    res.raise_for_status()
    return res
  except requests.HTTPError as e:
    print("HTTPError", e)
  except requests.RequestException as e:
    print(e)

def home():
  url = 'https://www.zhihu.com/'
  data = get_data(url)
  html = BeautifulSoup(data.text, 'lxml')
  print(html)
