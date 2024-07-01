from fastapi import APIRouter
from fastapi.responses import JSONResponse
import mysql.connector

from .config import connection_pool

router = APIRouter()

# 抓取所有捷運站名，按照週邊景點的數量由大到小排序	
@router.get("/api/mrts")
async def get_mrt_stations():
	try:
		conn = connection_pool.get_connection()
		cursor = conn.cursor(dictionary=True)
		mrt__query="""
		SELECT mrt, COUNT(*) as attraction_count
		FROM attractions
		WHERE mrt IS NOT NULL
		GROUP BY mrt
		ORDER BY attraction_count DESC
		"""
		cursor.execute(mrt__query)
		result = cursor.fetchall()

		
		if result:
			mrt_stations =[row["mrt"] for row in result]
			response_data = {
				"data":mrt_stations
			}
		response = JSONResponse(content=response_data)

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