from bs4 import BeautifulSoup
import requests
import urllib.request
import urllib
import xlwt
import re
import json


def get_url(url,headers={}):
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    content = response.read().decode('utf-8')
    response.close()
    return content


def singer_url(url):
    #只抓取前10位的歌手
    html = get_url(url)
    soup = BeautifulSoup(html, 'lxml')
    list_pic = soup.select('ul#m-artist-box li div img')
    list_nameUrl = soup.select('ul#m-artist-box li div a.msk')
    list_author = soup.select('ul#m-artist-box li p a.f-thide')
    singers = []
    for i in range(len(list_pic)):
        singers.append([list_nameUrl[i]['href'],list_author[i].text])
        #解析的代码和源代码的顺序不同，在用正则表达式的时候要注意
    #print(singers)
    song_info(singers)

def song_info(singers):
    url = 'http://music.163.com'
    
    for singer in singers:
        try:
            new_url = url + str(singer[0])
            songs = get_url(new_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
                'Host': 'music.163.com'
            })
            soup = BeautifulSoup(songs,'html.parser')
            soups = BeautifulSoup(songs, 'lxml')
            Info = soup.find_all('textarea',attrs = {'style':'display:none;'})[0]
            song = soups.select('div#song-list-pre-cache ul li a')
            #print(song)
            datas = []
            #data1 = re.findall(r'"album".*?"name":"(.*?)".*?',str(Info.text))
            data1 = json.loads(Info.text)
            #print(data1)

            for i in range(len(song)):
                datas.append([song[i].text,data1[i]['album']['name'],'http://music.163.com/#'+ song[i]['href']])

            save_excel(singer,datas)
        except:
            continue



def save_excel(singer,datas):
    fpath = 'D:/python/test/'
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1',cell_overwrite_ok = True)
    sheet1.col(0).width = (25*256)
    sheet1.col(1).width = (30*256)
    sheet1.col(2).width = (40*256)
    #xlwt中列宽的值表示方法：默认字体0的1/256为衡量单位。
    #xlwt创建时使用的默认宽度为2960，既11个字符0的宽度
    #所以我们在设置列宽时可以用如下方法：
    #width = 256 * 20    256为衡量单位，20表示20个字符宽度
    
    heads = ['歌曲名称','专辑','歌曲链接']
    count = 0 

    print('正在存入文件......')
    for head in heads:
        sheet1.write(0,count,head)
        count += 1

    
    i = 1
    for data in datas:
        j = 0
        for k in data:
            sheet1.write(i,j,k)
            j += 1
        i += 1

    book.save(fpath + str(singer[1]) + '.xls')#括号里写存入的地址
    print('OK！')

def main():
    url = 'http://music.163.com/discover/artist/cat?id=1001'#华语男歌手页面
    singer_url(url)

main()