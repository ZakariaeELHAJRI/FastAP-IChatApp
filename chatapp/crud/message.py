from sqlalchemy.orm import Session
from chatapp.models.message import Message

def create_message(db: Session, message_data: dict):
    new_message = Message(**message_data)
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


