# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 23:18:01 2015

@author: Song
"""

import urllib2
import sys
import codecs
import time
from bs4 import BeautifulSoup
import xlwt

reload(sys)
sys.setdefaultencoding("utf8")

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

COUNTER = 0 #文档编号

def getHtml(url, filename, sheet):
    global COUNTER
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
    soup = BeautifulSoup(html)
    res = soup.find_all('div', 'J_brief_cont_full Hide') #长评论
    if len(res)>0:
        for i in xrange(len(res)):
            COUNTER += 1
            text = res[i-1].text
            text = text.strip()
            sheet.write(COUNTER-1, 1, text)
            filename.write('<docno>' + str(COUNTER) + '</docno>' + '\r\n')
            filename.write('<text>' + text + '</text>' + '\r\n')    
            
    res = soup.find_all('div', 'J_brief_cont_full ') #短评论
    if len(res)>0:
        for i in xrange(len(res)):
            COUNTER += 1
            text = res[i-1].text
            text = text.strip()
            sheet.write(COUNTER-1, 1, text)
            filename.write('<docno>' + str(COUNTER) + '</docno>' + '\r\n')
            filename.write('<text>' + text + '</text>' + '\r\n')
        
if __name__ == '__main__':
    file1 = codecs.open('./canguan.txt', 'w', 'utf-8')
    book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
    sheet = book.add_sheet('canguan', cell_overwrite_ok = True)
    for i in range(1, 401):
        now = int(time.time()) #timestamp
        url = 'http://t.dianping.com/ajax/detailDealRate?dealGroupId=8738423&pageNo=' + str(i) + '&filtEmpty=1&timestamp=' + str(now)
        print 'Crawling No.' + str(i) + ' pages......'
        getHtml(url, file1, sheet)
    book.save('canguan.xls')
