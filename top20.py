# -*- coding:utf-8 -*-
#!/usr/bin/env python3
import os

import requests
import bs4
import time
import re
import datetime
from numpy import unicode

header={
    "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36",
    "Host": "t.dramastar.org",
}

def get_top():
    url='http://t.dramastar.org/zlist.php'
    response_url = requests.get(url)
    if response_url.status_code == 200:
        soup = bs4.BeautifulSoup(response_url.text,"html.parser")
        data = soup.body.find_all('ul')
        data_compile = re.compile(r'<ul><li>(\w+)</li><li>(\w+)</li><li>(\d+)</li></ul>')  # 匹配端口
        tops = re.findall(data_compile, str(data))
        top1_name =tops[0][0]
        top1_num = tops[0][2]
        if top1_name == "张三":
            top1_name = tops[1][0]
            top1_num = tops[1][2]
        print("第一竞争者：%s,票数:%s" % (top1_name ,top1_num))
        os.system("echo '第一竞争者：%s,票数:%s' >> log.txt" % (top1_name, top1_num))
        return top1_num
    time.sleep(5)
    get_top()
# 改进了上面的方法，可以指定监控的名次，默认第一名
def get_top2(i = 1):
    url='http://t.dramastar.org/zlist.php'
    response_url = requests.get(url)
    if response_url.status_code == 200:
        soup = bs4.BeautifulSoup(response_url.text,"html.parser")
        data = soup.body.find_all('ul')
        data_compile = re.compile(r'<ul><li>(\w+)</li><li>(\w+)</li><li>(\d+)</li></ul>')  # 匹配端口
        tops = re.findall(data_compile, str(data))
        top2_name =tops[i-1][0]
        top2_num = tops[i-1][2]
        # 这里要排除自己的名字，要不然自己跟自己挣就没意思了        
        if top2_name == "张三":
            top2_name = tops[i][0]
            top2_num = tops[i][2]
        print("第%s竞争者：%s,票数:%s" % (i,top2_name ,top2_num))
        os.system("echo '第%s竞争者：%s,票数:%s' >> log.txt" % (i,top2_name, top2_num))
        return top2_num
    time.sleep(5)
    get_top()

# 获取指定ID的得票情况，其实是从SpiderDSS.py里拿出来的方法
def spider_one(id):
    url_web="http://????????????.org/{}.html".format(id)
    response_web=requests.get(url=url_web,headers=header)
    soup = bs4.BeautifulSoup(response_web.text,'html.parser')
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
    list_one = [now,name,addr,votes]
    print(list_one)
    os.system("echo '时间：%s,我的票数:%s' >> log.txt" % (now, votes))
    return list_one

if __name__ == '__main__':
    get_top()

