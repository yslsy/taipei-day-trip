from flask import Flask,request,json,jsonify,render_template,redirect,session
import math
import mysql.connector
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

attrdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123321",
    database="taipeiattractions",
    charset="utf-8"
)
cursor = attrdb.cursor()

# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

# 取得景點資料列表
@app.route("/api/attractions", methods=["GET"])
def get_attractions():
	try:
		page = request.args.get("page",0)
		keyword = request.args.get("keyword","")
		pagetwo = int(page)
		next_page =  pagetwo + 1
		num = (pagetwo*12)
		sql = "SELECT * FROM attractions WHERE category = %s OR name LIKE CONCAT('%',%s,'%') ORDER BY id LIMIT %s,12" #
		cursor.execute(sql, (keyword,keyword,num))
		result = cursor.fetchall()
		newresult=[]
		for i in range(len(result)):
			id = result[i][0]
			name = result[i][1]
			category = result[i][2]
			description = result[i][3]
			address = result[i][4]
			transport = result[i][5]
			mrt = result[i][6]
			lat = result[i][7]
			lng = result[i][8]
			images = result[i][9]
			newresult1 = {
				"id":id,
				"name":name,
				"category":category,
				"description":description,
				"address":address,
				"transport":transport,
				"mrt":mrt,
				"lat":lat,
				"lng":lng,
				"images":eval(images)
			}
			newresult.append(newresult1)

		# 查詢nextpage
		sql = "SELECT * FROM attractions WHERE category = %s OR name LIKE CONCAT('%',%s,'%') ORDER BY id LIMIT %s,1"
		cursor.execute(sql, (keyword,keyword,num+12))
		result = cursor.fetchall()
		if result == []:
			next_page = None

	except Exception:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500

	return jsonify({
			"nextpage": next_page,
			"data": newresult
			})

# 根據景點標號取得景點資料
@app.route("/api/attraction/<int:attractionId>", methods=["GET"])
def get_attractions_byid(attractionId):
	sql = "SELECT * FROM attractions WHERE id = %s" 
	cursor.execute(sql, (attractionId,))
	result = cursor.fetchall()
	if result:
		newresult=[]
		for i in range(len(result)):
			id = result[i][0]
			name = result[i][1]
			category = result[i][2]
			description = result[i][3]
			address = result[i][4]
			transport = result[i][5]
			mrt = result[i][6]
			lat = result[i][7]
			lng = result[i][8]
			images = result[i][9]
			newresult1 = {
				"id":id,
				"name":name,
				"category":category,
				"description":description,
				"address":address,
				"transport":transport,
				"mrt":mrt,
				"lat":lat,
				"lng":lng,
				"images":eval(images)
			}
			newresult.append(newresult1)
		return jsonify({
				"data":newresult
			})

	elif (attractionId==0 or attractionId>len(result)) :
		return jsonify({
			"error":True,
			"message":"景點編號不正確"
		}), 400

	else:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500

# 取得景點分類名稱列表
@app.route("/api/categories", methods=["GET"])
def get_categories_list():
	try:
		sql = "SELECT DISTINCT category FROM attractions" 
		cursor.execute(sql)
		result = cursor.fetchall()
		result1=[]
		for i in range(len(result)):
			item = result[i][0]
			result1.append(item)
	except Exception:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500
	return jsonify({
			"data": result1
		})



app.run(port=3000)