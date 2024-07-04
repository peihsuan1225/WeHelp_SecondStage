from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
from pydantic import BaseModel
import json
from datetime import datetime
import random
import requests

from .config import connection_pool
from .utils import get_current_user

router = APIRouter()

def generate_order_number():
    now = datetime.now()
    random_num = random.randint(10, 99)
    return now.strftime("%Y%m%d%H%M") + str(random_num)

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
        order_num = generate_order_number()
        contant =  orderInfo.order.contact
        create_order_query = '''
        UPDATE booking
        SET order_num = %s, contact_name = %s, contact_email = %s, contact_phone = %s
        WHERE member_id = %s AND payment_status = %s
        '''
        cursor.execute(create_order_query, (order_num, contant.name, contant.email, contant.phone, user["id"], 0))
        conn.commit()
        print(orderInfo)

        url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
        headers = {
        'Content-Type': 'application/json',
        'x-api-key': 'partner_u2mylpNUnRvGdA1u3gJaJVji5PKqfQICP8PnBmYDgLJbM2yCi09Slzf3'
        }

        payload = {
            "prime": orderInfo.prime,  # 請填入實際的Prime值
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
        print(x.text)
        print(x.request)
        print(payload)
        response_data = {"data":True}
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

        
        