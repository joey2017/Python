# coding: UTF-8
import requests
url="http://hjwachhy.site/music.mp3"
path="music.mp3"
r=requests.get(url)
print("ok")
with open(path,"wb") as f:
    f.write(r.content)
f.close()