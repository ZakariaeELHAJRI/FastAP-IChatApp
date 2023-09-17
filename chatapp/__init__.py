from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships, authentication, conversation
from chatapp.auth import auth
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user
from chatapp.models import User

from typing import List, Dict


load_dotenv()

app = FastAPI()

# Configure CORS settings
origins = [
    "http://localhost:3000",  # Add the URL of your Next.js frontend
    "http://localhost:8000",  # Add the URL of your FastAPI server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define routes for CRUD operations (include your existing routes)
app.include_router(authentication.router, tags=["authentication"])
app.include_router(auth.auth_router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(message.router, prefix="/api", tags=["messages"])
app.include_router(friendships.router, prefix="/api", tags=["friendships"])
app.include_router(conversation.router, prefix="/api", tags=["conversations"])


