from urllib.request import urlopen
from bs4 import BeautifulSoup
# step0:import pandas
import pandas as pd
import time

ID = 1

# 抓取網址
lns = []
infoitem_startday = ""
infoitem_endday = ""
infoitem_about_road = ""
infoitem_about_mountain = ""
prices = ""

for i in range(1, 330):
    print("第" + str(i) + "頁")
    url = "https://hiking.biji.co/index.php?q=review&page=" + str(i)
    response = urlopen(url)
    html = BeautifulSoup(response)
    rs = html.find_all("a", class_="action-area")
    for r in rs:
        ln = "https://hiking.biji.co" + r["href"]
        lns.append(ln)

    time.sleep(1)

# 讀取網址後開始抓取內部資料
print("抓取網址完成")
# step1:ceate one table(columns:會先固定住欄位順序)
df = pd.DataFrame(columns=["ID", "標題", "作者", "時間", "出發日期", "回程日期", "相關路線", "相關山岳", "內文"])
print("開始抓取內部資料")

for url in lns:
    print(url)
    response = urlopen(url)
    html = BeautifulSoup(response)
    title = html.find("h1", class_="header-title")
    detal = html.find_all("span", class_="metrics-item")
    prices = html.find("div", class_="biji-news-format fr-view")
    if prices == None:
        prices = "123"
    infoitem = html.find_all("li", class_="info-item")
    for i in infoitem:
        if i.find("div", class_="info-title").text == "出發日期":
            # print("出發日期：", i.find("div", class_="info-content").text)
            infoitem_startday = i.find("div", class_="info-content").text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "").replace("　", "")
        if i.find("div", class_="info-title").text == "回程日期":
            # print("回程日期：", i.find("div", class_="info-content").text)
            infoitem_endday = i.find("div", class_="info-content").text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "").replace("　", "")
        if i.find("div", class_="info-title").text == "相關路線":
            # print("相關路線：", i.find("div", class_="info-content").text[1:])
            infoitem_about_road = i.find("div", class_="info-content").text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "").replace("　", "")
        if i.find("div", class_="info-title").text == "相關山岳":
            # print("相關山岳：", i.find("div", class_="info-content").text.replace("	", "")[1:])
            infoitem_about_mountain = i.find("div", class_="info-content").text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "").replace("　", "")

    try:
        data = {"ID": url,
                "標題": title.text,
                "作者": detal[0].text,
                "時間": detal[1].text[1:-4],
                "出發日期": infoitem_startday,
                "回程日期": infoitem_endday,
                "相關路線": infoitem_about_road,
                "相關山岳": infoitem_about_mountain,
                "內文": prices.text.replace("\t", "").replace("\r", "").replace("\n", "").replace(" ", "").replace("　", "").replace(",", "，").replace(".", "。")}
    except:
        print('讀取檔案發生錯誤')
        data = {"ID": url,
                "標題": title.text,
                "作者": detal[0].text,
                "時間": detal[1].text[1:-4],
                "出發日期": infoitem_startday,
                "回程日期": infoitem_endday,
                "相關路線": infoitem_about_road,
                "相關山岳": infoitem_about_mountain,
                "內文": ""}
    finally:
        df = df.append(data, ignore_index=True)
        time.sleep(1)
        # ID += 1
        df.to_csv("mountain.csv", encoding="utf-8", index=False)
