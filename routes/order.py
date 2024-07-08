from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from pydantic import BaseModel
import json
from datetime import datetime, timezone, timedelta
import random
import requests

from .config import connection_pool
from .utils import get_current_user

router = APIRouter()

def generate_order_number():
    tz = timezone(timedelta(hours=+8))
    current_time = datetime.now(tz)
    random_num = random.randint(10, 99)
    return current_time.strftime("%Y%m%d%H%M") + str(random_num)

class Attraction(BaseModel):
    id: int
    name: str
    address: str
    image: str

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class Trip(BaseModel):
    attraction: Attraction
    date: str
    time: str

class Order(BaseModel):
    price: int
    trip: Trip
    contact: Contact

class orderRequest(BaseModel):
    prime: str
    order: Order

# 建立訂單編號並付款
@router.post("/api/orders")
async def new_order(orderInfo: orderRequest, user: dict = Depends(get_current_user)):
    if not user:
        response_data = {"error": True, "message": "未登入系統，拒絕存取"}
        response = JSONResponse(content=response_data, status_code=403)
    try:
        conn = connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        contant =  orderInfo.order.contact
        order_num_need_check = True
        while order_num_need_check:
            order_num = generate_order_number()
            check_orderNum_exists = '''
            SELECT * FROM booking WHERE order_num = %s
            '''
            cursor.execute(check_orderNum_exists, (order_num,))
            result = cursor.fetchone()
            if result:
                continue
            if not result:
                order_num_need_check = False
                break

        create_order_query = '''
        UPDATE booking
        SET order_num = %s, contact_name = %s, contact_email = %s, contact_phone = %s
        WHERE member_id = %s AND payment_status = %s
        '''
        cursor.execute(create_order_query, (order_num, contant.name, contant.email, contant.phone, user["id"], 0))
        conn.commit()

        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'partner_u2mylpNUnRvGdA1u3gJaJVji5PKqfQICP8PnBmYDgLJbM2yCi09Slzf3'
        }

        payload = {
            "prime": orderInfo.prime,  
            "partner_key": "partner_u2mylpNUnRvGdA1u3gJaJVji5PKqfQICP8PnBmYDgLJbM2yCi09Slzf3",  # 請填入你的合作夥伴金鑰
            "merchant_id": "WHPH1225_CTBC",
            "details": "TapPay測試",
            "amount": orderInfo.order.price,
            "order_number": order_num,
            "cardholder": {
                "phone_number": contant.phone,
                "name": contant.name,
                "email": contant.email,
                "zip_code": "",
                "address": "",
                "national_id": ""
            }
        }

        x = requests.post(url, json = payload, headers = headers)
        tappay_response = json.loads(x.text)
        msg = tappay_response.get("msg")
        rec_trade_id = tappay_response.get("rec_trade_id")
        bank_transaction_id = tappay_response.get("bank_transaction_id")
        if msg == "Success":
            payment_status = 1
            response_data = {"data":{
                "number": order_num,
                "payment":{
                    "status":payment_status,
                    "message":"付款成功"
                }
            }}
        else:
            payment_status =0
            response_data = {"data":{
                "number": order_num,
                "payment":{
                    "status":payment_status,
                    "message":"付款失敗"
                }
            }}

        update_payment_status = '''
        UPDATE booking
        SET payment_status = %s
        WHERE order_num = %s
        '''
        cursor.execute(update_payment_status, (payment_status, order_num))
        conn.commit()

        create_payment_log ='''
        INSERT INTO payment (order_num, payment_status, msg, bank_transaction_id, rec_trade_id) VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(create_payment_log, (order_num, payment_status, msg, bank_transaction_id, rec_trade_id))
        conn.commit()

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

# 獲取訂單資訊
@router.get("/api/order/{orderNumber}")
async def get_order_info(orderNumber: str, user: dict = Depends(get_current_user)):
    if not user:
        response_data = {"error": True, "message": "未登入系統，拒絕存取"}
        response = JSONResponse(content=response_data, status_code=403)
    try:
        conn =connection_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        order_query ='''
        SELECT b.price, b.attraction_id, a.name, a.address, a.images, b.date, b.time, b.contact_name, b.contact_email, b.contact_phone, b.payment_status
        FROM booking b
        JOIN attractions a ON b.attraction_id = a.attraction_id
        WHERE b.order_num = %s
        '''
        cursor.execute(order_query, (orderNumber,))
        order_result = cursor.fetchone()
        
        if order_result:
            response_data = {
                "data": {
                    "number": orderNumber,
                    "price": order_result["price"],
                    "trip": {
                    "attraction": {
                        "id": order_result["attraction_id"],
                        "name": order_result["name"],
                        "address": order_result["address"],
                        "image": json.loads(order_result["images"])[0]
                    },
                    "date": order_result["date"],
                    "time": order_result["time"]
                    },
                    "contact": {
                    "name": order_result["contact_name"],
                    "email": order_result["contact_email"],
                    "phone":order_result["contact_phone"] 
                    },
                    "status": order_result["payment_status"]
                }
            }
            response = JSONResponse(content=response_data, status_code=200)
        if not order_result:
            response_data = None
            response = JSONResponse(content=response_data, status_code=200)
    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()
	
    return response  
