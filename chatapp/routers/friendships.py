from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.friendships import create_friendship, get_friendship, get_friendships , update_friendship, delete_friendship 
from chatapp.database import get_db
from chatapp.models.friendships import Friendship
from dependencies.auth import User, get_current_user
router = APIRouter()

@router.post("/friendships/")
def create_new_friendship(friendship_data: dict,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return create_friendship(db, friendship_data)

@router.get("/friendships/{friendship_id}")
def get_single_friendship(friendship_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    friendship = get_friendship(db, friendship_id)
    if friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return friendship

@router.get("/friendships/")
def get_all_friendships(skip: int = 0, limit: int = 10,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return get_friendships(db, skip, limit)

@router.put("/friendships/{friendship_id}")
def update_existing_friendship(friendship_id: int, friendship_data: dict,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    friendship = update_friendship(db, friendship_id, friendship_data)
    if friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return friendship

@router.delete("/friendships/{friendship_id}")
def delete_existing_friendship(friendship_id: int,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    friendship = delete_friendship(db, friendship_id)
    if friendship is False:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return {"message": "Friendship deleted successfully"}


def get_friendships_by_user(user_id: int, db: Session, current_user: User = Depends(get_current_user)):
    return db.query(Friendship).filter(Friendship.user_id == user_id).all()

def get_friendships_by_friend(friend_id: int, db: Session, current_user: User = Depends(get_current_user)):
    return db.query(Friendship).filter(Friendship.friend_id == friend_id).all()




