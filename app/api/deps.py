from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError


from app.core.security import  PUBLIC_KEY, JWT_ALGORITHM

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
            audience="skinshop-service",
            issuer="skinlytics-auth"
        )
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload



def require_shop_owner(user=Depends(get_current_user)):
    if user.get("role") not in ["SHOP_OWNER", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Shop owner access required")
    return user

def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
        
    return user