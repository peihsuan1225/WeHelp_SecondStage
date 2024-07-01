from fastapi import *
from fastapi.responses import FileResponse
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import mysql.connector
# import mysql.connector.pooling
# import json
from fastapi.staticfiles import StaticFiles
# from passlib.hash import bcrypt
# import jwt
# from datetime import datetime, timedelta
# from pydantic import BaseModel
from typing import Any

app=FastAPI()
# router = APIRouter()

# # 資料庫的連線資訊
# db_config = {
#     "user":"root",
#     "password":"jessica1225",
#     "host":"localhost",
#     "database":"taipei_day_trip"
# }
# # 資料庫的connection_pool設定
# connection_pool = mysql.connector.pooling.MySQLConnectionPool(
# 	pool_name = "taipeiDayTrip_pool",
# 	pool_size = 5,
# 	**db_config
# )

# # JWT 秘鑰
# SECRET_KEY = "s1l2o2t5h"
# ALGORITHM = "HS256"

# security = HTTPBearer() 

app.mount("/static", StaticFiles(directory="static",html=True), name="static")

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# # 抓取所有景點資料，每頁12筆，景點名稱模糊搜尋/捷運站名稱搜尋
# @app.get("/api/attractions")
# async def get_attractions(page: int = Query(0,ge=0), keyword: str = Query(None)):
# 	attractions_per_page = 12
# 	offset = page * attractions_per_page

# 	conn = connection_pool.get_connection()
# 	cursor = conn.cursor(dictionary=True)

# 	try:
# 		# 所有景點資料
# 		base_query = "SELECT attraction_id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions"
# 		# 所有景點筆數
# 		count_query = "SELECT COUNT(*) AS total FROM attractions"

# 		# 條件
# 		conditions =[]
# 		# 參數
# 		params = []
# 		# 如果獲取到keyword值，加入搜索條件的sql語法，放入對應參數
# 		if keyword:
# 			conditions.append("(name LIKE %s OR mrt = %s)")
# 			params.extend([f"%{keyword}%", keyword])
# 		# 把條件合併到query中
# 		if conditions:
# 			base_query += " WHERE " + " AND ".join(conditions)
# 			count_query += " WHERE "  + " AND ".join(conditions)
# 		# 在跳過幾行(offset)後顯示幾行(limit/attractions_per_page)
# 		base_query += " LIMIT %s OFFSET %s"
# 		params.extend([attractions_per_page, offset])
		
# 		# 計算總筆數，params的最後兩個參數忽略(計算筆數不需要分頁)
# 		cursor.execute(count_query, params[:-2])
# 		total_items = cursor.fetchone()["total"]
# 		# 抓取(所有or有條件)景點資料，12筆為一頁
# 		cursor.execute(base_query, params)
# 		attractions = cursor.fetchall()

# 		# 在所有顯示過的筆數還沒到總筆數時，下一頁=當前頁數+1，否則為None
# 		next_page = page + 1 if offset + attractions_per_page < total_items else None

# 		if attractions:
# 			result ={
# 				"nextPage":next_page,
# 				"data":[
# 					{
# 						"id": attr["attraction_id"],
# 						"name": attr["name"],
# 						"category": attr["category"],
# 						"description": attr["description"],
# 						"address": attr["address"],
# 						"transport":attr["transport"],
# 						"mrt": attr["mrt"],
# 						# 需要特別處理經緯的格式，轉換為float
# 						"lat":float(attr["lat"]),
# 						"lng":float(attr["lng"]),
# 						# 如果images有值，轉換成列表；沒有值，返回空列表
# 						"images":json.loads(attr["images"]) if attr["images"] else []
# 					}
# 					for attr in attractions
# 				]
# 			}
# 		response = JSONResponse(content=result)
	
# 	# 如果錯誤回傳錯誤內容，status_code=500
# 	except mysql.connector.Error as e:
# 		error_message = str(e)
# 		show={
# 			"error": True,
# 			"message": error_message
# 		}
# 		response = JSONResponse(content=show, status_code=500)
	
# 	# 關閉連線
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response

# # 抓取指定id的景點資料
# @app.get("/api/attraction/{attractionId}")
# async def get_attraction(attractionId: int):
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		id_query = "SELECT * FROM attractions WHERE attraction_id = %s"
# 		cursor.execute(id_query, (attractionId,))
# 		result = cursor.fetchone()
		
# 		if result:
# 			show ={
# 				"data":{
# 						"id": result["attraction_id"],
# 						"name": result["name"],
# 						"category": result["category"],
# 						"description": result["description"],
# 						"address": result["address"],
# 						"transport":result["transport"],
# 						"mrt": result["mrt"],
# 						"lat":float(result["lat"]),
# 						"lng":float(result["lng"]),
# 						"images":json.loads(result["images"]) if result["images"] else []
# 				}
# 			}
# 			response = JSONResponse(content=show)
# 		# 如果景點編號沒有查到資料，回傳對應的錯誤訊息，status_code=400
# 		else:
# 			show={
# 				"error": True,
# 				"message": "查無此景點編號"
# 			}
# 			response = JSONResponse(content=show, status_code=400)
	
# 	# 如果錯誤回傳錯誤內容，status_code=500
# 	except mysql.connector.Error as e:
# 		error_message = str(e)
# 		show={
# 			"error": True,
# 			"message": error_message
# 		}
# 		response = JSONResponse(content=show, status_code=500)
	
# 	# 關閉連線
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response

# # 抓取所有捷運站名，按照週邊景點的數量由大到小排序	
# @app.get("/api/mrts")
# async def get_mrt_stations():
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		mrt__query="""
# 		SELECT mrt, COUNT(*) as attraction_count
# 		FROM attractions
# 		WHERE mrt IS NOT NULL
# 		GROUP BY mrt
# 		ORDER BY attraction_count DESC
# 		"""
# 		cursor.execute(mrt__query)
# 		result = cursor.fetchall()

		
# 		if result:
# 			mrt_stations =[row["mrt"] for row in result]
# 			response_data = {
# 				"data":mrt_stations
# 			}
# 		response = JSONResponse(content=response_data)

# 	# 如果錯誤回傳錯誤內容，status_code=500
# 	except mysql.connector.Error as e:
# 		error_message = str(e)
# 		show={
# 			"error": True,
# 			"message": error_message
# 		}
# 		response = JSONResponse(content=show, status_code=500)
	
# 	# 關閉連線
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response

# class signinRequest(BaseModel):
# 	name: str
# 	email: str
# 	password: str

# # 註冊會員，驗證email是否已存在
# @app.post("/api/user")
# async def sign_up(signupInput: signinRequest):
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		# 檢查email是否已存在
# 		check_email_exist_query='''
# 		SELECT * FROM member WHERE email = %s
# 		'''
# 		cursor.execute(check_email_exist_query, (signupInput.email,))
# 		result = cursor.fetchall()
		
# 		if result:
# 			response_data = {"error": True,  "message": "電子信箱已存在"}
# 			response = JSONResponse(content=response_data, status_code=400)
		
# 		# 建立新的會員資料
# 		elif not result:
# 			hashed_password = bcrypt.hash(signupInput.password)
# 			insert_query='''
# 			INSERT INTO member (name, email, password) VALUES (%s, %s, %s)
# 			'''
# 			cursor.execute(insert_query, (signupInput.name, signupInput.email, hashed_password))
# 			conn.commit()
# 			response_data = {"ok": True}
# 			response = JSONResponse(content=response_data, status_code=200)
# 	# 如果錯誤回傳錯誤內容，status_code=500
# 	except mysql.connector.Error as e:
# 		error_message = str(e)
# 		response_data = {"error": True,  "message": error_message}
# 		response = JSONResponse(content=response_data, status_code=500)
# 	# 關閉連線
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response

# class signinRequest(BaseModel):
# 	email: str
# 	password: str

# # 登入會員，取得JWT加密字串
# @app.put("/api/user/auth")
# async def sign_in(signinInput: signinRequest):
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)

# 		serach_member_query='''
# 		SELECT * FROM member WHERE email = %s COLLATE utf8mb4_bin
# 		'''
# 		cursor.execute(serach_member_query, (signinInput.email,))
# 		result = cursor.fetchone()

# 		if result and bcrypt.verify(signinInput.password, result["password"]):
# 			expiration = datetime.utcnow() + timedelta(days=7)
# 			payload = {
# 				"id": result["member_id"],
#     			"name": result["name"],
#    				"email": result["email"],
# 				"exp": expiration.timestamp()
# 			}
# 			token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
# 			response_data = {"token":token}
# 			response = JSONResponse(content=response_data, status_code=200)
# 		else:
# 			response_data = {"error":True, "message":"帳號或密碼錯誤"}
# 			response = JSONResponse(content=response_data, status_code=400)
# 	except mysql.connector.Error as e:
# 		error_message = str(e)
# 		response_data = {"error": True,  "message": error_message}
# 		response = JSONResponse(content=response_data, status_code=500)
	
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
# 	return response

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
# 	token =credentials.credentials
# 	try:
# 		payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
# 		return payload
# 	except jwt.ExpiredSignatureError:
# 		return
# 	except jwt.InvalidTokenError:
# 		return

# 取得當前登入的會員資訊
# @app.get("/api/user/auth")
# async def get_member_info(user: dict = Depends(get_current_user)):
# 	if user:
# 		return{
# 			"data":{
# 				"id":user["id"],
# 				"name":user["name"],
# 				"email": user["email"]
# 			}
# 		}
# 	return{"data": None}

# # 取得尚未確認下單的預定行程
# @app.get("/api/booking")
# async def get_uncheckBooking(user: dict = Depends(get_current_user)):
# 	if not user:
# 		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
# 		response = JSONResponse(content=response_data, status_code=403)
# 		print("no user info")
# 		return
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		get_booking_info_query='''
# 		SELECT * FROM booking WHERE member_id = %s
# 		'''
# 		cursor.execute(get_booking_info_query, (user["id"],))
# 		booking_result = cursor.fetchone()

# 		if booking_result:
# 			get_booking_attraction_query = '''
# 			SELECT * FROM attractions WHERE attraction_id = %s
# 			'''
# 			cursor.execute(get_booking_attraction_query, (booking_result["attraction_id"],))
# 			attraction_result = cursor.fetchone()
# 			response_data = {
# 				"data": {
# 					"attraction":{
# 						"id": booking_result["attraction_id"],
# 						"name": attraction_result["name"],
# 						"address": attraction_result["address"],
# 						"image": json.loads(attraction_result["images"])[0]
# 					},
# 					"date": booking_result["date"],
# 					"time": booking_result["time"],
# 					"price": booking_result["price"]
# 				}
# 			}
# 			response = JSONResponse(content=response_data, status_code=200)
# 		if not booking_result:
# 			response_data = None
# 			response = JSONResponse(content=response_data, status_code=200)
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response


# class bookingRequest(BaseModel):
# 	attractionId: Any
# 	date: Any
# 	time: Any
# 	price: Any
	
# # 建立新的預定行程
# @app.post("/api/booking")
# async def new_booking(bookInfo:bookingRequest, user: dict = Depends(get_current_user)):
# 	if not user:
# 		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
# 		response = JSONResponse(content=response_data, status_code=403)
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		# 檢查是否已有預定資料
# 		check_booking_info_query='''
# 		SELECT * FROM booking WHERE member_id = %s
# 		'''
# 		cursor.execute(check_booking_info_query, (user["id"],))
# 		result = cursor.fetchone()
# 		print("檢查user是否已有booking:" + str(result))

# 		if result:
# 			change_booking_info_query='''
# 			UPDATE booking
# 			SET attraction_id = %s, date = %s, time = %s, price = %s
# 			WHERE member_id = %s
# 			'''
# 			cursor.execute(change_booking_info_query, (bookInfo.attractionId, bookInfo.date, bookInfo.time, bookInfo.price, user["id"]))
# 			conn.commit()
# 			response_data = {"ok": True}
# 			response = JSONResponse(content=response_data, status_code=200)
# 		if not result:
# 			add_booking_info_query='''
# 			INSERT INTO booking (member_id, attraction_id, date, time, price) VALUES (%s, %s, %s, %s, %s)
# 			'''
# 			cursor.execute(add_booking_info_query, (user["id"], bookInfo.attractionId, bookInfo.date, bookInfo.time, bookInfo.price))
# 			conn.commit()
# 			response_data = {"ok": True}
# 			response = JSONResponse(content=response_data, status_code=200)
# 	except ValueError as e:
# 		response_data = {"error": True, "message":str(e)}
# 		response = JSONResponse(content=response_data, status_code=400)
# 	except Exception as e:
# 		response_data = {"error": True, "message":str(e)}
# 		response = JSONResponse(content=response_data, status_code=500)
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response

# # 刪除目前的預定行程
# @app.delete("/api/booking")
# async def delete_booking(user: dict = Depends(get_current_user)):
# 	if not user:
# 		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
# 		response = JSONResponse(content=response_data, status_code=403)
# 	try:
# 		conn = connection_pool.get_connection()
# 		cursor = conn.cursor(dictionary=True)
# 		delete_booking_query='''
# 		DELETE FROM booking
# 		WHERE member_id = %s
# 		'''
# 		cursor.execute(delete_booking_query, (user["id"],))
# 		conn.commit()
# 		response_data = {"ok": True}
# 		response = JSONResponse(content=response_data, status_code=200)
# 	finally:
# 		if "cursor" in locals():
# 			cursor.close()
# 		if "conn" in locals():
# 			conn.close()
	
# 	return response