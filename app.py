from flask import Flask,request,json,jsonify,render_template,redirect,url_for
from flask import *
import jwt,requests
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

# 取得尚未確認下單的預定行程
@app.route("/api/booking", methods=["GET"])
def get_bookingdata():
	#驗證是否登入
	get_token = request.cookies.get("token")
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		sql = "SELECT attractionId, name, address, images, date, time, price FROM booking INNER JOIN attractions ON booking.attractionId = attractions.id"
		cursor.execute(sql)
		result = cursor.fetchone()
		if result:
			return jsonify({
				"data": {
					"attraction": {
						"id": result[0],
						"name": result[1],
						"address": result[2],
						"image": eval(result[3])
					},
					"date": result[4],
					"time": result[5],
					"price": result[6]
				}
			})
		return jsonify({
			"data": None
		})
	except Exception:
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}), 403
	finally:
		cursor.close()
		connection_object.close()


# 建立新的預定行程
@app.route("/api/booking", methods=["POST"])
def built_booking():
	data = request.get_json()
	attractionId = data["attractionId"]
	date = data["date"]
	time = data["time"]
	price = data["price"]
	print(price)
	# 驗證是否登入
	get_token = request.cookies.get("token")
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		try:
			if (attractionId == ""):
				return jsonify({
					"error": True,
					"message": "景點編號錯誤"
				}), 400
			elif(date == ""):
				return jsonify({
					"error": True,
					"message": "未選擇日期"
				}), 400
			else:
				cursor.execute("SELECT * FROM booking")
				check_bookingdata = cursor.fetchone()
				print(check_bookingdata)
				print(attractionId, date, time, price)
				if check_bookingdata:
					sql = "UPDATE booking SET attractionId=%s,date=%s,time=%s,price=%s WHERE id = 1"
					val = (attractionId, date, time, price)
					cursor.execute(sql, val)
					connection_object.commit()
					return jsonify({
						"ok": True
					}),200
				else:
					sql = "INSERT INTO booking(id, attractionId, date, time, price)VALUES(%s, %s, %s, %s, %s)"
					val = ("1", attractionId, date, time, price)
					cursor.execute(sql, val)
					connection_object.commit()
					return jsonify({
							"ok": True
						}),200
		except Exception:
			return jsonify({
				"error": True,
				"message": "伺服器內部錯誤"
			}), 500
	except Exception:
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}), 403
	finally:
		cursor.close()
		connection_object.close()
		print("MySQL connection is /api/booking, methods=POST")
		

# 刪除目前的預定行程
@app.route("/api/booking", methods=["DELETE"])
def delete_booking():
	# 驗證是否登入
	get_token = request.cookies.get("token")
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		cursor.execute("DELETE FROM booking WHERE id = 1")
		connection_object.commit()
		return jsonify({
				"ok": True
			}),200
	except Exception:
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}), 403
	finally:
		cursor.close()
		connection_object.close()

# 建立付款訂單
@app.route("/api/orders", methods=["POST"])
def postorder():
	# 驗證是否登入
	get_token = request.cookies.get("token")
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		data = request.get_json()

		order_data = json.dumps({
			"prime": data["prime"],
			"partner_key": "partner_60PDKZgTe5l1pacxWdikqvHAlvV8ExWhRKgxiIKagwhNcwc8MyfIoGEy",
			"merchant_id": "yslsy224_CTBC",
			"amount": data["order"]["price"],
			"currency": "TWD",
			"details": "order test",
			"cardholder": {
				"phone_number": data["order"]["contact"]["phone"],
				"name": data["order"]["contact"]["name"],
				"email": data["order"]["contact"]["email"],
			},
			"order_number": datetime.now().strftime("%Y%m%d%H%M%S"),
			"remember": False
    	})
		headers = {
			"Content-Type": "application/json",
			"x-api-key": "partner_60PDKZgTe5l1pacxWdikqvHAlvV8ExWhRKgxiIKagwhNcwc8MyfIoGEy"
		}
		response = requests.post("https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime", data = order_data, headers = headers)
		print(response.json())
		try:
			# 付款成功
			if response.json()["status"] == 0:
				order_detail = {
					"useremail": decodedtoken["email"],
					"ordernumber": response.json()["order_number"],
					"price": response.json()["amount"],
					"attrid": data["order"]["trip"]["attraction"]["id"],
					"attrname": data["order"]["trip"]["attraction"]["name"],
					"attraddress": data["order"]["trip"]["attraction"]["address"],
					"attrimage": data["order"]["trip"]["attraction"]["image"],
					"orderdate": data["order"]["trip"]["date"],
					"ordertime": data["order"]["trip"]["time"],
					"contactname":  data["order"]["contact"]["name"],
					"contactemail": data["order"]["contact"]["email"],
					"contactphone": data["order"]["contact"]["phone"],
					"status": 1
				}
				sql = "INSERT INTO payedorder(useremail, ordernumber, price, attrid, attrname, attraddress, attrimage, orderdate, ordertime, contactname, contactemail, contactphone, status)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				val = (order_detail["useremail"], order_detail["ordernumber"], order_detail["price"], order_detail["attrid"], order_detail["attrname"], order_detail["attraddress"], order_detail["attrimage"], order_detail["orderdate"], order_detail["ordertime"], order_detail["contactname"], order_detail["contactemail"], order_detail["contactphone"], order_detail["status"])
				cursor.execute(sql, val)
				connection_object.commit()
				return jsonify({
					"data": {
						"number": response.json()["order_number"],
						"payment": {
							"status": 0,
							"message": "付款成功"
						}
					}
				}), 200
			else:
				return jsonify({
					"error": true,
					"data": {
						"number": response.json()["order_number"],
						"payment": {
							"status": response.json().get("status", "無法取得status的值"),
							"message": "付款失敗"
						}
					}
				}), 400
		except Exception as e:
			print(e)
			return jsonify({
				"error": True,
				"message": "伺服器內部錯誤"
			}), 500
	except Exception as e:
		print(e)
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}), 403
	finally:
		cursor.close()
		connection_object.close()

@app.route("/api/order/<int:orderNumber>", methods=["GET"])
def getorder(orderNumber):
	# 驗證是否登入
	get_token = request.cookies.get("token")
	connection_object = connection_pool.get_connection()
	cursor = connection_object.cursor()
	try:
		decodedtoken = jwt.decode(get_token, app.config['SECRET_KEY'], algorithms=['HS256'])
		cursor.execute(f"SELECT * FROM payedorder WHERE ordernumber='{orderNumber}'")
		payed_orderdata = cursor.fetchone()
		return jsonify({
			"data":{
				"number": payed_orderdata[1],
				"price": payed_orderdata[2],
				"trip": {
					"attraction": {
						"id": payed_orderdata[3],
						"name": payed_orderdata[4],
						"address": payed_orderdata[5],
						"image": payed_orderdata[6],
					},
					"date": payed_orderdata[7],
					"time": payed_orderdata[8],
				},
				"contact": {
					"name": payed_orderdata[9],
					"email": payed_orderdata[10],
					"phone": payed_orderdata[11],
				},
				"status": payed_orderdata[12]
			}
		})
	except Exception as e:
		print(e)
		return jsonify({
			"error": True,
			"message": "未登入系統，拒絕存取"
		}), 403
	finally:
		cursor.close()
		connection_object.close()




app.run(host='0.0.0.0',port=3000)