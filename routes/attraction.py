from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import mysql.connector
import json

from .config import connection_pool

router = APIRouter()

# 抓取所有景點資料，每頁12筆，景點名稱模糊搜尋/捷運站名稱搜尋
@router.get("/api/attractions")
async def get_attractions(page: int = Query(0,ge=0), keyword: str = Query(None)):
	attractions_per_page = 12
	offset = page * attractions_per_page

	conn = connection_pool.get_connection()
	cursor = conn.cursor(dictionary=True)

	try:
		# 所有景點資料
		base_query = "SELECT attraction_id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions"
		# 所有景點筆數
		count_query = "SELECT COUNT(*) AS total FROM attractions"

		# 條件
		conditions =[]
		# 參數
		params = []
		# 如果獲取到keyword值，加入搜索條件的sql語法，放入對應參數
		if keyword:
			conditions.append("(name LIKE %s OR mrt = %s)")
			params.extend([f"%{keyword}%", keyword])
		# 把條件合併到query中
		if conditions:
			base_query += " WHERE " + " AND ".join(conditions)
			count_query += " WHERE "  + " AND ".join(conditions)
		# 在跳過幾行(offset)後顯示幾行(limit/attractions_per_page)
		base_query += " LIMIT %s OFFSET %s"
		params.extend([attractions_per_page, offset])
		
		# 計算總筆數，params的最後兩個參數忽略(計算筆數不需要分頁)
		cursor.execute(count_query, params[:-2])
		total_items = cursor.fetchone()["total"]
		# 抓取(所有or有條件)景點資料，12筆為一頁
		cursor.execute(base_query, params)
		attractions = cursor.fetchall()

		# 在所有顯示過的筆數還沒到總筆數時，下一頁=當前頁數+1，否則為None
		next_page = page + 1 if offset + attractions_per_page < total_items else None

		if attractions:
			result ={
				"nextPage":next_page,
				"data":[
					{
						"id": attr["attraction_id"],
						"name": attr["name"],
						"category": attr["category"],
						"description": attr["description"],
						"address": attr["address"],
						"transport":attr["transport"],
						"mrt": attr["mrt"],
						# 需要特別處理經緯的格式，轉換為float
						"lat":float(attr["lat"]),
						"lng":float(attr["lng"]),
						# 如果images有值，轉換成列表；沒有值，返回空列表
						"images":json.loads(attr["images"]) if attr["images"] else []
					}
					for attr in attractions
				]
			}
		response = JSONResponse(content=result)
	
	# 如果錯誤回傳錯誤內容，status_code=500
	except mysql.connector.Error as e:
		error_message = str(e)
		show={
			"error": True,
			"message": error_message
		}
		response = JSONResponse(content=show, status_code=500)
	
	# 關閉連線
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response

# 抓取指定id的景點資料
@router.get("/api/attraction/{attractionId}")
async def get_attraction(attractionId: int):
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		id_query = "SELECT * FROM attractions WHERE attraction_id = %s"
		cursor.execute(id_query, (attractionId,))
		result = cursor.fetchone()
		
		if result:
			show ={
				"data":{
						"id": result["attraction_id"],
						"name": result["name"],
						"category": result["category"],
						"description": result["description"],
						"address": result["address"],
						"transport":result["transport"],
						"mrt": result["mrt"],
						"lat":float(result["lat"]),
						"lng":float(result["lng"]),
						"images":json.loads(result["images"]) if result["images"] else []
				}
			}
			response = JSONResponse(content=show)
		# 如果景點編號沒有查到資料，回傳對應的錯誤訊息，status_code=400
		else:
			show={
				"error": True,
				"message": "查無此景點編號"
			}
			response = JSONResponse(content=show, status_code=400)
	
	# 如果錯誤回傳錯誤內容，status_code=500
	except mysql.connector.Error as e:
		error_message = str(e)
		show={
			"error": True,
			"message": error_message
		}
		response = JSONResponse(content=show, status_code=500)
	
	# 關閉連線
	finally:
		if "cursor" in locals():
			cursor.close()
		if "conn" in locals():
			conn.close()
	
	return response
