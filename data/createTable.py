import json
import mysql.connector
import re

db_config = {
    "user":"root",
    "password":"jessica1225",
    "host":"localhost",
    "database":"taipei_day_trip"
}

# 檢查是否已有此table的fuction
def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    return cursor.fetchone() is not None

def create_attraction_table():
    conn =mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    table_name = "attractions"
    # 判斷是否已存在，已存在會return，不存在才繼續往下
    if table_exists(cursor, table_name):
        print(f"Table '{table_name}' already exists. Skipping table creation and data insertion.")
        return

    create_attraction_table_query = '''
    CREATE TABLE IF NOT EXISTS attractions(
        attraction_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        description LONGTEXT NOT NULL,
        address VARCHAR(255) NOT NULL,
        transport LONGTEXT NOT NULL,
        mrt VARCHAR(255),
        lat DECIMAL(10, 8),
        lng DECIMAL(11, 8),
        images JSON
    )
    '''
    cursor.execute(create_attraction_table_query)

    with open("taipei-attractions.json","r",encoding="utf-8") as file:
        data = json.load(file)

    insert_query = '''
    INSERT INTO attractions (name, category, description, address, transport, mrt, lat, lng, images)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    '''

    for attraction in data["result"]["results"]:
        file_urls = re.findall(r'(https?://[^\s]+?\.(?:jpg|png))', attraction['file'], re.IGNORECASE)
        values =(
            attraction["name"],
            attraction["CAT"],
            attraction["description"],
            attraction["address"],
            attraction["direction"],
            attraction["MRT"],
            float(attraction["latitude"],),
            float(attraction["longitude"],),
            json.dumps(file_urls)
        )
        
        try:
            cursor.execute(insert_query, values)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    print("景點table建立並賦值成功")
    conn.commit()

    cursor.close()
    conn.close()

def create_member_table():
    conn =mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    table_name = "member"
    # 判斷是否已存在，已存在會return，不存在才繼續往下
    if table_exists(cursor, table_name):
        print(f"Table '{table_name}' already exists. Skipping table creation and data insertion.")
        return
    
    create_member_table_query = '''
    CREATE TABLE IF NOT EXISTS member(
        member_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL COLLATE utf8mb4_bin UNIQUE,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cursor.execute(create_member_table_query)

    insert_query = '''
    INSERT INTO member (name, email, password)
    VALUES (%s, %s ,%s);
    '''
    test_members = [
        ("Jessica", "jessica@test.com", "$2b$12$/pZyEkAWTkNDnJP47LDF0OpbhJp1KyGpiOt.vGUlAWrGG8dn9MVna"),
        ("Hebe", "hebe@test.com", "$2b$12$5QkdVxz4CzAJ5fW/f27BQOLzBu2ZDr8fa8eQSTZD6VJH6eMC/z1bq")
    ]
    for member in test_members:
        cursor.execute(insert_query, member)

    print("會員table建立並賦值成功")
    conn.commit()

    cursor.close()
    conn.close()

def create_booking_table():
    conn =mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    table_name = "booking"
    # 判斷是否已存在，已存在會return，不存在才繼續往下
    if table_exists(cursor, table_name):
        print(f"Table '{table_name}' already exists. Skipping table creation and data insertion.")
        return
    
    create_booking_table_query = '''
    CREATE TABLE IF NOT EXISTS booking(
        booking_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_num VARCHAR(20) DEFAULT NULL,
        member_id BIGINT NOT NULL,
        attraction_id BIGINT NOT NULL,
        date VARCHAR(255) NOT NULL,
        time VARCHAR(255) NOT NULL,
        price VARCHAR(255) NOT NULL,
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'booking time',
        contact_name VARCHAR(255) DEFAULT NULL,
        contact_email VARCHAR(255) DEFAULT NULL,
        contact_phone VARCHAR(255) DEFAULT NULL,
        payment_status CHAR(1) NOT NULL DEFAULT 0 COMMENT '0 Unpaid/Payment failed, 1 Paid'
    )
    '''
    cursor.execute(create_booking_table_query)
    
    print("預約table建立成功")

    cursor.close()
    conn.close()

def create_payment_table():
    conn =mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    table_name = "payment"
    # 判斷是否已存在，已存在會return，不存在才繼續往下
    if table_exists(cursor, table_name):
        print(f"Table '{table_name}' already exists. Skipping table creation and data insertion.")
        return

    create_payment_table_query = '''
    CREATE TABLE IF NOT EXISTS payment(
        payment_id BIGINT PRIMARY KEY AUTO_INCREMENT,
        order_num VARCHAR(20) UNIQUE NOT NULL,
        create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        payment_status CHAR(1) NOT NULL COMMENT '0 Unpaid/Payment failed, 1 Paid',
        msg VARCHAR(255),
        bank_transaction_id VARCHAR(40),
        rec_trade_id VARCHAR(20)
    )
    '''
    cursor.execute(create_payment_table_query)
    print("付款table建立成功")

    cursor.close()
    conn.close()

# 主程式呼叫fuction
create_attraction_table()
create_member_table()
create_booking_table()
create_payment_table()



  