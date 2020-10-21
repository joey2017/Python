#coding=utf-8
import urllib.request
import urllib
from bs4 import BeautifulSoup
import os
import re


url="https://www.zhihu.com/question/36390957"#指定的URL


def download(_url,name):#下载函数
    if(_url==None):#地址若为None则跳过
        pass
    #result=urllib2.urlopen(_url)#打开链接
    req = urllib.request.Request(url)
    result = urllib.request.urlopen(req)
    content = result.read().decode('utf-8')
    #result.close()
    #print result.getcode()
    if(result.getcode()!=200):#如果链接不正常，则跳过这个链接
        pass
    else:
        data=result.read()#否则开始下载到本地
        with open(name, "wb") as code:
            code.write(data)
            code.close()


res=urllib.request.Request(url)
resp=urllib.request.urlopen(res)#打开目标地址
respond=resp.read()#获取网页地址源代码

count=0#计数君
soup=BeautifulSoup(respond,'html.parser')#实例化一个BeautifulSoup对象
lst=[]#创建list对象

for link in soup.find_all("img"):#获取标签为img的内容
    address=link.get('data-original')#获取标签属性为data-original的内容，即图片地址
    lst.append(address)#添加到list中

s=set(lst)#去重
for address in s:
    if(address!=None):
        pathName="D:\\Python\\images\\"+str(count+1)+".jpg"#设置路径和文件名
        download(address,pathName)#下载
        count=count+1#计数君+1
        print("正在下载第：",count)



