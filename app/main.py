# app/main.py

from fastapi import FastAPI
from app.api import routes 
from app.api import auth
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes import api_router
from app.models.database import Base, engine  # Import for DB creation
import asyncio
import os 

app= FastAPI()

app.include_router(auth.router)  # Include auth routes
app.include_router(routes.api_router)  # Include other API routes

load_dotenv()  # Load environment variables from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI(
    title="MediScan AI",
    description="An AI-powered system to extract and analyze data from prescriptions",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to MediScan AI API"}

# 👇 Create database tables on startup
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
