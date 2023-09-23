from fastapi import APIRouter, Depends, HTTPException , Query
from sqlalchemy.orm import Session
from chatapp.crud.user import create_user, get_user, get_users, update_user, delete_user
from chatapp.database import get_db
from dependencies.auth import User, get_current_user ,UserInfo
from chatapp.models.user import User as UserModel
from chatapp.models.friendships import Friendship

router = APIRouter()

@router.post("/users/")
def create_new_user(user_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_user(db, user_data)

@router.get("/users/{user_id}")
def get_single_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/")
def get_all_users(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_users(db, skip, limit)

# get user by username

@router.get("/currentuser/{username}")
def get_single_user_by_username(username: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_info = UserInfo(
        id=user.id,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        country=user.country,
        city=user.city
    )
    return user_info
 

@router.put("/users/{user_id}")
def update_existing_user(user_id: int, user_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = update_user(db, user_id, user_data)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
def delete_existing_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if user is False:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.get("/friends/")
def get_all_users_with_common_friends(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get the IDs of friends of the current user
    current_user_friend_ids = [friend.friend_id for friend in current_user.friends]

    # Query for users excluding the current user
    users = (
        db.query(User)
        .filter(User.id != current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Create a list to store user data with common friends and status
    user_data = []

    # Iterate through the users
    for user in users:
        # Get the common friends between the current user and this user
        common_friends = (
            db.query(Friendship)
            .filter(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == user.id,
              
            )
            .count()
        )

        # Get the Friendship.status of this user with the current user
        friendship_status = (
            db.query(Friendship.status)
            .filter(
                Friendship.user_id == current_user.id,
                Friendship.friend_id == user.id
            )
            .scalar()
        )

        # Create a dictionary with user details, common friends count, and status
        user_info = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "username": user.username,
            "email": user.email,
            "country": user.country,
            "city": user.city,
            "common_friends_count": common_friends,
            "friendship_status": friendship_status,
        }

        # Append the user info to the user_data list
        user_data.append(user_info)

    return user_data