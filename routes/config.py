import mysql.connector.pooling

# 資料庫的連線資訊
db_config = {
    "user":"root",
    "password":"jessica1225",
    "host":"localhost",
    "database":"taipei_day_trip"
}

# 資料庫的connection_pool設定
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
	pool_name = "taipeiDayTrip_pool",
	pool_size = 5,
	**db_config
)