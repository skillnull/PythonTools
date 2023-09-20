import time
from tqdm import tqdm
import requests
import multiprocessing
import pandas as pd
import os


def file_download(arr, ele, sheet):
  for item in tqdm(arr):
    if not pd.isna(item):
      path_arr = item.lstrip('https://').split('/')
      path = ''
      for idx, path_str in enumerate(path_arr):
        if idx < len(path_arr) - 1:
          path += rf'/{path_str}'
      file = path_arr[len(path_arr) - 1]
      file_arr = file.split('.')
      filetype = file_arr[len(file_arr) - 1]
      filename = file.rstrip(rf'.{filetype}')

      os.makedirs(rf'./PythonTools/FileHandler/{sheet}/{ele}/{path}', mode=0o777, exist_ok=True)

      res = requests.get(item, headers={'Connection': 'close'}, verify=True)

      with open(rf'./PythonTools/FileHandler/{sheet}/{ele}/{path}/{filename}.{filetype}', 'wb') as file:
        file.write(res.content)

    time.sleep(0.1)



def readAndDownload(file, sheet):
  excel_sheet = pd.read_excel(rf'{file}', sheet_name=rf'{sheet}')
  # 获取第一行
  columns = excel_sheet.columns.values.tolist()
  json_sheet = {}

  for column in columns:
    arr = []
    for index, item in excel_sheet.iterrows():
      arr.append(item[column])
    json_sheet[column] = arr

  for ele in json_sheet:
    p = multiprocessing.Process(target=file_download, args=(json_sheet[ele], ele, sheet))
    p.start()
    p.join()
    time.sleep(1)


def excel():
  file = input('请输入Excel路径:') or ''
  sheet = input('请输入要读取的Sheet:') or ''
  readAndDownload(file, sheet)
