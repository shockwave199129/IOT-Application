from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from datetime import datetime

from Core.security import authenticate_token, bot_token

from Database.redis_connection import redis_db
from Database.mongo_connection import mongo_db

router = APIRouter(prefix='/bot')


@router.get("/receive")
async def receive_control_data(
    bot_id=Depends(bot_token),
    redis=Depends(redis_db),
) -> JSONResponse:
    """
    Receive control data in Redis for a specific device.
    """
    try:
        redis_key = f"device:{bot_id}"
        _data = await redis.redis.hgetall(redis_key)

        if not _data:
            control_data = {}
            control_data["status"] = 'True'
            control_data["control_value"] = ''
            control_data["user_status"] = 'False'
            control_data["last_user_update"] = ''
            control_data["last_bot_update"] = str(datetime.utcnow())

            await redis.redis.hmset(redis_key, control_data)

        else:
            await redis.redis.hset(redis_key, 'status', 'True')
            await redis.redis.hset(redis_key, 'last_bot_update', str(datetime.utcnow()))

        control_value = await redis.redis.hget(redis_key, 'control_value')
        return JSONResponse(content=control_value, status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
