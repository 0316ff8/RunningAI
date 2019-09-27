from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# 使用chrome driver
driver = webdriver.Chrome('E:\\Drive\\DB103\\ETL\\ch1\\chromedriver.exe')
# 定義登入帳號密碼
username = 'jimmy29304825@yahoo.com.tw'
password = 'Jimmy8193026'
# 進入連結
url_login = 'https://hiking.biji.co/index.php?q=trail&act=gpx_list'
driver.get(url_login)
# 點選登入人頭
driver.find_element_by_class_name('g-member').click()
# 點選FB登入
driver.find_element_by_class_name('login-btn').click()
# 輸入帳號密碼並點擊登入
driver.find_element_by_id('email').send_keys(username)
driver.find_element_by_id('pass').send_keys(password)
driver.find_element_by_id('loginbutton').click()
# 回到GPX畫面
url_login = 'https://hiking.biji.co/index.php?q=trail&act=gpx_list'
driver.get(url_login)
# 儲存cookies
cookie_list = driver.get_cookies()
# 關閉瀏覽器
driver.close()
# 建立資料表
df = pd.DataFrame(columns=['id', "路線名稱", "距離", "時間", "上坡高度", '下坡高度',
                           '上傳者', '檔名', '描述', '相關山岳', '相關路線'])

# 通知下方程式要使用瀏覽器的cookie
with requests.Session() as s:
    # 取出儲存的cookie資料
    for i, cookie in enumerate(cookie_list):
        s.cookies.set(cookie['name'], cookie['value'])
    p = 1
    count = 0
    while True:
        response = s.get('https://hiking.biji.co/'
                         'index.php?q=trail&act=gpx_list&city=%E5%85%A8%E9%83%A8&keyword=&page=' + str(p))
        html = BeautifulSoup(response.text)
        rs = html.find_all("li", class_="pic-item")
        # print(rs)
        if rs not in []:
            n = 0
            for r in rs:
                # 抓取每一個
                gpx = r.find("a", class_="download")
                name = r.find("h3", class_="list-title").text
                info = r.find_all("div", class_="metrics-num")
                upload = r.find("a", class_="avatar-link").text
                # get other detail
                roadweb = r.find("a", class_="postMeta-img")
                url = requests.get('https://hiking.biji.co/' + roadweb['href'])
                html2 = BeautifulSoup(url.text)
                # print(html2)
                detail = html2.find('div', class_='details-table')
                detail_dict = {}
                if detail not in None:
                    # print(detail.text)
                    detail2 = detail.find_all('div', class_='flex-none')
                    detail3 = detail.find_all('div', class_='flex-1')
                    list_len = len(detail2)
                    # print(list_len)

                    for i in range(list_len):
                        title = detail2[i].text
                        content = detail3[i].text
                        # print(repr(content)[1:3])
                        title = title.replace('\n', '')
                        if repr(content)[1:3] == '\\n' or repr(content)[-3:-1] == '\\n':
                            content = content[1:-1]
                            content = content.replace(' ', '_')
                            content = content.replace('\r', '')
                            content = content.replace('\n', '&')
                        content = content.replace('\n', '&')
                        detail_dict[title] = content
                        # print(title, content)
                        # print()
                    # print(detail_dict)

                try:
                    # 整理資料(取代換行、tab)
                    name = name.replace('\n', '')
                    name = name.replace('	', '')
                    upload = upload.replace('\n', '')
                    upload = upload.replace('	', '')

                    print("名稱:", name)
                    print("距離:", info[0].text)
                    print("時間:", info[1].text)
                    print("上波高度:", info[2].text)
                    print("下坡高度:", info[3].text)
                    print("上傳者:", upload)
                    print(detail_dict)
                    print()

                    # 下載GPX檔
                    purl = 'https://hiking.biji.co' + gpx['href']  # file name
                    dn = 'E:/Drive/DB103/人頭組專題/專題-智慧運動輔助系統/gpx/'
                    not_allowed = ['?', '/', '>', '<', '|', '\\', '\"',
                                   '*', ':', '=', '.', '！', ' ', '!']
                    title_revised = ''
                    for c in name:  # 若有上述字元不要使用
                        if c not in not_allowed:
                            title_revised = title_revised + c
                    # 檔案儲存名稱(最後一個'/'後面的東西是檔名)與路徑
                    fn = dn + str(count + n) + '-' + title_revised.replace('\n', '') + ".gpx"
                    # print(fn, purl)
                    # Step2. 準備要插入的資料
                    data = {'id': count + n,
                            "路線名稱": name,
                            "距離": info[0].text,
                            "時間": info[1].text,
                            "上坡高度": info[2].text,
                            "下坡高度": info[3].text,
                            "上傳者": upload,
                            '檔名': str(count + n) + '-' + title_revised.replace('\n', '') + ".gpx"}
                    data.update(detail_dict)
                    print(data)
                    # Step3. 插入進去(append)
                    # 只要是dataframe專屬功能, 都是屬於第一種(有兩份)
                    df = df.append(data, ignore_index=True)
                    # 建立存放資料夾
                    if not os.path.exists(dn):
                        os.makedirs(dn)
                    df.to_csv(dn + 'gpx.csv', encoding="utf-8", mode='w', index=False)
                    # df.to_csv('gpx.csv', encoding="utf-8", mode='w', index=False)
                    # 呼叫下載連結
                    data = s.get(purl, stream=True)
                    # 存檔
                    with open(fn, 'wb') as f:
                        f.write(data.content)
                    # 關閉檔案
                    f.close()
                    n += 1
                except IndexError:
                    continue
            count += n
            print('\n完成第{}頁，共{}個檔案'.format(p, count))
            p += 1
        else:
            print("\n\n完成，共爬了{}頁，{}個GPX檔案已儲存".format(p - 1, count))
            # Step4. 儲存檔案
            # index=False, 不要儲存0,1,2....
            # df.to_csv("hiking/gpx.csv",
            #           encoding="utf-8",
            #           index=False)
            break
