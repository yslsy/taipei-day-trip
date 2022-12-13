from flask import Flask,request,json,jsonify,render_template,redirect,url_for
from flask import *
import jwt
from datetime import datetime, timedelta
from mysql.connector import Error
from mysql.connector import pooling

app=Flask(
	__name__,
	static_folder="static",
	static_url_path="/"
	)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
app.config['SECRET_KEY'] = 'M\xe9\x98\x18\x94|\xca\xdf\xadg\xd31'

connection_pool = pooling.MySQLConnectionPool(
    pool_name="pynative_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",
    database="taipeiattractions",
    user="root",
    password="123321zz",
    charset="utf-8"
)

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
		sql = "SELECT * FROM attractions WHERE category = %s OR name LIKE CONCAT('%',%s,'%') ORDER BY id LIMIT %s,12"
		# Get connection object from a pool
		connection_object = connection_pool.get_connection()
		cursor = connection_object.cursor()
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
				"lat":float(lat),
				"lng":float(lng),
				"images":eval(images)
			}
			newresult.append(newresult1)

		# 查詢nextpage
		sql = "SELECT * FROM attractions WHERE category = %s OR name LIKE CONCAT('%',%s,'%') ORDER BY id LIMIT %s,1"
		cursor.execute(sql, (keyword,keyword,num+12))
		result = cursor.fetchall()
		if result == []:
			next_page = None

		return jsonify({
			"nextpage": next_page,
			"data": newresult
			})
	except Exception:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")
		

# 根據景點標號取得景點資料
@app.route("/api/attraction/<int:attractionId>", methods=["GET"])
def get_attractions_byid(attractionId):
	sql = "SELECT * FROM attractions WHERE id = %s"
	# Get connection object from a pool
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	cursor.execute(sql, (attractionId,))
	result = cursor.fetchall()
	try:
		if result:
			newresult = {
				"id":result[0][0],
				"name":result[0][1],
				"category":result[0][2],
				"description":result[0][3],
				"address":result[0][4],
				"transport":result[0][5],
				"mrt":result[0][6],
				"lat":float(result[0][7]),
				"lng":float(result[0][8]),
				"images":eval(result[0][9])
			}
			return jsonify({
				"data":newresult
			})
		elif (attractionId==0 or attractionId>len(result)) :
			return jsonify({
				"error":True,
				"message":"景點編號不正確"
			}), 400
	except Exception:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")
	

# 取得景點分類名稱列表
@app.route("/api/categories", methods=["GET"])
def get_categories_list():
	try:
		sql = "SELECT DISTINCT category FROM attractions"
		# Get connection object from a pool
		connection_object = connection_pool.get_connection()
		cursor = connection_object.cursor()
		cursor.execute(sql)
		result = cursor.fetchall()
		result1=[]
		for i in range(len(result)):
			item = result[i][0]
			result1.append(item)
		return jsonify({
			"data": result1
			})
	except Exception:
		return jsonify({
			"error":True,
			"message":"伺服器內部錯誤"
		}), 500
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")

# 註冊
@app.route("/api/user", methods=["POST"])
def user_signup():
	data = request.get_json()
	name = data["user"]
	email = data["email"]
	password = data["password"]
	try:
		sql = ("SELECT email FROM member WHERE email = %s")
		# Get connection object from a pool
		connection_object = connection_pool.get_connection()
		cursor = connection_object.cursor()
		cursor.execute(sql, (email,))
		check_email = cursor.fetchone()
		if check_email:
			return jsonify({
				"error": True,
				"message": "該信箱已被註冊"
			}), 400
		else:
			sql_insert = "INSERT INTO member(name,email,password)VALUES (%s, %s, %s)"
			val = (name, email, password)
			# Get connection object from a pool
			connection_object = connection_pool.get_connection()
			cursor = connection_object.cursor()
			cursor.execute(sql_insert, val)
			connection_object.commit()
			return jsonify({
				"ok": True
			}), 200
	except Exception:
		return jsonify({
			"error": True,
			"message": "伺服器內部錯誤"
		}), 500
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")

# 取得會員資訊
@app.route("/api/user/auth", methods=["GET"])
def user_state():
	get_token = request.cookies.get("token")
	# Get connection object from a pool
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		token_email = decodedtoken["email"]
		cursor.execute(("SELECT * FROM member WHERE email = %s"), (token_email, ))
		userdata = cursor.fetchone()
		if userdata:
			return jsonify({
				"data":{
					"id": userdata[0],
					"name": userdata[1],
					"email": userdata[3]
				}
			})
	except Exception:
		response = make_response({
			"error": True,
			"message": "伺服器內部錯誤"
		},500)
		response.set_cookie('token',"", max_age=-1)
		return response
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")

# 登入
@app.route("/api/user/auth", methods=["PUT"])
def user_login():
	data = request.get_json()
	email = data["email"]
	password = data["password"]
	# Get connection object from a pool
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	cursor.execute(("SELECT * FROM member WHERE email = %s and password = %s"), (email, password,))
	check_user = cursor.fetchone()
	try:
		if not check_user:
			return jsonify({
				"error": True,
				"message": "登入失敗，信箱或密碼錯誤"
			}), 400
		else:
			response = make_response({
				"ok": True
			}, 200)
			encodetoken = jwt.encode(
				{"email": data["email"],"exp": datetime.utcnow() + timedelta(days=7)},
				app.config['SECRET_KEY'],
				algorithm='HS256')
			response.set_cookie('token', encodetoken, max_age=604800)
			return response
	except Exception:
		return jsonify({
			"error": True,
			"message": "伺服器內部錯誤"
		}), 500
	finally:
		cursor.close()
		connection_object.close()
		# print("MySQL connection is closed")

# 登出
@app.route("/api/user/auth", methods=["DELETE"])
def user_logout():
	response = make_response({
				"ok": True
			}, 200)
	response.set_cookie('token',"", max_age=-1)
	return response

app.run(host='0.0.0.0',port=3000)