from fastapi import APIRouter, Depends, HTTPException
from dependencies.auth import TokenData, get_current_user
from fastapi.security import  OAuth2PasswordRequestForm
from dependencies.auth import authenticate_user, create_access_token
from dependencies.auth import User, Token
from chatapp.database import get_db
from sqlalchemy.orm import Session
auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password , db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Path: chatapp/auth/auth.py