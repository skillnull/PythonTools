import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from BaiduHot import BaiduHot

fun_type = ''

def main(skip_tips):
  opt = Options()
  opt.add_argument('--headless')
  opt.add_argument('--disable-gpu')
  # 本地 chromedriver
  service = Service('/Users/macadmin/Public/chromedriver')
  web = Chrome(service=service, options=opt)
  web.get('https://www.baidu.com')

  global fun_type

  if not skip_tips:
    print('==================')
    print('=== 1.百度热搜  ===')
    print('=== 2.百度搜索  ===')
    print('==================')
    fun_type = input('请输入对应编号选择功能：')

  if fun_type == '1':
    BaiduHot(web.page_source)
  elif fun_type == '2':
    search_input = web.find_element(By.ID, 'kw')
    search_btn = web.find_element(By.ID, 'su')
    search_input.clear()
    search_input_value = input('\r\n请输入搜索内容：')
    search_input.send_keys(search_input_value)
    search_btn.send_keys(Keys.ENTER)
    time.sleep(1)
    print(web.title)
  else:
    fun_type = '1'
    main(True)

  web.close()

if __name__ == '__main__':
  main(False)