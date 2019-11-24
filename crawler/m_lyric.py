import requests
from bs4 import BeautifulSoup
import json
import random
import time

general = "Rock"
total = []
page = 1
user_agents = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0)",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko)",
               "Mozilla/5.0 (compatible; MSIE 10.0)",
               'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11)',
               'Opera/9.25 (Windows NT 5.1; U; en)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
               'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
               "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7",
               "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)",
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8',
               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US)',
               'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; SV1; .NET CLR 1.1.4322)',
               'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50',
               'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50',
               'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
               'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36']

proxy_list = ['103.20.204.104:80', '102.129.249.67:3129', '80.211.31.121:3128',
              '180.183.244.193:8213', '47.89.49.187:80', '45.77.56.114:30205',
              '142.93.145.70:80', '165.22.33.143:8080', '13.78.116.29:80',
              '83.239.86.150:80', '159.138.1.185:80', '202.85.52.151:80',
              '211.23.2.54:3128', '60.248.199.206:80', '118.163.96.167:3129',
              '36.228.215.213:3128', '123.110.185.95:8888', '114.37.194.87:3128',
              '159.138.3.119:80', '159.138.1.185:80', '45.125.192.158:80',
              '159.138.21.170:80', '159.138.22.112:80']

# 抓50頁
while page <= 50:
    user = random.choice(user_agents)
    headers = {'User-Agent': user,
               "Upgrade-Insecure-Requests": "1",
               "DNT": "1",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Accept-Language": "en-US;q=0.8,en;q=0.7",
               "Accept-Encoding": "gzip, deflate, br"}
    proxy_ip = str(random.choice(proxy_list))
    proxy = {"http": "http://" + proxy_ip}

    url = "https://www.musixmatch.com/explore/genre/" + general + "/language/en/" + str(page)
    response = requests.get(url, headers=headers, proxies=proxy)
    html = BeautifulSoup(response.text)
    # print(html)

    # 抓取所有歌曲連結
    rs = html.find_all("h2", class_="media-card-title")
    for r in rs:
        turl = "https://www.musixmatch.com" + r.find("a")["href"]
        total.append(turl)
    print("頁數：", page, "\tURL數：", len(total))
    page += 1
    time.sleep(random.uniform(1.1, 5.4))

print("共URL數：", len(total))

# 歌曲資料抓取
count = 1
for u in total:
    print("筆數：", count)
    url = u

    user = random.choice(user_agents)
    headers = {'User-Agent': user,
               "Upgrade-Insecure-Requests": "1",
               "DNT": "1",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Accept-Language": "en-US;q=0.8,en;q=0.7",
               "Accept-Encoding": "gzip, deflate, br"}
    proxy_ip = str(random.choice(proxy_list))
    proxy = {"http": "http://" + proxy_ip}

    response = requests.get(url, headers=headers, proxies=proxy)
    html = BeautifulSoup(response.text)
    # print(html)

    print("\n歌名")
    try:
        s_name = html.find("h1", class_="mxm-track-title__track").text.strip("Lyrics")
        print(s_name)
    except:
        s_name = None

    # print("\n歌手")
    s_artist = html.find("a", class_="mxm-track-title__artist mxm-track-title__artist-link")
    # print(s_artist.text)

    # print("專輯")
    try:
        s_album = html.find("h2", class_="mui-cell__title").text
        # print(s_album)
    except:
        s_album = None

    # print("\n歌詞")
    try:
        ll = []
        s_lyric = html.find_all("p", class_="mxm-lyrics__content")
        lyric_type = html.find("p", class_="mxm-lyrics__content").find("span")["class"][0]
        if lyric_type == "lyrics__content__ok":
            print("ok")
            for j in s_lyric:
                lyric = j.find("span", class_="lyrics__content__ok")
                ll.append(lyric.text)
            l_combine = "\n".join(ll)
            # print(l_combine)

        if lyric_type == "lyrics__content__warning":
            print("warning")
            for j in s_lyric:
                lyric = j.find("span", class_="lyrics__content__warning")
                ll.append(lyric.text)
            l_combine = "\n".join(ll)
            # print(l_combine)

        if lyric_type == "lyrics__content__error":
            print("error")
            for j in s_lyric:
                lyric = j.find("span", class_="lyrics__content__error")
                ll.append(lyric.text)
            l_combine = "\n".join(ll)
            # print(l_combine)
    except:
        l_combine = None

    # print("\n作曲：")
    try:
        ww = []
        s_writter = html.find("div", class_="authors").find_all("a")
        # print(len(s_writter))
        for writter in s_writter:
            ww.append(writter.text)
        w_combine ="+".join(ww)
        # print(w_combine)
    except:
        w_combine = None

    saved = {"album":s_album,
             "artist":s_artist.text,
             "song":s_name,
             "lyric":l_combine,
             "witter":w_combine,
             "general":"country"}

    # 使用參數a，連續寫檔
    wf = open("country.json", "a", encoding="utf-8")
    json.dump(saved, wf)
    wf.write("\n")
    wf.close()

    # print(saved)
    count += 1
    # time.sleep(random.uniform(1.1, 5.4))

print("\nDone")

