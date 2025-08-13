from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URI")  # replace if needed

client = AsyncIOMotorClient(MONGO_URL)
db = client["easyapply_db"]  # your database name
