import json
import mysql.connector
import re

db_config = {
    "user":"root",
    "password":"jessica1225",
    "host":"localhost",
    "database":"taipei_day_trip"
}

conn =mysql.connector.connect(**db_config)
cursor = conn.cursor()

create_table_query = '''
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
); 
'''
cursor.execute(create_table_query)

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
    
    cursor.execute(insert_query, values)

conn.commit()

cursor.close()
conn.close()

print("建立table並賦值成功")