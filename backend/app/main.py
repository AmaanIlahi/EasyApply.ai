from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
import os

# Load environment variables from .env
load_dotenv()

# === Firebase Initialization ===
cred = credentials.Certificate("app/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET")
})


# === MongoDB Connection ===
client = MongoClient(os.getenv("MONGO_URI"))
db = client["covercraft"]

# === FastAPI App Setup ===
app = FastAPI(
    title="EasyApply.ai Backend",
    description="FastAPI backend for generating AI-powered cover letters and job tracking.",
    version="1.0.0"
)

# === CORS Setup (adjust origins in prod) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Route Imports ===
from app.routes import auth, resume, coverletter, application

# === Route Registration ===
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(resume.router, prefix="/resume", tags=["Resume"])
app.include_router(coverletter.router, prefix="/coverletter", tags=["Cover Letter"])
app.include_router(application.router, prefix="/application", tags=["Job Applications"])

# === Root Route ===
@app.get("/")
def read_root():
    return {"message": "EasyApply.ai Backend is running 🚀"}
