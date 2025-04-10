import json
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["user_db"]
users_collection = db["users"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


# Pydantic User Model
class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    hashed_password: str


# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Signup Route
@app.post("/signup")
async def signup(user: User):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    user_data = {"username": user.username, "hashed_password": hashed_password}
    await users_collection.insert_one(user_data)

    return {"message": "User created successfully"}


# Login Route
@app.post("/login")
async def login(user: User):
    stored_user = await users_collection.find_one({"username": user.username})

    if not stored_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"message": "Login successful", "username": user.username}


# Get User Route
@app.get("/user/{username}")
async def get_user(username: str):
    user = await users_collection.find_one({"username": username}, {"_id": 0, "hashed_password": 0})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
