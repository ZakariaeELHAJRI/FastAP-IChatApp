from sqlalchemy.orm import Session
from chatapp.models.friendships import Friendship
from chatapp.models.user import User

def create_friendship(db: Session, friendship_data: dict):
    user_id = friendship_data.get('user_id')
    friend_id = friendship_data.get('friend_id')
    status = friendship_data.get('status')

    if user_id is None or friend_id is None or status is None:
        print("Invalid friendship data provided.")
        return False

    # Ensure that the user_id and friend_id combination is unique
    existing_friendship = db.query(Friendship).filter(
        ((Friendship.user_id == user_id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == user_id))
    ).first()

    if existing_friendship:
        print("The friendship already exists.")
        return False

    # Check if the inverse friendship exists
    inverse_friendship = db.query(Friendship).filter(
        (Friendship.user_id == friend_id) & (Friendship.friend_id == user_id)
    ).first()

    if inverse_friendship:
        print("Inverse friendship already exists.")
        return False

    try:
        # Add the friendship
        new_friendship = Friendship(user_id=user_id, friend_id=friend_id, status=status)
        db.add(new_friendship)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"An error occurred while adding the friendship: {str(e)}")
        return False


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
    try:
        friendships = db.query(Friendship).filter(
            (Friendship.user_id == user_id) | (Friendship.friend_id == user_id)
        ).all()
        return friendships
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        return []

def get_friendships_invitations(db: Session, user_id: int):
    try:
        invitations = db.query(Friendship).filter(
            (Friendship.friend_id == user_id) & (Friendship.status == "pending")
        ).all()
        
        custom_invitations = [
            {
                "id": invitation.id,
                "status": invitation.status,
                "user_id": invitation.user_id,
                "friend_id": invitation.friend_id,
                "friend_first_name": db.query(User).filter(User.id == invitation.friend_id).first().firstname,
                "friend_last_name": db.query(User).filter(User.id == invitation.friend_id).first().lastname,
            }
            for invitation in invitations
        ]
        
        return custom_invitations

    except Exception as e:
        print(f"An error occurred while fetching invitations: {str(e)}")
        return []
    

def get_friendships_by_friend(db: Session, friend_id: int):
    return db.query(Friendship).filter(Friendship.friend_id == friend_id).all()




