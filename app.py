from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
import mysql.connector.pooling
import json
app=FastAPI()

db_config = {
    "user":"root",
    "password":"jessica1225",
    "host":"localhost",
    "database":"taipei_day_trip"
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
	pool_name = "taipeiDayTrip_pool",
	pool_size = 5,
	**db_config
)

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

@app.get("/api/attractions")
async def get_attractions(page: int = Query(0,ge=0), keyword: str = Query(None)):
	attractions_per_page = 12
	offset = page * attractions_per_page

	conn = connection_pool.get_connection()
	cursor = conn.cursor(dictionary=True)

	try:
		base_query = "SELECT attraction_id, name, category, description, address, transport, mrt, lat, lng, images FROM attractions"
		count_query = "SELECT COUNT(*) AS total FROM attractions"

		conditions =[]
		params = []
		if keyword:
			conditions.append("(name LIKE %s OR mrt = %s)")
			params.extend([f"%{keyword}%", keyword])

		if conditions:
			base_query += " WHERE " + " AND ".join(conditions)
			count_query += " WHERE "  + " AND ".join(conditions)

		base_query += " LIMIT %s OFFSET %s"
		params.extend([attractions_per_page, offset])

		cursor.execute(count_query, params[:-2])
		total_items = cursor.fetchone()["total"]

		cursor.execute(base_query, params)
		attractions = cursor.fetchall()

		next_page = page + 1 if offset + attractions_per_page < total_items else None

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
					"lat":float(attr["lat"]),
					"lng":float(attr["lng"]),
					"images":json.loads(attr["images"]) if attr["images"] else []
				}
				for attr in attractions
			]
		}

		return JSONResponse(content=result)
	
	finally:
		cursor.close()
		conn.close()

@app.get("/api/attractions/{attractionId}")
async def get_attraction(attractionId: int):
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
	else:
		show={
			"error":True,
			"message":"查無此景點編號"
		}

	cursor.close()
	conn.close()
	
	return JSONResponse(content=show)

	
@app.get("/api/mrts")
async def get_mrt_stations():
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

	print(result)
	if result:
		mrt_stations =[row["mrt"] for row in result]
		response_data = {
			"data":mrt_stations
		}
	else:
		response_data = {
			"error": True,
  			"message": "查詢出錯"
		}

	cursor.close()
	conn.close()

	return JSONResponse(content=response_data)
