# -*- coding = utf-8 -*-
# @Author : 路琦
# @File : spider1.py
# @Software : PyCharm


from bs4 import BeautifulSoup
import re
import urllib.error
import urllib.request
import requests
import pandas


def main():
    print("爬取到的https://www.alexa.com/topsites/countries/CN网站的主页内容以及排名前30网站主页的内容")
    baseurl = "https://www.alexa.com/topsites/countries/CN"
    datalist = getData(baseurl)
    print(datalist)

    # askURL("https://www.tmall.com/")

    for i in range(0, 30):
        try:
            comment = []
            print("爬取的第%d个网站主页的网址：" % (i+1))
            comment.append("爬取的第%d个网站主页的网址：" % (i+1))
            url1 = 'https://www.' + datalist[i][0]
            print(url1)
            comment.append(url1)
            comment.append("爬取的第%d个网站主页的内容：" % (i + 1))
            df = pandas.DataFrame(comment)
            df.to_csv('E:\pycharm project\spider\spider1\spider1.csv', mode='a', header=False)
            askURL1(url1)
            print("爬取的第%d个网站主页的内容已保存再CSV文件中" % (i + 1))
        except Exception as err:
            try:
                comment = []
                comment.append("爬取的第%d个网站主页的网址：" % (i + 1))
                url1 = 'http://www.' + datalist[i][0]
                print(url1)
                comment.append(url1)
                comment.append("爬取的第%d个网站主页的内容：" % (i + 1))
                df = pandas.DataFrame(comment)
                df.to_csv('E:\pycharm project\spider\spider1\spider1.csv', mode='a', header=False)
                askURL1(url1)
                print("爬取的第%d个网站主页的内容已保存再CSV文件中" % (i + 1))
            except Exception as err:
                print(err)





# 找到排名信息
findlink = re.compile(r'<a href="/siteinfo/(.*?)">')  # 创建正则表达式对象，找到排名前30的网址


# 得到一个指定的URL网页内容
def askURL(url):
    # 用户代理，表示告诉服务器，我们是什么类型的机器，浏览器
    # 模拟浏览器头部信息，向服务器发送消息
    comments = []

    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    proxies = {'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'}
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        #  请求网址信息，得到数据
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
        comments.append(html)
        df = pandas.DataFrame(comments)
        df.to_csv('E:\pycharm project\spider\spider1\spider1.csv', mode='a', header=False)

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 得到一个指定的URL网页内容
def askURL1(url):
    # 用户代理，表示告诉服务器，我们是什么类型的机器，浏览器
    # 模拟浏览器头部信息，向服务器发送消息
    comments = []

    # head = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
    #
    # request = urllib.request.Request(url, headers=head)
    # html = ""
    try:
        r = requests.get(url)
        # print(r.text)

        comments.append(r.text)
        df = pandas.DataFrame(comments)
        df.to_csv('E:\pycharm project\spider\spider1\spider1.csv', mode='a', header=False)

    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # print(r.text)
    return r.text


def getData(baseurl):
    datalist = []
    url = baseurl
    html = askURL(url)  # 保存获取到的网页源码

    #  2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="tr site-listing"):
        # print(item)  # 测试：查看item的全部信息
        data = []
        item = str(item)
        # print(item)
        # break
        # 获取到影片详情的链接
        link = re.findall(findlink, item)[0]
        data.append(link)  # 添加链接
        datalist.append(data)

    return datalist


if __name__ == '__main__':
    main()
    print("爬取成功")


# askURL1("http://www.17ok.com")