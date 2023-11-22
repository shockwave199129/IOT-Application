from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse

from datetime import datetime

from Database.redis_connection import redis_db
from Database.mongo_connection import mongo_db

from Core.security import authenticate_token

router = APIRouter(prefix="/device")


@router.get("")
async def get_user_device(user: dict = Depends(authenticate_token), redis=Depends(redis_db)) -> JSONResponse:
    """
    get list of user's device
    """
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    try:
        # Perform a MongoDB aggregation to join user_device and device collections
        pipeline = [
            {
                "$match": {"user": user['user']}
            },
            {
                "$lookup": {
                    "from": "device",
                    "localField": "user_device_id",
                    "foreignField": "device_id",
                    "as": "device_info"
                }
            },
            {
                "$unwind": "$device_info"
            },
            {
                "$project": {
                    # Exclude the _id field if needed
                    "_id": {"$toString": "$device_info._id"},
                    "device_name": "$device_info.device_name",
                    "device_id": "$device_info.device_id",
                    "user": "$user"
                }
            }
        ]

        result = await mongo_db.client.IOT_database.user_device.aggregate(pipeline).to_list(None)

        for __i in result:
            redis_key = f"device:{__i['device_id']}"
            _data = await redis.redis.hgetall(redis_key)

            __i['status'] = False if (not _data) or (
                _data.get('status') == 'False') else True

        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        # Handle database or other errors
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.post("/register")
async def register_user_device(device_id: str = Body(...), device_name: str = Body(...), user: dict = Depends(authenticate_token)) -> JSONResponse:
    """
    register device and assign to user
    """
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed")

    device_data = {"device_id": device_id, "device_name": device_name}

    try:
        # Store device information in the database
        await mongo_db.client.IOT_database.device.insert_one(device_data)

        # Assign the device to the user
        user_device_data = {"user": user['user'], "user_device_id": device_id}
        await mongo_db.client.IOT_database.user_device.insert_one(user_device_data)

        return JSONResponse(content={"message": "Device registered successfully"}, status_code=201)
    except Exception as e:
        # Handle database or other errors
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/{device_id}")
async def get_device_info(device_id: str, user: dict = Depends(authenticate_token), redis=Depends(redis_db)) -> JSONResponse:
    """
    get a user's device info by device_id
    """
    # Check if the device_id belongs to the user
    pipeline = [
        {"$match": {"user": user['user'], "user_device_id": device_id}},
        {"$lookup": {
            "from": "device",
            "localField": "user_device_id",
            "foreignField": "device_id",
            "as": "device_info"
        }},
        {"$unwind": "$device_info"},
        {"$project": {"_id": {"$toString": "$device_info._id"},
                      "device_name": "$device_info.device_name",
                      "device_id": "$device_info.device_id",
                      "user": "$user"}}
    ]

    # Use to_list(None) to get a list from the cursor
    device_exists = await mongo_db.client.IOT_database.user_device.aggregate(pipeline).to_list(None)

    if not device_exists:
        raise HTTPException(
            status_code=404, detail="Device not found or does not belong to the user")

    # Get device info from Redis
    redis_key = f"device:{device_id}"
    device_info = await redis.redis.hgetall(redis_key)

    # Include the 'status' field in the response
    device_exists[0]['status'] = False if ('status' not in device_info) or (
        device_info.get('status') == 'False') else True

    return JSONResponse(content=device_exists[0], status_code=200)


@router.post("/{device_id}/store")
async def store_control_data(
    device_id: str,
    control_value: str = Body(...),
    device: str = Body(...),
    user: dict = Depends(authenticate_token),
    redis=Depends(redis_db),
) -> JSONResponse:
    """
    Store control data in Redis for a specific device.
    """
    try:
        redis_key = f"device:{device_id}"
        _data = await redis.redis.hgetall(redis_key)

        if not _data:
            control_data = {}
            control_data["status"] = 'False'
            control_data["control_value"] = control_value
            control_data["user_status"] = 'True'
            control_data["last_user_update"] = str(datetime.utcnow())
            control_data["last_bot_update"] = ''
            await redis.redis.hmset(redis_key, control_data)

        else:
            await redis.redis.hset(redis_key, 'user_status', 'True')
            await redis.redis.hset(redis_key, 'control_value', control_value)
            await redis.redis.hset(redis_key, 'last_user_update', str(datetime.utcnow()))

        return JSONResponse(content={"message": "Control data stored successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Internal Server Error: {str(e)}")
