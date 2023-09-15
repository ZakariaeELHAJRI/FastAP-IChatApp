# Import necessary dependencies
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import  OAuth2PasswordRequestForm
from dependencies.auth import authenticate_user, create_access_token, User, Token
from chatapp.database import get_db  
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
