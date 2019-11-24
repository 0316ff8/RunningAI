from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

total = []
count = 1
page = 50
while page > 0:
    print("目前第幾頁?", page)
    url = "https://www.lyrics.com/genres.php?genre=Hip+Hop&p=" + str(page)
    print(url)
    try:
        response = urlopen(url)
    except:
        print("應該是到底了吧")
        break

    html = BeautifulSoup(response)

    rs = html.find_all("div", class_="lyric-meta col-sm-6 col-xs-6")
    # print(len(rs))

    for r in rs:
        s_number = r.find("p", class_="lyric-meta-title").find("a")["href"]
        url_pop = "https://www.lyrics.com" + s_number
        #print(url_save)
        total.append(url_pop)
        #print(len(total))

    page = page - 1
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



    saved = {"album":aa,
             "artist":s_artist.text,
             "song":s_name.text,
             "lyric":s_lyric.text,
             "witter":ww,
             "general":genre,
             "style":style}

    wf = open("HipHop.json", "a", encoding="utf-8")
    json.dump(saved, wf)
    wf.write("\n")
    wf.close()
    print(count)
    count = count + 1
    # print(saved)


print("\nDone")