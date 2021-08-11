# -*- coding = utf-8 -*-
# @Author : 路琦
# @File : spider3.py
# @Software : PyCharm


from bs4 import BeautifulSoup
import re
import urllib.error
import urllib.request
import xlwt


def main():
    baseurl = "https://search.jd.com/Search?keyword=%E8%81%94%E9%82%A6%E5%AD%A6%E4%B9%A0&enc=utf-8"

    datalist = getData(baseurl)
    print(len(datalist))
    savepath = "联邦学习.xls"
    saveData(datalist, savepath)


# 此书的链接
findlink = re.compile(r'<a href="(.*?)" ')  # 创建正则表达式对象，表示规则
# 图片的链接
findImgsrc = re.compile(r'<img data-img="1" data-lazy-img="(.*?)"', re.S)  # 让换行符包含在字符中
# 找到书名
findTille = re.compile(r'" target="_blank" title="(.*)"')
# 找到价格
findRating = re.compile(r'<em>￥</em><i data-price="(.*)">(.*)</i>')
# 找到出版社或经销商
findjudge = re.compile(r'target="_blank" title="(.*)"')


def getData(baseurl):
    datalist = []
    # for i in range(0, 10):  # 调用页面获取信息的函数，10次
    url = baseurl
    html = askURL(url)  # 保存获取到的网页源码

    #  2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    for item in soup.find_all("div", class_="gl-i-wrap"):
        data = []
        item = str(item)


        link = re.findall(findlink, item)[0]
        data.append(link)  # 添加链接
        imgSrc = re.findall(findImgsrc, item)[0]
        data.append(imgSrc)  # 添加图片链接
        # # # print(link)
        titles = re.findall(findTille, item)[0]

        data.append(titles)  # 添加标题
        #
        rating = re.findall(findRating, item)[0][1]
        data.append(rating)  # 添加价格
        #
        judgenum = re.findall(findjudge, item)[-1]
        data.append(judgenum)  # 添加出版社或经销商
        #
        datalist.append(data)

    return datalist


# 得到一个指定的URL网页内容
def askURL(url):
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器，浏览器（本质上是告诉浏览器，我们可以接受什么水平的文字）
    # 模拟浏览器头部信息，向豆瓣服务器发送消息
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # print(html)
    return html


def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet("联邦学习", cell_overwrite_ok=True)
    col = ("图书链接", "图片链接", "书名", "价格", "出版社或经销商")
    for i in range(0, 5):
        sheet.write(0, i, col[i])
    for i in range(len(datalist)):
        print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 5):
            sheet.write(i + 1, j, data[j])
    book.save(savepath)


#
if __name__ == '__main__':
    main()
    print("爬取成功")
