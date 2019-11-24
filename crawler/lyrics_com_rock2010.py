from urllib.request import urlopen
from bs4 import BeautifulSoup
import json
import pymongo
import time
import random
import requests

# year = 1990
# general = "Rock"
total = []
count = 1
page = 200

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

# proxy_list = ['103.20.204.104:80', '102.129.249.67:3129', '80.211.31.121:3128',
#               '180.183.244.193:8213', '47.89.49.187:80', '45.77.56.114:30205',
#               '142.93.145.70:80', '165.22.33.143:8080', '13.78.116.29:80',
#               '83.239.86.150:80', '159.138.1.185:80', '202.85.52.151:80',
#               '211.23.2.54:3128', '60.248.199.206:80', '118.163.96.167:3129',
#               '36.228.215.213:3128', '123.110.185.95:8888', '114.37.194.87:3128',
#               '159.138.3.119:80', '159.138.1.185:80', '45.125.192.158:80',
#               '159.138.21.170:80', '159.138.22.112:80']


# client = pymongo.MongoClient(host='mongodb://192.168.20.145', port=27017)
# db = client['db103']
# collection = db['Rock']

while page > 0:
    user = random.choice(user_agents)
    headers = {'User-Agent': user,
               "Upgrade-Insecure-Requests": "1",
               "DNT": "1",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
               "Accept-Language": "en-US;q=0.8,en;q=0.7",
               "Accept-Encoding": "gzip, deflate, br"}
    # proxy_ip = str(random.choice(proxy_list))
    # proxy = {"http": "http://" + proxy_ip}

    print("目前第幾頁?", page)
    url = "https://www.lyrics.com/genres.php?genre=Rock&p=" + str(page) + "&dec=2010"
    print(url)

    response = requests.get(url, headers=headers)
    html = BeautifulSoup(response.text)
    # print(html)

    rs = html.find_all("div", class_="lyric-meta col-sm-6 col-xs-6")
    # print(len(rs))

    for r in rs:
        s_number = r.find("p", class_="lyric-meta-title").find("a")["href"]
        url_pop = "https://www.lyrics.com" + s_number
        #print(url_save)
        total.append(url_pop)
        # print(len(total))

    # time.sleep(random.uniform(1.1, 5.4))
    page = page - 1
    print(len(total))
print(len(total))



for u in total:
    url = u
    try:
        response = urlopen(url)
    except:
        print("不見了")
        continue

    html = BeautifulSoup(response)

    try:
        s_name = html.find("h1", class_="lyric-title")
        print("歌名：", s_name.text)
    except:
        print("無資料")
        continue

    try:
        s_album = html.find_all("hgroup", class_="clearfix")[1].find("a")
        aa = s_album.text
        # print("專輯名稱：", aa)
    except:
        aa = None
        # print("專輯名稱：", aa)

    s_artist = html.find("h3", class_="lyric-artist").find("a")
    #print("歌手：", s_artist.text)

    try:
        s_year = html.find("dd", class_="dd-margin").text
        # print("年份：", s_year.text)
    except:
        s_type = None

    s_lyric = html.find("pre", id="lyric-body-text")
    #print("歌詞：\n", s_lyric.text)
    try:
        s_written = html.find("div", class_="lyric-credits clearfix").find_all("p")[1]
        ww = s_written.text
        # print("\n作詞者：", ww)
    except:
        ww = None
        # print("\n作詞者：", ww)

    try:
        cata = (html.find_all("div", class_="lyric-infobox clearfix"))[1]
        # print(cata)
        s_type = cata.find_all("div", class_="col-sm-6")
        # print("長度：", len(s_type))
        if len(s_type) == 2:
            genre = s_type[0].find("div").text.strip('\n').rstrip()
            # print(len(genre))
            # print("類別：", genre)

            style = s_type[1].find("div").text.strip('\n').rstrip()
            # print(len(style))
            # print("風格：", style)
        else:
            genre = s_type[0].find("div").text.strip('\n').rstrip()
            style = None
            # print(len(genre))
            # print("類別：", genre)
    except:
        genre = None
        style = None



    saved = {"song":s_name.text,
             "artist":s_artist.text,
             "album":aa,
             "year":s_year,
             "lyric":s_lyric.text,
             "witter":ww,
             "general":genre,
             "style":style}

    wf = open("rock2010_100.json", "a", encoding="utf-8")
    json.dump(saved, wf)
    wf.write("\n")
    wf.close()
    print(count)
    count = count + 1
    # print(saved)

    # result = collection.insert_one(saved)

print("\nDone")