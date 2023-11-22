from Routes import user, user_device, control
from Database.redis_connection import redis_db
from Database.mongo_connection import mongo_db
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from datetime import datetime, timedelta
from typing import Union, List
import uvloop

from Core.logger import logger
uvloop.install()


app = FastAPI(title="IOT - api", version='1.0.0',
              description='This api part for IOT project powered by FastAPI')


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await mongo_db.connect()
    await redis_db.connect()


# 1 min
@app.on_event("startup")
@repeat_every(seconds=60 * 1, logger=logger, wait_first=True)
async def run_background_task():
    # Your logic to find devices older than 1 minute and update their status
    outdated_devices = await find_outdated_devices()

    for device_id in outdated_devices:
        await update_device_status(device_id)

@app.on_event("startup")
@repeat_every(seconds=30, logger=logger, wait_first=True)  # 30 min
async def update_redis_to_db():
    # Your logic to find devices and store in db table user control table with device_id, user email, control data, last_user_update,
    # Get all device_ids from user_device
    pipeline = [
        {
            "$project": {
                "_id": 0,  # Exclude the _id field if needed
                "user": "$user",
                "user_device_id": "$user_device_id"
            }
        }
    ]

    user_devices = await mongo_db.client.IOT_database.user_device.aggregate(pipeline).to_list(None)

    for device in user_devices:
        redis_key = f"device:{device['user_device_id']}"

        last_update = await redis_db.redis.hget(redis_key, 'last_user_update')
        last_control_data = await redis_db.redis.hget(redis_key, 'control_value')

        if last_update and last_control_data:
            filter_criteria = {"timestamp": last_update}
            update_data = {"$set": {"user_device_id": device['user_device_id'],
                                    "user": device['user'], "contol": last_control_data, "timestamp": last_update}}

            await mongo_db.client.IOT_database.user_device_control_data.update_one(filter_criteria, update_data, upsert=True)


async def find_outdated_devices() -> List[str]:
    outdated_devices = []

    # Get all device_ids from user_device
    user_device_ids = await mongo_db.client.IOT_database.user_device.distinct("user_device_id")

    # Check each device_id in Redis
    for device_id in user_device_ids:
        redis_key = f"device:{device_id}"
        last_user_update = await redis_db.redis.hget(redis_key, 'last_user_update')

        if last_user_update:
            last_user_update_timestamp = datetime.strptime(
                last_user_update, "%Y-%m-%d %H:%M:%S.%f")
            one_minute_ago = datetime.utcnow() - timedelta(minutes=1)

            if last_user_update_timestamp < one_minute_ago:
                outdated_devices.append(device_id)

    return outdated_devices


async def update_device_status(device_id: str):
    # Your logic to update user_status and control_value fields
    redis_key = f"device:{device_id}"
    await redis_db.redis.hset(redis_key, 'user_status', 'False')
    await redis_db.redis.hset(redis_key, 'control_value', '')


@app.on_event("shutdown")
async def shutdown_event():
    await mongo_db.close()
    await redis_db.close()

app.include_router(user.router, tags=['User'])
app.include_router(user_device.router, tags=['User Device'])
app.include_router(control.router, tags=['Bot'])


# Common exception handler
async def common_exception_handler(request: Request, exc: Exception):
    logger.exception(
        f"An exception occurred during request processing: {str(exc)}")

    # Customize the response based on the exception type if needed
    if isinstance(exc, HTTPException):
        return JSONResponse(content={"detail": exc.detail}, status_code=exc.status_code)

    return JSONResponse(content={"detail": "Internal Server Error"}, status_code=500)

# Register the common exception handler
app.add_exception_handler(Exception, common_exception_handler)

""" @app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q} """
