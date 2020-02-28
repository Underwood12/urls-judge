# -*- coding: UTF-8 -*-
import asyncio
import aiohttp
import time
import re
import difflib
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
                        if status2 in [200, 304,404, 403, 400]:
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
                            async with session.get(url=url2,  verify_ssl=False, timeout=15) as resp3:
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
                            other_list.add('3XX\t' + url2 + "\t%d\t%s\n" % (status2, title))
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
                e_list.add(url.strip('/booksiyi/')+'\t'+"ClientConnectorError:"+str_e+'\n')
        except aiohttp.client.ClientOSError as e:
            print(url+"\tClientOSError:", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/')+'\t'+"ClientOSError:"+str_e+'\n')
        except aiohttp.client.ClientConnectionError as e:
            print(url+"\tClientConnectionError:", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/')+'\t'+"ClientConnectionError:"+str_e+'\n')
        except aiohttp.client.ClientResponseError as e:
            print(url+"\tClientResponseError", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/')+'\t'+"ClientResponseError:"+str_e+'\n')
        except aiohttp.client.ClientError as e:
            print(url+"\tClientError", e)
            str_e = str(e)
            e_list.add(url.strip('/booksiyi/')+'\t'+"ClientError:"+str_e+'\n')
        if len(c_list):
            error_lists = open(r'C:\Users\sws123\Desktop\python_test\test3\c.txt', 'w+', encoding='utf-8')
            error_lists.writelines(c_list)
            error_lists.close()
        if len(e_list):
            exception_lists = open(r'C:\Users\sws123\Desktop\python_test\test3\e.txt', 'w+', encoding='utf-8')
            exception_lists.writelines(e_list)
            exception_lists.close()
        if len(a_list):
            normal = open(r'C:\Users\sws123\Desktop\python_test\test3\a.txt', 'w+', encoding='utf-8')
            normal.writelines(a_list)
            normal.close()
        if len(b_list):
            root_abnormal = open( r'C:\Users\sws123\Desktop\python_test\test3\b.txt', 'w+', encoding='utf-8')
            root_abnormal.writelines(b_list)
            root_abnormal.close()
        if len(other_list):
            other = open(r'C:\Users\sws123\Desktop\python_test\test3\other.txt', 'w+', encoding='utf-8')
            other.writelines(other_list)
            other.close()
        if len(d_list):
            root_500 = open(r'C:\Users\sws123\Desktop\python_test\test3\d.txt', 'w+', encoding='utf-8')
            root_500.writelines(d_list)
            root_500.close()

with open(r'C:\Users\sws123\Desktop\txt\demo.txt', 'r') as f:   # 输入收集的url文件路径
    for line in f.readlines():
        lines.append(line.strip() + '\n')
        reset.add(line.strip() + '\n')
count = len(lines) - len(reset)
quchong = open(r'C:\Users\sws123\Desktop\txt\demo.txt', 'w+')
quchong.writelines(reset)
quchong.close()
with open(r'C:\Users\sws123\Desktop\txt\demo.txt', 'r') as fr:
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
