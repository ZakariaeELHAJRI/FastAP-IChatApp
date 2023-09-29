from fastapi import HTTPException
from sqlalchemy.orm import Session 
from chatapp.models.message import Message
from chatapp.models.friendships import Friendship
from chatapp.models.user import User

def create_new_message(
    message_data: dict,
    current_user: User,
    db: Session,
):
    sender_id = current_user.id
    receiver_id = message_data.get("receiver_id")
    conversation_id = message_data.get("conversation_id")

    try:
        receiver = db.query(User).filter(User.id == receiver_id).first()
        if not receiver:
            raise ValueError("Invalid receiver.")

        if "sender_id" in message_data:
            del message_data["sender_id"]

        message = create_message(db, message_data, sender_id, receiver_id, conversation_id)

        return message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_message(db: Session, message_data: dict, sender_id: int, receiver_id: int, conversation_id: int):
    # Check if the sender and receiver are valid users (you can add more validation here)
    sender = db.query(User).filter(User.id == sender_id).first()
    receiver = db.query(User).filter(User.id == receiver_id).first()

    if not sender or not receiver:
        raise ValueError("Invalid sender or receiver.")

    # Check if a valid friendship exists between sender and receiver (both directions)
    friendship_sender_to_receiver = db.query(Friendship).filter(
        (Friendship.user_id == sender_id) & (Friendship.friend_id == receiver_id) &
        (Friendship.status == "accepted")
    ).first()

    friendship_receiver_to_sender = db.query(Friendship).filter(
        (Friendship.user_id == receiver_id) & (Friendship.friend_id == sender_id) &
        (Friendship.status == "accepted")
    ).first()

    print("friendship_sender_to_receiver:", friendship_sender_to_receiver)
    print("friendship_receiver_to_sender:", friendship_receiver_to_sender)

    if not (   friendship_receiver_to_sender or friendship_sender_to_receiver):
        raise ValueError("There is no accepted friendship between the sender and receiver zaki. "+friendship_sender_to_receiver+" "+friendship_receiver_to_sender+" zaki")

    # Create a new Message instance directly with the arguments
    new_message = Message(
        content=message_data.get("content"),
        sender_id=sender_id,
        receiver_id=receiver_id,
        conversation_id=conversation_id
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message



def get_message(db: Session, message_id: int):
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Message).offset(skip).limit(limit).all()

def get_messages_by_conversation(db: Session, conversation_id: int):
    return db.query(Message).filter(Message.conversation_id == conversation_id).all()

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


