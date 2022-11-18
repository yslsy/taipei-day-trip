import json
import mysql.connector
import re

src="taipei-attractions.json"
with open(src, encoding="utf-8") as file:
    data = json.load(file)
attractions=data["result"]["results"]

# 建立 MySQL 連線
attrdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123321",
    database="taipeiattractions",
    charset="utf-8"
)
cursor = attrdb.cursor()

for item in attractions:
    id = item["_id"]
    name = item["name"]
    category = item["CAT"]
    description = item["description"]
    address = item["address"]
    transport = item["direction"]
    mrt = item["MRT"]
    lat = item["latitude"]
    lng = item["longitude"]
    # 圖片
    pic_list1 = item["file"].split("https://")
    regex = re.compile(r".jpg|.JPG")
    pic_list2 = [i for i in pic_list1 if regex.search(i)] # 篩選格式
    images = []
    for i in pic_list2:
        images.append("https://"+i)
    images = str(images)
    # 存進 TABLE 
    sql = ("INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng, images) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    val = (id, name, category, description, address, transport, mrt, lat, lng, images)
    cursor.execute(sql, val)
attrdb.commit()

