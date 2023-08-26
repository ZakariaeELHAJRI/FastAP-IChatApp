from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.user import create_user, get_user, get_users, update_user, delete_user
from chatapp.database import get_db

router = APIRouter()

@router.post("/users/")
def create_new_user(user_data: dict, db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.get("/users/{user_id}")
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
def get_all_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_users(db, skip, limit)

@router.put("/users/{user_id}")
def update_existing_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}




