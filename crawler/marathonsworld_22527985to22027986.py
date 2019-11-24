from urllib.request import urlopen
import json
import os
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=["姓名","UID","賽事名稱","運動種類","日期","卡路里","地點","平均心率",
                           "平均步頻","踏頻","濕度","天氣","總爬升","溫度","里程","完成時間",
                           "平均配速","每分鐘配速","總名次","分組名次","當月累積里程","評分","心得"])
page = 22527985
count = 1
while True:
    url = "http://www.marathonsworld.com/artapp/trainingDailyDetail.php?recordId="+str(page)  # 開啟網址
    print("頁數：", page, "筆數：", count)
    if page == 22027986:
        break
    page -= 1
    response = urlopen(url)
    df.to_csv('marathonworld.csv', encoding="utf-8", mode='w', index=False) #mode預設w覆蓋
    html = BeautifulSoup(response)
    title = html.find("title").text
    if title[1:3] == "00":
        continue
    # 姓名
    try:
        name = html.find("a", class_="FaceName").text.replace("\r","").replace("\n","")
        excel = {"姓名":name}
    except:
        excel = {"姓名": None}
    try:
        uid = html.find("a", class_="FaceName")["href"]
        excel["UID"] = uid
    except:
        excel["UID"] =None
    data = html.find_all("div", class_="FontRec-Gray", id="Row1-dataUp-showData")
    # 賽事名稱
    try:
        excel["賽事名稱"] = data[0].find("span", class_="FontX1-BlackSB").text.replace("\r","").replace("\n","")
    except:
        excel["賽事名稱"] = None
    try:
        block = html.find("div", id="Row1-dataUp-show")
        kind = block.find("img",height="19")
        if kind["src"] == "images/running-small.png":
            excel["運動種類"] = "running"
        elif kind["src"] == "images/bicycle.png":
            excel["運動種類"] = "bicycle"
        elif kind["src"] == "images/swim.png":
            excel["運動種類"] = "swim"
        elif kind["src"] == "images/workout-small.png":
            excel["運動種類"] = "workout"
        elif kind["src"] == "images/hiking.png":
            excel["運動種類"] = "hiking"
        elif kind["src"] == "images/yoga.png":
            excel["運動種類"] = "yoga"
        else:
            excel["運動種類"] = "others"
    except:
        excel["運動種類"] = None
    d = 0
    count += 1
    if len(data) == 1:
        d = d
    elif len(data) == 2:
        d += 1
    # 因狀態欄位全部位置參數都相同，故轉為str再切割成list
    try:
        status = data[d].text.replace("     - ", ": ").split(": ")
        status_dict = {}
        for s in range(0, len(status) - 1, 2):
            status_dict[status[s]] = status[s + 1]
    except:
        continue
    # "日期","地點","平均心率","卡路里","溫度","濕度","總爬升"
    # 因使用者缺少一欄位就會出錯，每個都需要try、expect
    try:
        excel["日期"] = status_dict["日期"]
    except:
        excel["日期"] = None
    try:
        excel["卡路里"] = status_dict["卡路里"]
    except:
        excel["卡路里"] = None
    try:
        excel["地點"] = status_dict["地點"]
    except:
        excel["地點"] = None
    try:
        excel["平均心率"] = status_dict["平均心率"]
    except:
        excel["平均心率"] = None
    try:
        excel["平均步頻"] = status_dict["平均步頻"]
    except:
        excel["平均步頻"] = None
    try:
        excel["踏頻"] = status_dict["踏頻"]
    except:
        excel["踏頻"] = None
    try:
        excel["濕度"] = status_dict["濕度"]
    except:
        excel["濕度"] = None
    try:
        excel["天氣"] = status_dict["天氣"]
    except:
        excel["天氣"] = None
    try:
        excel["總爬升"] = status_dict["總爬升"]
    except:
        excel["總爬升"] = None
    try:
        excel["溫度"] = status_dict["溫度"]
    except:
        excel["溫度"] = None
    # "里程","完成時間","配速"
    try:
        excel["里程"] = html.find_all("span", class_="FontRec-BlackS")[0].text.replace("\r","").replace("\n","").replace("全馬","42.195 km").replace("半馬","21 km")
    except:
        excel["里程"] = None
    try:
        excel["完成時間"] = html.find_all("span", class_="FontRec-BlackS")[1].text.replace("|","").replace(" ","")
    except:
        excel["完成時間"] = None
    try:
        excel["平均配速"] = html.find_all("span", class_="FontRec-BlackS")[2].text.replace("\r","").replace("\n","")
    except:
        excel["平均配速"] = None
    try:
        run = html.find_all("div", class_="FontV1-Gray", id="Row1-dataUp-showData")[0].text.replace("'", ":").replace(" Pace: ", "").replace("\" / ", ",")[:-1]
        if run[0] == "官" or run[0] == "看":
            excel["每分鐘配速"] = None
        else:
            excel["每分鐘配速"] = run.split(",")
    except:
        excel["每分鐘配速"] = None
        # "總名次","分組名次"
    try:
        excel["總名次"] = html.find_all(align="center", class_="FontV1-BlackSB")[3].text.replace("\r","").replace("\n","").replace(",","，").replace(".","。")
        excel["分組名次"] = html.find_all(align="center", class_="FontV1-BlackSB")[4].text.replace("\r","").replace("\n","").replace(",","，").replace(".","。")
    except:
        excel["總名次"] = None
        excel["分組名次"] = None
    # "當月累積里程"
    try:
        mileage= html.find("div", class_="FontV1-GrayLight", id="Row1-dataUp-showTotal").text.split(" ")
        excel["當月累積里程"] = mileage[0]+mileage[1]+mileage[2]+mileage[3]
    except:
        excel["當月累積里程"] = None
    #"評分"
    try:
        write = html.find_all("span",class_="FontRec-Gray")
        excel["評分"] = write[1].text.replace("給","").replace("星","").replace(" ","")
    except:
        excel["評分"] = None
    #心得
    try:
        excel["心得"] = html.find("p", style="word-wrap:break-word; word-break:break-all;").text.replace("\r","").replace("\n","。").replace(",","，").replace(".","。")
    except:
        excel["心得"] = None
    df = df.append(excel,ignore_index=True)