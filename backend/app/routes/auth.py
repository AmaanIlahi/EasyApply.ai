from fastapi import APIRouter, HTTPException, Request, Depends, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import hashlib
import jwt
from app.db import db

# Replace this with your own secret key in production
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()

# In-memory mock user "database"
# users_db = {}


# Pydantic Schemas
class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


# Helper Functions
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload.get("sub")
        return request.state.user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# Routes
@router.post("/signup")
async def signup(user: SignupRequest):
    users_collection = db["users"]  # 👈 get the collection

    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "password": hash_password(user.password),
        "createdAt": datetime.utcnow()
    }

    await users_collection.insert_one(user_data)

    return {"message": "User registered successfully"}


@router.post("/login")
async def login(credentials: LoginRequest):
    print(LoginRequest)
    users_collection = db["users"]

    user = await users_collection.find_one({"username": credentials.username})
    if not user or user["password"] != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": credentials.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(request: Request, username=Depends(verify_token)):
    users_collection = db["users"]

    user_data = await users_collection.find_one({"username": username}, {"password": 0})  # exclude password
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user_data["_id"] = str(user_data["_id"])  # Convert ObjectId to string
    return {"user": user_data}
