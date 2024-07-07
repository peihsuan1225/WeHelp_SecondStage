from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from passlib.hash import bcrypt
from pydantic import BaseModel
from datetime import datetime, timedelta
import mysql.connector
import jwt

from .config import connection_pool
from .utils import get_current_user, SECRET_KEY, ALGORITHM

router = APIRouter()

class signupRequest(BaseModel):
	name: str
	email: str
	password: str
	
class signinRequest(BaseModel):
	email: str
	password: str
	
# 註冊會員，驗證email是否已存在
@router.post("/api/user")
async def sign_up(signupInput: signupRequest):
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		# 檢查email是否已存在
		check_email_exist_query='''
		SELECT * FROM member WHERE email = %s
		'''
		cursor.execute(check_email_exist_query, (signupInput.email,))
		result = cursor.fetchall()
		
		if result:
			response_data = {"error": True,  "message": "電子信箱已存在"}
			response = JSONResponse(content=response_data, status_code=400)
		
		# 建立新的會員資料
		elif not result:
			hashed_password = bcrypt.hash(signupInput.password)
			insert_query='''
			INSERT INTO member (name, email, password) VALUES (%s, %s, %s)
			'''
			cursor.execute(insert_query, (signupInput.name, signupInput.email, hashed_password))
			conn.commit()
			response_data = {"ok": True}
			response = JSONResponse(content=response_data, status_code=200)
	# 如果錯誤回傳錯誤內容，status_code=500
	except mysql.connector.Error as e:
		error_message = str(e)
		response_data = {"error": True,  "message": error_message}
		response = JSONResponse(content=response_data, status_code=500)
	# 關閉連線
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response

# 登入會員，取得JWT加密字串
@router.put("/api/user/auth")
async def sign_in(signinInput: signinRequest):
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)

		serach_member_query='''
		SELECT * FROM member WHERE email = %s COLLATE utf8mb4_bin
		'''
		cursor.execute(serach_member_query, (signinInput.email,))
		result = cursor.fetchone()

		if result and bcrypt.verify(signinInput.password, result["password"]):
			expiration = datetime.utcnow() + timedelta(days=7)
			payload = {
				"id": result["member_id"],
    			"name": result["name"],
   				"email": result["email"],
				"exp": expiration.timestamp()
			}
			token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
			response_data = {"token":token}
			response = JSONResponse(content=response_data, status_code=200)
		else:
			response_data = {"error":True, "message":"帳號或密碼錯誤"}
			response = JSONResponse(content=response_data, status_code=400)
	except mysql.connector.Error as e:
		error_message = str(e)
		response_data = {"error": True,  "message": error_message}
		response = JSONResponse(content=response_data, status_code=500)
	
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	return response

# 取得當前登入的會員資訊
@router.get("/api/user/auth")
async def get_member_info(user: dict = Depends(get_current_user)):
	if user:
		return{
			"data":{
				"id":user["id"],
				"name":user["name"],
				"email": user["email"]
			}
		}
	return{"data": None}