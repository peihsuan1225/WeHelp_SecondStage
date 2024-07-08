from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from pydantic import BaseModel
import json
from datetime import datetime, timezone, timedelta


from .config import connection_pool
from .utils import get_current_user

router = APIRouter()

# 取得尚未確認下單的預定行程
@router.get("/api/booking")
async def get_uncheckBooking(user: dict = Depends(get_current_user)):
	if not user:
		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
		response = JSONResponse(content=response_data, status_code=403)
		print("no user info")
		return
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		get_booking_info_query='''
		SELECT * FROM booking WHERE member_id = %s AND payment_status = %s
		'''
		cursor.execute(get_booking_info_query, (user["id"],0))
		booking_result = cursor.fetchone()

		if booking_result:
			get_booking_attraction_query = '''
			SELECT * FROM attractions WHERE attraction_id = %s
			'''
			cursor.execute(get_booking_attraction_query, (booking_result["attraction_id"],))
			attraction_result = cursor.fetchone()
			response_data = {
				"data": {
					"attraction":{
						"id": booking_result["attraction_id"],
						"name": attraction_result["name"],
						"address": attraction_result["address"],
						"image": json.loads(attraction_result["images"])[0]
					},
					"date": booking_result["date"],
					"time": booking_result["time"],
					"price": booking_result["price"]
				}
			}
			response = JSONResponse(content=response_data, status_code=200)
		if not booking_result:
			response_data = None
			response = JSONResponse(content=response_data, status_code=200)
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response


class bookingRequest(BaseModel):
	attractionId: str
	date: str
	time: str
	price: str
	
# 建立新的預定行程
@router.post("/api/booking")
async def new_booking(bookInfo:bookingRequest, user: dict = Depends(get_current_user)):
	if not user:
		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
		response = JSONResponse(content=response_data, status_code=403)
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		# 檢查是否已有預定資料
		check_booking_info_query='''
		SELECT * FROM booking
		WHERE member_id = %s AND payment_status = %s
		'''
		cursor.execute(check_booking_info_query, (user["id"], 0))
		result = cursor.fetchone()

		if result:
			tz = timezone(timedelta(hours=+8))
			current_time = datetime.now(tz)
			
			change_booking_info_query='''
			UPDATE booking
			SET attraction_id = %s, date = %s, time = %s, price = %s, create_at = %s    
			WHERE member_id = %s AND payment_status = %s
			'''
			cursor.execute(change_booking_info_query, (bookInfo.attractionId, bookInfo.date, bookInfo.time, bookInfo.price, current_time, user["id"], 0))
			conn.commit()
			response_data = {"ok": True}
			response = JSONResponse(content=response_data, status_code=200)
		if not result:
			tz = timezone(timedelta(hours=+8))
			current_time = datetime.now(tz)
			add_booking_info_query='''
			INSERT INTO booking (member_id, attraction_id, date, time, price, create_at) VALUES (%s, %s, %s, %s, %s, %s)
			'''
			cursor.execute(add_booking_info_query, (user["id"], bookInfo.attractionId, bookInfo.date, bookInfo.time, bookInfo.price, current_time))
			conn.commit()
			response_data = {"ok": True}
			response = JSONResponse(content=response_data, status_code=200)
	except ValueError as e:
		response_data = {"error": True, "message":str(e)}
		response = JSONResponse(content=response_data, status_code=400)
	except Exception as e:
		response_data = {"error": True, "message":str(e)}
		response = JSONResponse(content=response_data, status_code=500)
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response

# 刪除目前的預定行程
@router.delete("/api/booking")
async def delete_booking(user: dict = Depends(get_current_user)):
	if not user:
		response_data = {"error": True, "message": "未登入系統，拒絕存取"}
		response = JSONResponse(content=response_data, status_code=403)
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		delete_booking_query='''
		DELETE FROM booking
		WHERE member_id = %s AND payment_status = %s
		'''
		cursor.execute(delete_booking_query, (user["id"], 0))
		conn.commit()
		response_data = {"ok": True}
		response = JSONResponse(content=response_data, status_code=200)
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response