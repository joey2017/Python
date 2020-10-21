# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import xlwt
from datetime import datetime

def getHTMLText(url,k):
    try:
        if(k==0):kw={}
        else: kw={'start':k,'filter':''}
        r = requests.get(url,params=kw,headers={'User-Agent': 'Mozilla/4.0'})
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("Failed!")

def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    movieList=soup.find('ol',attrs={'class':'grid_view'})#找到第一个class属性值为grid_view的ol标签
    moveInfo=[]
    for movieLi in movieList.find_all('li'):#找到所有li标签
        data = []
        #得到电影名字
        movieHd=movieLi.find('div',attrs={'class':'hd'})#找到第一个class属性值为hd的div标签
        movieName=movieHd.find('span',attrs={'class':'title'}).getText()#找到第一个class属性值为title的span标签
                                                                           #也可使用.string方法
        data.append(movieName)

        #得到电影的评分
        movieScore=movieLi.find('span',attrs={'class':'rating_num'}).getText()
        data.append(movieScore)

        #得到电影的评价人数
        movieEval=movieLi.find('div',attrs={'class':'star'})
        movieEvalNum=re.findall(r'\d+',str(movieEval))[-1]
        data.append(movieEvalNum)

        # 得到电影的短评
        movieQuote = movieLi.find('span', attrs={'class': 'inq'})
        if(movieQuote):
            data.append(movieQuote.getText())
        else:
            data.append("无")

        #print(outputMode.format(data[0], data[1], data[2],data[3],chr(12288)))
        return data

def write_data_to_excel(name,result):

    # 实例化一个Workbook()对象(即excel文件)
    wbk = xlwt.Workbook()
    # 新建一个名为Sheet1的excel sheet。此处的cell_overwrite_ok =True是为了能对同一个单元格重复操作。
    sheet = wbk.add_sheet('Sheet1',cell_overwrite_ok=True)
    # 获取当前日期，得到一个datetime对象如：(2016, 8, 9, 23, 12, 23, 424000)
    today = datetime.today()
    # 将获取到的datetime对象仅取日期如：2016-8-9
    today_date = datetime.date(today)
    #设置首行标题
    sheet.write(0,0,'电影名称')
    sheet.write(0,1,'评分')
    sheet.write(0,2,'评论人数')
    sheet.write(0,3,'短评')
    #总数
    length = len(result)
    # 遍历result中的每个元素。
    for i in range(1,length):
        #对result的每个子元素作遍历，
        for j in range(len(result[i-1])):
            #将每一行的每个元素按行号i,列号j,写入到excel中。
            sheet.write(i,j,result[i-1][j])
    # 以传递的name+当前日期作为excel名称保存。
    wbk.save(name+str(today_date)+'.xls')

basicUrl='https://movie.douban.com/top250'
k=0
data = []
while k<=225:
    html=getHTMLText(basicUrl,k)
    #time.sleep(2)
    info = getData(html)
    data.append(info)
    k += 1
    print(info)

print(data)
write_data_to_excel('douban',data)