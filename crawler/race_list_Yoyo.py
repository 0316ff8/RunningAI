from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=["日期","賽事種類","賽事名稱","地點","組別","賽事介紹",
                           "開始報名","截止日期"])

page = 1
while True:
    print("頁數：",page)
    url = "https://www.marathonsworld.com/artapp/racedetail.php?rid="+str(page)  # 開啟網址
    page += 1
    try:
        response = urlopen(url)
        html = BeautifulSoup(response)
    except:
        continue
    df.to_csv('race_Yoyo.csv', encoding="utf-8",index=False) #mode預設w覆蓋
    try:
        title = html.find("td", class_="RaceTitle").text
        race = {"賽事名稱":title}
    except:
        break
    #網頁唯一區分賽事種類為圖片，以有無此種類圖片判斷賽事種類
    if html.find("img",src="skin/blue/images-award/Award-swim.png") != None:
        race["賽事種類"] = "游泳"
    elif html.find("img",src="skin/blue/images-award/Award-bike.png") != None:
        race["賽事種類"] = "自行車"
    elif html.find("img",src="skin/blue/images-award/Award-run.png") != None:
        race["賽事種類"] = "路跑"
    try:
        date = html.find("td", class_="FontV1-White").text.replace("HOT! ", "")
        race["日期"] = date
    except:
        race["日期"] = None
    try:
        place = html.find("td",class_="FontV1-GrayLight").text
        race["地點"] = place
    except:
        race["地點"] = None
    try:
        data = html.find("td",class_="RaceKind").text
        racekind = data.replace('全馬','全馬,').replace('半馬','半馬,').replace(' km','km,')
        race["組別"] = racekind
    except:
        race["組別"] = None
    try:
        link = html.find("a",class_="FontV1-LikeBlueS")["href"]
        race["賽事介紹"] = link
    except:
        race["賽事介紹"] = None
    try:
        start_date = html.find_all("span",class_="FontV1-Gray")[2].text
        race["開始報名"] = start_date
    except:
        race["開始報名"] = None
    try:
        end_date = html.find_all("span",class_="FontV1-Gray")[3].text
        race["截止日期"] = end_date
    except:
        race["截止日期"] = None
    df = df.append(race, ignore_index=True)