from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader, HTTPBearer
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt, JWTError
from passlib.context import CryptContext

from Core.config import setting
from Database.mongo_connection import mongo_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = setting.ACCESS_TOKEN_EXPIRE_MINUTES

SECRET_KEY = setting.SECRET_KEY

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "user": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


api_key_header = HTTPBearer(description="This is user authentication with bearer api key provided at login", auto_error=True)


def authenticate_token(authorization: str = Depends(api_key_header)):
    try:
        payload = jwt.decode(authorization.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token, Kindly login",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


bot_key_header = APIKeyHeader(name='device_id', auto_error=True, description="This is BOT authentication with it's own device id")


async def bot_token(bot_device_id: str = Depends(bot_key_header)):
    device_exists = await mongo_db.client.IOT_database.device.find_one({"device_id": bot_device_id})

    if not device_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device_id, device not found",
        )

    return bot_device_id
