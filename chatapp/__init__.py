from fastapi import FastAPI , Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import Base , SessionLocal
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships  , authentication # Import routers
from chatapp.auth import auth # Import auth
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user 
from chatapp.models import User
load_dotenv()
# app
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
    allow_methods=["*"],  # You can specify specific HTTP methods (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers
)


# Define routes for CRUD operations
app.include_router(authentication.router, tags=["authentication"])
app.include_router(auth.auth_router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(message.router, prefix="/api", tags=["messages"])
app.include_router(friendships.router, prefix="/api", tags=["friendships"])



@app.get("/")
async def root(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"message": "Hello World", "username": current_user.username}