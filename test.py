from passlib.hash import bcrypt

# 哈希密碼
password = "0330"
hashed_password = bcrypt.hash(password)
print(f"Hashed password: {hashed_password}")

# # 驗證密碼
# input_password = "my_secret_password"
# is_correct = bcrypt.verify(input_password, hashed_password)
# print(f"Password is correct: {is_correct}")
