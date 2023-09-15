from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from dependencies.auth import authenticate_user, create_access_token, User, Token
from chatapp.database import get_db
from sqlalchemy.orm import Session
from dependencies.auth import UserCredentials

router = APIRouter()



@router.post("/token", response_model=Token)
async def login_for_access_token(
    user_credentials: UserCredentials,  # Accept JSON data as UserCredentials
    db: Session = Depends(get_db),
):
    user = authenticate_user(user_credentials.username, user_credentials.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user_credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}


