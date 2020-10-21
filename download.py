import urllib
import sys
from bs4 import BeautifulSoup
import urllib.request
import re
import os

path = []

def extract(url):
    #content = urllib.request.urlopen(url).read()
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    #reg = r'(?:href|HREF)="?((?:http://)?.+?\.txt)'    
    reg = r'<a href="(.*)">.*'
    url_re = re.compile(reg)
    url_lst = re.findall(url_re, content)
    print(url_lst)

    for lst in url_lst:
        ext = lst.split('.')[-1]
    
        if ext[-1] == '/':
           newUrl = url + lst
           extract(newUrl)
        else:
            path.append(url + lst)
       


print("downloading with urllib")
url = 'http://www.17cct.com'
extract(url)
print(path)

filePath = 'D:/python/Download' 
filePath = unicode(filePath, 'utf8')

for p in path:
    fileTitle = p.split('/js')[-1]
    file = filePath + fileTitle
    dir = os.path.dirname(file)
    isExists=os.path.exists(dir)

    if isExists == False:
        os.makedirs(dir)
    urllib.urlretrieve(p, file)
