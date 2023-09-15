from fastapi import FastAPI , Depends
from .database import Base , SessionLocal
from sqlalchemy.orm import Session
from chatapp.routers import user, message, friendships  , authentication # Import routers
from dotenv import load_dotenv
from chatapp.database import get_db
from dependencies.auth import get_current_user 
from chatapp.models import User
load_dotenv()
# app
app = FastAPI()



# Define routes for CRUD operations
app.include_router(authentication.router, tags=["authentication"])
app.include_router(user.router, prefix="/api", tags=["users"])
app.include_router(message.router, prefix="/api", tags=["messages"])
app.include_router(friendships.router, prefix="/api", tags=["friendships"])



@app.get("/")
async def root(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return {"message": "Hello World", "username": current_user.username}