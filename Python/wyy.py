# 爬取网易云音乐的爬虫
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request
import urllib
import xlwt

#获取网页
def gethtml(url, headers={}):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content

#解析音乐列表网页
def parsehtmlMusicList(html):
    soup = BeautifulSoup(html, 'lxml')
    list_pic = soup.select('ul#m-pl-container li div img')
    list_nameUrl = soup.select('ul#m-pl-container li div a.msk')
    list_num = soup.select('div.bottom span.nb')
    list_author = soup.select('ul#m-pl-container li p a')
    n = 0
    data = []
    length = len(list_pic)
    while n < length:
        #print('歌单图片：'+list_pic[n]['src']+'\n\n')
        #print('歌单名称：'+list_nameUrl[n]['title']+'\n\n歌单地址：'+list_nameUrl[n]['href']+'\n\n')
        #print('歌单播放量：'+list_num[n].text+'\n\n')
        #print('歌单作者：'+list_author[n]['title']+'\n\n作者主页：'+list_author[n]['href']+'\n\n\n')
        data.append([list_pic[n]['src'],list_nameUrl[n]['title'],list_nameUrl[n]['href'],list_num[n].text,list_author[n]['title'],list_author[n]['href']])
        n += 1
    save_excel(data)

def save_excel(datas):
    fpath = 'D:/python/test/'
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1',cell_overwrite_ok = True)
    sheet1.col(0).width = (25*256)
    sheet1.col(1).width = (30*256)
    sheet1.col(2).width = (40*256)
    sheet1.col(3).width = (40*256)
    sheet1.col(4).width = (40*256)
    sheet1.col(5).width = (40*256)
    #xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位。
    #xlwt创建时使用的默认宽度为2960，既11个字符0的宽度
    #所以我们在设置列宽时可以用如下方法：
    #width = 256 * 20    256为衡量单位，20表示20个字符宽度
    
    heads = ['歌单图片','歌单名称','歌单地址','歌单播放量','歌单作者','作者主页']
    count = 0 

    print('正在存入文件......')
    for head in heads:
        sheet1.write(0,count,head)
        count += 1

    
    i = 1
    for dt in datas:
        j = 0
        for k in dt:
            sheet1.write(i,j,k)
            j += 1
        i += 1

    book.save(fpath + 'wyy' + '.xls')#括号里写存入的地址
    print('OK！')

url = 'http://music.163.com/discover/playlist'
url = gethtml(url, headers={
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'music.163.com'
})
parsehtmlMusicList(url)