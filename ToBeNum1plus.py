# -*- coding:utf-8 -*-
#!/usr/bin/env python3
import random
import sys,os
from random import choice
import top20
import time
import requests
import datetime
import threading

votes=0
lock = threading.Lock()
uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]


def get_ip_fromkuaidaili(num = 100):
    """获取代理IP256163982446923610"""
    api_url = "http://dev.kdlapi.com/api/getproxy/?orderid=984484686189625&num={}&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_tr=1&an_an=1&an_ha=1&dedup=1&sep=1".format(num)
    response_api= requests.get(api_url)
    # print(response_api.status_code)  # 获取Reponse的返回码
    r_html = response_api.text
    # print(response_api.text)
    if  response_api.status_code != 200:
        print("获取IP失败，正在重试")
        time.sleep(15)
        get_ip_fromkuaidaili()
    if ('ERROR' in r_html):
        print(r_html)
        time.sleep(90)
        get_ip_fromkuaidaili()
    new_ips = r_html.splitlines()
    return new_ips

def get_url(code=0,ips=[],tids=['838',]):
    """        投票    """
    global votes
    try:
        ip = choice(ips)
        lock.acquire()
        try:
            ips.remove(ip)
        finally:
            lock.release()
    except Exception as e:
        print("choice(ips)异常%s" % e)
        return False
    else:
        proxies = {
            "http":ip,
        }
        headers2 = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                        "Accept-Encoding":"gzip, deflate, sdch",
                        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                        "Referer":"",
                        "User-Agent":choice(uas),
                        }
    try:
        # num = random.uniform(0,1)
        hz_url = "http://????????????/ajax/add_zan.php"   # 某投票网站的地址
        for tid in tids:
            hz_r = requests.post(hz_url,headers=headers2,data = {'tid':tid},proxies=proxies,timeout=20)
            time.sleep(0.3)
        status = str(hz_r.json()['result'])
    except requests.exceptions.RequestException as e:
        # print(e)
        if not ips:
            print("not ip")
            sys.exit()
    except Exception as e:
        pass
        # print(e)
    # else:
    #     if status == 'True':
    #         votes += 1
        # date = datetime.datetime.now().strftime('%H:%M:%S')
        # print(u"第%s次 [%s] [%s]：投票%s ,累计%s,(剩余可用代理IP数：%s)" % (code,date,ip,status,votes,len(ips)))

# 监控得票差距，发送任务
def goworking(vote_num):
    print("我要拉%s票"% vote_num)
    pers = []
    ips = []
    while (vote_num > 200):
        # 每次拉取的数量！！！！！！！！！！！！！
        pers.append(200)
        vote_num = vote_num - 200
    pers.append(vote_num)

    for per in pers:
        new_ips = get_ip_fromkuaidaili(per)
        lock.acquire()
        try:
            ips.extend(new_ips)
        finally:
            lock.release()

        print("获得IP地址%s条"% len(ips))
        for i in range(len(ips)):
            # 启用线程，隔1秒产生一个线程，可控制时间加快投票速度 ,time.sleep的最小单位是毫秒
            # print("开始第%s次post请求" % i)
            # t2 = threading.Thread(target=get_url, args=(i, ips, ['836', '837', '840', '440', '444']))
            t2 = threading.Thread(target=get_url, args=(i, ips,['838',]))
            t2.start()
            time.sleep(0.1)

if __name__ == '__main__':
    while(True):
        top1_num = int(top20.get_top())
        top1_num = int(top20.get_top2(3))
        me_num = int(top20.spider_one(838)[3])
        print("敌人票数%s" % top1_num)
        print("我的票数%s" % me_num)
        os.system("echo ")
        req_num = int(me_num) - int(top1_num)
        print("距离第一差%s票(正表示我比别人多)" % req_num)
        # 输入目标，正数表示位居第一，超越后来者N票。负数表示比第一少N票，位居第二
        goal = 800
        # 发送拉票请求
        vote_num = int((goal + top1_num - me_num) * 1.2)
        if vote_num > 1500:
            goworking(1500)
        elif vote_num > 10:
            goworking(vote_num)
        elif vote_num > 0:
            goworking(10)
        # 每3分钟监控一次
        print("-"*25+"一轮结束了"+"-"*25)
        time.sleep(180)
    # goworking(1000)