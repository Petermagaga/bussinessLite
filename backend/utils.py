from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt

SECRET_KEY = "bizpilotsecret123"
ALGORITHM = "HS256"

security = HTTPBearer()

def verify_token(credentials=Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
