from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.crud.message import create_message, get_message, get_messages , update_message, delete_message
from chatapp.database import get_db
from chatapp.models.message import Message

router = APIRouter()

@router.post("/messages/")
def create_new_message(message_data: dict, db: Session = Depends(get_db)):
    return create_message(db, message_data)

@router.get("/messages/{message_id}")
def get_single_message(message_id: int, db: Session = Depends(get_db)):
    message = get_message(db, message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.get("/messages/")
def get_all_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_messages(db, skip, limit)

@router.put("/messages/{message_id}")
def update_existing_message(message_id: int, message_data: dict, db: Session = Depends(get_db)):
    message = update_message(db, message_id, message_data)
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@router.delete("/messages/{message_id}")
def delete_existing_message(message_id: int, db: Session = Depends(get_db)):
    message = delete_message(db, message_id)
    if message is False:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

def get_messages_by_user(db: Session, user_id: int):
    return db.query(Message).filter(Message.user_id == user_id).all()


