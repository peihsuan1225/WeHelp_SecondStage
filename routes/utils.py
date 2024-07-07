from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# JWT 秘鑰
SECRET_KEY = "s1l2o2t5h"
ALGORITHM = "HS256"

security = HTTPBearer() 

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
	token =credentials.credentials
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
		return payload
	except jwt.ExpiredSignatureError:
		return
	except jwt.InvalidTokenError:
		return