# coding:utf-8
import re
import requests
from bs4 import BeautifulSoup
import json
import xlwt
import time
import pymysql


proxies = {'113.240.226.164:8080'}
headers = { 'Host':'example.com',
                    'Connection':'keep-alive',
                    'Cache-Control':'max-age=0',
                    'Accept': 'text/html, */*; q=0.01',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
                    'DNT':'1',
                    'Referer': 'http://example.com/',
                    'Accept-Encoding': 'gzip, deflate, sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
            }

db = pymysql.connect("127.0.0.1", "root", "123456", "test",charset="utf8")
cursor = db.cursor()

def test():
    # work = xlwt.Workbook(encoding='utf-8')
    # sheet = work.add_sheet('mysheet', cell_overwrite_ok=True)
    # sheet.write(int(i / 14), i % 14, a)
    # work.save('1.xls')
    # r = requests.get('http://m.dce.com.cn/dalianshangpinmobile/xqsj71/rtj26/rxq46/index.html')
    for month in range(1,8):
        for day in range(1,32):
            if month >= 7:
               if day >= 10:
                  break
            if day < 10:
                d = '0'+ str(day)
                m = '0'+ str(month)
            elif day >= 10:
                d = str(day)
                m = '0'+ str(month)
            data = {
                    'dayQuotes.variety': 'pp',
                    'dayQuotes.trade_type': '0',
                    'year': '2018',
                    'month': m,
                    'day': d,
                    'mobile': 'mobileFlag'
            }
            r1 = requests.post('http://m.dce.com.cn/publicweb/m_quotesdata/dayQuotesCh.html', data=data,
                                   headers=headers).text
            soup = BeautifulSoup(r1, 'html.parser')
            temp = soup.select('tr td')
            if temp != []:
                 for num,i in enumerate(temp):
                     if num%14 ==0:
                          new = []
                          new.append(m+'-'+d)
                     new.append(re.sub('\s', '', re.sub(',', '', i.text)))
                     if num%14 ==13:
                        sql = 'INSERT INTO `abc` VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        cursor.execute(sql, new)
                        db.commit()
                        print(m, d)
            else:
                 print(m, d, temp)
            time.sleep(5)

if __name__ == '__main__':
    test()

