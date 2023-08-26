from sqlalchemy.orm import Session
from chatapp.models.friendships import Friendship

def create_friendship(db: Session, friendship_data: dict):
    new_friendship = Friendship(**friendship_data)
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    return new_friendship

def get_friendship(db: Session, friendship_id: int):
    return db.query(Friendship).filter(Friendship.id == friendship_id).first()

def get_friendships(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Friendship).offset(skip).limit(limit).all()

def update_friendship(db: Session, friendship_id: int, friendship_data: dict):
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if friendship:
        for key, value in friendship_data.items():
            setattr(friendship, key, value)
        db.commit()
        db.refresh(friendship)
        return friendship
    
def delete_friendship(db: Session, friendship_id: int):
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if friendship:
        db.delete(friendship)
        db.commit()
        return True
    return False

def get_friendships_by_user(db: Session, user_id: int):
    return db.query(Friendship).filter(Friendship.user_id == user_id).all()

def get_friendships_by_friend(db: Session, friend_id: int):
    return db.query(Friendship).filter(Friendship.friend_id == friend_id).all()



