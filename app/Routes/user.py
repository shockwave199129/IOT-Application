from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse

from Database.mongo_connection import mongo_db

from Core.security import get_password_hash, verify_password, create_access_token, authenticate_token

from Models.models import UserCreate, UserLogin

router = APIRouter()


@router.post("/register")
async def create_user(
    user: UserCreate = Body(...)
) -> JSONResponse:
    """
    Create new user.
    """
    user_data = user.dict()

    # Hash the password before storing it
    user_data["password"] = get_password_hash(user_data["password"])

    # Store user_data in the database
    await mongo_db.client.IOT_database.users.insert_one(user_data)
    return JSONResponse(content={"message": "User created successfully"}, status_code=201)


@router.post("/login")
async def login_user(user: UserLogin = Body(...)) -> JSONResponse:
    """
    Login user and return an access token.
    """
    user_data = user.dict()

    # Retrieve the user from the database based on the provided email
    stored_user = await mongo_db.client.IOT_database.users.find_one({"email": user_data["email"]})

    if stored_user and verify_password(user_data["password"], stored_user["password"]):
        # Password is correct, generate and return an access token
        access_token = create_access_token(user_data["email"])
        return JSONResponse(content={"access_token": access_token, "token_type": "bearer"}, status_code=200)

    # Incorrect email or password
    raise HTTPException(status_code=401, detail="Incorrect email or password")


@router.get("/me")
async def user_details(user: dict = Depends(authenticate_token)) -> JSONResponse:
    """
    get logedin user details
    """
    pipeline = [
        {
            "$match": {"email": user['user']}
        },
        {
            "$project": {
                # Exclude the _id field if needed
                "_id": {"$toString": "$_id"},
                "username": "$username",
                "email": "$email",
            }
        }
    ]
    result = await mongo_db.client.IOT_database.users.aggregate(pipeline).to_list(None)

    return JSONResponse(content=result, status_code=200)
