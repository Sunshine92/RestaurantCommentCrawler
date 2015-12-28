# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:02:54 2015

@author: Song
"""

import urllib2
import sys
import time
from bs4 import BeautifulSoup
import xlwt
import random

reload(sys)
sys.setdefaultencoding("utf8")

user_agent = [
    "Mozilla/5.0 (Windows NT 5.1; rv:37.0) Gecko/20100101 Firefox/37.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50"]
COUNTER = 0 #文档编号

def getHtml(url, sheet, userAgent):
    global COUNTER
    random_userAgent = random.choice(userAgent)
    print random_userAgent
    headers = { 'User-Agent' : random_userAgent }
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
        return
    html = response.read()
    soup = BeautifulSoup(html, "lxml")
    res = soup.find_all('div', 'J_brief_cont_full Hide') #长评论
    if len(res)>0:
        for i in xrange(len(res)):
            a = res[i-1].parent.parent
            res1 = a.find_all('span', 'syellowstar50 star-icon')
            res2 = a.find_all('span', 'syellowstar40 star-icon')
            if (len(res1) + len(res2) == 1):
                print 'jump' #跳过4,5星评论
                continue
            COUNTER += 1
            text = res[i-1].text
            text = text.strip()
            sheet.write(COUNTER-1, 1, text) 
            
    res = soup.find_all('div', 'J_brief_cont_full ') #短评论
    if len(res)>0:
        for i in xrange(len(res)):
            a = res[i-1].parent.parent
            res1 = a.find_all('span', 'syellowstar50 star-icon')
            res2 = a.find_all('span', 'syellowstar40 star-icon')
            if (len(res1) + len(res2) == 1):
                print 'jump'
                continue
            COUNTER += 1
            text = res[i-1].text
            text = text.strip()
            sheet.write(COUNTER-1, 1, text)
        
if __name__ == '__main__':
    book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
    sheet = book.add_sheet('canguan', cell_overwrite_ok = True)
    for i in range(1301, 1401):
        now = int(time.time()) #timestamp
        url = 'http://t.dianping.com/ajax/detailDealRate?dealGroupId=8738423&pageNo=' + str(i) + '&filtEmpty=1&timestamp=' + str(now)
        print 'Crawling No.' + str(i) + ' pages......'
        getHtml(url, sheet, user_agent)
    book.save('canguan.xls')
