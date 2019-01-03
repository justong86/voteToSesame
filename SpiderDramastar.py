# -*- coding:utf-8 -*-
#!/usr/bin/env python3
import time

import requests,os,csv,datetime
import pandas as pd
from numpy import unicode
from bs4 import BeautifulSoup

header={
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Host": "t.dramastar.org",
}

path = './star'
file_name =path + '/all_info.csv'
# 将解析好的list存入文件
def file_do(list_info):
    if not os.path.isdir(path):
        os.makedirs(path)
    if not os.path.exists(file_name):
        with open(file_name, 'a', encoding='utf-8') as f:
            f.write('')

    file_size = os.path.getsize(file_name)
    if file_size == 0:
        # 建立文件格式dataframe对象
        name = ['时间', '姓名', '地址', '票数']
        file_test = pd.DataFrame(data=list_info, columns=name)
        # 数据写入
        file_test.to_csv(file_name, encoding='utf-8', index=False)
    else:
        with open(file_name, 'a+', encoding='utf-8', newline='') as file_test:
            # 追加到文件后面
            writer = csv.writer(file_test)
            writer.writerows(list_info)

def spider_one(id):
    url_web="http://t.dramastar.org/{}.html".format(id)
    response_web=requests.get(url=url_web,headers=header)
    soup = BeautifulSoup(response_web.text,'html.parser')
    sp_div = soup.find('div',class_ = 'teacher_info_yc')
    # print(sp_div)
    sp_li = sp_div.find_all('li',limit=3)
    # print(sp_li)
    name = unicode(sp_li[1].string)
    # print("姓名：%s" % name)
    addr = unicode(sp_li[2].string)
    # print("地点：%s" % addr)
    votes = unicode(sp_div.span.string)
    # print("票数：%s" % votes)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    type(now)
    list_one = [now,name,addr,votes]
    return list_one

if __name__ == '__main__':
    while(True):
        list_all = []
        for id in range(1,862):
            list_one = spider_one(id)
            list_all.append(list_one)
        # print(list_all)
        file_do(list_all)
        time.sleep(3600)


