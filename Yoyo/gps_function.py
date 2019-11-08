import serial
import os
import gpxpy.gpx
import folium
import pynmea2
import datetime
import matplotlib.pylab as plt
import time
import GCP_storge as gcp

id="yoyo"
# 定義在AWS上kafka的IP及topics
gps_location = "http://3.112.123.88:8082/topics/location"
gps_pace = "http://3.112.123.88:8082/topics/pace"
headers = { "Content-Type" : "application/vnd.kafka.json.v2+json" }
# 從port口取得GPS資料
ser = serial.Serial('/dev/ttyACM0', 9600)
# 開始運動時間
start = datetime.datetime.now()
# 以時間為此次運動紀錄檔案名稱
date = str(start.year)+str(start.month)+str(start.day)

# 傳送資料到kafka及儲存歷史紀錄曲線圖
def to_kafka_png():
    # 儲存原始gps訊號資料
    gps = open("gps"+name+".nmea","ab")
    # 累計型資料初始化
    distance = 0
    avg_pace = 0
    count = 0
    # 繪製紀錄圖座標初始化
    pace_list = []
    time_list = []
    distance_list = []
    while True:
        # 本次資料傳輸時間
        t = datetime.datetime.now()
        line = ser.readline()
        gps.write(line)
        # 將二位元資料轉為字串並用套件解析
        record = pynmea2.parse(str(line)[2:-5])
        # 取得緯度、精度及海拔
        if str(line)[5:8] == "GGA":
            Latitude = record.latitude
            Longitude = record.longitude
            Altitude = record.altitude
            # 製作傳送到kafka資料
            if Latitude != "" or Longitude != "" or Altitude != "":
                payload1 = {"records": [{"value": {"device_id": id, "timestamp": t, "Latitude": Latitude,
                                                   "Longitude": Longitude, "Altitude": Altitude}}]}
                # 傳送資料到kafka
                r1 = requests.post(gps1, data=json.dumps(payload1), headers=headers)
                if r1.status_code != 200:
                    print(r1.text)
        # 取得有關速度、距離資料
        elif str(line)[5:8] == "VTG":
            # 計算運動總時間、總距離
            now = datetime.datetime.now()
            diff = (now - start).seconds
            h = diff // 3600
            m = (diff % 3600) // 60
            s = diff % 60
            time_total = "{0:02d}:{1:02d}:{2:02d}".format(h, m, s)
            speed = float(str(line).split(",")[7])
            pace = round(60 / float(speed), 1)
            distance += round(speed * diff / 3600, 1)
            if speed != "":
                payload2 = {"records": [
                    {"value": {"device_id": id, "timestamp": t, "start": start.strftime("%Y-%m-%d %H:%M:%S"),
                               "pace": pace, "time_total": time_total, "diff": diff, "distance": distance}}]}
                r2 = requests.post(gps2, data=json.dumps(payload2), headers=headers)
                if r2.status_code != 200:
                    print(r2.text)
            count += 1
            avg_pace = (pace + avg_pace) / count
            # 繪製運動紀錄圖
            pace_list.append(pace)
            distance_list.append(distance)
            time_list.append(diff * 10)
            plt.subplot(2, 1, 1)
            plt.plot(time_list, pace_list)
            plt.ylabel("Pace")
            plt.subplot(2, 1, 2)
            plt.plot(time_list, distance_list)
            plt.ylabel("Distance")
            plt.xlabel("Time")
            plt.savefig('runarea' + name + '.png')
            print(time_list)

# 轉檔成gpx並上傳到Google Cloud Storage
def to_gpx():
    common = 'gpsbabel -i nmea -f gps' + name + '.nmea -o gpx -F gps' + name + '.gpx'
    os.system(common)
    gcp.upload_blob_gpx('gps' + name + '.gpx', 'gps' + name + '.gpx')

# 轉檔成路徑圖的html並上傳到Google Cloud Storage
def to_html():
    gpx_file = open('gps'+name+'.gpx', 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    ave_lat = sum(p[0] for p in points) / len(points)
    ave_lon = sum(p[1] for p in points) / len(points)
    # load map centred on average coordinates
    my_map = folium.Map(location=[ave_lat, ave_lon], zoom_start=14)
    # add a markers
    for each in points:
        folium.Marker(each).add_to(my_map)
    # add lines
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(my_map)
    # save map
    my_map.save("./gpx_tracker"+name+".html")
    # upload gpx file to google cloud storage
    gcp.upload_blob_html("gpx_tracker"+name+".html", "gpx_tracker"+name+".html")

# 紀錄曲線圖上傳到GCP
def upload_png():
    gcp.upload_blob_png('runarea' + name + '.png', 'runarea' + name + '.png')