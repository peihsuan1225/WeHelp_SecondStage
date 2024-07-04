from passlib.hash import bcrypt

# 哈希密碼
password = "0330"
hashed_password = bcrypt.hash(password)
print(f"Hashed password: {hashed_password}")

# # 驗證密碼
# input_password = "my_secret_password"
# is_correct = bcrypt.verify(input_password, hashed_password)
# print(f"Password is correct: {is_correct}")


from datetime import datetime
import random

def generate_order_number():
    now = datetime.now()
    random_num = random.randint(10, 99)
    return now.strftime("%Y%m%d%H%M") + str(random_num)

print(generate_order_number())  # Example: 20240704123023