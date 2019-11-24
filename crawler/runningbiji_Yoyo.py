from urllib.request import urlopen
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests
page = 1
i = 1
while True:
    print("頁數:",page)
    url = "https://running.biji.co/index.php?pop=ajax&func=route&fename=load_more_route&page="+str(page)+"&sid=&type="
    headers = {
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6"
    }
    try:
        response = requests.get(url,headers=headers)
        html = BeautifulSoup(response.text)
        link = html.find_all("a", class_="func-item helper_btn")
    except:
        print("下載完成")
        break
    #找到gpx檔連結位置
    #提取gpx檔連結
    for a in link:
        gpx = a.get("href")
        print("筆數:",i)
        path = "running/"+str(i)+".gpx"
        i += 1
        r = requests.get(gpx)
        with open(path,"wb") as f:
            f.write(r.content)
        f.close()
    page += 1