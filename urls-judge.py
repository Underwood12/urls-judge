# -*- coding: UTF-8 -*-
import asyncio
import aiohttp
import time
import re
import difflib
import argparse
import os
from bs4 import BeautifulSoup

start = time.time()
lines = []
urls = []
reset = set()
e_list = set()
c_list = set()
a_list = set()
other_list = set()
b_list = set()
d_list = set()


async def get(url, sem):
    async with sem:
        try:
            async with aiohttp.ClientSession() as session:          # 访问不存在的目录页面
                async with session.get(url=url, allow_redirects=False, verify_ssl=False, timeout=15) as resp:
                    text = await resp.text(errors='ignore')
                    status = resp.status
                    url2 = url.strip('/booksiyi/')
                    async with session.get(url=url2, allow_redirects=False, verify_ssl=False, timeout=15) as resp2:
                        status2 = resp2.status
                        text2 = await resp2.text(errors='ignore')
                        soup = BeautifulSoup(text2, 'html.parser')
                        title = str(soup.find('title'))
                        title = title.strip('</title>')
                        title = title.replace('\t', '').replace('\n', '').replace('\r', '')
                        if '=' in title:
                            title = re.search('>.+</title>', text2)
                            if title:
                                title = title.group()
                                title = title.strip('>').strip('</title')
                    if status == 404:
                        print(url + "\t%d\t不存在的目录页面正常" % status)
                        if status2 in [200, 301, 302, 303, 304, 307, 508, 401]:
                            print(url2 + "\t状态码：%d\t首页正常" % status2)
                            a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 in [403]:
                            print(url2 + "\t状态码：%d\t首页非正常" % status2)
                            b_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 in [404, 500]:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        # elif status2 in [501, 502, 503, 504]:
                        #     d_list.append(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add('404\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status == 400:
                        if status2 == 400:
                            if url2.startswith('http://'):
                                url3 = url2.replace('http://', 'https://')
                                async with session.get(url=url3, allow_redirects=False, verify_ssl=False, timeout=15) as resp3:
                                    status3 = resp3.status
                                    text3 = await resp3.text(errors='ignore')
                                    soup2 = BeautifulSoup(text3, 'html.parser')
                                    title2 = str(soup2.find('title'))
                                    title2 = title2.strip('</title>')
                                    title2 = title2.replace('\t', '').replace('\n', '').replace('\r', '')
                                    if '=' in title2:
                                        title2 = re.search('>.+</title>', text3)
                                        if title2:
                                            title2 = title2.group()
                                            title2 = title2.strip('>').strip('</title')
                                    c_list.add(url2 + "\t%d\t%s\n" % (status3, title2))
                            else:
                                c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 in [200, 301, 302, 303, 304, 307, 401]:
                            a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        # elif status2 in [403, 404, 500]:
                        #     c_list.append(url2 + "\t%d\t%s\n" % (status2, title))
                        # elif status2 in [501, 502, 503, 504]:
                        #     d_list.append(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            print("其他情况:%s\t%d\t%s\n" % (url2, status2, title))
                            other_list.add('400\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status == 500:
                        if status2 in [200, 500]:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add('500\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status == 403:
                        if status2 in [200, 304, 404, 403, 400]:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add('403\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status in [501, 502, 503, 504]:
                        if status2 == status:
                            for i in range(3):
                                async with session.get(url=url2, allow_redirects=False, verify_ssl=False, timeout=15,
                                                       ) as resp3:
                                    status3 = resp3.status
                                    if status3 != status2:
                                        other_list.add('其他5XX\t' + url2 + "\t%d\t%s\n" % (status2, title))
                                        break
                            if status3 == status2:
                                d_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 == 403:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add('5XX\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status == 200:
                        if status2 in [301, 302, 303, 304, 307]:
                            async with session.get(url=url2, verify_ssl=False, timeout=15) as resp3:
                                status3 = resp3.status
                                text3 = await resp3.text(errors='ignore')
                                soup2 = BeautifulSoup(text3, 'html.parser')
                                title2 = str(soup2.find('title'))
                                title2 = title2.strip('</title>')
                                title2 = title2.replace('\t', '').replace('\n', '').replace('\r', '')
                                if '=' in title2:
                                    title2 = re.search('>.+</title>', text3)
                                    if title2:
                                        title2 = title2.group()
                                        title2 = title2.strip('>').strip('</title')
                                if status3 in [200]:
                                    s = difflib.SequenceMatcher(isjunk=None, a=text, b=text3, autojunk=False)
                                    if s.ratio() > 0.95:
                                        c_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                    else:
                                        a_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                elif status3 in [403, 500, 404, 400]:
                                    c_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                elif status3 in [501, 502, 503, 504]:
                                    d_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                        elif status2 == 200:
                            s = difflib.SequenceMatcher(isjunk=None, a=text, b=text2, autojunk=False)
                            if s.ratio() > 0.95:
                                c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                            else:
                                a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 in [400, 403]:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add('200\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status in [301, 302, 303, 304, 307]:
                        if status2 == 403:
                            c_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        elif status2 in [301, 302, 303, 304, 307]:
                            async with session.get(url=url2, verify_ssl=False, timeout=15) as resp3:
                                status3 = resp3.status
                                text3 = await resp3.text(errors='ignore')
                                soup2 = BeautifulSoup(text3, 'html.parser')
                                title2 = str(soup2.find('title'))
                                title2 = title2.strip('</title>')
                                title2 = title2.replace('\t', '').replace('\n', '').replace('\r', '')
                                if '=' in title2:
                                    title2 = re.search('>.+</title>', text3)
                                    if title2:
                                        title2 = title2.group()
                                        title2 = title2.strip('>').strip('</title')
                                if status3 in [200]:
                                    a_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                elif status3 in [403, 404, 400, 500]:
                                    c_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                elif status3 in [501, 502, 503, 504]:
                                    d_list.add(url2 + "\t%d\t%s\n" % (status2, title2))
                                else:
                                    other_list.add('3xx\t' + url2 + "\t%d\t%s\n" % (status3, title2))
                        elif status2 == 200:
                            a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                        else:
                            other_list.add( '3XX\t' + url2 + "\t%d\t%s\n" % (status2, title))
                    elif status in [401]:
                        a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                    elif status in [405]:
                        if status2 in [301, 302, 200]:
                            a_list.add(url2 + "\t%d\t%s\n" % (status2, title))
                    else:
                        e_list.add(url2 + "\t%d\t%s\n" % (status2, title))
        except asyncio.TimeoutError:
            print("TimeoutError:", url)
            e_list.add(url.strip('/booksiyi/') + '\t连接超时\n')
        except aiohttp.client.ClientConnectorError as e:
            print("ClientConnectorError", e)
            str_e = str(e)
            if str_e.find('getaddrinfo') + 1:
                e_list.add(url.strip('/booksiyi/') + '\t未知的服务器\n')
            elif str_e.find('远程计算机拒绝网络连接') + 1:
                e_list.add(url.strip('/booksiyi/') + '\t远程计算机拒绝网络连接\n')
            else:
                e_list.add( url.strip('/booksiyi/') + '\t' + "ClientConnectorError:" + str_e + '\n')
        except aiohttp.client.ClientOSError as e:
            print(url + "\tClientOSError:", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/') + '\t' + "ClientOSError:" + str_e + '\n')
        except aiohttp.client.ClientConnectionError as e:
            print(url + "\tClientConnectionError:", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/') + '\t' + "ClientConnectionError:" + str_e + '\n')
        except aiohttp.client.ClientResponseError as e:
            print(url + "\tClientResponseError", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/') + '\t' + "ClientResponseError:" + str_e + '\n')
        except aiohttp.client.ClientError as e:
            print(url + "\tClientError", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/') + '\t' + "ClientError:" + str_e + '\n')
        if len(a_list):
            f1 = open(path1, 'w+', encoding='utf-8')
            f1.writelines(a_list)
            f1.close()
        if len(b_list):
            f2 = open(path2, 'w+', encoding='utf-8')
            f2.writelines(b_list)
            f2.close()
        if len(c_list):
            fc = open(path3, 'w+', encoding='utf-8')
            fc.writelines(c_list)
            fc.close()
        if len(d_list):
            fd = open(path4, 'w+', encoding='utf-8')
            fd.writelines(d_list)
            fd.close()
        if len(e_list):
            fe = open(path5, 'w+', encoding='utf-8')
            fe.writelines(e_list)
            fe.close()
        if len(other_list):
            f6 = open(path6, 'w+', encoding='utf-8')
            f6.writelines(other_list)
            f6.close()
        

parser = argparse.ArgumentParser(description='test2.py')
parser.add_argument('-o', '--output', help='The dirname where the files are located', dest='output', required=False)
parser.add_argument('-i', '--input', help='The path to the file that holds the url or IP', dest='input', required=True)
args = parser.parse_args()
location = args.input
name = args.output
if name:
    if not os.path.exists(name):		# 如果路径 path 存在，返回 True；如果路径 path 不存在，返回 False。
        os.mkdir(name)					# 创建目录
        print("创建目录:", name)
    else:
        print("该目录已存在，请更换目录名")
if os.path.exists(name):
    path1 = os.path.join(name, 'a.txt')
    path2 = os.path.join(name, 'b.txt')
    path3 = os.path.join(name, 'c.txt')
    path4 = os.path.join(name, 'd.txt')
    path5 = os.path.join(name, 'e.txt')
    path6 = os.path.join(name, 'other.txt')
with open(location, 'r') as f:  # 输入收集的url文件路径
    for line in f.readlines():
        lines.append(line.strip() + '\n')
        reset.add(line.strip() + '\n')
count = len(lines) - len(reset)
quchong = open(location, 'w+')
quchong.writelines(reset)
quchong.close()
with open(location, 'r') as fr:
    for line in fr.readlines():
        line_h = 'http://' + line.strip() + '/booksiyi/'
        line_hs = 'https://' + line.strip() + '/booksiyi/'
        if line_h == 'http:///booksiyi/' or line_hs == 'https:///booksiyi/':
            continue
        urls.append(line_h)
        urls.append(line_hs)
loop = asyncio.get_event_loop()
sem = asyncio.Semaphore(100)
tasks = [asyncio.ensure_future(get(url, sem)) for url in urls]
loop.run_until_complete(asyncio.wait(tasks))
time = time.time() - start
print("url总数量：", len(lines))
print("去重复url数量", count)
print("实际子域名数量:", len(reset))
print("实际待测url数量:", len(urls))
print("总用时:%s" % time)
