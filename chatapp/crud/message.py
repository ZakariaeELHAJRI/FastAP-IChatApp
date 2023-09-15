from sqlalchemy.orm import Session
from chatapp.models.message import Message
from chatapp.models.friendships import Friendship


def create_message(db: Session, message_data: dict, sender_id: int, receiver_id: int):
    # Check if a valid friendship exists between sender and receiver
    friendship = db.query(Friendship).filter(
        (Friendship.user_id == sender_id) & (Friendship.friend_id == receiver_id) &
        (Friendship.status == "accepted")
    ).first()

    if not friendship:
        raise ValueError("There is no accepted friendship between the sender and receiver.")

    new_message = Message(**message_data, user_id=sender_id)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message

def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Message).offset(skip).limit(limit).all()

def update_message(db: Session, message_id: int, message_data: dict):
    message = db.query(Message).filter(Message.id == message_id).first()
    for key, value in message_data.items():
        setattr(message, key, value)
    db.commit()
    db.refresh(message)
    return message

def delete_message(db: Session, message_id: int):
    message = db.query(Message).filter(Message.id == message_id).first()
    db.delete(message)
    db.commit()
    return message

def get_messages_by_user(db: Session, user_id: int):
    return db.query(Message).filter(Message.user_id == user_id).all()


