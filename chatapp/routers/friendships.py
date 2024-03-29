from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.friendships import create_friendship, get_friendship, get_friendships, get_friendships_by_user, get_friendships_invitations , update_friendship, delete_friendship 
from chatapp.database import get_db
from chatapp.models.friendships import Friendship
from dependencies.auth import User, get_current_user
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
router = APIRouter()

@router.post("/friendships/")
def create_new_friendship(friendship_data: dict,current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    return create_friendship(db, friendship_data)

@router.get("/friendships/{user_id}")
def get_single_friendship(user_id: int, current_user: User = Depends(get_current_user),  db: Session = Depends(get_db)):
    try:
        friendship = get_friendships_invitations(db, user_id)
        if friendship is None:
            raise HTTPException(status_code=404, detail="Friendship not found")
        return friendship
    except Exception as e:
        logging.error(f"Error in get_single_friendship: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

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

@router.put("/mark-invitation-as-read/{user_id}")
def mark_invitation_as_read(user_id: int, db: Session = Depends(get_db)):
    try:
        friendships = get_friendships_by_user(db, user_id)
        if not friendships:
            raise HTTPException(status_code=404, detail="Friendship not found")

        for friendship in friendships:
            if not friendship.is_read:
                friendship.is_read = True

        db.commit()
        print("friendships:", friendships)  # Check if the changes are reflected here
        return friendships
    except Exception as e:
        logging.error(f"Error in mark_invitation_as_read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

    


def get_friendships_by_friend(friend_id: int, db: Session, current_user: User = Depends(get_current_user)):
    return db.query(Friendship).filter(Friendship.friend_id == friend_id).all()




