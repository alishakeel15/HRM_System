from datetime import datetime, timedelta, timezone
import jwt

SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 15

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({
        "exp": expire
    })
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def create_reset_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=RESET_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(
        {
            "sub": str(user_id),
            "type": "password_reset",
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token, expire