#from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
# 使用chrome driver
#driver = webdriver.Chrome('./chromedriver')
# 定義登入帳號密碼
#username = 'recluse1025@hotmail.com'
#password = 'seiko690514'
# 進入連結
#url_login = 'https://running.biji.co/index.php?q=record&act=detail&activ_id=0'
#driver.get(url_login)
# 點選登入人頭
#driver.find_element_by_class_name('g-member-text').click()
# 點選FB登入
#driver.find_element_by_class_name('login-btn').click()
# 輸入帳號密碼並點擊登入
#driver.find_element_by_id('email').send_keys(username)
#driver.find_element_by_id('pass').send_keys(password)
#driver.find_element_by_id('loginbutton').click()
# 回到GPX畫面
#url_login = 'https://running.biji.co/index.php?q=record&act=detail&activ_id=0#_=_'
#driver.close()

df = pd.DataFrame(columns=["page","日期","姓名","配速(/km)","移動時間","距離(km)","總爬升(m)","活動時間","卡路里", "鞋款","每公里分段:距離 (km)/時間(min)/爬升 (m)","分段計時:分段/距離(km)/時間/配速(/km)/海拔(m)/心律(分)"])
#178785
page = 1
for r in range(page,178785):
    print("目前第幾頁?", page)
    url = "https://running.biji.co/index.php?q=record&act=detail&activ_id="+ str(page)
    response = requests.get(url)

    df.to_csv("1.csv",
              encoding="utf-8",
              index=False)

    html = BeautifulSoup(response.text)

    date = html.find_all("div",class_="forum-func")
    for p in date:
        print("日期",p.find("span").text)

    name = html.find_all("a", class_="author-name")
    print("姓名:",name[0].text)

    info = html.find_all("div", class_="info")
    info00 = str(info[0].text)
    info01 = str(info[1].text)
    info02 = str(info[2].text)
    info03 = str(info[3].text)
    info04 = str(info[4].text)
    info05 = str(info[5].text)
    info06 = str(info[6].text)
    print("配速(km)",info00)
    print("移動時間",info01)
    print("距離(km)",info02)
    print("總爬升(m)",info03)
    print("活動時間",info04)
    print("卡路里",info05)
    print("鞋款",info06)

    print("每公里分段:距離 (km),時間 (min),爬升 (m)")


    segments2 = ''
    segments3 = []
    segment = html.find_all("li", class_="segment-item")
    for i in segment:
        segments=i.find_all("div",class_="segment-info")
        #print(segments[0].text,segments[1].text,segments[2].text)
        segments00 = str(segments[0].text)
        segments01 = str(segments[1].text)
        segments02 = str(segments[2].text)
        segments00 = segments00[:-2]
        segments02 = segments02[:-1]
        segments2 = segments2 + str(segments00+','+segments01+','+segments02)

        segments3.append(segments2)

    print(segments3)
    print(segments3[0])


    print("分段計時")
    section = html.find_all("li", class_="timing-item")
    item2 = ""
    item4 = []
    for u in section:
        item = u.find_all("div",class_="item-info")
        #print(item[0].text+','+item[1].text+','+item[2].text+','+item[3].text+','+
              #item[4].text+','+item[5].text)

        item01 = str(item[1].text)
        item03 = str(item[3].text)
        item04 = str(item[4].text)
        item05 = str(item[5].text)
        item01 = item01[:-2]
        item03 = item03[:-3]
        item04 = item04[:-1]
        item05 = item05[:-1]

        #print(item[0].text + ',' + item01 + ',' + item[2].text + ',' + item03 + ',' +item04 + ',' + item05)
        item3 = str(item[0].text + ',' + item01 + ',' + item[2].text + ',' + item03 + ',' + item04 + ',' + item05)
        print(item3)
        item2 = item2 + str(item[0].text+','+item[1].text+','+item[2].text+','+item[3].text+','+
              item[4].text+','+item[5].text)

        item4.append(item3)
        item5 = item4
    print(item5)
    print(item5[1])

   # print(item4)
    #print(item4[0])



    data = {"page":page,
            "日期":p.find("span").text,
            "姓名": name[0].text,
            "配速(/km)":info00[:-3],
            "移動時間":info01,
            "距離(km)":info02[:-3],
            "總爬升(m)":info03[:-1],
            "活動時間":info04,
            "卡路里":info05,
            "鞋款":info06,
            "每公里分段:距離 (km)/時間(min)/爬升 (m)":segments3,
            "分段計時:分段/距離(km)/時間/配速(/km)/海拔(m)/心律(分)":item5[1:]
            }

    df = df.append(data, ignore_index=True)
    page = page+1





