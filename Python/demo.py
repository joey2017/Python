# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import time
import sys
import xlwt
from datetime import datetime

def write_data_to_excel(name):

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
    # 以传递的name+当前日期作为excel名称保存。
    wbk.save(name+str(today_date)+'.xls')

write_data_to_excel('doubandemo')